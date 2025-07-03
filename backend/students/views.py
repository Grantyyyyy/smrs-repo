from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet



from .models import Course, Department
from .serializers import CourseSerializer, DepartmentSerializer



class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer