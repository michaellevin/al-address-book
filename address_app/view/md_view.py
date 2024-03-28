from .base_view import IViewer

from ..database.db_schema import DbSchema


class MarkdownView(IViewer):
    @classmethod
    def format(cls) -> str:
        return "md"

    @classmethod
    def render(self, db: DbSchema) -> str:
        lines = []
        for book_name in db.books:
            lines.append(f"# Address Book: {book_name}\n\n")
            lines.append("## Contacts\n")
            for contact_id in db.books[book_name]:
                contact_as_dict = db.contacts[contact_id]
                lines.append("### Contact\n")
                for key, value in contact_as_dict.items():
                    lines.append(f"- **{key}**: {value}\n")
        return "".join(lines)
