from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User, StudentProfile
from .serializers import LoginSerializer, UserSerializer, StudentSerializer, StudentRegistrationSerializer





class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_student and user.student_profile.account_status == 'Pending':
                return Response({'error': 'Your account is pending'}, status=status.HTTP_403_FORBIDDEN)
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
        from .serializers import StudentRegistrationSerializer
        serializer = StudentRegistrationSerializer(data=request.data)


        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'student registered', 'user_id': user.id}, status=201)
        return Response(serializer.errors, status=400)
    
    
    @action(detail=True, methods=['patch'])
    def approve_student(self, request, pk=None):
        try:
            student = self.get_object()

            if not student.is_student:
                return Response({'error': 'This user is not a student'}, status=400)
            
            profile = student.student_profile
            profile.account_status = 'Approved'
            profile.save()

            return Response({'status': 'Student approved'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=404)
        

class MeView(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class StudentViewSet(ModelViewSet):
    queryset = User.objects.filter(is_student=True)
    serializer_class = StudentSerializer


    
    

