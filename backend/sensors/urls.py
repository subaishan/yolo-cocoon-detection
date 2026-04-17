from django.urls import path
from .views import SensorCreateView, SensorListView, SensorUpdateView, SensorDeleteView

urlpatterns = [
    path('create/', SensorCreateView.as_view()),
    path('list/', SensorListView.as_view()),
    path('delete/<int:id>/', SensorDeleteView.as_view()),
    path('update/<int:id>/', SensorUpdateView.as_view()),
]
 