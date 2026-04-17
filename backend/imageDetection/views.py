from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import PestDetectionRecord
from .CDetYoloService import CDetYoloClient
from .serializers import PestDetectionCreateSerializer, PestDetectionListSerializer, PestDetectionRetrieveSerializer


cDetYoloClient = CDetYoloClient()

class DetectionView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PestDetectionCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        response = cDetYoloClient.get_detect_response(request)
        return Response(response, status=status.HTTP_200_OK)
    

class DetectionListView(generics.ListAPIView):
    
    serializer_class = PestDetectionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PestDetectionRecord.objects.filter(user=self.request.user)
    

class DetectionDeleteView(generics.DestroyAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return PestDetectionRecord.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied({'user': {'code': 'Perm-ERROR', 'message': '权限不足'}})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DetectionRetrieveView(generics.RetrieveAPIView):
    
    serializer_class = PestDetectionRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return PestDetectionRecord.objects.filter(user=self.request.user)