from django.urls import path   
from . import views

urlpatterns = [
    path('', views.index, name='schedule'),
    path('manage_shifts', views.manage_shifts),
    path('manage_users', views.manage_users),
    path('totals', views.totals),
    path('schedule', views.schedule_shifts, name='schedule_users'),
    path('update_schedule', views.update_schedule),
    path('update_shifts', views.update_shifts),
    path('update_types', views.update_types),
    path('get_shifts/<str:date>/<str:change>', views.get_shifts, name="get_shifts"),
]