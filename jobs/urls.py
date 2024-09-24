from django.urls import path
from .views import index , WorkerListView, WorkerDetailView, WorkerCreateView, CustomerCreateView, handle_login

urlpatterns=[
    path('', WorkerListView.as_view(), name='worker-list'),
    path('account-setup/', handle_login, name='handle-login'),
    path('worker/<int:pk>/',WorkerDetailView.as_view(), name='worker-detail'),
    path('worker/create/',WorkerCreateView.as_view(), name='worker-create'),
    path('customer/create/',CustomerCreateView.as_view(), name='customer-create'),

]