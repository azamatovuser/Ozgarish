from django.urls import path
from .views import DayListAPIView, TaskListAPIView, \
    TaskRUDAPIView, TimeCreateAPIView, \
    TaskCreateAPIView, TimeTotalAPIView


urlpatterns = [
    # day
    path('day/list/', DayListAPIView.as_view()),

    #task
    path('create/', TaskCreateAPIView.as_view()),
    path('day/detail/<int:day_id>/task/', TaskListAPIView.as_view()),
    path('day/detail/<int:day_id>/task/detail/<int:pk>/', TaskRUDAPIView.as_view()),

    # time
    path('time/create/', TimeCreateAPIView.as_view()),
    path('day/detail/<int:day_id>/time/total/', TimeTotalAPIView.as_view()),
]