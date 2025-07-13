from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, DepartmentViewSet, SubjectViewSet, SubjectOfferingViewSet, DepartmentDetailViewSet, ScheduleViewSet

app_name = 'students'

router = DefaultRouter()

router.register(r'courses', CourseViewSet, basename='course')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'offerings', SubjectOfferingViewSet, basename='offerings')
router.register(r'schedules', ScheduleViewSet, basename='schedules')

router.register(r'department-detail', DepartmentDetailViewSet, basename='department-detail')


urlpatterns = [
    path('', include(router.urls)),
]


