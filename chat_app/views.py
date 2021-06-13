from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def index(request):
	return HttpResponse("Hello, world!")			
			
def login_view(request):
	if request.method == "POST":

		# Attempt to sign user in
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "network/login.html", {
				"message": "Invalid username and/or password."
			})
	else:
		return render(request, "network/login.html")


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))


def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "network/register.html", {
				"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, "network/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "network/register.html")


# def update_all(request):
	# if request.method != "GET":
		# # error message
		# pass
	# user = request.user
	# rooms = user.chat_room.all()
	# rooms_update = []
	# rooms_update_not = []
	# for room in rooms:
		# messages = room.messages.all().order_by('-time_sent')
		# unread_count = 0
		# for message in messages:
			# if message.original_of.get(owner = user).checked:
				# break
			# else:
				# unread_count += 1
		# if unread_count = 0:
			# rooms_update_not += [{'room': room, 'latest_message': messages[0], 'unread_count': unread_count}]
		# else:
			# rooms_update += [{'room': room, 'latest_message': messages[0], 'unread_count': unread_count}]
	# rooms_update = sorted(rooms_update, lambda x: x['latest_message'].time_sent, reverse = True)
	# rooms_update_not = sorted(rooms_update_not, lambda x: x['latest_message'].time_sent, reverse = True)
	# pass 




# def create_users(usernames, passwords):
	# for i in range(len(usernames)):
		# User(username = usernames[i], password = passwords[i]).save()
		
# def create_group(people_username, room_name):
	# room = Room(name = room_name)
	# room.save()	
	# for name in people_username:
		# person = User.objects.get(username = name)
		# person.chat_room.add(room)
		
# def send_message(sender, room, content):
	# message = Message(content = content, sender = sender, room = room)
	# message.save()
	# members = room.members.all()
	# for member in members:
		# # create_copy
		# MessageCopy(original = message, owner = member).save()
	
# def add_friend(user1, user2):
	# user1.friends.add(user2)
	
# def enter_room(user, room):
	# messages = Message.objects.filter(room = room)
	# for message in messages:
		# copies = MessageCopy.objects.filter(original = message, owner = user, checked = False)
		# for copy in copies:
			# copy.checked = True
			# copy.save()




	
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
	