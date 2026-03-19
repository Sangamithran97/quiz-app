from django.urls import path
from .views import HistoryView, PerformanceView

urlpatterns=[
    path('performance/', PerformanceView.as_view(), name='performance'),
    path('history/', HistoryView.as_view(), name='history'),
]