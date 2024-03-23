from abc import ABC, abstractmethod

from .exceptions import UnknownFormatterException


class FormatterStrategy(ABC):
    @abstractmethod
    def format(self, address_book) -> str:
        pass


class PlainTextFormatter(FormatterStrategy):
    def format(self, address_book) -> str:
        lines = [f"Address Book: {address_book.name}"]
        for i, contact in enumerate(address_book):
            lines.append(f"{i}. {contact.name}, {contact.address}, {contact.phone_no}")
        return "\n".join(lines)


class HtmlFormatter(FormatterStrategy):
    def format(self, address_book) -> str:
        lines = [f"<h1>Address Book: {address_book.name}</h1>", "<ul>"]
        for contact in address_book:
            lines.append(
                f"<li>{contact.name}, {contact.address}, {contact.phone_no}</li>"
            )
        lines.append("</ul>")
        return "".join(lines)


class MarkdownFormatter(FormatterStrategy):
    def format(self, address_book) -> str:
        lines = [f"# Address Book: {address_book.name}", "## Contacts"]
        for contact in address_book:
            lines.append(
                f"- **Name**: {contact.name}\n  - **Address**: {contact.address}\n  - **Phone Number**: {contact.phone_no}"
            )
        return "\n".join(lines)


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
