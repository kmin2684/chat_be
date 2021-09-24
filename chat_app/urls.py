from django.urls import path
from . import views
from chat_app.views import CustomAuthToken, add_friend

app_name = "chat_app"

urlpatterns = [
    path("", views.index, name="index"),
    # path("login", views.login_view, name="login"),
    # path("logout", views.logout_view, name="logout"),
    # path("register", views.register, name="register"),
    path('add_friend', views.add_friend),
    path('room_create', views.room_create),
    path('json_check', views.json_check),
    path('datetime', views.datetime_test),
    path('general_update', views.general_update),
    path('chat_update/<int:room_id>', views.room_update),

    path('api-token-auth/', CustomAuthToken.as_view()),
    path('logout', views.logout),

    path('user_check', views.user_check),
    # path('logout', Logout.as_view()),
    path('registration', views.registration),
    # url(r'^logout/', Logout.as_view()),

    # path("update_room", views.update_room, name = "update_room"),
    # path("update_all", views.update_all, name = "update_all"),
    # path("send_message", views.send_message, name = "send_message"),
    # path("add_friend", views.add_friend, name = "add_friend"),
    # path("create_group", views.create_group, name = "create_group"),
]
