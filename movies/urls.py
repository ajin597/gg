"""
URL configuration for movies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from greet import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', views.user_register, name='signup'),
     path('refund/', views.process_refund, name='process_refund'),

   path('user/',views.user_login,name="login"),
    path('shows/<str:date>/',views.shows_by_date),
    path('bookings/<int:show_id>/', views.book_tickets, name='book_ticket'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('movies2/', views.create_show, name='movie_list'),
    # path('movies/<int:pk>/', views.update_show, name='movie_detail'),
    path('movies1/<int:pk>/', views.delete_show, name='movie_detail'),
    # path('movies1/<int:pk>/', views.disable_movie_show, name='movie_detail'),
    path('download/<int:booking_id>/', views.download_ticket, name='downloa'),
              path('logout/',views.logout_view,name="login"),
               path('api/shows/<int:id>/', views.show_list, name='show-list'),
                path('',include("payments.urls")),
                
              path('razorpay/', include('api.urls')),
               path('list',views.list),
                path('listt',views.list1),
                path('send/<int:booking_id>/', views.send_confirmation_email, name='send_confirmation_email'),
                path('shows-at-time/<str:time>/',views. shows_at_time, name='shows-at-time'),
                path('verify-booking/<int:booking_id>/', views.verify_booking, name='verify_booking'),
                path('booking-verified/', views.booking_verified, name='booking_verified'),
               

     


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)