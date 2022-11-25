from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path,include
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from construct import views as  views 
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from . import login_views, views,client_views,architect_views,engineer_views

urlpatterns = [
     path('',views.homepage),
     path('home/',client_views.admin_home,name='client_home'),
     path('addproject/',client_views.addproject,name='addproject'),
     path("send_architect_notification/", client_views.send_architect_notification,
         name='send_architect_notification'),
     path("admin_notify_architect", client_views.admin_notify_architect,
         name='admin_notify_architect'),

     path("send_engineer_notification/", client_views.send_engineer_notification,
         name='send_engineer_notification'),
     path("admin_notify_engineer", client_views.admin_notify_engineer,
         name='admin_notify_engineer'),

     path('viewprojects',client_views.client_viewprojects,name="client_viewprojects"),
     path('deleteproject',client_views.deleteproject,name='deleteproject'),
     path('editproject/<int:id>',client_views.updateproject),
     path('updateprojectdetails/<int:id>',client_views.updateprojectdetails),
     path("architect/view/feedback/", client_views.architect_task_message,
         name="architect_task_message",),
     path("engineer/view/feedback/", client_views.engineer_task_message,
         name="engineer_task_message",),



     path("login", login_views.login_page, name='login_page'),
     path("architectlogin", login_views.architect_login_page, name='architect_login_page'),
     path("engineerlogin", login_views.engineer_login_page, name='engineer_login_page'),
     path("doLogin/", login_views.doLogin, name='user_login'),
     path("architectdoLogin/", login_views.architectdoLogin, name='architect_user_login'),
     path("engineerdoLogin/", login_views.engineerdoLogin, name='engineer_user_login'),
     path("architect_register",login_views.architect_register,name="architect_register"),
     path("engineer_signup",login_views.engineer_signup,name='engineer_signup'),
     path("logout_user/", login_views.logout_user, name='user_logout'),
     path("check_email_availability", login_views.check_email_availability,
         name="check_email_availability"),



    ###architect
     path('architect_home',architect_views.architect_home,name="architect_home"),
     path("architect/fcmtoken/", architect_views.architect_fcmtoken,
         name='architect_fcmtoken'),
     path("architect/view/notification/", architect_views.architect_view_notification,
         name="architect_view_notification"),
     path("architect/task/", architect_views.architect_task,
         name='architect_task'),
     path("architect/project/", architect_views.architect_project,
         name='architect_project'),
     path("architect/details/", architect_views.architect_details,
         name='architect_details'),
     path("architect/view/profile/", architect_views.architect_view_profile,
         name='architect_view_profile'),



    ###engineer
     path('engineer_home',engineer_views.engineer_home,name="engineer_home"),
     path("engineer/task/", engineer_views.engineer_task,
         name='engineer_task'),
     path("engineer/project/", engineer_views.engineer_project,
         name='engineer_project'),
     path("engineer/view/profile/", engineer_views.engineer_view_profile,
         name='engineer_view_profile'),
     path("engineer/fcmtoken/", engineer_views.engineer_fcmtoken,
         name='engineer_fcmtoken'),
     path("engineer/view/notification/", engineer_views.engineer_view_notification,
         name="engineer_view_notification")




]
