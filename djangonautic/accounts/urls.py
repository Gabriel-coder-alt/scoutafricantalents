from django.urls import re_path, path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('signup/<uidb64>/', views.SignupView, name='signup'),
    path('forgot_password/', views.passwordretrievalform, name='forgot_password'),
    path('password_reset_link/<uidb64>/<token>/', views.resetpassword, name='password_reset_link')
#     re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.SignupView, name='signup'),   
]