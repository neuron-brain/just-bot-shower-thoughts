# Fixes the grammar in specific cases.

from typing import Dict, Tuple


VOWELS = ('a', 'e', 'i', 'o', 'u')


def indef_article(noun: str) -> str:
    if noun[-1] == 's':
        return noun
    elif noun[0] in VOWELS:
        return f'an {noun}'
    else:
        return f'a {noun}'


def plural(noun: str) -> str:
    if noun[-1] == "y" and noun[-2] not in VOWELS:
        return f"{noun[:-1]}ies"
    elif noun[-2:] == "is":
        return f"{noun[:-2]}es"
    elif noun[-2:] == "on":
        return f"{noun[:-2]}a"
    elif noun.endswith(("s", "ss", "sh", "ch", "x", "z")):
        return f'{noun}es'
    else:
        return f"{noun}s"


# Load irregular verbs
# infinitive | simple past | past participle
file = open("irregular_verbs.csv", "r+")
header = True
irregular_verbs: Dict[str, Tuple[str, str, str]] = {}
for line in file:
    line = line.strip()
    if header:
        header = False
        continue
    if line != "":
        item = tuple(line.lower().split(","))
        irregular_verbs[item[0]] = item


# Verbs
def present_participle(verb: str) -> str:
    verb = verb.lower()
    if verb[-1] == 'e':
        return f'{verb[:-1]}ing'
    else:
        return f'{verb}ing'


def past_tense(verb: str) -> str:
    verb = verb.lower()
    if verb in irregular_verbs:
        return irregular_verbs[verb][1].split["/"][0]
    elif verb[-1] == "y":
        return f"{verb[:-1]}ied"
    elif verb[-1] == 'e':
        return f"{verb}d"
    else:
        return f"{verb}ed"


def past_participle(verb: str) -> str:
    verb = verb.lower()
    if verb in irregular_verbs:
        return irregular_verbs[verb][2].split["/"][0]
    elif verb[-1] == "y":
        return f"{verb[:-1]}ied"
    elif verb[-1] == 'e':
        return f"{verb}d"
    else:
        return f"{verb}ed"
