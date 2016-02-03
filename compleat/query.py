import urllib
import hashlib
import requests
import json
import datetime
import random

class Query(object):
    """
    Query object representing autocomplete suggestions from Google Search.

    @methods:
    - suggestions: an array of dicts with fields: 'relevance', 'text', 'title', 'type'
    - meta: dict with fields: lang, query, uuid, site, timestamp

    """
    URL_TEMPLATE = "http://suggestqueries.google.com/complete/search?client=chrome&hl={lang}&q={query}&ds={site}"
    def __init__(self, query, lang="en", site=""):
        self.query = query
        self.lang = lang
        self.site = site
        self.timestamp = datetime.datetime.now()
        self.rand = str(random.random())
        req = requests.get(self.url, headers={'User-Agent': requests.utils.default_user_agent() + '/r=' + self.rand})
        self.response = req.json()

    def __repr__(self):
        return '<compleat.query.Query: %s, results=%s >' % (self.meta, len(self.suggestions))

    def __str__(self):
        return 'Query: %s, results %s, time=%s' % (self.meta['query'], len(self.suggestions), self.meta['timestamp'])

    @property
    def url(self):
        encoded = self.query.encode("utf-8")
        escaped = urllib.parse.quote(encoded)
        return self.URL_TEMPLATE.format(
            query=escaped,
            lang=self.lang,
            site=self.site)

    @property
    def suggestions(self):
        query, sugg_texts, sugg_titles, _, meta = self.response
        zipped = zip(
            sugg_texts,\
            sugg_titles,\
            meta["google:suggesttype"],\
            meta["google:suggestrelevance"])
        dicts = [ {
            "text": z[0],
            "title": z[1],
            "type": z[2],
            "relevance": z[3]
        } for z in zipped ]
        return dicts

    @property
    def uid(self):
        _ = ":".join([
            self.query,
            self.lang,
            self.timestamp.ctime(),
            self.rand
        ]).encode("utf-8")
        return hashlib.md5(_).hexdigest()

    @property
    def meta(self):
        return {
            "query": self.query,
            "lang": self.lang,
            "timestamp": self.timestamp.ctime(),
            "uid": self.uid,
            "site": self.site,
        }
