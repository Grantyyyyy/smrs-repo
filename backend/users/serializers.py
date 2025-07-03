from rest_framework import serializers
from .models import User




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
            'gender', 'contact_number', 'account_status',
            'is_student', 'is_instructor', 'is_dsa',
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
        # Use Django's create_user to hash the password
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
    # account_status = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [ 'id', 'username', 'first_name', 'last_name', 'email', 'gender', 'is_student', 'is_instructor', 'is_dsa', 'account_status' ]