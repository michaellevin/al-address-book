from dataclasses import dataclass, field, asdict, fields

try:
    from ..base.hash_utils import hash_input
except ImportError:
    from address_app.base.hash_utils import hash_input


@dataclass
class IContact:
    """
    A Contact dataclass, which includes name, address, and phone number.

    :ivar name: The name of the contact.
    :ivar address: The contact's address.
    :ivar phone_no: The contact's phone number.
    :ivar _id: A unique identifier for the contact, generated based on
               the contact's details. This field is not intended to be
               directly accessed or serialized. The `_id` is computed
               such that contacts with identical names, addresses, and
               phone numbers (stripped from spaces) will have the same `_id`, ensuring uniqueness
               across different contacts. Conversely, contacts with any
               differing detail will generate different `_id` values.

               **Example**:

               Given two contacts:

               - Contact 1: John Doe, 123 Main St, 555-1234
               - Contact 2: John Doe,  123 Main St , 555-1234

               Both contacts will have the same `_id` since their details are identical.

               - Contact 3: Jane Doe, 456 Park Ave, 555-5678

               Contact 3 will have a different `_id` due to differing details.
    """

    name: str
    address: str
    phone_no: str
    _id: int = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        """Generates a unique identifier for the contact upon initialization."""
        self._id = hash_input(
            self.name.strip() + self.address.strip() + self.phone_no.strip()
        )

    @property
    def id(self) -> int:
        """The unique identifier for the contact, read-only.

        :return: The contact's unique identifier.
        :rtype: int
        """
        return self._id

    def to_dict(self) -> dict:
        """Converts the contact's details into a dictionary, excluding the unique identifier.

        :return: The contact's details as a dictionary.
        :rtype: dict
        """
        return {f.name: getattr(self, f.name) for f in fields(self) if f.name != "_id"}

    def __eq__(self, __o: object) -> bool:
        """Checks if another object is an `IContact` with the same unique identifier.

        :param other: The object to compare.
        :type other: object
        :return: True if both objects are `IContact` instances with the same id, False otherwise.
        :rtype: bool
        """
        if not isinstance(__o, IContact):
            return False
        return self.id == __o.id

    def __repr__(self) -> str:
        """
        Provides a human-readable representation of the contact.

        :return: A string representation of the contact.
        :rtype: str
        """
        return f"Person(name={self.name}, address={self.address}, phone_no={self.phone_no})"


if __name__ == "__main__":
    person = IContact("John Doe", "123 Main St", "555-1234")
    print(person)
    print(person.id)
    person2 = IContact("John Doe", "123 Main St", "555-1234")
    print(person2)
    print(person2.id)
    print(person == person2)
    print(id(person), id(person2))
