from html.parser import HTMLParser
import re

import click

from dennis.tools import get_available_formats, UnknownFormat


class Token(object):
    def __init__(self, s, type="text", mutable=True):
        self.s = s
        self.type = type
        self.mutable = mutable

    def __str__(self):
        return self.s

    def __repr__(self):
        return "<{0} {1}>".format(self.type, repr(self.s))

    def __eq__(self, token):
        return (
            self.s == token.s
            and self.mutable == token.mutable
            and self.type == token.type
        )

    def __ne__(self, token):
        return not self.__eq__(token)


class Tokenizer(object):
    name = ""
    desc = ""

    def tokenize_stream(self, token_stream):
        """Takes a token stream and returns a further tokenized stream

        :arg token_stream: the input token stream this transform
            is operating on

        :return: iterable of transformed tokens

        """
        new_tokens = []

        for token in token_stream:
            if token.mutable:
                new_tokens.extend(self.tokenize(token))
            else:
                new_tokens.append(token)

        return new_tokens

    def tokenize(self, token):
        """Breaks up a token into multiple token_stream

        :arg token: Token

        :returns: list of tokens

        """
        raise NotImplementedError


def collapse_whitespace(text):
    return re.compile(r"\s+", re.UNICODE).sub(" ", text).strip()


class HTMLTokenizer(HTMLParser, Tokenizer):
    name = "html"
    desc = "Parses HTML tokens."

    def __init__(self):
        HTMLParser.__init__(self)
        self.new_tokens = []
        self.immutable_data_section = None

    def reset_state(self):
        self.new_tokens = []
        self.immutable_data_section = None

    def tokenize(self, token):
        if not token.s:
            new_tokens = [token]
        else:
            self.feed(token.s)
            new_tokens = self.new_tokens
        self.reset_state()
        return new_tokens

    def handle_starttag(self, tag, attrs, closed=False):
        # style and script contents should be immutable
        if tag in ("style", "script"):
            self.immutable_data_section = tag

        # We want to translate alt and title values, but that's
        # it. So this gets a little goofy looking token-wise.

        s = "<" + tag
        for name, val in attrs:
            s += " "
            s += name
            s += '="'

            if name in ["alt", "title", "placeholder"]:
                self.new_tokens.append(Token(s, "html", False))
                if val:
                    self.new_tokens.append(Token(val))
                s = ""
            elif val:
                s += val
            s += '"'
        if closed:
            s += " /"
        s += ">"

        if s:
            self.new_tokens.append(Token(s, "html", False))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, closed=True)

    def handle_endtag(self, tag):
        self.immutable_data_section = None
        self.new_tokens.append(Token("</" + tag + ">", "html", False))

    def handle_data(self, data):
        if self.immutable_data_section:
            self.new_tokens.append(Token(data, self.immutable_data_section, False))
        else:
            self.new_tokens.append(Token(collapse_whitespace(data)))

    def handle_charref(self, name):
        self.new_tokens.append(Token("&#" + name + ";", "html", False))

    def handle_entityref(self, name):
        self.new_tokens.append(Token("&" + name + ";", "html", False))


class VariableTokenizer(Tokenizer):
    # FIXME: Change this to take a list of format classes and not pull in
    # all available formats--that's the responsibility of the caller.
    def __init__(self, formats=None):
        """
        :arg formats: List of variable formats

            If None, creates a VariableTokenizer that tokenizes on all
            formats of variables. Otherwise just recognizes the listed
            formats.

        """
        all_formats = get_available_formats()

        if formats is None:
            formats = all_formats.keys()

        # Convert names to classes
        self.formats = []

        for fmt in formats:
            try:
                self.formats.append(all_formats[fmt])
            except KeyError:
                raise UnknownFormat("{0} is not a known variable format".format(fmt))

        # Generate variable regexp
        self.vars_re = re.compile(
            r"(" + "|".join([vt.regexp for vt in self.formats]) + r")"
        )

    def contains(self, fmt):
        """Does this tokenizer contain specified variable format?"""
        return fmt in [tok.name for tok in self.formats]

    def tokenize(self, text):
        """Breaks s into strings and Python variables

        This preserves whitespace.

        :arg text: the string to tokenize

        :returns: list of tokens---every even one is a Python variable

        """
        return [token for token in self.vars_re.split(text) if token]

    def extract_tokens(self, text, unique=True):
        """Returns the set of variable in the text"""
        try:
            tokens = self.vars_re.findall(text)
            if unique:
                tokens = set(tokens)
            return tokens
        except TypeError:
            click.echo("TYPEERROR: {0}".format(repr(text)))

    def is_token(self, text):
        """Is this text a variable?"""
        return self.vars_re.match(text) is not None

    def extract_variable_name(self, text):
        for fmt in self.formats:
            if re.compile(fmt.regexp).match(text):
                return fmt.extract_variable_name(text)
