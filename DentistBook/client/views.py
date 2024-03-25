from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views
from DentistBook.client.models import ClientProfile


class EditClientProfileView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = ClientProfile
    template_name = 'client/edit-client.html'
    fields = ['first_name', 'last_name', 'city', 'phone', 'profile_picture']

    def get_success_url(self):
        return reverse_lazy('client-details')

    def get_object(self, queryset=None):
        return ClientProfile.objects.get(user_id=self.request.user)

    def form_valid(self, form):
        if self.request.user != self.get_object().user:
            return redirect('home-page')

        result = super().form_valid(form)

        return result


class ClientProfileDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = ClientProfile
    template_name = 'client/client-details.html'
    context_object_name = 'client_profile'

    def get_object(self, queryset=None):
        return ClientProfile.objects.get(user_id=self.request.user)