from django.shortcuts import render

from .models import User
from .serializers import CreateUserSerializers,TokenTestSerializers,UpdateUserSerializers
from rest_framework.views import APIView, Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
# Create your views here.

class UserCreateView(CreateAPIView):
    serializer_class = CreateUserSerializers
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def perform_create(self, serializer):
        serializer.save(role='user', is_active=True)

class TokenView(TokenObtainPairView):
    serializer_class = TokenTestSerializers

class ControllUser(APIView):
    serializer_class = CreateUserSerializers
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.role == "admin":
            queryset = User.objects.all()
            return Response(data=queryset,status=200)
        return Response({"detail": "У вас нет прав на получени пользователей"},status=status.HTTP_401_UNAUTHORIZED)
    
class ControllUserPutDelete(APIView):
    serializer_class = CreateUserSerializers
    permission_classes = [IsAuthenticated]
    def post(self,request,pk):
        user = get_object_or_404(User,pk=pk)
        if request.user.role =='admin':
            user.role = request.data.get('role')
            user.save()
            return Response({"detail": f"Роль изменена на"},status=200)
        return Response({"detail": "У вас нет прав"},status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self,request,pk):
        user = get_object_or_404(User,pk=pk)
        if request.user.role =='admin':
            user.is_active= False
            user.save()
            return Response({"detail": "Аккаунт деактивирован"}, status=status.HTTP_200_OK)
        return Response({"detail": "У вас нет прав"},status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):
    serializer_class = CreateUserSerializers
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(data=serializer.data,status=200)
    @extend_schema(
        request=UpdateUserSerializers,
        responses={200: UpdateUserSerializers},
    )
    def put(self, request):
        serializer = UpdateUserSerializers(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(data = {"message":"del ak"})

class PublicMockView(APIView):
    permission_classes = []  
    def get(self, request):
        return Response({"data": "Это публичный ресурс, доступный всем"})


class PrivateMockView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"data": "Это приватный ресурс, доступный только авторизованным"})


class AdminMockView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.role != 'admin':
            return Response(
                {"detail": "Доступ только для администраторов"},
                status=status.HTTP_403_FORBIDDEN
            )
        return Response({"data": "Это админский ресурс, доступный только администраторам"})