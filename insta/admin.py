from django.contrib import admin
from insta.models import Profile,User_Post,AddFriend,User_Post_commt
# Register your models here.
admin.site.register(Profile)
admin.site.register(User_Post)
admin.site.register(AddFriend)
admin.site.register(User_Post_commt)