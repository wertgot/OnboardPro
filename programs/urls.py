from rest_framework.routers import DefaultRouter

from .views import OnboardingProgramViewSet, OnboardingStageViewSet, TaskViewSet

router = DefaultRouter()
router.register('programs', OnboardingProgramViewSet, basename='program')
router.register('stages', OnboardingStageViewSet, basename='stage')
router.register('tasks', TaskViewSet, basename='task')

urlpatterns = router.urls
