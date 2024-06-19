# accounts/admin.py
from django import forms
from django.contrib import admin
from .models import Movie, Show, Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'duration', 'release_date')
    search_fields = ('title', 'description')
    list_filter = ('release_date',)

class ShowAdminForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'
        widgets = {
            'time': forms.TimeInput(format='%H:%M:%S'),
        }

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    form = ShowAdminForm
    list_display = ('title', 'movie', 'time', 'date', 'capacity', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('title', 'movie__title')
    list_filter = ('date', 'is_active')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show', 'number_of_tickets', 'total_amount', 'payment_status')
    list_filter = ('show__title', 'user', 'payment_status')
    search_fields = ('show__title', 'user__username')
