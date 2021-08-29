from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# def registration(request):

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data['user'])
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            # 'email': user.email
        })

class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def user_check(request):
	print(request.user)
	return Response({'username': request.user.username})
	# return JsonResponse({'username': 'none'})

@api_view(['POST'])
def registration(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	password2 = request.POST.get('password2')
	
	if len(password) > 0 and password != password2:
		return JsonResponse({"error": "passwords either empty and/or don't match"})
	
	try:
		user = User.objects.create(
			username = username,
		)
		user.set_password(password)
		user.save()
	except:
		return JsonResponse({"error": "failed to register the user"})

	token, created = Token.objects.get_or_create(user=user)
	return JsonResponse({'token': token.key, 'username': user.username})


# Create your views here.

def index(request):
	return HttpResponse("Hello, world!")			
		
def login_view(request):
	if request.method == "POST":

		# Attempt to sign user in
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return render(request, {"username": username})
		else:
			return JsonResponse({"message": "invalid crendentials"})



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
	