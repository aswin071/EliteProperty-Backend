# Import necessary modules
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
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

            print(f"Property ID: {property_id}")
            print(f"Deposit Amount: {deposit_amount}")
            print(f"Amount in Paise: {amount_in_paise}")
            print(f"Commission Amount: {commission_amount}")

            RAZORPAY_KEY_ID = settings.RAZORPAY_KEY_ID
            RAZORPAY_KEY_SECRET = settings.RAZORPAY_KEY_SECRET
            
            print(f"Razorpay Key ID: {RAZORPAY_KEY_ID}")
            print(f"Razorpay Key Secret: {RAZORPAY_KEY_SECRET}")

            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

            # Convert 15% to admin_fee
            admin_fee = (0.15 * amount_in_paise) / 100
            deducted_amount = commission_amount - admin_fee 

            print(f"Admin Fee: {admin_fee}")
            print(f"Deducted Amount: {deducted_amount}")

            order_response = client.order.create({
                'amount': amount_in_paise,
                'currency': 'INR',
                'payment_capture': 1,
            })
            order_id = order_response["id"]

            print(f"Order ID: {order_id}")

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
            print(f"Error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class SuccessPaymentView(APIView):

    def post(self, request, format=None):
        print("Request Data:", request.data)
        from rest_framework import status
        from rest_framework.response import Response
        from rest_framework.permissions import IsAuthenticated
        from .models import PropertyBooking  
        from .models import Interest  
        import razorpay

        permission_classes = [IsAuthenticated]

        data = request.data.get("data", {})
        print("Extracted Data:", data) 
        
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

        print("Order ID:", ord_id)
        print("Razorpay Payment ID:", raz_pay_id)
        print("Razorpay Signature:", raz_signature)

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
                print("Step 1: Invalid date range.")
                return Response({'message': 'Invalid date range.'}, status=status.HTTP_400_BAD_REQUEST)

            
            property = get_object_or_404(Property, id=property_id)
            print(f"Step 2: Property retrieved: {property}")

           
            existing_bookings = RentBooking.objects.filter(
                property=property,
                check_in_date__lte=check_out_date,
                check_out_date__gte=check_in_date,
            )
            print(f"Step 3: Existing bookings: {existing_bookings}")

            if existing_bookings.exists():
                
                error_message = f"Property is not available from {check_in_date} to {check_out_date}. Please select other dates."
                print(f"Step 4: {error_message}")
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
                print(f"Step 5: New booking created: {new_booking}")

                
                serializer = RentBookingSerializer(new_booking)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
           
            print(f"Step 7: Error: {e}")
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

            print(f"Property ID: {property_id}")
            print(f"Rent Amount: {rent_amount}")
            print(f"Check-in Date: {check_in_date}")
            print(f"Check-out Date: {check_out_date}")

            amount_in_paise = int(float(rent_amount) * 100)
            commission_amount=int(float(rent_amount))

            RAZORPAY_KEY_ID = settings.RAZORPAY_KEY_ID
            RAZORPAY_KEY_SECRET = settings.RAZORPAY_KEY_SECRET

            print(f"Razorpay Key ID: {RAZORPAY_KEY_ID}")
            print(f"Razorpay Key Secret: {RAZORPAY_KEY_SECRET}")

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
            print(f"Error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SuccessRentPaymentView(APIView):
    

    def post(self, request, format=None):
        print("Request Data:", request.data)  

        permission_classes = [IsAuthenticated]

        data = request.data.get("data", {})
        print("Extracted Data:", data)  
        
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

        print("Order ID:", ord_id)
        print("Razorpay Payment ID:", raz_pay_id)
        print("Razorpay Signature:", raz_signature)

        PUBLIC_KEY = "rzp_test_mQPTW9W3qUgwIE"
        SECRET_KEY = "jUdfHmvTQdduTjUBOraTxlhz"

        client = razorpay.Client(auth=(PUBLIC_KEY, SECRET_KEY))

        check = client.utility.verify_payment_signature(data)
        print("Payment Verification Check Result:", check)

        if check:
            try:
                order = RentPropertyBooking.objects.get(booking_order_id=ord_id)
                print("Found Order:", order)

                rent = RentBooking.objects.get(property=order.property, user=request.user)
                print("Found Rent:", rent)

                rent.payment_status = True
                rent.save()
                
                order.booking_payment_id = payment_id
                order.is_paid = True
                order.save()

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
    user_message = f'Dear valued customer,\n\nThank you for booking a property with us. Your booking for {booking.property.title} has been confirmed.\n\nYou can view and manage your booking by visiting the following link: <a href="{user_redirect}">Booking Management Portal</a>.\n\nIf you have any questions or need assistance, please contact our customer support.\n\nBest regards,\nYour Real Estate Team'

    admin_redirect = "https://your-real-estate-admin.com/dashboard"
    admin_subject = "New Booking Received"
    admin_message = f'Hello,\n\nA new booking for property {booking.property.title} has been received.\n\nYou can review and manage this booking by visiting the following link: <a href="{admin_redirect}">Admin Dashboard</a>.\n\nIf you have any questions, please get in touch.\n\nBest regards,\nYour Real Estate Team'

    # Send messages to user and admin
    send_mail(
        user_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        html_message=user_message,
    )
    send_mail(
        admin_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],  # Replace with your admin email
        html_message=admin_message,
    )
