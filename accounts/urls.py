from django.urls import path
from .views import RegsiterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('register/', RegsiterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='obtain_pair_view'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
]