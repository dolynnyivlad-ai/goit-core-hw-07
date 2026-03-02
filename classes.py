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
        today = datetime.today()
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


book = AddressBook()

john_record = Record('John')
john_record.add_phone('1234567890')
john_record.add_phone('5555555555')

book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

print(book)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)

found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")

# Видалення запису Jane
book.delete("Jane")
