# valentine_contest/admin.py
from django.contrib import admin
from .models import Contestant

@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'is_verified', 'is_winner', 'date_joined']
    list_filter = ['is_verified', 'is_winner']
    search_fields = ['full_name', 'email']
