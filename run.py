import address_app as address_app
from pprint import pprint

logger = address_app.get_logger()
adb = address_app.AdbDatabase()
print(address_app.get_supported_serialization_formats())
print(adb.get_address_book("TestBook"))
adb.deinit()
# adb.clear()
# book = adb.create_address_book("Book1")

# book1 = adb.get_address_book("Book1")
# # book2 = adb.get_address_book("Book1")
# # print(book1, book2, book1 is book2)

# book1.add_record("John Doe", "123 Main St", "555-1234")
# book1.add_record("John Doe", "123 Main St", "555-1234")
# book1.add_record("   ", "123 Main St", "555-1234")
# book1.add_record("John Denver", "123 Main St", "556-1234")
# book1.add_record("Bill Cane", "1 Goodwin St", "+1 (903) 1556-124")
# book1.add_record("Bill Cane", "1 Goodwin St", "+1df (903) 1556-124")
# print(book1)
# # adb.create_address_book("Book2")
# print(book1.find_contacts(name="John*"))
# print(book1.find_contacts(address="123*"))
# print(book1.find_contacts(phone_no="555*"))
# print(book1.find_contacts(phone_no="555*4"))

# dm = app.ViewManager(book1)
# dm.set_formatter("md")
# dm.display()
# dm.set_formatter("xz")
# dm.display()
# dm.set_formatter("text")
# dm.display()

# sm = app.SerializationManager(book1)

# try:
#     sm.serialize(".build/book1.json")
#     sm.serialize(".build/book1.xml")
#     sm.serialize(".build/book1.yaml")
#     sm.serialize(".build/book1.csv")
#     sm.serialize(".build/book1.xyz")
# except app.exceptions.AddressAppException as e:
#     logger.error(e.message)
# # # adb.deinit()
