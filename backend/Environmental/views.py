from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import EnvironmentData
from .serializers import EnvironmentDataCreateSerializer, EnvironmentDataListSerializer 

# Create your views here.
class EnvironmentDataCreateView(generics.CreateAPIView):

    serializer_class = EnvironmentDataCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

class EnvironmentDataListView(generics.ListAPIView):
    
    serializer_class = EnvironmentDataListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EnvironmentData.objects.filter(sensor__gateway__region__user=self.request.user)


class EnvironmentDataDeleteView(generics.DestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    lookup_field='id'

    def get_queryset(self):
        return EnvironmentData.objects.filter(sensor__gateway__region__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sensor.gateway.region.user != self.request.user:
            raise PermissionDenied({'user': {'code': 'Perm-ERROR', 'message': '权限不足'}})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
