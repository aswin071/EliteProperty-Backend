
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from decouple import config
import razorpay
from .models import Order,PropertyBooking,RentBooking,Interest,RentPropertyBooking
from .serializers import OrderSerializer,PropertyBookingSerializer,RentBookingSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from accounts.models import Account
from property.models import Property
from datetime import datetime
from superadmin.models import AdminPayment
import json
from datetime import date
from .signals import my_signal
from django.core.mail import send_mail
from django.dispatch import receiver
from user.signals import property_interest_signal


class InitiatePaymentView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            current_user = request.user
            user = Account.objects.get(email=current_user)

            property_id = request.data.get('property_id')
            deposit_amount = request.data.get('deposit_amount')
            amount_in_paise = int(float(deposit_amount) * 100)
            commission_amount = int(float(deposit_amount))

            

            RAZORPAY_KEY_ID = settings.RAZORPAY_KEY_ID
            RAZORPAY_KEY_SECRET = settings.RAZORPAY_KEY_SECRET
            
           

            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

            # Convert 15% to admin_fee
            admin_fee = (0.15 * amount_in_paise) / 100
            deducted_amount = commission_amount - admin_fee 

            
            order_response = client.order.create({
                'amount': amount_in_paise,
                'currency': 'INR',
                'payment_capture': 1,
            })
            order_id = order_response["id"]

           

            order = PropertyBooking.objects.create(
                user=user,
                booking_order_id=order_id,
                booking_date=datetime.now().date(),
                property_id=property_id,
                deposit_amount=deducted_amount
            )

            # Creating a new instance in the AdminPayment model
            
            admin_payment = AdminPayment.objects.create(
                vendor=user,
                property_id=property_id,  # Note: You should specify the property here
                amount=admin_fee,
                date=date.today(),
            )

            serializer = PropertyBookingSerializer(order)
            data = {"order_response": order_response, "order": serializer.data}
            return Response(data)
        except Account.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Property.DoesNotExist:
            return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class SuccessPaymentView(APIView):

    def post(self, request, format=None):
        
        from rest_framework import status
        from rest_framework.response import Response
        from rest_framework.permissions import IsAuthenticated
        from .models import PropertyBooking  
        from .models import Interest  
        import razorpay

        permission_classes = [IsAuthenticated]

        data = request.data.get("data", {})
         
        
        ord_id = ""
        raz_pay_id = ""
        raz_signature = ""

        for key in data.keys():
            if key == "razorpay_order_id":
                ord_id = data[key]
            elif key == "razorpay_payment_id":
                raz_pay_id = data[key]
            elif key == "razorpay_signature":
                raz_signature = data[key]

        raz_pay_id = data.get("razorpay_payment_id")
        payment_id = raz_pay_id

        

        PUBLIC_KEY = "rzp_test_mQPTW9W3qUgwIE"
        SECRET_KEY = "jUdfHmvTQdduTjUBOraTxlhz"

        client = razorpay.Client(auth=(PUBLIC_KEY, SECRET_KEY))

        check = client.utility.verify_payment_signature(data)

        if check:
            # Payment is successful, update is_paid for the corresponding Interest
            try:
                order = PropertyBooking.objects.get(booking_order_id=ord_id)
                interest = Interest.objects.get(property=order.property, user=request.user)
                interest.is_paid = True
                interest.save()
                
                order.booking_payment_id = payment_id
                order.is_paid = True
                order.save()

                send_real_estate_notification(sender=PropertyBooking, booking=order)

                res_data = {"message": "Payment successfully received!", "order_id": ord_id}
                return Response(res_data)
            except (PropertyBooking.DoesNotExist, Interest.DoesNotExist) as e:
                return Response(
                    {"error": "Error processing payment or interest not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Payment verification failed
            return Response(
                {"error": "Payment verification failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

class RentBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            property_id = request.data.get('property_id')
            check_in_date = request.data.get('check_in_date')
            check_out_date = request.data.get('check_out_date')

            
            if check_in_date >= check_out_date:
                
                return Response({'message': 'Invalid date range.'}, status=status.HTTP_400_BAD_REQUEST)

            
            property = get_object_or_404(Property, id=property_id)
            

           
            existing_bookings = RentBooking.objects.filter(
                property=property,
                check_in_date__lte=check_out_date,
                check_out_date__gte=check_in_date,
            )
            

            if existing_bookings.exists():
                
                error_message = f"Property is not available from {check_in_date} to {check_out_date}. Please select other dates."
                
                return Response({'message': error_message})
            else:
                
                new_booking = RentBooking(
                    user=request.user,
                    property=property,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    payment_status=False,
                )
                new_booking.save()
                property_interest_signal.send(sender=RentBooking, booking=new_booking)

                

                
                serializer = RentBookingSerializer(new_booking)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
           
           
            return Response({'message': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class InitiateRentPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            current_user = request.user
            user = Account.objects.get(email=current_user)

            property_id = request.data.get('property_id')
            rent_amount = request.data.get('rent_amount')
            check_in_date = request.data.get('check_in_date')
            check_out_date = request.data.get('check_out_date')

            

            amount_in_paise = int(float(rent_amount) * 100)
            commission_amount=int(float(rent_amount))

            RAZORPAY_KEY_ID = settings.RAZORPAY_KEY_ID
            RAZORPAY_KEY_SECRET = settings.RAZORPAY_KEY_SECRET

            

            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            
            
            # Convert 15% to admin_fee
            admin_fee = (0.15 * amount_in_paise) / 100
            deducted_amount = commission_amount - admin_fee  # Adjust for paise

            

            order_response = client.order.create({
                'amount': amount_in_paise,
                'currency': 'INR',
                'payment_capture': 1,
            })
            order_id = order_response["id"]

            # Retrieve the property and user instances
            property = Property.objects.get(id=property_id)
            user = Account.objects.get(email=current_user)

            order = RentPropertyBooking.objects.create(
                user=user,
                booking_order_id=order_id,
                booking_date=datetime.now().date(),
                property=property,
                rent_amount=deducted_amount,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
            )

            #creating new instance to adminpayment model
            
            admin_payment = AdminPayment.objects.create(
                vendor=user,
                property=property,
                amount=admin_fee,
                date=date.today(),
            )

            serializer = PropertyBookingSerializer(order)
            data = {"order_response": order_response, "order": serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Property.DoesNotExist:
            return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SuccessRentPaymentView(APIView):
    

    def post(self, request, format=None):
         

        permission_classes = [IsAuthenticated]

        data = request.data.get("data", {})
         
        
        ord_id = ""
        raz_pay_id = ""
        raz_signature = ""

        for key in data.keys():
            if key == "razorpay_order_id":
                ord_id = data[key]
            elif key == "razorpay_payment_id":
                raz_pay_id = data[key]
            elif key == "razorpay_signature":
                raz_signature = data[key]

        raz_pay_id = data.get("razorpay_payment_id")
        payment_id = raz_pay_id

        

        PUBLIC_KEY = "rzp_test_mQPTW9W3qUgwIE"
        SECRET_KEY = "jUdfHmvTQdduTjUBOraTxlhz"

        client = razorpay.Client(auth=(PUBLIC_KEY, SECRET_KEY))

        check = client.utility.verify_payment_signature(data)
        

        if check:
            try:
                order = RentPropertyBooking.objects.get(booking_order_id=ord_id)
                

                rent = RentBooking.objects.get(property=order.property, user=request.user)
                

                rent.payment_status = True
                rent.save()
                
                order.booking_payment_id = payment_id
                order.is_paid = True
                order.save()

                send_real_estate_notification_for_rentproperty(sender=RentPropertyBooking, booking=order)


                res_data = {"message": "Payment successfully received!", "order_id": ord_id}
                return Response(res_data)
            except (RentPropertyBooking.DoesNotExist, RentBooking.DoesNotExist) as e:
                return Response(
                    {"error": "Error processing payment or interest not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
           
            return Response(
                {"error": "Payment verification failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )



@receiver(my_signal)
def send_real_estate_notification(sender, booking, **kwargs):
    # Define the URLs and email subjects/messages
    user_redirect = "http://localhost:3000/my-bookings"  
    user_subject = "Booking Confirmation"
    user_message = f'Dear valued customer,\n\nThank you for booking a property with us. Your booking for {booking.property.title} has been confirmed.\n\nYou can view and manage your booking by visiting the following link: {user_redirect}.\n\nIf you have any questions or need assistance, please contact our customer support.\n\nBest regards,\nYour Real Estate Team'

   

    # Send an email to the user
    send_mail(
        user_subject,
        user_message,
        config('EMAIL_HOST_USER'),  
        [booking.user.email],
        fail_silently=False,  )

  


@receiver(my_signal)
def send_real_estate_notification_for_rentproperty(sender, booking, **kwargs):
    
    user_redirect = "http://localhost:3000/my-bookings"  
    user_subject = "Booking Confirmation"
    user_message = f'Dear valued customer,\n\nThank you for booking a property with us. Your booking for {booking.property.title} has been confirmed for the following dates:\n\nCheck-In Date: {booking.check_in_date}\nCheck-Out Date: {booking.check_out_date}\n\nYou can view and manage your booking by visiting the following link: {user_redirect}.\n\nIf you have any questions or need assistance, please contact our customer support.\n\nBest regards,\nYour Real Estate Team'

    

   
    send_mail(
        user_subject,
        user_message,
        config('EMAIL_HOST_USER'),  
        [booking.user.email],
        fail_silently=False,  )
    


@receiver(my_signal)
def send_vendor_notification(sender, booking, **kwargs):
    # Define the URLs and email subjects/messages
    user_redirect = "http://localhost:3000/my-bookings"  
    user_subject = "Booking Confirmation"
    user_message = f'Dear valued customer,\n\nThank you for booking a property with us.\n\nYou can view and manage your booking by visiting the following link: {user_redirect}.\n\nIf you have any questions or need assistance, please contact our customer support.\n\nBest regards,\nYour Real Estate Team'

   

    # Send an email to the user
    send_mail(
        user_subject,
        user_message,
        config('EMAIL_HOST_USER'),  
        [booking.user.email],
        fail_silently=False,  )

    
@receiver(property_interest_signal)
def send_vendor_rent_notification(sender, booking, **kwargs):
    # Define the message to send to the vendor
    vendor_message = f'New booking arrived for your property "{booking.property.title}"'

    # Send a message to the vendor
    send_mail(
        "New Booking Notification",
        vendor_message,
        settings.EMAIL_HOST_USER,
        [booking.property.vendor.email],
        fail_silently=False,
    )





