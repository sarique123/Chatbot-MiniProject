from django.urls import path
from . import views
from .views import SignupView,LoginView


urlpatterns = [
    path('',views.home,name = 'home'),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
]