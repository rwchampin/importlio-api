
from django.template.defaultfilters import slugify


filler_words = [
    "A",
    "ABOUT",
    "ACTUALLY",
    "ALMOST",
    "ALSO",
    "ALTHOUGH",
    "ALWAYS",
    "AM",
    "AN",
    "AND",
    "ANY",
    "ARE",
    "AS",
    "AT",
    "BE",
    "BECAME",
    "BECOME",
    "BUT",
    "BY",
    "CAN",
    "COULD",
    "DID",
    "DO",
    "DOES",
    "EACH",
    "EITHER",
    "ELSE",
    "FOR",
    "FROM",
    "HAD",
    "HAS",
    "HAVE",
    "HENCE",
    "HOW",
    "I",
    "IF",
    "IN",
    "IS",
    "IT",
    "ITS",
    "JUST",
    "MAY",
    "MAYBE",
    "ME",
    "MIGHT",
    "MINE",
    "MUST",
    "MY",
    "MINE",
    "MUST",
    "MY",
    "NEITHER",
    "NOR",
    "NOT",
    "OF",
    "OH",
    "OK",
    "WHEN",
    "WHERE",
    "WHEREAS",
    "WHEREVER",
    "WHENEVER",
    "WHETHER",
    "WHICH",
    "WHILE",
    "WHO",
    "WHOM",
    "WHOEVER",
    "WHOSE",
    "WHY",
    "WILL",
    "WITH",
    "WITHIN",
    "WITHOUT",
    "WOULD",
    "YES",
    "YET",
    "YOU",
    "YOUR",
    "the",
    "a",
    "an",
    "and",
    "but",
    "or",
    "for",
    "nor",
    "on",
    "at",
    "to",
    "from",
    "by",
    "so",
    "than",
    "then",
    "too",
    "very",
    "can",
    "will",
    "shall",
    "could",
    "would",
    "should",
    "may",
    "might",
    "must",
    "do",
    "a",
    "about",
    "above",
    "after",
    "again",
    "against",
    "all",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "below",
    "between",
    "both",
    "but",
    "by",
    "could",
    "did",
    "do",
    "does",
    "doing",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "has",
    "have",
    "having",
    "he",
    "he'd",
    "he'll",
    "he's",
    "her",
    "here",
    "here's",
    "hers",
    "herself",
    "him",
    "himself",
    "his",
    "how",
    "how's",
    "i",
    "i'd",
    "i'll",
    "i'm",
    "i've",
    "if",
    "in",
    "into",
    "is",
    "it",
    "it's",
    "its",
    "itself",
    "let's",
    "me",
    "more",
    "most",
    "my",
    "myself",
    "nor",
    "of",
    "on",
    "once",
    "only",
    "or",
    "other",
    "ought",
    "our",
    "ours",
    "ourselves",
    "out",
    "over",
    "own",
    "same",
    "she",
    "she'd",
    "she'll",
    "she's",
    "should",
    "so",
    "some",
    "such",
    "than",
    "that",
    "that's",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "there",
    "there's",
    "these",
    "they",
    "they'd",
    "they'll",
    "they're",
    "they've",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "until",
    "up",
    "very",
    "was",
    "we",
    "we'd",
    "we'll",
    "we're",
    "we've",
    "were",
    "what",
    "what's",
    "when",
    "when's",
    "where",
    "where's",
    "which",
    "while",
    "who",
    "who's",
    "whom",
    "why",
    "why's",
    "with",
    "would",
    "you",
    "you'd",
    "you'll",
    "you're",
    "you've",
    "your",
    "yours",
    "yourself",
    "yourselves"
]


def clean_slug(slug):
    print(slug)
    sentence = slugify(slug)
    print(sentence)
    sentence = sentence.split('-')
    print(sentence)
    for filler in filler_words:
        if filler in sentence:
            sentence.remove(filler)
    print(sentence)
    new_slug = slugify(sentence)
    print(new_slug)
    print('*********************************')
    return new_slug
