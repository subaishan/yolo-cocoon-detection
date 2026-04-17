from django.urls import path
from .views import RegionCreateView, RegionListView, RegionUpdateView, RegionDeleteView

urlpatterns = [
    path('create/', RegionCreateView.as_view()),
    path('list/', RegionListView.as_view()),
    path('delete/<int:id>/', RegionDeleteView.as_view()),
    path('update/<int:id>/', RegionUpdateView.as_view()),
]
