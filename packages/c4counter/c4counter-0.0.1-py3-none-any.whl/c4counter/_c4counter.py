#!/usr/bin/env python
"""c4counter
returns the number and types of C4 regions. minimap2 is used for mapping

Usage:
    c4counter <references.fasta> ...
"""

import docopt
from c4counter import paf
from c4counter import minimapcut
import enum
from pathlib import Path
from collections import namedtuple
from importlib import resources
import c4counter.data
from Bio import SeqIO, Seq
import sys

# in coordinates of C4A with HERV
END_EXON_9 = 2351
START_EXON_10 = 9135

START_EXON_26 = 13898
END_EXON_26 = 14054
LENGTH_C4A = 20625


def sortedByTargetCoords(mappings: list[paf.PafEntry]):
    return sorted(mappings, key=lambda segment: segment.tstart)


def groupSegments(mappings: list[paf.PafEntry]) -> list[list[paf.PafEntry]]:
    mappings = sortedByTargetCoords(mappings)
    groups = []
    currentGroup = []
    prev_qend = 0
    for seg in mappings:
        if seg.qstart < prev_qend:
            groups.append(currentGroup)
            currentGroup = []
        prev_qend = seg.qend
        currentGroup.append(seg)
    groups.append(currentGroup)
    return groups


def hasHERV(segments: list[paf.PafEntry]) -> bool:
    margin = 500
    for paf in segments:
        if paf.qstart < END_EXON_9 + margin and START_EXON_10 - margin < paf.qend:
            return True
    return False


class Haplotype(enum.Enum):
    C4A = enum.auto()
    C4B = enum.auto()
    Unknown = enum.auto()


def readFirstFastaSeq(fastapath: Path) -> SeqIO.SeqRecord:
    for rec in SeqIO.parse(fastapath, "fasta"):
        return rec


def extractEx26ToFile(C4fasta: Path, outfasta: Path):
    C4rec = readFirstFastaSeq(C4fasta)
    ex26rec = SeqIO.SeqRecord(
        C4rec.seq[START_EXON_26 + 1 : END_EXON_26 + 1],
        id="NC_000006.12:31995955-31996111",
        description="C4_exon26 [organism=Homo sapiens]",
    )
    with open(outfasta, "w") as fout:
        fout.write(ex26rec.format("fasta"))


def inferHaplotype(
    segments: list[paf.PafEntry], reffasta: str, c4afasta: str
) -> Haplotype:
    c4start = segments[0].tstart
    c4end = segments[-1].tend
    tmpC4Fasta = Path(".c4.fa.tmp")
    ex26fasta = Path("c4_exon26.fa")
    if not ex26fasta.exists():
        extractEx26ToFile(Path(c4afasta), ex26fasta)
    minimapcut.extractRange(reffasta, c4start, c4end, destfile=tmpC4Fasta.as_posix())
    ex26start, ex26end = minimapcut.getAlignmentCoords(tmpC4Fasta, ex26fasta.as_posix())
    c4rec = readFirstFastaSeq(tmpC4Fasta)
    ex26seq = c4rec.seq[ex26start:ex26end]
    c4aMarker = Seq.Seq("PCPVLD")
    c4bMarker = Seq.Seq("LSPVIH")
    ex26pep = ex26seq.translate()
    if c4aMarker in ex26pep and not c4bMarker in ex26pep:
        return Haplotype.C4A
    elif not c4aMarker in ex26pep and c4bMarker in ex26pep:
        return Haplotype.C4B
    else:
        print(f"no Haplotype found for {reffasta}")
        print(ex26seq)
        print(ex26pep)
        return Haplotype.Unknown


C4Mapped = namedtuple("C4Mapped", "tstart, tend, hasHERV, haplotype")


