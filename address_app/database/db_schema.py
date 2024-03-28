from typing import Dict, List
from dataclasses import dataclass, field

ContactDictTypeAlias = Dict[str, str]
BookContactIdsTypeAlias = List[int]

DbContactsTypeAlias = Dict[int, ContactDictTypeAlias]
DbBooksTypeAlias = Dict[str, BookContactIdsTypeAlias]


@dataclass
class DbSchema:
    """
    Represents the database schema, including a mapping of contacts and address books.

    This class maintains two primary attributes: `contacts` and `books`. The `contacts`
    attribute is a dictionary mapping unique contact IDs to contact details, while the
    `books` attribute maps the name of address books to lists of contact IDs contained
    within each book.

    Attributes:
        contacts (Dict[int, Dict[str, str]]): A dictionary where each key is a unique
            contact ID (an integer), and each value is another dictionary containing
            the contact's name, address, and phone number.
        books (Dict[str, List[int]]): A dictionary where each key is the name of an
            address book (a string), and each value is a list of IDs (integers) of
            contacts contained within that address book.

    Example Usage:
        >>> schema = DbSchema()
        >>> print(schema)
        DbSchema(contacts={}, books={})

        >>> schema.contacts = {
        ...     3914141904: {
        ...         'name': 'John Doe',
        ...         'address': '123 Main St',
        ...         'phone_no': '555-1234'
        ...     },
        ...     3914141905: {
        ...         'name': 'Jane Doe',
        ...         'address': '456 Elm St',
        ...         'phone_no': '555-6789'
        ...     }
        ... }
        >>> schema.books = {
        ...     'TestBook': [3914141904, 3914141905],
        ...     'AnotherBook': [3914141904]
        ... }
        >>> print(schema.contacts)
        {3914141904: {'name': 'John Doe', 'address': '123 Main St', 'phone_no': '555-1234'}, 3914141905: {'name': 'Jane Doe', 'address': '456 Elm St', 'phone_no': '555-6789'}}

        >>> print(schema.books)
        {'TestBook': [3914141904, 3914141905], 'AnotherBook': [3914141904]}
    """

    contacts: DbContactsTypeAlias = field(default_factory=dict)
    books: DbBooksTypeAlias = field(default_factory=dict)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, DbSchema):
            return False
        # TODO - Implement the comparison logic
        return self.books.keys() == __value.books.keys()


if __name__ == "__main__":
    def_schema = DbSchema()
    print(def_schema)
