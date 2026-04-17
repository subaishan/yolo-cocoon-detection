from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import RegionCreateSerializer, RegionListSerializer, RegionUpdateSerializer
from .models import Region


class RegionCreateView(generics.CreateAPIView):
    
    serializer_class = RegionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

class RegionListView(generics.ListAPIView):
    
    serializer_class = RegionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Region.objects.filter(user=self.request.user)
    
class RegionUpdateView(generics.UpdateAPIView):
    
    serializer_class = RegionUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field='id'

    def get_queryset(self):
        return Region.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        return super().perform_update(serializer)
    

class RegionDeleteView(generics.DestroyAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    lookup_field='id'
    
    def get_queryset(self):
        return Region.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied({'user': {'code': 'Perm-ERROR', 'message': '权限不足'}})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)