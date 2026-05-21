from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import OnboardingInstanceViewSet, TaskProgressViewSet

router = DefaultRouter()
router.register('instances', OnboardingInstanceViewSet, basename='instance')

urlpatterns = router.urls + [
    path(
        'instances/<int:instance_pk>/tasks/<int:pk>/',
        TaskProgressViewSet.as_view({'patch': 'partial_update'}),
        name='instance-task-progress',
    ),
]
