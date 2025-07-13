from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status




from .models import Course, Department, Subject, SubjectOffering, Schedule








class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    class Meta:
        model = Subject
        fields = '__all__'

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None
    

class SubjectOfferingSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    subject_id = serializers.IntegerField(write_only=True)
    department_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = SubjectOffering
        fields = '__all__'

    def get_subject(self, obj):
        return {
            'code': obj.subject.code,
            'name': obj.subject.name
        }

    def get_department(self, obj):
        return obj.department.name
    
    def create(self, validated_data):
        subject_id = validated_data.get('subject_id')
        department_id = validated_data.get('department_id')

        if SubjectOffering.objects.filter(subject_id=subject_id, department_id=department_id).exists():
            return Response({'error': 'Subject is already offered in this department'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(validated_data)
    
class ScheduleSerializer(serializers.ModelSerializer):
    subject_offering = serializers.SerializerMethodField()
    class Meta:
        model = Schedule
        fields = '__all__'

    def get_subject_offering(self, obj):
        return {
            'code': obj.subject_offering.subject.code,
            'name': obj.subject_offering.subject.name
        }


class DepartmentDetailSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    class Meta:
        model = Department
        fields = '__all__'


    def get_subjects(self, obj):
        return SubjectSerializer(obj.subjects.all(), many=True).data