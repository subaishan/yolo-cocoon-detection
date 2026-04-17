from django.urls import path
from .views import GatewayCreateView, GatewayListView, GatewayUpdateView, GatewayDeleteView

urlpatterns = [
    path('create/', GatewayCreateView.as_view()),
    path('list/', GatewayListView.as_view()),
    path('delete/<int:id>/', GatewayDeleteView.as_view()),
    path('update/<int:id>/', GatewayUpdateView.as_view()),
]
