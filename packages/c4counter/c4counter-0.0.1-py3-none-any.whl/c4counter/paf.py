from collections import namedtuple
from typing import Union

PafEntry = namedtuple(
    "PafEntry",
    "qname, qlen, qstart, qend, strand, tname, tlen, tstart, tend, nresiduematch, alignlen, quality, freeinfo",
)


def parsePafEntry(line: str) -> Union[PafEntry, None]:
    spl = line.split(maxsplit=12)
    if len(spl) < 12:
        print("skipping line " + line)
        parsed = None
    parsed = PafEntry(
        spl[0],
        int(spl[1]),
        int(spl[2]),
        int(spl[3]),
        spl[4],
        spl[5],
        int(spl[6]),
        int(spl[7]),
        int(spl[8]),
        int(spl[9]),
        int(spl[10]),
        int(spl[11]),
        spl[12],
    )
    return parsed
