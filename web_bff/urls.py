from django.urls import path

from .views import InstanceDetailBFFView

urlpatterns = [
    path('instances/<int:pk>/', InstanceDetailBFFView.as_view(), name='instance-bff-detail'),
]
