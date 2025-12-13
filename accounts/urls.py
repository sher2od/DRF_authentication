from django.urls import path
from .views import RegisterView,LoginView,LogoutView, ProfileView,PasswordChangeView,AdminPanelView,UserPanelView,ManagerPanleView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/profile/', ProfileView.as_view()),
    path('auth/password-change/',PasswordChangeView.as_view()),
    path('admin-panel/',AdminPanelView.as_view()),
    path('user-panel/',UserPanelView.as_view()),
    path('manager-panel/',ManagerPanleView.as_view())

]


