import random
from typing import Callable, Dict, List, Union

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
        for part in self.sentence:
            if isinstance(part, str):
                text += part
            else:  # It's a function
                text += part()
        return text


@fcode("nn")
def noun():
    return random.choice(lists_noun)


@fcode("ni")
def indef_noun():
    return indef_article(random.choice(lists_noun))


@fcode("np")
def plural_noun():
    return plural(random.choice(lists_noun))


@fcode("vb")
def verb():
    return random.choice(lists_verb)


@fcode("vp")
def present_verb():
    return present_tense(random.choice(lists_verb))


@fcode("ad")
def adjective():
    return random.choice(lists_adj)


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
    buildStructure("a %nn is like %ni but if it was %ad"),
    buildStructure("if %nn had %ni then more %nn would %vb it"),
    buildStructure("life is a %vb %nn"),
    buildStructure("you know when you're %vp your %nn, you're %vp your %nn"),
    buildStructure("why do we have %ad %nn if we have %nn?"),
    buildStructure(
        "if you become %ni then you are legally allowed to %vb %np"),
    buildStructure("%nn has big %nn energy")
]