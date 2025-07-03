from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, DepartmentViewSet

app_name = 'students'

router = DefaultRouter()

router.register(r'courses', CourseViewSet, basename='course')
router.register(r'departments', DepartmentViewSet, basename='department')


urlpatterns = [
    path('', include(router.urls)),
]


