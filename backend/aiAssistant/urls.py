# aiAssistant模块的URL

from django.contrib import admin
from django.urls import path
from .views import ChatView, ChatCreateView, ChatListView, ChatDeleteView, MessageListView, ChatUpdateView

urlpatterns = [
    path('chat/', ChatView.as_view()),
    path('chat/create/', ChatCreateView.as_view()),
    path('chat/list/', ChatListView.as_view()),
    path('chat/update/<int:id>/', ChatUpdateView.as_view()),
    path('chat/delete/<int:id>/', ChatDeleteView.as_view()),
    path('chat/list/messages/<int:conversation_id>/', MessageListView.as_view())
]
