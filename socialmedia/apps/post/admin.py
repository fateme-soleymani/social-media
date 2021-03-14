from django.contrib import admin

from apps.post.models import Comment
from apps.post.models.post import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']
    readonly_fields = ['created']


admin.site.register(Comment)

