import asyncio
import random
from typing import Dict, List, Optional, Union

import aiohttp

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
10 MMIA    Number of Non-Normed Potential Mediating Associates
11 #O      Number of Overlaping Associates
12 OMIA    Number of Non-Normed Overlapping Associates
13 QSS     Cue: Set Size
14 QFR     Cue: Frequency
15 QCO     Cue: Concreteness
16 QH      Cue is a Homograph?
17 QPS     Cue: Part of Speech
18 QMC     Cue: Mean Connectivity Among Its Associates
19 QPR     Cue: Probability of a Resonant Connection
20 QRSG    Cue: Resonant Strength
21 QUC     Cue: Use Code
22 TSS     Target: Set Size
23 TFR     Target: Frequency
24 TCON    Target: Concreteness
25 TH      Target is a Homograph?
26 TPS     Target: Part of Speech
27 TMC     Target: Mean Connectivity Among Its Associates
28 TPR     Target: Probability of a Resonant Connection
29 TRSG    Target: Resonant Strength
30 TUC     Target: Use Code

Parts of Speech
N   Noun
V   Verb
AJ  Adjective
AD  Adverb
P   Pronoun
PP  Preposition
I   Interjection
C   Conjunction
"""


class association:
    def __init__(self, data: List[str]):
        self.cue = data[0]
        self.target = data[1]
        self.FSG = float(data[5])
        self.QPS = data[17]
        self.TPS = data[26]

    def __str__(self):
        return f"{self.cue} ({self.QPS}) -> {self.target} ({self.TPS}): {self.FSG}"

    def __repr__(self):
        return f"association({self.__str__()})"


def _parseResponse(response: str, data: Dict[str, List[str]]):
    passedCSVHeader = False
    for _line in response.splitlines():
        if not _line.startswith("<") and _line.strip() != "":
            if not passedCSVHeader:
                passedCSVHeader = True
                continue
            # _line = _line.replace("¥", "0")
            linedata = _line.split(",")
            linedata = [i.strip() for i in linedata]
            if linedata[0] in data:
                data[linedata[0]].append(association(linedata))
            else:
                data[linedata[0]] = [association(linedata)]


async def _loadURL(url: str, data: Dict[str, List[str]], session: aiohttp.ClientSession):
    print(f"{url}: Downloading")
    response = await session.get(url)
    print(f"{url}: Parsing")
    _parseResponse(await response.text(), data)
    print(f"{url}: Done")


async def load() -> Dict[str, List[association]]:
    _data: Dict[str, List[association]] = {}
    session = aiohttp.ClientSession()
    await asyncio.gather(*[_loadURL(url, _data, session) for url in sources])
    return _data

data = asyncio.run(load())
print("Finished loading word associations")


def getAssociations(cue: str, pos: Optional[str] = None) -> List[association]:
    """
    Gets the associations for a given part of speech (see above).
    If pos is None, all parts of speech will be accepted.
    """
    associations: List[association] = []
    for assoc in data[cue.upper()]:
        if pos is None or assoc.TPS == pos.upper():
            associations.append(assoc)
    return associations


class cumulativeAssociation:
    def __init__(self, target: str, TPS: str, cues: Dict[str, float] = {}):
        self.target = target
        self.TPS = TPS
        self.cues = cues

    @property
    def FSG(self) -> float:
        return sum(self.cues.values())

    def __str__(self):
        return f"{self.target} ({self.TPS}): {self.FSG} {self.cues}"

    def __repr__(self):
        return f"cumulativeAssociation({self.__str__()})"


def getCumulativeAssociations(cues: List[str], pos: Optional[str] = None) -> List[cumulativeAssociation]:
    associations: Dict[str, cumulativeAssociation] = {}
    for cue in cues:
        cAssocs = getAssociations(cue, pos)
        for cAssoc in cAssocs:
            if cAssoc.target in associations:
                associations[cAssoc.target].cues[cAssoc.cue] = cAssoc.FSG
            else:
                associations[cAssoc.target] = cumulativeAssociation(
                    cAssoc.target, cAssoc.TPS, {cAssoc.cue: cAssoc.FSG})
    return list(associations.values())


def randWeightedAssociation(cue: Union[str, List[str]], pos: Optional[str] = None) -> association:
    if isinstance(cue, str):
        associations = getAssociations(cue, pos)
    else:
        associations = getCumulativeAssociations(cue, pos)
    if len(associations) == 0:
        return None
    return random.choices(associations, [assoc.FSG for assoc in associations])[0]


def randUnweightedAssociation(cue: Union[str, List[str]], pos: Optional[str] = None) -> association:
    if isinstance(cue, str):
        associations = getAssociations(cue, pos)
    else:
        associations = getCumulativeAssociations(cue, pos)
    if len(associations) == 0:
        return None
    return random.choice(associations)


def randomWord(pos: Optional[str] = None) -> str:
    """
    Selects a random word of a given part of speech (see above).
    If pos is None, all parts of speech will be accepted.
    This may be slow if we are unlucky, since it basically selects random words and checks their part of speech until it finds one. Will time out after 100 words.
    """
    for i in range(100):  # We have to loop to ensure the word is the correct part of speech.
        word: str = random.choice(list(data.keys()))
        if len(data[word]) != 0 and (pos is None or pos.upper() == data[word][0].QPS):
            return word
    return f"WORD_NOT_FOUND_POS_({pos})"
