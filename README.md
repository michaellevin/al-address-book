# al-address-book
A small library which collects, filters, and saves users' personal data. 


## Module usage example

```python
import address_app

# Create an instance of AdbConnector with a specified storage strategy (e.g., JSON). Thus, the data will be stored in a JSON file in the specified directory (e.g., 'tests'). Default root directory is the temporary folder on your OS.
adb = address_app.AdbConnector("tests", "json")

# This instance is singleton, so you can access it from anywhere in your code. Two instances of AdbConnector will always be equal if they have the same root directory, but for different root directories, they will be different.

# Now lets demonstrate the usage of the library

# Query supported serialization formats
print(adb.supported_serialization_formats)
# Expected output: ['json', 'xml', 'yaml']

# Clear the database to start fresh
adb.db_manager.clear_database()

# Create an empty book named 'book1'
adb.db_manager.create_empty_book("book1")

# Add contacts to 'book1'
adb.db_manager.add_contact("book1", "John Doe", "123 Main St", "555-1234")
adb.db_manager.add_contact("book1", "John Denver", "123 Main St", "555-1234")
adb.db_manager.add_contact("book1", "Jane Doe", "587 St", "555-1234")
adb.db_manager.add_contact("book1", "Craig Hack", "456 Elm St", "1555-1234")

# Retrieve and print the contents of 'book1'
book1 = adb.db_manager.get_book("book1")
print(book1)
# Expected output: Details of 'book1' including contacts

# List all contacts in 'book1'
contacts = adb.db_manager.list_contacts("book1")
print(contacts)

# Filter contacts in 'book1' by name using a wildcard search
filtered_contacts = adb.db_manager.find_contacts("book1", name="John*")
print(filtered_contacts)

# Render and display the address book in HTML format
print(adb.render(format="html"))

# Change storage strategy to XML and YAML, demonstrating the flexibility in storage formats
adb.change_strategy("xml")
# Now the data will be stored in an XML file in the specified directory

adb.change_strategy("yaml")
# Now the data will be stored in a YAML file in the specified directory

```

## CLI Usage

This application can also be used as a CLI tool. To use it, run the following command:

```bash
python -m cli
```

Examples of CLI commands:
```bash
$ list-books
Listing all books...
[AddressBook(name=book1, (3 contacts))]

$ list-contacts book1
Listing all contacts in book1...
[Contact(name=John Tall, address=123 Elm St, phone_no=555-555), Contact(name=Joh Ball, address=456 Elm St, phone_no=555-555), Contact(name=Jane, address=123 Elm St, phone_no=555-555)]

$ create-book book2

$ filter-contacts book1 "@name=John*"
Filtering contacts in book: book1 with name: John*
[Contact(name=John Tall, address=123 elm St, phone_no=555-555)]

$ filter-contacts book1 "*S*"
[Contact(name=John Tall, address=123 elm St, phone_no=555-555), Contact(name=Joh Ball, address=456 elm St, phone_no=555-555), Contact(name=Jane, address=123 Elm St, phone_no=555-555)]
```


## Supported formats

### Serialization
- JSON
- XML
- YAML
- CSV (coming soon)


### Rendering
- HTML
- Markdown 
  


## Testing
To run the tests, execute the following command:

```bash
python -m unittest discover tests
```

## Documentation

For more detailed information on setting up your development environment, see the following [API Guide](./docs/_build/html/index.html)
