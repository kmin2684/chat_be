from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def index(request):
	return HttpResponse("Hello, world!")

def create_users(usernames, passwords):
	for i in range(len(usernames)):
		User(username = usernames[i], password = passwords[i]).save()
		
def create_group(people_username, room_name):
	room = Room(name = room_name)
	room.save()	
	for name in people_username:
		person = User.objects.get(username = name)
		person.chat_room.add(room)
		
def send_message(sender, room, content):
	message = Message(content = content, sender = sender, room = room)
	message.save()
	members = room.members.all()
	for member in members:
		# create_copy
		MessageCopy(original = message, owner = member).save()
	
def add_friend(user1, user2):
	user1.friends.add(user2)
	
def enter_room(user, room):
	messages = Message.objects.filter(room = room)
	for message in messages:
		copies = MessageCopy.objects.filter(original = message, owner = user, checked = False)
		for copy in copies:
			copy.checked = True
			copy.save()
	
# def enter_group(user, group):
	# make all message copies read in the group

# def create_group(request):
	# user_list = []
	# name =
	
# def send_message(request):
	# group = 
	# sender = request.user
	# message_content = 
	
# def add_friend(request):
	# friend = 
	