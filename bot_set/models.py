from peewee import *
from playhouse.migrate import *
from datetime import datetime

db = SqliteDatabase('users.db')
migrator = SqliteMigrator(db)

class Users(Model):
	id = IntegerField(primary_key=True)
	telegram_id = IntegerField()
	username = CharField()
	date = DateField(default=datetime.utcnow())
	is_admin = BooleanField(default=False)

	class Meta:
		database = db

class AnimeCode(Model):
	code = IntegerField(primary_key=True)
	name = CharField()
	source = CharField(null=True)

	class Meta:
		database = db