from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserRegisterSerializer, BookingSerializer 
from .models import Show, Booking
from .permissions import IsAdminOrReadOnly
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserRegisterSerializer

from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate token for the user
            token, _ = Token.objects.get_or_create(user=user)

            # Include token in response
            response_data = {
                'user': serializer.data,
                'token': token.key
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user=authenticate(username=username,password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'username':user.username,'isAdmin':user.is_staff}, status=status.HTTP_200_OK) 
    else:
        return Response({
            'error': 'Invalid Credentials or not admin',
        },status=status.HTTP_400_BAD_REQUEST)                                              


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Show
from .serializers import ShowSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shows_by_date(request, date):
    try:
        shows = Show.objects.filter(date=date, is_active=True)
        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)





from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Show

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminOrReadOnly])
def delete_show(request, pk):
    try:
        show = Show.objects.get(pk=pk)
    except Show.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    show.delete()
    return Response("Show deleted successfully", status=status.HTTP_204_NO_CONTENT)


# @api_view(['PUT'])
# @permission_classes([IsAdminOrReadOnly])
# def update_show(request, pk):
#     show = get_object_or_404(Show, pk=pk)
#     serializer = ShowSerializer(show, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminOrReadOnly])
def create_show(request):
    serializer = ShowSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





""" @api_view(['PUT'])
@permission_classes([IsAdminOrReadOnly])
def disable_movie_show(request, pk):
    try:
        show = Show.objects.get(pk=pk)
    except Show.DoesNotExist:
        return Response({'message': 'Movie show not found'}, status=status.HTTP_404_NOT_FOUND)

    show.is_active = False
    show.save()
    serializer = ShowSerializer(show)
    return Response(serializer.data, status=status.HTTP_200_OK) """






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    # Retrieve all bookings associated with the current user
    user = request.user
    bookings = Booking.objects.filter(user=user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)



from io import BytesIO
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_ticket(request, booking_id):  
    try:
        # Retrieve the booking associated with the given ID
        booking = Booking.objects.select_related('user', 'show').get(id=booking_id)  

        # Generate QR code containing the show and user details
        show_details = f"\nTitle: {booking.show.title}\nDate: {booking.show.date}\nTime: {booking.show.time}\nPrice: {booking.show.ticket_price}\n"
        user_details = f"User: {booking.user.username}\nEmail: {booking.user.email}\n"
        qr_data = show_details + user_details
        
        qr_img = qrcode.make(qr_data)

        # Resize the QR code image
        qr_img = qr_img.resize((200, 200))  

        # Create PDF ticket
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, "Movie Ticket")
        p.drawString(100, 730, f"Booking ID: {booking.id}")
        p.drawString(100, 710, f"User: {booking.user.username}")
        p.drawInlineImage(qr_img, 100, 500)  
        p.drawString(100, 400, "Show Details:")
        p.drawString(100, 380, show_details)
        p.drawString(100, 360, "User Details:")
        p.drawString(100, 340, user_details)
        p.save()

        # Prepare HTTP response with PDF content
        buffer.seek(0)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_booking_{booking.id}.pdf"'
        response.write(buffer.getvalue())
        return response
    except Booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)





from django.contrib.auth import logout

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import logout

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)





from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Show
from .serializers import ShowSerializer1

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_list(request, id):
    if request.method == 'GET':
        shows = Show.objects.filter(id=id)
        serializer = ShowSerializer1(shows, many=True)
        return Response(serializer.data)



# Import necessary modules and packages
from django.http import JsonResponse
import razorpay
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from payments.models import RazorpayPayment
from django.conf import settings
from .models import Show, Booking
from .serializers import ShowSerializer, BookingSerializer


