from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  LoginView, LogoutView, MeView, UserViewSet, StudentViewSet

app_name = 'users'

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'students', StudentViewSet, basename='student')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),

]


