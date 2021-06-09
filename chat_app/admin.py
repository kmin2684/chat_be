from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Message)
admin.site.register(MessageCopy)
admin.site.register(Room)