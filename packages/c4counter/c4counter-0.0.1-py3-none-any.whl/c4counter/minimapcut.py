#!/usr/bin/env python

"""minimapcut
cuts the section similar to a query or an interval between two query sequences from a refernce with minimap2 

Usage:
    minimapcut <reference.fasta> [--offset1=<offset1>] [--offset2=<offset2] <query.fasta> [<query_end.fasta>]

Options:
    --offset1=<offset1>     cut n bp downstream (-:upstream) of querry start
    --offset2=<offset2>     cut n bp downstream (-:upstream) of querry end / querry_end end
"""

from Bio import SeqIO
import os
import docopt
import subprocess
from c4counter import paf


def sortedByTargetCoords(segments: list[paf.PafEntry]):
    return sorted(segments, key=lambda segment: segment.tstart)


def findBestMatch(segments: list[paf.PafEntry]):
    completeMatches = [
        seg for seg in segments if seg.qstart == 0 and seg.qend == seg.qlen
    ]
    if not completeMatches:
        return None
    if len(completeMatches) > 2:
        completeMatches.sort(key=lambda segment: segment.quality, reverse=True)
    return completeMatches[0]


def align(reffasta: str, queryfasta: str, verbose=False) -> list[paf.PafEntry]:
    command = ["minimap2", "-c", "-p 0.1", reffasta, queryfasta]
    output = subprocess.run(command, capture_output=True)
    segments = []
    if verbose:
        print(" ".join(command))
    for line in output.stdout.decode("utf-8").split("\n"):
        line.strip()
        if not line:
            continue
        if verbose:
            print(line)
        parsed = paf.parsePafEntry(line)
        if parsed:
            segments.append(parsed)
    return segments


def getAlignmentCoords(
    reffasta: str, queryfasta: str, verbose=False
) -> tuple[int, int]:
    segments = align(reffasta, queryfasta, verbose=verbose)
    bestMatch = findBestMatch(segments)
    if bestMatch:
        return bestMatch.tstart, bestMatch.tend
    else:
        segments = sortedByTargetCoords(segments)
        if segments:
            return segments[0].tstart, segments[-1].tend
        else:
            return 0, 0


def extractRange(reffasta: str, start: int, end: int, destfile=""):
    appendage = "_sub"
    for seq_record in SeqIO.parse(reffasta, "fasta"):
        sub_record = seq_record[start:end]
        path, ext = os.path.splitext(reffasta)
        fname = path + appendage + ext if destfile == "" else destfile
        with open(fname, "w") as subfasta:
            subfasta.write(sub_record.format("fasta"))
        break


if __name__ == "__main__":
    args = docopt.docopt(__doc__, version="0.1")
    start1, end1 = getAlignmentCoords(
        args["<reference.fasta>"], args["<query.fasta>"], verbose=True
    )
    offset1 = int(float(args["--offset1"])) if args["--offset1"] else 0
    offset2 = int(float(args["--offset2"])) if args["--offset2"] else 0
    if args["<query_end.fasta>"]:
        start2, end2 = getAlignmentCoords(
            args["<reference.fasta>"], args["<query_end.fasta>"], verbose=True
        )
        extractRange(args["<reference.fasta>"], start1 + offset1, end2 + offset2)
    else:
        extractRange(args["<reference.fasta>"], start1 + offset1, end1 + offset2)
    print()
