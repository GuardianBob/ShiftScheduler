from django.urls import path   
from . import views

urlpatterns = [
    path('', views.index, name='schedule'),
    path('manage_shifts', views.manage_shifts, name='manage_shifts'),
    path('manage_users', views.manage_users, name='manage_vets'),
    path('new_user', views.new_user, name='new_user'),
    path('users/info', views.show_user, name='user_info'),
    path('users/info/<int:user_id>', views.show_user, name='user_info'),
    path('users/edit/<int:user_id>', views.edit_user, name='edit_user'),
    path('users/remove/<int:remove_id>', views.remove_user, name='remove_user'),
    path('update_password', views.update_password, name='update_password'),
    path('update_user', views.update_user, name='update_user'),
    path('admin_tools', views.admin_tools, name='admin_tools'),
    path('schedule', views.schedule_shifts, name='schedule_users'),
    path('update_schedule', views.update_schedule),
    path('update_shifts', views.update_shifts, name="update_shifts"),
    path('delete_sched_shift', views.delete_sched_shift, name="delete_sched_shift"),
    path('delete_multiple', views.delete_multiple, name="delete_multiple"),
    path('update_shifts/<int:shift_id>', views.update_shifts, name="update_shifts"),
    path('update_types', views.update_types, name='update_types'),
    path('update_types/<int:type_id>', views.update_types, name='update_types'),
    path('remove_shift/<int:shift_id>', views.remove_shift, name='remove_shift'),
    path('remove_shift_type/<int:type_id>', views.remove_shift_type, name='remove_shift_type'),
    path('get_shifts/<str:date>', views.get_shifts, name="get_shifts"),
    path('get_shifts/<str:date>/<int:user_id>', views.get_shifts, name="get_shifts"),
    # path('new_events/<str:events>', views.new_evens, name="new_events"),
]