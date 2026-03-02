from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError('Phone number must be 10 digits')
        super().__init__(phone_number)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, phone_numb_current, phone_numb_new):
        phone = self.find_phone(phone_numb_current)
        if phone:
            self.remove_phone(phone_numb_current)
            self.add_phone(phone_numb_new)
            return
        raise ValueError(f"{phone_numb_current} didn't find")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

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

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        max_date = today + timedelta(days=days)
        upcoming_birthdays = []

        for record in self.data.values():
            birthday = record.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year.isoweekday() == 6:
                birthday_this_year += timedelta(days=2)
            if birthday_this_year.isoweekday() == 7:
                birthday_this_year += timedelta(days=1)

            if today <= birthday_this_year <= max_date:
                upcoming_birthdays.append(
                    {'name': record.name.value
                        , 'birthday': birthday_this_year.strftime('%d.%m.%Y')}
                )

        return upcoming_birthdays

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError:
            return 'Enter name and phone please.'
        except KeyError:
            return 'Enter user name'
        except IndexError:
            return 'Enter the argument for the command'

    return inner


def parse_input(user_input):
    if user_input == '':
        return '', []  # Повертаємо пусту команду і пустий список

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts: AddressBook):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, contacts: AddressBook):
    name, phone, phone_number_old, phone_number_new = args
    record = contacts.find(name)
    if record:
        record.edit_phone(phone_number_old, phone_number_new)
        return "Contact updated."
    else:
        return f"Contact {name} not found."


@input_error
def phone_username(args, contacts: AddressBook):
    name = args[0]
    record = contacts.find(name)
    if record:
        return record
    else:
        return f"Contact {name} not found."

@input_error
def show_all(contacts: AddressBook):
    if contacts:
        return '\n'.join(str(record) for record in contacts.values())
    else:
        return "No contacts found."

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        f"Contact {name} not found."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return record.birthday.value
    else:
        return f"Contact {name} not found."

@input_error
def birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        return '\n'.join(f'{item['name']}: {item['birthday']}' for item in upcoming)
    else:
        return "No upcoming birthdays."



def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add".lower():
            print(add_contact(args, book))

        elif command == "change".lower():
            print(change_contact(args, book))

        elif command == "phone".lower():
            print(phone_username(args, book))

        elif command == "all".lower():
            print(show_all(book))

        elif command == "add-birthday".lower():
            print(add_birthday(args, book))

        elif command == "show-birthday".lower():
            print(show_birthday(args, book))

        elif command == "birthdays".lower():
            print(birthdays(book))

        else:
            print("Invalid command.")



if __name__ == "__main__":
    main()
