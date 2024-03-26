from .base_formatter import IBaseFormatter


class HtmlFormatter(IBaseFormatter):
    def format(self, address_book) -> str:
        lines = [f"<h1>Address Book: {address_book.name}</h1>", "<ul>"]
        for contact in address_book:
            lines.append(
                f"<li>{contact.name}, {contact.address}, {contact.phone_no}</li>"
            )
        lines.append("</ul>")
        return "".join(lines)
