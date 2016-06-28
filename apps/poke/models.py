from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
class UserManager(models.Manager):
	def login(self, email, password):
		try:
			user = self.get(email=email)
			if bcrypt.hashpw(password.encode('utf-8'), user.password.encode('utf-8')) == user.password:
				return(True, user)
		except:
			# raise
			return(False,{"login": "login failed"})
		return(False,{"login": "login failed"})

	def register(self, name, alias, email, password, confirm_password):
		errors={}
		if len(name) < 2:
			errors['name'] = "Name is too short"
		if len(alias) < 1:
			errors['alias'] = "Enter the name you would like to be called"
		if len(password) < 8:
			errors['password'] = "Password is too short"
		if password != confirm_password:
			errors['confirm_password'] = "Passwords must match"
		try:
			user = self.get(email__iexact=email)
			errors['invalid'] = "Invalid registration"
		except:
			pass
		if not EMAIL_REGEX.match(email):
			errors['email'] = "Please enter a valid email"
		if errors:
			return(False, errors)
		password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
		self.create(name=name, alias=alias, password=password, email=email)
		return(True, self.get(email=email))
# Create your models here.
class User(models.Model):
	name = models.CharField(max_length = 45)
	alias = models.CharField(max_length = 45)
	email = models.EmailField() #auto validation for us!
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	userManager = UserManager()

class Poke(models.Model):
	poke = models.IntegerField(default=1)
	user1 = models.ForeignKey(User, related_name='f1')
	user2 = models.ForeignKey(User, related_name='f2')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
