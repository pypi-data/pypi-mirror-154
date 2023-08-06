import requests
from random import choice
from abc import ABC, abstractmethod


class QuoteViewer(ABC):
    @classmethod
    @abstractmethod
    def get_quote(self) -> str:
        pass


class ZenQuotes(QuoteViewer):
    _url = "https://zenquotes.io/api/random"
    _quote = None

    @classmethod
    def _quote_format(cls):
        try:
            q = cls._quote[0]["q"]
            a = cls._quote[0]["a"]
            return f"{q}\n - {a}"
        except Exception:
            return "What's there in quotes?\n - No quotes."

    @classmethod
    def get_quote(cls):
        response = requests.get(cls._url)
        cls._quote = response.json()
        return cls._quote_format()


class ProgrammingQuotes(QuoteViewer):
    _url = "https://programming-quotes-api.herokuapp.com/Quotes/random"
    _quote = None

    @classmethod
    def _quote_format(cls):
        try:
            q = cls._quote["en"]
            a = cls._quote["author"]
            return f"{q}\n - {a}"
        except Exception:
            return "What's there in quotes?\n - No quotes."

    @classmethod
    def get_quote(cls):
        response = requests.get(cls._url)
        cls._quote = response.json()
        return cls._quote_format()


def QuoteFactory(category: list = None) -> QuoteViewer:
    obj = choice([ProgrammingQuotes(), ZenQuotes()])
    if not category:
        pass
    elif "zen" in category:
        obj = ZenQuotes()
    elif "tech" in category:
        obj = ProgrammingQuotes()
    return obj
