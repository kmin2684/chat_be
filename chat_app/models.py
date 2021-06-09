from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

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

