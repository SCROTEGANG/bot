import re

PRONOUNS = [
    "they/them",
    "she/her",
    "he/him",
    "they/she",
    "they/he",
]

PRONOUN_RE = re.compile(r"\w+\/\w+")
