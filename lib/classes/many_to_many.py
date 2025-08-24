# lib/classes/many_to_many.py

from collections import Counter


def _unique(seq):
    """Return unique elements preserving order."""
    return list(dict.fromkeys(seq))


class Article:
    all = []  # <-- list, not a method

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)

    # ---- properties ----
    @property
    def title(self):
        return getattr(self, "_title", None)

    @title.setter
    def title(self, value):
        if hasattr(self, "_title"):  # immutable after set
            return
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value

    @property
    def author(self):
        return getattr(self, "_author", None)

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value

    @property
    def magazine(self):
        return getattr(self, "_magazine", None)

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value


class Author:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return getattr(self, "_name", None)

    @name.setter
    def name(self, value):
        if hasattr(self, "_name"):  # immutable
            return
        if isinstance(value, str) and len(value) > 0:
            self._name = value

    # relationships
    def articles(self):
        return [a for a in Article.all if a.author is self]

    def magazines(self):
        return _unique([a.magazine for a in self.articles()])

    def add_article(self, magazine, title):
        if isinstance(magazine, Magazine):
            return Article(self, magazine, title)

    def topic_areas(self):
        arts = self.articles()
        if not arts:
            return None
        cats = _unique([a.magazine.category for a in arts if isinstance(a.magazine.category, str)])
        return cats or None


class Magazine:
    all = []

    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return getattr(self, "_name", None)

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value

    @property
    def category(self):
        return getattr(self, "_category", None)

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value

    # relationships
    def articles(self):
        return [a for a in Article.all if a.magazine is self]

    def contributors(self):
        return _unique([a.author for a in self.articles()])

    def article_titles(self):
        arts = self.articles()
        if not arts:
            return None
        return [a.title for a in arts]

    def contributing_authors(self):
        counts = Counter([a.author for a in self.articles() if isinstance(a.author, Author)])
        result = [author for author, n in counts.items() if n > 2]
        return result or None

    @classmethod
    def top_publisher(cls):
        if not Article.all or not cls.all:
            return None
        return max(cls.all, key=lambda m: len(m.articles()))
