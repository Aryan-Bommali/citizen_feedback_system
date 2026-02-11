from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'issue_type', 'severity', 'city', 'status', 'created_at')
    list_filter = ('issue_type', 'severity', 'status', 'city')
    search_fields = ('location', 'city', 'pincode', 'description', 'user__username')
