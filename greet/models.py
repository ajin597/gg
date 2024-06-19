from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    duration = models.IntegerField()  # Duration of the movie in minutes
    release_date = models.DateField()
    is_active = models.BooleanField(default=True)
    language=models.CharField(max_length=100)

from django.db import models

class Show(models.Model):
    image = models.ImageField(upload_to='movie_images/')
    title = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    language=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"




class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=255)  # Store Razorpay order ID
    payment_status = models.CharField(max_length=20, default='SUCCESS')
    verified = models.BooleanField(default=False)  # Store QR code image

    @property
    def show_title(self):
        return self.show.title

    def __str__(self):
        return f'Booking #{self.id}'
    
