from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Sensor
from .serializers import SensorCreateSerializer, SensorListSerializer, SensorUpdateSerializer

# Create your views here.
class SensorCreateView(generics.CreateAPIView):

    serializer_class = SensorCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class SensorListView(generics.ListAPIView):
    
    serializer_class = SensorListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Sensor.objects.filter(gateway__region__user=self.request.user)


class SensorUpdateView(generics.UpdateAPIView):
    
    serializer_class = SensorUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field='id'

    def get_queryset(self):
        return Sensor.objects.filter(gateway__region__user=self.request.user)
    
    def perform_update(self, serializer):
        return super().perform_update(serializer)


class SensorDeleteView(generics.DestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    lookup_field='id'

    def get_queryset(self):
        return Sensor.objects.filter(gateway__region__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.gateway.region.user != self.request.user:
            raise PermissionDenied({'user': {'code': 'Perm-ERROR', 'message': '权限不足'}})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
