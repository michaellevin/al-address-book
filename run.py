import address_app as app
from pprint import pprint

adb = app.AdbDatabase()
pprint(adb.get_address_books())
print(adb)
adb2 = app.AdbDatabase()
print(adb2)
adb.clear_all()
book = adb.create_address_book("Book1")

book1 = adb.get_address_book("Book1")
# book2 = adb.get_address_book("Book1")
# print(book1, book2, book1 is book2)

book1.add_record("John Doe", "123 Main St", "555-1234")
book1.add_record("John Doe", "123 Main St", "555-1234")
book1.add_record("   ", "123 Main St", "555-1234")
book1.add_record("John Denver", "123 Main St", "556-1234")
book1.add_record("Bill Cane", "1 Goodwin St", "+1 (903) 1556-124")
book1.add_record("Bill Cane", "1 Goodwin St", "+1df (903) 1556-124")
print(book1)
# adb.create_address_book("Book2")
print(book1.find_contact(name="John*"))
print(book1.find_contact(address="123*"))
print(book1.find_contact(phone_no="555*"))
print(book1.find_contact(phone_no="555*4"))

dm = app.ViewManager(book1)
dm.set_formatter("md")
dm.display()
dm.set_formatter("xz")
dm.display()
dm.set_formatter("text")
dm.display()

sm = app.SerializationManager(book1)
try:
    sm.serialize("xrender/book1.json")
    sm.serialize("xrender/book1.xml")
    sm.serialize("xrender/book1.yaml")
    sm.serialize("xrender/book1.csv")
    sm.serialize("xrender/book1.xyz")
except app.exceptions.SerializationException as e:
    app.logger.error(e.message)
# # adb.deinit()
