# Description: This file is used to test the address_app module.
import address_app

# Create an instance of AdbConnector
adb = address_app.AdbConnector("tests", "json")

# Clear the database
adb.db_manager.clear_database()

# Create an empty book
adb.db_manager.create_empty_book("book1")

# Add contacts to the book
adb.db_manager.add_contact("book1", "John Doe", "123 Main St", "555-1234")
adb.db_manager.add_contact("book1", "John Denver", "123 Main St", "555-1234")
adb.db_manager.add_contact("book1", "Jane Doe", "587 St", "555-1234")
adb.db_manager.add_contact("book1", "Craig Hack", "456 Elm St", "1555-1234")

# Get the book and list the contacts
book1 = adb.db_manager.get_book("book1")
print(book1)
# Output: Book(name='book1', contacts=[Contact(name='John Doe', address='123 Main St', phone_no='555-1234'), Contact(name='John Denver', address='123 Main St', phone_no='555-1234')])

# List the contacts in the book
contacts = adb.db_manager.list_contacts("book1")
print(contacts)

# Find contacts by name
filtered_contacts = adb.db_manager.find_contacts("book1", name="John*")
print(filtered_contacts)

# Show the address book as HTML
print(adb.render(format="html"))

adb.change_strategy("xml")
adb.change_strategy("yaml")

# adb.delete()
print(adb)

adb2 = address_app.AdbConnector("tests2", "json")
adb3 = address_app.AdbConnector(r"C:\Cd\tests\al-address-book\tests", "json")
print(adb2 == adb3)
print(adb3 == adb)
