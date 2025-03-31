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
