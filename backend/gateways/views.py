from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import GatewayCreateSerializer, GatewayListSerializer, GatewayUpdateSerializer
from .models import Gateway

# Create your views here.
class GatewayCreateView(generics.CreateAPIView):
    
    serializer_class = GatewayCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

class GatewayListView(generics.ListAPIView):
    
    serializer_class = GatewayListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Gateway.objects.filter(region__user=self.request.user)
    

class GatewayUpdateView(generics.UpdateAPIView):

    serializer_class = GatewayUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field='id'

    def get_queryset(self):
        return Gateway.objects.filter(region__user=self.request.user)
    
    def perform_update(self, serializer):
        return super().perform_update(serializer)
    

class GatewayDeleteView(generics.DestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    lookup_field='id'

    def get_queryset(self):
        return Gateway.objects.filter(region__user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.region.user != self.request.user:
            raise PermissionDenied({'user': {'code': 'Perm-ERROR', 'message': '权限不足'}})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)