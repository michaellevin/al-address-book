import typing
from .contact import IContact


class AddressBook:
    def __init__(self):
        self._contacts = []

    def add(self, name: str, address: str, phone_no: typing.Optional[str]):
        self._contacts.append(IContact(name, address, phone_no))

    # def remove(self, name):
    #     self._entries = [(n, a) for n, a in self._entries if n != name]

    # def lookup(self, name):
    #     return [address for n, address in self._entries if n == name]

    # def names(self):
    #     return [name for name, address in self._entries]

    def clear(self):
        self._contacts = []

    def __len__(self):
        return len(self._contacts)
