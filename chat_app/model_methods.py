def update_all_method(user):
	rooms = user.chat_room.all()
	rooms_update = []
	rooms_update_not = []
	for room in rooms:
		messages = room.messages.all().order_by('-time_sent')
		unread_count = 0
		for message in messages:
			if message.original_of.get(owner = user).checked:
				break
			else:
				unread_count += 1
		if unread_count == 0:
			rooms_update_not += [{'room': room, 'latest_message': messages[0], 'unread_count': unread_count}]
		else:
			rooms_update += [{'room': room, 'latest_message': messages[0], 'unread_count': unread_count}]
	rooms_update = sorted(rooms_update, key = lambda x: x['latest_message'].time_sent, reverse = True)
	rooms_update_not = sorted(rooms_update_not, key = lambda x: x['latest_message'].time_sent, reverse = True)
	return (rooms_update, rooms_update_not)
	
def update_room_method(user, room):
	# query messages that belongs to a room in reverse order
	# for each message get a copy that belongs to the user
	# [{'message': message, 'copy':copy}]
	messages = room.messages.all().order_by('-time_sent')
	message_update = []
	message_update_not = []
	for message in messages:
		copy = message.original_of.get(owner = user)
		if copy.checked:
			message_update_not += [copy]
		else: 
			# better to check message after the client receives the messages 
			copy.checked = True
			copy.save()
			message_update += [copy]
	return (message_update, message_update_not)
	
def add_friend_method(user, friend):
	user.friends.add(friend)
	