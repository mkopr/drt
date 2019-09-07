from django.contrib import admin

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Basic implementation of Comment model for admin panel.
    """
    pass
