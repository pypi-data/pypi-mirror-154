# flake8: noqa
from dennis.tokenizer import HTMLTokenizer, Token, VariableTokenizer


# FIXME: test VariableTokenizer


class TestHTMLTokenizer:
    def test_basic(self):
        tok = HTMLTokenizer()
        output = tok.tokenize(Token(""))
        assert output == [Token("", "text", True)]

        output = tok.tokenize(Token("<b>hi</b>"))
        assert output == [
            Token("<b>", "html", False),
            Token("hi", "text", True),
            Token("</b>", "html", False),
        ]

    def test_alt_title_placeholder(self):
        tok = HTMLTokenizer()
        output = tok.tokenize(Token('<img alt="foo">'))
        assert output == [
            Token('<img alt="', "html", False),
            Token("foo", "text", True),
            Token('">', "html", False),
        ]

        output = tok.tokenize(Token('<img title="foo">'))
        assert output == [
            Token('<img title="', "html", False),
            Token("foo", "text", True),
            Token('">', "html", False),
        ]

        output = tok.tokenize(Token('<input placeholder="foo">'))
        assert output == [
            Token('<input placeholder="', "html", False),
            Token("foo", "text", True),
            Token('">', "html", False),
        ]

    def test_script_style(self):
        tok = HTMLTokenizer()
        output = tok.tokenize(Token("<style>TR {white-space: nowrap;}</style>"))
        assert output == [
            Token("<style>", "html", False),
            Token("TR {white-space: nowrap;}", "style", False),
            Token("</style>", "html", False),
        ]

        output = tok.tokenize(Token('<script>console.log("foo");</script>'))
        assert output == [
            Token("<script>", "html", False),
            Token('console.log("foo");', "script", False),
            Token("</script>", "html", False),
        ]

    def test_whitespace_collapse(self):
        def _tokenize(text):
            return HTMLTokenizer().tokenize(Token(text))

        assert _tokenize("<html><body>hello!</body></html>") == _tokenize(
            "<html><body>    hello!    </body></html>"
        )