def write_svg(faToC4: dict[str, C4Mapped]):
    with open("c4.svg", "w") as svg:
        svg.write(SVG_HEAD)
        y = 0
        for name, c4s in faToC4.items():
            x = 0
            y += 20
            svg.write(
                FASTA_NAME_TEMPLATE.replace("Y_COORDINATE", str(y + 4)).replace(
                    "NAME", name
                )
            )
            svg.write(PATH_BEGIN_TEMPLATE.replace("Y_COORDINATE", str(y)))
            for i, c4 in enumerate(c4s):
                if i > 0:
                    svg.write(
                        PATH_MIDDLE_TEMPLATE.replace("X_COORDINATE", str(x)).replace(
                            "Y_COORDINATE", str(y)
                        )
                    )
                    x += 20
                if c4.haplotype == Haplotype.C4A.name:
                    color = "aab495"
                elif c4.haplotype == Haplotype.C4B.name:
                    color = "fdf8cc"
                else:
                    color = "ffffff"
                if c4.hasHERV:
                    geneTemplate = HERV_TEMPLATE
                else:
                    geneTemplate = NOHERV_TEMPLATE

                svg.write(
                    geneTemplate.replace("COLOR", color)
                    .replace("X_COORDINATE", str(x))
                    .replace("Y_COORDINATE", str(y))
                )
                if c4.hasHERV:
                    x += 65
                else:
                    x += 45
            svg.write(
                PATH_END_TEMPLATE.replace("X_COORDINATE", str(x)).replace(
                    "Y_COORDINATE", str(y)
                )
            )
        svg.write(SVG_FOOT)


def main():
    arguments = docopt.docopt(__doc__, version="0.1")
    faToC4 = {}
    c4a_fasta = resources.path(c4counter.data, 'C4A.fa')
    for ref_fasta in arguments["<references.fasta>"]:
        c4Segments = minimapcut.align(ref_fasta, c4a_fasta)
        print("########################################")
        print(f"{ref_fasta}")
        if not c4Segments:
            print("\tno C4 mappings found by minimap")
            continue
        c4Groups = groupSegments(c4Segments)
        c4s = []
        for (i, c4) in enumerate(c4Groups):
            print(f"{i+1}")
            if c4[-1].tend - c4[0].tstart < 0.5 * LENGTH_C4A:
                print("\tC4 mapping too small... skipping")
                continue
            # print( "    " + str(c4))
            print(f"    start: {c4[0].tstart}")
            print(f"    end  : {c4[-1].tend}")
            hasHERV_ = hasHERV(c4)
            print(f"    HERV : {hasHERV_}")
            haplotype = inferHaplotype(c4, ref_fasta, c4a_fasta).name
            c4s.append(C4Mapped(c4[0].tstart, c4[-1].tend, hasHERV_, haplotype))
            print(f"    A/B  : {haplotype}")
        faToC4[Path(ref_fasta).stem] = c4s
        print()
        print()
    write_svg(faToC4)


FASTA_NAME_TEMPLATE = """
    <text
       xml:space="preserve"
       style="font-size:10px;font-family:sans-serif"
       x="10"
       y="Y_COORDINATE"
       id="textNAME">NAME</text>
"""

PATH_BEGIN_TEMPLATE = (
    '\n<use xlink:href="#path-begin" transform="translate(0,Y_COORDINATE)" />'
)
PATH_MIDDLE_TEMPLATE = '\n<use xlink:href="#path-middle" transform="translate(X_COORDINATE,Y_COORDINATE)" />'
PATH_END_TEMPLATE = (
    '\n<use xlink:href="#path-end" transform="translate(X_COORDINATE,Y_COORDINATE)" />'
)
NOHERV_TEMPLATE = '\n<use xlink:href="#rect-noherv" fill="#COLOR" transform="translate(X_COORDINATE,Y_COORDINATE)" />'
HERV_TEMPLATE = '\n<use xlink:href="#rect-herv" fill="#COLOR" transform="translate(X_COORDINATE,Y_COORDINATE)" />'

SVG_FOOT = """
  </g>
</svg>
"""

