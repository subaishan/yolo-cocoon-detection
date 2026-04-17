# imageDetection模块的URL

from django.urls import path
from .views import DetectionView, DetectionListView, DetectionDeleteView, DetectionRetrieveView

urlpatterns = [
    path('create/', DetectionView.as_view()),
    path('list/', DetectionListView.as_view()),
    path('delete/<int:id>/', DetectionDeleteView.as_view()),
    path('retrieve/<int:id>/', DetectionRetrieveView.as_view())
]
