from . import views
from django.urls import path
from django.contrib.auth import views as authentication_views
from plp_users.forms import LoginForm

urlpatterns = [
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('login/', authentication_views.LoginView.as_view(template_name='plp_users/login.html', authentication_form=LoginForm), name="login"),
    path('logout/', authentication_views.LogoutView.as_view(template_name='plp_users/logout.html'), name="logout"),
]

