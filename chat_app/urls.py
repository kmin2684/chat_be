from django.urls import path
from . import views

app_name = "chat_app"

urlpatterns = [
	path("", views.index, name="index"),
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register"),
	
	# path("update_room", views.update_room, name = "update_room"),
	# path("update_all", views.update_all, name = "update_all"),
	# path("send_message", views.send_message, name = "send_message"),
	# path("add_friend", views.add_friend, name = "add_friend"),
	# path("create_group", views.create_group, name = "create_group"),
]