# Initialize Razorpay client with API Keys
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_tickets(request, show_id):
    try:
        # Retrieve show based on show_id
        show = Show.objects.get(pk=show_id)
        
        # Retrieve user from request
        user = request.user
        
        # Retrieve number of tickets from request data
        number_of_tickets = request.data.get('number_of_tickets')
        
        if number_of_tickets is not None:
            # try:
            # #     number_of_tickets = int(number_of_tickets)
            # # except ValueError:
            # #     return JsonResponse({'error': 'Invalid number of tickets'}, status=status.HTTP_400_BAD_REQUEST)

            if number_of_tickets <= 0:
                return JsonResponse({'error': 'Number of tickets must be a positive integer'}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate total amount
            total_amount = calculate_total_amount(show, number_of_tickets)

            # Create Razorpay order
            razorpay_order = razorpay_client.order.create({
                'amount': int(total_amount * 100),  # Amount should be in smallest currency unit (e.g., paisa for INR)
                'currency': 'INR',
                'payment_capture': '0'
            })

            # # Save the order in DB
            # # order = RazorpayPayment.objects.create(
            # #     name=user.username,
            # #     amount=total_amount,
            # #     provider_order_id=razorpay_order['id']
            # )

            # Create booking
            booking = Booking.objects.create(
                user=user,
                show=show,
                number_of_tickets=number_of_tickets,
                total_amount=total_amount,
                ticket_price=total_amount / number_of_tickets,  # Calculate ticket price based on total amount
                razorpay_order_id=razorpay_order['id']  # Save Razorpay order ID to the booking
            )

            # Return data to frontend for Razorpay payment initialization
            data = {
                'booking_id': booking.id,
                'razorpay_order_id': razorpay_order['id'],
                'amount': total_amount,
            }

            return JsonResponse(data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': 'Number of tickets field is required'}, status=status.HTTP_400_BAD_REQUEST)
    except Show.DoesNotExist:
        return JsonResponse({'error': 'Show not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while processing the request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Helper function to calculate total amount
def calculate_total_amount(show, number_of_tickets):
    # Example logic: Total amount based on ticket price and number of tickets
    return show.ticket_price * number_of_tickets




from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Show
from .serializers import ShowSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list(request):
    if request.method == 'GET':
        shows = Show.objects.filter(is_active=True)  
        serializer = ShowSerializer(shows, many=True)  
        return Response(serializer.data)

    



from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Booking
from django.core.mail import send_mail

from django.core.mail import send_mail
from django.urls import reverse

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_confirmation_email(request, booking_id):  
    try:
        # Retrieve booking object
        booking = Booking.objects.get(pk=booking_id)

        # Get user email from the authenticated user
        user_email = request.user.email

        # Compose verification link
        verification_link = request.build_absolute_uri(reverse('verify_booking', args=[booking_id]))

        # Compose email message
        subject = 'Booking Confirmation'
        message = f"""
Dear {booking.user},  

Your booking has been confirmed! 🎟️  

📽️ *Show:* {booking.show}  
📅 *Date:* {booking.show.date}  
⏰ *Time:* {booking.show.time}  
🎫 *Tickets:* {booking.number_of_tickets}  
💰 *Total Amount:* ₹{booking.total_amount}  
💳 *Payment Status:* {booking.payment_status}  
🆔 *Razorpay Order ID:* {booking.razorpay_order_id}  

🔗 Click below to view your ticket and details:  
{verification_link}  

Enjoy the show! 🍿✨  
Thank you for booking with us.  
"""

        from_email = 'no-reply@theatre.com' 
        to_email = [user_email]

        # Send email
        send_mail(subject, message, from_email, to_email)

        return Response({'message': 'Confirmation email sent successfully'}, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'An error occurred while sending confirmation email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from django.shortcuts import render

def booking_verified(request):
    return render(request, 'booking_verified.html')

from django.shortcuts import redirect, get_object_or_404
from .models import Booking

def verify_booking(request, booking_id):
    # Retrieve booking object
    booking = get_object_or_404(Booking, pk=booking_id)

    # Perform the verification process (e.g., update booking status)
    booking.verified = True
    booking.save()

    # Redirect the user to a confirmation page
    return redirect('booking_verified')  # 'booking_verified' is the name of the URL pattern for the confirmation page






from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Show
from .serializers import ShowSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shows_at_time(request, time):
    shows = Show.objects.filter(time=time)
    serializer = ShowSerializer(shows, many=True)
    return Response(serializer.data)



# from django.http import JsonResponse
# from .models import Show

# def get_image_urls(request):
#     shows = Show.objects.all()
#     image_urls = [show.image.url for show in shows]
#     return JsonResponse({'image_urls': image_urls})


# from django.shortcuts import render
# from .models import Show

# def search_shows(request):
#     query = request.GET.get('query')
#     if query:
#         shows = Show.objects.filter(title__icontains=query)
#     else:
#         shows = Show.objects.none()

#     return render(request, 'search.html', {'shows': shows})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminOrReadOnly])
def list1(request):
    if request.method == 'GET':
        shows = Show.objects.filter(is_active=True)  
        serializer = ShowSerializer(shows, many=True)  
        return Response(serializer.data)


# your_project_name/management/commands/runmigrations.py
from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run migrations'

    def handle(self, *args, **kwargs):
        call_command('migrate')





from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import razorpay
from django.core.mail import send_mail
from django.conf import settings
from .models import Refund

# Razorpay API setup
RAZORPAY_KEY_ID = "your_razorpay_key_id"
RAZORPAY_SECRET = "your_razorpay_secret"
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))

@csrf_exempt  # 🚀 This disables CSRF protection for this API
def process_refund(request):
    if request.method == "POST":
        payment_id = request.POST.get("payment_id")
        email = request.POST.get("email")

        try:
            refund = client.payment.refund(payment_id)
            Refund.objects.create(
                payment_id=payment_id,
                refund_id=refund["id"],
                email=email,
                amount=100,  # Modify based on your use case
                status="processed"
            )

            send_mail(
                subject="Refund Processed",
                message=f"Your refund for payment {payment_id} has been processed successfully.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({"message": "Refund processed successfully!", "refund_id": refund["id"]}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


# Configure Razorpay API
RAZORPAY_KEY_ID = "rzp_test_H8tj7QU829vkdv"
RAZORPAY_SECRET = "2sFLB15B4yMPMmScPFTh9IIw"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))

def process_refund(request):
    if request.method == "POST":
        payment_id = request.POST.get("payment_id")
        email = request.POST.get("email")
        amount = 1000  # Set the refund amount (in paisa for Razorpay, e.g., 100 = ₹1)

        try:
            # Create refund request in Razorpay
            refund = client.payment.refund(payment_id, {"amount": amount})

            # Save refund details in the database
            refund_obj = Refund.objects.create(
                payment_id=payment_id,
                refund_id=refund["id"],
                email=email,
                amount=amount / 100,  # Convert to rupees
                status="processed"
            )

            # Send refund confirmation email
            send_mail(
                subject="Refund Processed Successfully",
                message=f"Your refund for payment {payment_id} has been processed successfully.\n\nRefund ID: {refund['id']}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({"message": "Refund processed and email sent!", "refund_id": refund["id"]}, status=200)

        except razorpay.errors.BadRequestError:
            return JsonResponse({"error": "Invalid payment ID or refund failed."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

