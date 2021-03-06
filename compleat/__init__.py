"""
compleat

Fetch autocomplete suggestions from Google Search. Use responsibly. Not affiliated with Google.
"""

from .query import Query

VERSION = (0, 0, 2)
__version__ = ".".join(map(str, VERSION))


def suggest(query_string, lang="en", site="", ):
    return Query(query_string, lang, site)
