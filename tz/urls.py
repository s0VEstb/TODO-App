
from django.contrib import admin
from django.urls import path
from TaskManager.models import Task, Status
from TaskManager.views import (main_page_view, task_page_view, task_detail_view,
                               create_task_view, delete_task_view)
from User.views import register_view, confirm_sms_view, login_view, profile_view, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page_view),
    path('tasks/', task_page_view),
    path('tasks/<int:task_id>/', task_detail_view),
    path('create_task/', create_task_view),
    path('tasks/<int:task_id>/delete', delete_task_view),


    path('register/', register_view),
    path('confirm_sms/', confirm_sms_view),
    path('login/', login_view),
    path('profile/', profile_view),
    path('logout/', logout_view),
]
