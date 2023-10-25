from django.urls import path
from .views import DayListAPIView, TaskListAPIView, TaskRUDAPIView


urlpatterns = [
    path('day/list/', DayListAPIView.as_view()),
    path('day/detail/<int:day_id>/task/', TaskListAPIView.as_view()),
    path('day/detail/<int:day_id>/task/detail/<int:pk>/', TaskRUDAPIView.as_view()),
]