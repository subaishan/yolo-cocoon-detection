from django.urls import path
from .views import EnvironmentDataCreateView, EnvironmentDataListView, EnvironmentDataDeleteView

urlpatterns = [
    path('create/', EnvironmentDataCreateView.as_view()),
    path('list/', EnvironmentDataListView.as_view()),
    path('delete/<int:id>/', EnvironmentDataDeleteView.as_view()),
]
 