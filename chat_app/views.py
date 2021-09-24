from types import MemberDescriptorType
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, SingleOperandHolder
import json
import datetime

# def registration(request):


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_friend(request):
    if request.method == 'GET':
        username = request.GET.get('username').strip()
        if len(username) < 2:
            return Response({'error': 'search query must contain at least 2 characters'}, status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.filter(username__contains=username.lower())
        friends = request.user.friends.all()
        searchResult = []
        for user in users:
            if user == request.user:
                continue
            elif user in friends:
                searchResult += [{'username': user.username, 'isFriend': True}]
            else:
                searchResult += [{'username': user.username,
                                  'isFriend': False}]
        return Response(searchResult)
    elif request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("username").strip()
        try:
            user = User.objects.get(username=username)
            request.user.add_friend(user)
            return Response({"added": username})
        except Exception as e:
            print("\nFailed to add friend", e, "\n")
            return Response({"added": False})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def room_create(request):
    data = json.loads(request.body)
    print(data.get('members'))
    print(type(data.get('members')))
    members = [User.objects.get(username=member)
               for member in data.get('members')]
    room_name = data.get('name')
    content = data.get('content')
    room = request.user.create_group(
        room_name=room_name, members=members, content=content)
    return Response(room)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def room_update(request, room_id):
    room = request.user.chat_room.get(id=room_id)
    if request.method == 'GET':
        return Response(room.serialize(mode='detail', user=request.user))
    elif request.method == 'POST':
        data = json.loads(request.body)
        content = data.get("content")
        # print('\n\nroom_update\n\n')
        # print(request.POST)
        if content:
            # return Response({'sent': request.user.send_message(room=room, content=content).serialize()})
            sentMessage = request.user.send_message(room=room, content=content)
            return Response({'sent': sentMessage.serialize()})
        pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Token.objects.get(user=request.user).delete()
    request.user.auth_token.delete()
    return Response({'message': "logged out"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def general_update(request):
    friends = request.user.friends.all().order_by('username')
    rooms = request.user.chat_room.all().order_by()

    return Response({
        'friends': [friend.username for friend in friends],
        'rooms': [room.serialize(mode='brief', user=request.user) for room in rooms],
    })


def message_test(request):
    if request.method == 'GET':
        mode = request.GET.get('mode')
    pass


def datetime_test(request):
    return JsonResponse({'current_UTC_time': datetime.datetime.now()})
    # return JsonResponse({'current_UTC_time': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')})


@api_view(['POST'])
def json_check(request):
    # list_item = request.POST.get('list_item')
    # bool_item = request.POST.get('bool_item')
    data = json.loads(request.body)
    list_item = data.get('list_item')
    bool_item = data.get('bool_item')
    print('\n\n', list_item, type(list_item), list(list_item),
          '\n', bool_item, type(bool_item), bool(bool_item), '\n\n')
    return Response({'message': 'json check success'})


# @api_view(['POST'])


# def CreateNewRoom(request):
#     data = json.loads(request.body)
    # room_name
    # members
    # message
    # sender
    # create new room
    # create new message and link it to the new room


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        modified_data = request.data
        modified_data['username'] = request.data['username'].lower()
        serializer = self.serializer_class(data=modified_data,
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


# class Logout(APIView):
#     def get(self, request, format=None):
#         # simply delete the token to force a login
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def user_check(request):
    print(request.user)
    return Response({'username': request.user.username})
    # return JsonResponse({'username': 'none'})


@api_view(['POST'])
def registration(request):
    data = json.loads(request.body)
    username = data.get('username').strip()
    password = data.get('password').strip()
    password2 = data.get('password2').strip()

    if not (len(password) > 0 and password == password2):
        return JsonResponse({"error": "passwords either empty and/or don't match"})

    try:
        user = User.objects.create(
            username=username.lower(),
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


# def login_view(request):
#     if request.method == "POST":

#         # Attempt to sign user in
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         # Check if authentication successful
#         if user is not None:
#             login(request, user)
#             return render(request, {"username": username})
#         else:
#             return JsonResponse({"message": "invalid crendentials"})


# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("index"))


# def register(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         email = request.POST["email"]

#         # Ensure password matches confirmation
#         password = request.POST["password"]
#         confirmation = request.POST["confirmation"]
#         if password != confirmation:
#             return render(request, "network/register.html", {
#                 "message": "Passwords must match."
#             })

#         # Attempt to create new user
#         try:
#             user = User.objects.create_user(username, email, password)
#             user.save()
#         except IntegrityError:
#             return render(request, "network/register.html", {
#                 "message": "Username already taken."
#             })
#         login(request, user)
#         return HttpResponseRedirect(reverse("index"))
#     else:
#         return render(request, "network/register.html")


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
