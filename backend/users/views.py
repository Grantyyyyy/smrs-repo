from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User
from .serializers import LoginSerializer, UserSerializer, StudentSerializer





class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_student and user.account_status == 'pending':
                return Response({'error': 'Your account is pending approval'}, status=status.HTTP_403_FORBIDDEN)
            else:
                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                })

        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class LogoutView(APIView):
    def post(self, request):
        try:

            request.auth.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register_student(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_student=True)
            return Response({'status': 'student registered', 'user_id': user.id}, status=201)
        return Response(serializer.errors, status=400)
    
    
    @action(detail=True, methods=['post'])
    def approve_student(self, request, pk=None):
        try:
            student = self.get_object()
            student.account_status = 'approved'
            student.save()
            return Response({'status': 'student approved'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        
class MeView(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class StudentViewSet(ModelViewSet):
    queryset = User.objects.filter(is_student=True)
    serializer_class = StudentSerializer


    
    

