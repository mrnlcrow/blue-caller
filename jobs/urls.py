from django.urls import path
from .views import index , WorkerListView, WorkerDetailView, WorkerCreateView, CustomerCreateView, handle_login
from django.views.generic import TemplateView


urlpatterns=[
    path('', TemplateView.as_view(template_name="landing/index.html"), name='landing-page'),
    path('get-started/', WorkerListView.as_view(), name='worker-list'),
    path('account-setup/', handle_login, name='handle-login'),
    path('worker/<int:pk>/',WorkerDetailView.as_view(), name='worker-detail'),
    path('worker/create/',WorkerCreateView.as_view(), name='worker-create'),
    path('customer/create/',CustomerCreateView.as_view(), name='customer-create'),

]