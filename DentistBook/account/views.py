from django.contrib import messages
from django.contrib.auth import views as auth_views, get_user_model, login
from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import render, redirect
from DentistBook.account.forms import RegisterUserForm

UserModel = get_user_model()


class UserRegisterView(views.CreateView):
    template_name = 'account/register-page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'account/login-page.html'

    def get_success_url(self):
        return reverse_lazy('home-page')


class UserLogoutView(auth_views.LogoutView):
    template_name = 'account/logout-page.html'
    next_page = reverse_lazy('home-page')

    def dispatch(self, request, *args, **kwargs):
        if 'confirm' in request.GET:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, self.template_name)


class UserDeleteView(views.DeleteView):
    model = UserModel
    template_name = 'account/delete-account-page.html'
    success_url = reverse_lazy('home-page')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            return redirect('home-page')

        return super().delete(request, *args, **kwargs)


class UserChangePasswordView(auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
    model = UserModel
    template_name = 'account/change-password.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password changed successfully.")
        return response
