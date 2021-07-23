from typing import Dict, List
import aiohttp
import asyncio

sources = [
    "http://w3.usf.edu/FreeAssociation/AppendixA/Cue_Target_Pairs.A-B",
    "http://w3.usf.edu/FreeAssociation/AppendixA/Cue_Target_Pairs.C",
    "http://w3.usf.edu/FreeAssociation/AppendixA/Cue_Target_Pairs.D-F",
    "http://w3.usf.edu/FreeAssociation/AppendixA/Cue_Target_Pairs.G-K",
    "http://w3.usf.edu/FreeAssociation/AppendixA/Cue_Target_Pairs.L-O",
    "http://w3.usf.edu/FreeAssociation/AppendixA/Cue_Target_Pairs.P-R",
    "http://w3.usf.edu/FreeAssociation/AppendixA/Cue_Target_Pairs.S",
    "http://w3.usf.edu/FreeAssociation/AppendixA/Cue_Target_Pairs.T-Z"
]
"""
Details:
http://w3.usf.edu/FreeAssociation/AppendixA/index.html

0  CUE     Normed Word
1  TARGET  Response to Normed Word
2  NORMED? Is Response Normed?
3  #G      Group size
4  #P      Number of Participants Producing Response
5  FSG     Forward Cue-to-Target Strength
6  BSG     Backward Target-to-Cue Strength
7  MSG     Mediated Strength
8  OSG     Overlapping Associate Strength
9  #M      Number of Mediators
10 MMIA	   Number of Non-Normed Potential Mediating Associates
11 #O      Number of Overlaping Associates
12 OMIA	   Number of Non-Normed Overlapping Associates
13 QSS     Cue: Set Size
14 QFR     Cue: Frequency
15 QCO     Cue: Concreteness
16 QH      Cue is a Homograph?
17 QPS     Cue: Part of Speech
18 QMC     Cue: Mean Connectivity Among Its Associates
19 QPR     Cue: Probability of a Resonant Connection
20 QRSG	   Cue: Resonant Strength
21 QUC     Cue: Use Code
22 TSS     Target: Set Size
23 TFR     Target: Frequency
24 TCON	   Target: Concreteness
25 TH      Target is a Homograph?
26 TPS     Target: Part of Speech
27 TMC     Target: Mean Connectivity Among ItsAssociates
28 TPR     Target: Probability of a Resonant Connection
29 TRSG	   Target: Resonant Strength
30 TUC     Target: Use Code
"""

def _parseResponse(response: str, data: Dict[str, List[str]]):
    passedCSVHeader = False
    for _line in response.splitlines():
        if not _line.startswith("<") and _line.strip() != "":
            if not passedCSVHeader:
                passedCSVHeader = True
                continue
            # _line = _line.replace("¥", "0")
            linedata = _line.split(",")
            if linedata[0] in data:
                data[linedata[0]].append(linedata)
            else:
                data[linedata[0]] = [linedata]

async def _loadURL(url: str, data: Dict[str, List[str]], session: aiohttp.ClientSession):
    print(f"{url}: Downloading")
    response = await session.get(url)
    print(f"{url}: Parsing")
    _parseResponse(await response.text(), data)
    print(f"{url}: Done")

async def load() -> Dict[str, List[str]]:
    _data: Dict[str, List[str]] = {}
    session = aiohttp.ClientSession()
    await asyncio.gather(*[_loadURL(url, _data, session) for url in sources])
    return _data

data = asyncio.run(load())
print("Done!")
while True:
    print(data[input()])