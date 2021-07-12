from peewee import *
from datetime import date

from src.main.python.exceptions.application_exception import ApplicationException
from src.main.python.models.base_station import BaseStation

db = SqliteDatabase('people.db')


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db  # This model uses the "people.db" database.


db.connect()
# db.create_tables([Person, ])
#
# uncle_bob = Person(name='Samuel', birthday=date(1960, 1, 15))
# r = uncle_bob.save()  # bob is now stored in the database
# for person in Person.select():
#     print(person)

# r = Person.get(Person.id == 1)
# print(r.id, r.name, r.birthday)
# r.name = 'teste'
# r.save()

try:
    r = Person.get()
    print(r.id, r.name, r.birthday)
except BaseException:
    e = ApplicationException()
    print(e)

db.close()
