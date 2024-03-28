from .base_view import IViewer
from ..database.db_schema import DbSchema


class HtmlView(IViewer):
    @classmethod
    def format(cls) -> str:
        return "html"

    @classmethod
    def render(cls, db: DbSchema) -> str:
        lines = ["<div>"]
        for book_name in db.books:
            lines.append(f"<h1>Address Book: {book_name}</h1><ul>")
            for contact_id in db.books[book_name]:
                contact_as_dict = db.contacts[contact_id]
                for key, value in contact_as_dict.items():
                    lines.append(f"<li>{key}: {value}</li>")
            lines.append("</ul>")
        lines.append("</div>")
        return "".join(lines)
