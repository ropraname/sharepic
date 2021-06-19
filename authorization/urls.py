from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('registr/', views.regist, name='registr'),
    path('logout/', views.user_logout, name='logout')
]
