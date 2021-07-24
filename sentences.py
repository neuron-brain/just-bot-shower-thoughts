import random
from typing import Callable, Dict, List, Union

import association
from grammar_checks import *
from word_lists import *

formattingCodes: Dict[str, Callable] = {}


def fcode(code: str):
    """
    Registers a function with a formatting code for use when building sentences.
    """
    def decorator(func: Callable):
        formattingCodes[code] = func
        return func
    return decorator


class structure:
    def __init__(self, sentence: List[Union[str, Callable]]):
        self.sentence = sentence

    def generate(self) -> str:
        text = ""
        prev: List[str] = []
        for part in self.sentence:
            if isinstance(part, str):
                text += part
            else:  # It's a function
                text += part(prev)
        return text


@fcode("nn")
def noun(prev: List[str]):
    r = random.random()
    # Chance of association
    if r < 0.9 and len(prev) > 0:
        assoc = association.randUnweightedAssociation(prev, "N")
        if assoc is not None:
            #print(assoc)
            word = assoc.target.lower()
            prev.append(word)
            return word
    # If chance not met or no association found, pick random.
    word = association.randomWord("N").lower()
    #print(f"Random noun: {word}")
    prev.append(word)
    return word


@fcode("ni")
def indef_noun(prev: List[str]):
    return indef_article(noun(prev))


@fcode("np")
def plural_noun(prev: List[str]):
    return plural(noun(prev))


@fcode("vb")
def verb(prev: List[str]):
    r = random.random()
    # Chance of association
    if r < 0.9 and len(prev) > 0:
        assoc = association.randUnweightedAssociation(prev, "V")
        if assoc is not None:
            #print(assoc)
            word = assoc.target.lower()
            prev.append(word)
            return word
    # If chance not met or no association found, pick random.
    word = association.randomWord("V").lower()
    #print(f"Random verb: {word}")
    prev.append(word)
    return word


@fcode("vp")
def present_verb(prev: List[str]):
    return present_tense(verb(prev))


@fcode("aj")
def adjective(prev: List[str]):
    r = random.random()
    # Chance of association
    if r < 0.9 and len(prev) > 0:
        assoc = association.randUnweightedAssociation(prev, "AJ")
        if assoc is not None:
            #print(assoc)
            word = assoc.target.lower()
            prev.append(word)
            return word
    # If chance not met or no association found, pick random.
    word = association.randomWord("AJ").lower()
    #print(f"Random adjective: {word}")
    prev.append(word)
    return word


def buildStructure(formatted: str) -> structure:
    parts: List[Union[str, function]] = []
    ignorestart = True
    for part in formatted.split("%"):
        if ignorestart:
            parts.append(part)
            ignorestart = False
            continue
        parts.append(formattingCodes[part[:2]])
        parts.append(part[2:])
    return structure(parts)


sentence_structure: List[structure] = [
    buildStructure("%nn is just %ni"),
    buildStructure("%ni is like %ni but if it was %aj"),
    buildStructure("if %nn had %ni then more %nn would %vb it"),
    buildStructure("life is a %vb %nn"),
    buildStructure("you know when you're %vp your %nn, you're %vp your %nn"),
    buildStructure("why do we have %aj %nn if we have %nn?"),
    buildStructure(
        "if you become %ni then you are legally allowed to %vb %np"),
    buildStructure("%nn has big %nn energy")
]

#while True:
#    input()
#    print(random.choice(sentence_structure).generate())
