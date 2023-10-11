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
            
            accounts = Account.objects.filter(is_staff=False)
            
            
            
            serializer = AccountSerializer(accounts, many=True)
            
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MessageListView(APIView):
    def get(self, request, sender_id, recipient_id):
        room_id = f"{sender_id}{recipient_id}"
        

        queryset = Message.objects.filter(room_id=room_id).order_by('timestamp')
        

        serializer = MessageSerializer(queryset, many=True)
       

        return Response(serializer.data)


class MessageCreateView(APIView):
    def post(self, request, sender_id, recipient_id):
        room_id = f"{sender_id}{recipient_id}"
         
        try:
            sender = Account.objects.get(id=sender_id)
              
        except Account.DoesNotExist:
            
            return Response({"error": f"Sender with ID {sender_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        existing_conversation = Message.objects.filter(room_id=room_id).first()
        
        if existing_conversation:
           
            existing_conversation.content = request.data.get("content", "")
            existing_conversation.save()
            serializer = MessageSerializer(existing_conversation)
             
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
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
              
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
              
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
