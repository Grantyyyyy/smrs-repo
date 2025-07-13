from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import status



from .models import Course, Department, Subject, SubjectOffering, Schedule
from .serializers import CourseSerializer, DepartmentSerializer, SubjectSerializer, SubjectOfferingSerializer, DepartmentDetailSerializer, ScheduleSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=False, methods=['get'])
    def connected_subjects(self, request):
        department_id = request.query_params.get('department')
        if not department_id:
            return Response({'error': 'Department ID is required'}, status=400)
        
        # subjects = Subject.objects.filter(department_id=department_id)
        # serializer = SubjectSerializer(subjects, many=True)
        # return Response(serializer.data)

        all_subjects = Subject.objects.filter(department_id=department_id)
        offered_ids = SubjectOffering.objects.filter(
            department_id=department_id
        ).values_list('subject_id', flat=True)

        data = []
        for subject in all_subjects:
            serialized = SubjectSerializer(subject).data
            serialized['is_offered'] = subject.id in offered_ids
            data.append(serialized)

        return Response(data)

class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectOfferingViewSet(ModelViewSet):
    queryset = SubjectOffering.objects.select_related('department', 'subject').all()
    serializer_class = SubjectOfferingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        department_id = self.request.query_params.get('department')

        if department_id:
            queryset = queryset.filter(department_id=department_id)

        return queryset
    
    @action(detail=False, methods=['get'])
    def get_schedules(self, request):
        subject_offering_id = request.query_params.get('subject_offer')
        schedules = Schedule.objects.all()

        if subject_offering_id:
            schedules = schedules.filter(subject_offering_id=subject_offering_id)

        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=['post'])
    def add_schedule(self, request, pk=None):
        subject_offering = self.get_object()
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(subject_offering=subject_offering)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer



class DepartmentDetailViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentDetailSerializer  




class EnrollmentViewSet(ModelViewSet):
    def enroll_student(self, request, student_id, course_id):
        """
        Enroll a student in a course.
        """
        try:
            student = StudentProfile.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            student.courses.add(course)
            return Response({'status': 'enrolled'}, status=status.HTTP_200_OK)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)