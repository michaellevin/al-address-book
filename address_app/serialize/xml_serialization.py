import xml.etree.ElementTree as ET
from .base_serialization import ISerializeStrategy
from ..database.db_schema import DbSchema


class XMLStrategy(ISerializeStrategy):
    @classmethod
    def format(cls) -> str:
        return "xml"

    @classmethod
    def serialize(cls, data: DbSchema) -> str:
        root = ET.Element("DbSchema")
        contacts = ET.SubElement(root, "contacts")
        for cid, info in data.contacts.items():
            contact = ET.SubElement(contacts, "contact", id=str(cid))
            for key, value in info.items():
                ET.SubElement(contact, key).text = value

        books = ET.SubElement(root, "books")
        for book_name, ids in data.books.items():
            book = ET.SubElement(books, "book", name=book_name)
            for cid in ids:
                ET.SubElement(book, "contact_id").text = str(cid)

        return ET.tostring(root, encoding="unicode")

    @classmethod
    def deserialize(cls, data: str) -> DbSchema:
        root = ET.fromstring(data)
        contacts = {}
        for contact in root.find("contacts").findall("contact"):
            cid = int(contact.get("id"))
            info = {child.tag: child.text for child in contact}
            contacts[cid] = info

        books = {}
        for book in root.find("books").findall("book"):
            book_name = book.get("name")
            ids = [int(cid.text) for cid in book.findall("contact_id")]
            books[book_name] = ids

        return DbSchema(contacts=contacts, books=books)
