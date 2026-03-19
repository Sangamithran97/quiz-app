from django.urls import path
from .views import StartAttemptView, SubmitAttemptView

urlpatterns=[
    path('start/', StartAttemptView.as_view(), name='start-attempt'),
    path('submit/', SubmitAttemptView.as_view(), name='submit-attempt'),
]