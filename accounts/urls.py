from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('email_verify/', VerifyEmailView.as_view()),
    path('login/', LoginView.as_view()),
]

