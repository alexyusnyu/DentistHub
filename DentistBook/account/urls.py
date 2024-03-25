from django.urls import path
from DentistBook.account.views import UserRegisterView, UserLoginView, UserLogoutView, UserDeleteView, \
    UserChangePasswordView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register-page'),
    path('login/', UserLoginView.as_view(), name='login-page'),
    path('delete/', UserDeleteView.as_view(), name='delete-account'),
    path('logout/', UserLogoutView.as_view(), name='logout-page'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password')
]