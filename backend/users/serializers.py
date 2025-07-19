from rest_framework import serializers
from .models import User, StudentProfile




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)



class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.ReadOnlyField()
    student_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'gender', 'contact_number', 'is_student', 'is_instructor', 'is_dsa',
            'user_type', 'student_profile'
        ]
    
    def get_student_profile(self, obj):
        if obj.is_student and hasattr(obj, 'student_profile'):
            return {
                "elementary_school": obj.student_profile.elementary_school,
                "high_school": obj.student_profile.high_school,
                "senior_high": obj.student_profile.senior_high,
            }
        return None
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
    def update(self, instance, validated_data):
        # Update password correctly if it's provided
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
    
class StudentSerializer(serializers.ModelSerializer):
    account_status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [ 'id', 'username', 'first_name', 'last_name', 'email', 'gender',
                   'is_student', 'is_instructor', 'is_dsa', 'account_status', ]
        
    def get_account_status(self, obj):
        if obj.is_student and hasattr(obj, 'student_profile'):
            return obj.student_profile.account_status
        return None


class StudentRegistrationSerializer(serializers.ModelSerializer):
    elementary_school = serializers.CharField(max_length=100, required=False)
    high_school = serializers.CharField(max_length=100, required=False)
    senior_high = serializers.CharField(max_length=100, required=False)

    student_type = serializers.ChoiceField(choices=StudentProfile.STUDENT_TYPE_CHOICES, required=True)
    date_of_birth = serializers.DateField(required=True)
    address = serializers.CharField(required=True)
    guardian_name = serializers.CharField(required=True)
    guardian_contact = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'gender',
                    'contact_number', 'elementary_school', 'high_school', 'senior_high',
                    'student_type', 'date_of_birth', 'address', 'guardian_name', 'guardian_contact']
        extra_kwargs = { 'password': {'write_only': True} }
    
    def create(self, validated_data):
        enrollment_fields = {
            'elementary_school': validated_data.pop('elementary_school', None),
            'high_school': validated_data.pop('high_school', None),
            'senior_high': validated_data.pop('senior_high', None),
            'student_type': validated_data.pop('student_type'),
            'date_of_birth': validated_data.pop('date_of_birth'),
            'address': validated_data.pop('address'),
            'guardian_name': validated_data.pop('guardian_name'),
            'guardian_contact': validated_data.pop('guardian_contact'),
        }


        user = User.objects.create_user(**validated_data, is_student=True)

        profile = user.student_profile
        for field, value in enrollment_fields.items():
            setattr(profile, field, value)
        profile.save()

        return user