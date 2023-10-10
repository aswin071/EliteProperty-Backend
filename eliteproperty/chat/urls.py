# urls.py
from django.urls import path, include
from . import consumers
from . import views

websocket_urlpatterns = [
    path("ws/chat/<int:send>/<int:receive>/", consumers.ChatConsumer.as_asgi(), name='chat_ws'),
]

urlpatterns = [
    # Include WebSocket routing for chat consumers
    path("", include(websocket_urlpatterns)),

    # Include URLs for chat-related API views
    path('api/accounts-list/', views.AccountsListView.as_view(), name='chat-accounts'),
    path("api/rooms/<int:sender_id>/<int:recipient_id>/messages/list/", views.MessageListView.as_view(), name='message-list'),
    path("api/rooms/<int:sender_id>/<int:recipient_id>/messages/send/", views.MessageCreateView.as_view(), name='message-send'),
]