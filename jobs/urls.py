from django.urls import path
from .views import index , WorkerListView, WorkerDetailView

urlpatterns=[
    path('', WorkerListView.as_view(), name='worker-list'),
    path('worker/<int:pk>/',WorkerDetailView.as_view(), name='worker-detail'),
]