SVG_HEAD = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   width="210mm"
   height="297mm"
   viewBox="0 0 793.70081 1122.5197"
   version="1.1"
   id="svg1"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs
     id="defs1">
    <marker
       id="InfiniteLineStart"
       orient="auto"
       refY="0"
       refX="0"
       style="overflow:visible">
      <g
         id="gThreeDots"
         transform="translate(-13,0)"
         style="#000">
        <circle
           cx="3"
           cy="0"
           r="0.8"
           id="circle1164" />
        <circle
           cx="6.5"
           cy="0"
           r="0.8"
           id="circle1166" />
        <circle
           cx="10"
           cy="0"
           r="0.8"
           id="circle1168" />
      </g>
    </marker>
    <marker
       id="ArrowSend"
       style="overflow:visible;"
       refX="0.0"
       refY="0.0"
       orient="auto">
      <path
         transform="scale(0.3) rotate(180) translate(-2.3,0)"
         d="M 8.7185878,4.0337352 L -2.2072895,0.016013256 L 8.7185884,-4.0017078 C 6.9730900,-1.6296469 6.9831476,1.6157441 8.7185878,4.0337352 z "
         style="stroke:context-stroke;fill-rule:evenodd;#000;stroke-width:0.62500000;stroke-linejoin:round;"
         id="path953" />
    </marker>
    <path
       id="path-begin" 
       style="opacity:1;fill:none;stroke:#000000;stroke-width:0.75;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;marker-start:url(#InfiniteLineStart)"
       d="m 65,0 h 10" />
    <path
       id="path-middle"
       style="fill:none;stroke:#000000;stroke-width:0.75;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="m 75,0 h 20"/>
    <path
       id="path-end"
       style="fill:none;stroke:#000000;stroke-width:0.75;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;marker-end:url(#ArrowSend)"
       d="m 75,0 h 15"/>
    <rect
       style="stroke:#000000;stroke-width:0.75;stroke-miterlimit:4;stroke-dasharray:none"
       id="rect-noherv"
       width="45"
       height="10"
       x="75"
       y="-5" />
    <g
      id="rect-herv">
      <rect
         style="stroke:#000000;stroke-width:0.75;stroke-miterlimit:4;stroke-dasharray:none"
         id="rect-herv_sub1"
         width="65"
         height="10"
         x="75"
         y="-5" />
      <rect
         style="fill:#000000;stroke:#000000;stroke-width:0.75;stroke-miterlimit:4;stroke-dasharray:none"
         id="rect-herv_sub2"
         width="20"
         height="10"
         x="80"
         y="-5" />
    </g>
  </defs>
  <g
     id="layer1">
     <g
        id="legend">
       <text
          xml:space="preserve"
          style="font-size:10px;font-family:sans-serif"
          x="290"
          y="35.1"
          id="legend_text_C4A">C4A</text>
       <text
          xml:space="preserve"
          style="font-size:10px;font-family:sans-serif"
          x="290"
          y="51.6"
          id="legend_text_C48">C4B</text>
       <text
          xml:space="preserve"
          style="font-size:10px;font-family:sans-serif"
          x="290"
          y="68.1"
          id="legend_text_Herv">HERV</text>
       <rect
          style="fill:none;stroke:#000000;stroke-width:0.37795277;stroke-linecap:round;stroke-linejoin:bevel;stroke-miterlimit:4;stroke-dasharray:none"
          id="rect_legend"
          width="58"
          height="54"
          x="282"
          y="20.8" />
       <rect
          style="fill:#aab495;stroke:#000000;stroke-width:0.37795277;stroke-linecap:round;stroke-linejoin:bevel;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
          id="rect_legend_C4A"
          width="11"
          height="6.7"
          x="319.6"
          y="28.1" />
       <rect
          style="fill:#fdf8cc;stroke:#000000;stroke-width:0.377953;stroke-linecap:round;stroke-linejoin:bevel;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
          id="rect_legend_C4B"
          width="11"
          height="6.7"
          x="319.6"
          y="44.6" />
       <rect
          style="fill:#000;stroke:#000000;stroke-width:0.377953;stroke-linecap:round;stroke-linejoin:bevel;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
          id="rect_legend_HERV"
          width="11"
          height="6.7"
          x="319.6"
          y="61.1" />
     </g>
"""

if __name__ == "__main__":
    main()
