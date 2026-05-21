from django.urls import path

from .views import MyTaskPatchView, MyTasksView

urlpatterns = [
    path('my-tasks/', MyTasksView.as_view(), name='mobile-my-tasks'),
    path('my-tasks/<int:pk>/', MyTaskPatchView.as_view(), name='mobile-my-task-patch'),
]
