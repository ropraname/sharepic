from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.view_home, name='view_home'),
    path('share/', views.upload, name='upload'),
    path('view/<int:pk>/', views.picture_detail, name='picture-detail'),
    path('profile/', views.view_profile, name='view_profile'),
    path('my_profile/', views.view_your_profile, name='view_your_profile'),
    path('scoreboard/', views.view_scoreboard, name='view_scoreboard'),
    path('view/<int:pk>/update',
         views.PictureUpdateView.as_view(), name='picture-update'),
    path('view/<int:pk>/delete',
         views.PictureDeleteView.as_view(), name='picture-delete'),
]
