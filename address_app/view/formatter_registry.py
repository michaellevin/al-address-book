from ..base.exceptions import UnknownFormatterException
from .strategies import PlainTextFormatter, HtmlFormatter, MarkdownFormatter


class FormatterRegistry:
    registry = {}

    @classmethod
    def register(cls, name, formatter):
        cls.registry[name] = formatter

    @classmethod
    def get_formatter(cls, name):
        formatter_class = cls.registry.get(name)
        if formatter_class:
            return formatter_class()
        raise UnknownFormatterException(name)


# Register formatters
FormatterRegistry.register("text", PlainTextFormatter)
FormatterRegistry.register("html", HtmlFormatter)
FormatterRegistry.register("md", MarkdownFormatter)
