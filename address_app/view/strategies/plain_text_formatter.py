from .base_formatter import IBaseFormatter


class PlainTextFormatter(IBaseFormatter):
    def format(self, address_book) -> str:
        lines = [f"Address Book: {address_book.name}"]
        for i, contact in enumerate(address_book):
            lines.append(f"{i}. {contact.name}, {contact.address}, {contact.phone_no}")
        return "\n".join(lines)
