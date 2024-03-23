from dataclasses import dataclass, field

try:
    from .utils import hash_input
except ImportError:
    from utils import hash_input


@dataclass
class IContact:
    name: str
    address: str
    phone_no: str
    _id: int = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        self._id = hash_input(self.name + self.address + self.phone_no)

    @property
    def id(self) -> int:
        return self._id

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, IContact):
            return False
        return self.id == __value.id

    def __repr__(self) -> str:
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
