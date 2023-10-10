import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from accounts.models import Account
from .models import Message
from .serializers import MessageSerializer, AccountSerializer

logger = logging.getLogger(__name__)

class AccountsListView(APIView):
    def get(self, request):
        try:
            print("Fetching accounts...")
            accounts = Account.objects.filter(is_staff=False)
            print(f"Fetched {len(accounts)} accounts")
            
            print("Serializing accounts...")
            serializer = AccountSerializer(accounts, many=True)
            
            print("Returning data...")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MessageListView(APIView):
    def get(self, request, sender_id, recipient_id):
        room_id = f"{sender_id}{recipient_id}"
        print("room_id:", room_id)

        queryset = Message.objects.filter(room_id=room_id).order_by('timestamp')
        print("queryset:", queryset)

        serializer = MessageSerializer(queryset, many=True)
        print("serializer.data:", serializer.data)

        return Response(serializer.data)



# class MessageCreateView(APIView):
#     def post(self, request, sender_id, recipient_id):
#         room_id = f"{sender_id}{recipient_id}"
        
#         print(f"room_id: {room_id}") 
        
#         try:
#             sender = Account.objects.get(id=sender_id)
#             print(f"Sender found: {sender}")  
#         except Account.DoesNotExist:
#             print(f"Sender with ID {sender_id} does not exist.") 
#             return Response({"error": f"Sender with ID {sender_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
#         data = {
#             "sender": sender,
#             "recipient_id": recipient_id,
#             "content": request.data.get("content", "")
#         }
        
#         message = Message(**data)
#         message.room_id = room_id
        
#         try:
#             message.save()
#             serializer = MessageSerializer(message)
#             print(f"Message saved: {serializer.data}")  
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             print(f"Error saving message: {str(e)}")  
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MessageCreateView(APIView):
    def post(self, request, sender_id, recipient_id):
        room_id = f"{sender_id}{recipient_id}"
        
        print(f"room_id: {room_id}") 
        
        try:
            sender = Account.objects.get(id=sender_id)
            print(f"Sender found: {sender}")  
        except Account.DoesNotExist:
            print(f"Sender with ID {sender_id} does not exist.") 
            return Response({"error": f"Sender with ID {sender_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if a conversation with the same room_id already exists
        existing_conversation = Message.objects.filter(room_id=room_id).first()
        
        if existing_conversation:
            # If a conversation exists, update it with the new message
            existing_conversation.content = request.data.get("content", "")
            existing_conversation.save()
            serializer = MessageSerializer(existing_conversation)
            print(f"Message updated: {serializer.data}")  
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If no existing conversation, create a new one
        data = {
            "sender": sender,
            "recipient_id": recipient_id,
            "content": request.data.get("content", "")
        }
        
        message = Message(**data)
        message.room_id = room_id
        
        try:
            message.save()
            serializer = MessageSerializer(message)
            print(f"Message saved: {serializer.data}")  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error saving message: {str(e)}")  
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
