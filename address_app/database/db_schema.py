from typing import Any, Dict, List
from dataclasses import dataclass, field

ContactDictTypeAlias = Dict[str, str]
BookContactIdsTypeAlias = List[int]

DbContactsTypeAlias = Dict[int, ContactDictTypeAlias]
DbBooksTypeAlias = Dict[str, BookContactIdsTypeAlias]


@dataclass
class DbSchema:
    """Represents the database schema.

    Example Usage:
        >>> schema = DbSchema()
        >>> schema
        DbSchema(contacts=[], books=[])

    contacts: A list of contacts in the database.
    books: A list of address books in the database.

    contacts = {
        3914141904: {
                'name': 'John Doe',
                'address': '123 Main St',
                'phone_no': '555-1234'
        },
        3914141905: {
                'name': 'Jane Doe',
                'address': '456 Elm St',
                'phone_no': '555-6789'
        }
    }
    books = {
        'TestBook': [3914141904, 3914141905],
        'AnotherBook': [3914141904]
    }

    """

    contacts: DbContactsTypeAlias = field(default_factory=list)
    books: DbBooksTypeAlias = field(default_factory=list)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, DbSchema):
            return False
        # TODO - Implement the comparison logic
        return self.books.keys() == __value.books.keys()


if __name__ == "__main__":
    def_schema = DbSchema()
    print(def_schema)
