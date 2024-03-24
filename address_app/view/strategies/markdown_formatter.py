from .base_formatter import FormatterStrategy


class MarkdownFormatter(FormatterStrategy):
    def format(self, address_book) -> str:
        lines = [f"# Address Book: {address_book.name}", "## Contacts"]
        for contact in address_book:
            lines.append(
                f"- **Name**: {contact.name}\n  - **Address**: {contact.address}\n  - **Phone Number**: {contact.phone_no}"
            )
        return "\n".join(lines)
