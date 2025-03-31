from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits long")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        try:
            phone = Phone(phone_number)
            self.phones.append(phone)
            return f"Phone number {phone_number} added"
        except ValueError as e:
            return str(e)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return f"Phone number {phone_number} removed"
        return "Phone number not found"

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                try:
                    phone.value = Phone(new_number).value
                    return f"Phone number {old_number} changed to {new_number}"
                except ValueError as e:
                    return str(e)
        return "Phone number not found"

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return f"{phone_number}"
        return "Phone number not found"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
            return f"Contact {name} deleted"
        return "Contact not found"


def parse_input(user_input):
    """
    Parses user input into a command and arguments.
    Takes user input as parametr and return a tupple with a command and arguments.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    """
    Decorator for handling errors in user input.
    It catches ValueError, KeyError, and IndexError and returns
    appropriate error messages instead of stopping the program.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone number please"
        except KeyError:
            return "Enter user name"
        except IndexError:
            return "Enter the argument for the command"

    return inner


@input_error
def add_contact(args, contacts):
    """Adds a new contact to the contacts dictionary."""
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    """
    Updates an existing contact's phone number.
    If such contact does not founded, the function return error.
    """
    name, new_phone = args
    if name in contacts:
        contacts[name] = new_phone
        return "Contact updated."
    return "Error: Contact not found."


@input_error
def show_phone(args, contacts):
    """
    Shows the phone number of a contact.
    If such contact does not founded, the function return error.
    """
    name = args[0]
    if name in contacts:
        return contacts[name]
    return "Error: Contact not found."


@input_error
def show_all(contacts):
    """Displays all saved contacts.
    If contacts do not founded, the function return relevant message.
    """
    if not contacts:
        return "Contacts not found"
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main():
    """
    The main function that runs the assistant bot.
    """
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "bye"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
