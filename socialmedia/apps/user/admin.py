from django.contrib import admin
from apps.user.models.post import Post
from apps.user.models.user import User

admin.site.register(Post)
admin.site.register(User)
