from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from .model_methods import *

# Create your models here.

class Room(models.Model):
	name = models.CharField(max_length=255)
	
	def __str__(self):
		return f"{self.name}"

# class User(AbstractBaseUser):
	# email = models.EmailField(max_length=60, blank = True)
	# username = models.CharField(max_length=40, unique=True)
	# friends = models.ManyToManyField("self", blank = True)
	# chat_room = models.ManyToManyField(Room, related_name = 
	# "members", blank = True)
	# USERNAME_FIELD = 'username'
	# EMAIL_FIELD = 'email'

class User(AbstractUser):
	email = models.EmailField(max_length=60, blank = True)
	first_name = models.CharField(max_length=40, blank = True)
	last_name = models.CharField(max_length=40, blank = True)
	friends = models.ManyToManyField("self", blank = True)
	chat_room = models.ManyToManyField(Room, related_name = 
	"members", blank = True)

	def create_group(self, room_name, members):
		room = Room(name = room_name)
		room.save()
		for member in members:
			member.chat_room.add(room)
		self.chat_room.add(room)
	
	def send_message(self, room, content):
		message = Message(content = content, sender = self, room = room)
		message.save()
		members = room.members.all()
		for member in members:
			if member == self:
				MessageCopy(original = message, owner = member, checked = True).save()
			else:
				MessageCopy(original = message, owner = member).save()
		
	def enter_room(self, room):
		messages = Message.objects.filter(room = room)
		for message in messages:
			copies = MessageCopy.objects.filter(original = message, owner = self, checked = False)
			for copy in copies:
				copy.checked = True
				copy.save()
	
	def update_all(self):
		return update_all_method(self)
		
	def update_room(self, room):
		return update_room_method(self, room) 
		
	def add_friend(self, friend):
		add_friend_method(self, friend) 
	
	def __str__(self):
		return f"{self.username}"
	
class Message(models.Model):
	content = models.TextField()
	sender = models.ForeignKey(User, models.SET_NULL, null = True, related_name="sender_of")
	time_sent = models.DateTimeField(auto_now_add = True)
	room = models.ForeignKey(Room, models.SET_NULL, null = True, related_name = "messages")
	
	def __str__(self):
		return f"{self.content}, sender: {self.sender.username}"
	

class MessageCopy(models.Model):
	original = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="original_of")
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_of")
	checked = models.BooleanField(default=False)
	# time_sent = models.DateTimeField()
	# class Meta
		# ordering = ["-time_sent"]
		
	def __str__(self):
		return f"{self.original.content}, sender: {self.original.sender.username}, ownder: {self.owner.username}, checked: {self.checked}"

