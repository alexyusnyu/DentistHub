from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core import exceptions
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from excel_response import ExcelResponse
from DentistBook.dentist.models import Dentist
from DentistBook.dentistsoffice.models import DentistsofficeProfile, DentistsofficeService
from DentistBook.reservation.forms import DentistsofficeServiceForm, DentistsofficeDentistForm, DateSelectionForm, \
    TimeSelectionForm, ReservationForm
from DentistBook.reservation.models import Reservation
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

UserModel = get_user_model()


@login_required
def select_dentistsoffice(request, slug):
    user = request.user
    dentistsoffice = DentistsofficeProfile.objects.get(slug=slug)
    request.session['user_id'] = user.pk
    request.session['dentistsoffice_slug'] = slug
    context = {
        'user': user,
        'dentistsoffice': dentistsoffice
    }
    return render(request, 'reservation/step1-select-dentistsoffice.html', context)


@login_required
def select_dentistsoffice_service(request):
    user = UserModel.objects.get(pk=request.session['user_id'])
    dentistsoffice = DentistsofficeProfile.objects.get(slug=request.session['dentistsoffice_slug'])
    services = dentistsoffice.dentistsofficeservice_set.all()

    if request.method == 'POST':
        form = DentistsofficeServiceForm(request.POST, services=services)
        if form.is_valid():
            request.session['service_id'] = form.cleaned_data['service'].id
            return redirect('step3-select-dentist')

    else:
        form = DentistsofficeServiceForm(services=services)

    context = {
        'user': user,
        'dentistsoffice': dentistsoffice,
        'form': form
    }
    return render(request, 'reservation/step2-select-dentistsoffice-service.html', context)


@login_required
def select_dentist(request):
    user = UserModel.objects.get(pk=request.session['user_id'])
    dentistsoffice = DentistsofficeProfile.objects.get(slug=request.session['dentistsoffice_slug'])
    service = DentistsofficeService.objects.get(id=request.session['service_id'])
    dentists = dentistsoffice.dentist_set.all()
    if request.method == 'POST':
        form = DentistsofficeDentistForm(request.POST, dentists=dentists)
        if form.is_valid():
            request.session['dentist_id'] = form.cleaned_data['dentist'].id
            return redirect('step4-select-date')

    else:
        form = DentistsofficeDentistForm(dentists=dentists)

    context = {
        'user': user,
        'dentistsoffice': dentistsoffice,
        'service': service,
        'form': form
    }
    return render(request, 'reservation/step3-select-dentist.html', context)


@login_required
def select_date(request):
    user = UserModel.objects.get(pk=request.session['user_id'])
    dentistsoffice = DentistsofficeProfile.objects.get(slug=request.session['dentistsoffice_slug'])
    service = DentistsofficeService.objects.get(id=request.session['service_id'])
    dentist = Dentist.objects.get(id=request.session['dentist_id'])

    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            reservation_date = form.cleaned_data['date']
            weekday_index = reservation_date.weekday()
            working_hours = dentistsoffice.dentistsofficeworkinghours_set.filter(day=weekday_index).first()
            start_time = working_hours.start_time
            end_time = working_hours.end_time
            if start_time is None and end_time is None:
                form.add_error('date', 'This day is not available for reservations.')
            else:
                request.session['date'] = form.cleaned_data['date'].isoformat()
                return redirect('step5-select-time')
    else:
        form = DateSelectionForm()

    context = {
        'user': user,
        'dentistsoffice': dentistsoffice,
        'service': service,
        'dentist': dentist,
        'form': form
    }
    return render(request, 'reservation/step4-select-date.html', context)


@login_required
def select_time(request):
    user = UserModel.objects.get(pk=request.session['user_id'])
    dentistsoffice = DentistsofficeProfile.objects.get(slug=request.session['dentistsoffice_slug'])
    service = DentistsofficeService.objects.get(id=request.session['service_id'])
    dentist = Dentist.objects.get(id=request.session['dentist_id'])
    reservation_date_str = request.session['date']
    reservation_date = datetime.strptime(reservation_date_str, '%Y-%m-%d').date()
    weekday_index = reservation_date.weekday()
    working_hours = dentistsoffice.dentistsofficeworkinghours_set.get(day=weekday_index)
    start_time = working_hours.start_time
    end_time = working_hours.end_time

    existing_reservations = Reservation.objects.filter(
        dentistsoffice=dentistsoffice,
        dentist=dentist,
        date=reservation_date
    )

    available_time_slots = []
    current_time = datetime.combine(reservation_date, start_time)
    end_datetime = datetime.combine(reservation_date, end_time)
    current_time = datetime.now() if current_time < datetime.now() else current_time

    if current_time.minute == 0:
        current_time = current_time.replace(minute=0, second=0, microsecond=0)
    elif current_time.minute >= 30:
        current_time = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        current_time = current_time.replace(minute=30, second=0, microsecond=0)

    while current_time < end_datetime:
        time_slot = current_time.time()
        if not existing_reservations.filter(time=time_slot):
            available_time_slots.append((time_slot, time_slot.strftime('%H:%M')))
        current_time += timedelta(minutes=30)

    if request.method == 'POST':
        form = TimeSelectionForm(request.POST, choices=available_time_slots)
        if form.is_valid():
            reservation_time = form.cleaned_data['time_slot']
            request.session['reservation_time'] = reservation_time
            return redirect('create-reservation')
    else:
        form = TimeSelectionForm(choices=available_time_slots)

    context = {
        'user': user,
        'dentistsoffice': dentistsoffice,
        'service': service,
        'dentist': dentist,
        'reservation_date': reservation_date,
        'form': form
    }
    return render(request, 'reservation/step5-select-time.html', context)


@login_required
def create_reservation(request):
    user = UserModel.objects.get(pk=request.session['user_id'])
    dentistsoffice = DentistsofficeProfile.objects.get(slug=request.session['dentistsoffice_slug'])
    service = DentistsofficeService.objects.get(id=request.session['service_id'])
    dentist = Dentist.objects.get(id=request.session['dentist_id'])
    reservation_date_str = request.session['date']
    reservation_date = datetime.strptime(reservation_date_str, '%Y-%m-%d').date()
    reservation_time_str = request.session['reservation_time']
    reservation_time = datetime.strptime(reservation_time_str, '%H:%M:%S').time()

    initial_data = {
        'user': user,
        'dentistsoffice': dentistsoffice,
        'service': service,
        'dentist': dentist,
        'date': reservation_date,
        'time': reservation_time,
    }

    if request.method == 'POST':
        form = ReservationForm(request.POST, initial=initial_data)
        if form.is_valid():
            try:
                reservation = form.save()
                request.session['reservation_id'] = reservation.id
                return redirect('reservation-success')
            except exceptions.ValidationError:
                form.add_error(None, 'A reservation with the same details already exists.')
    else:
        form = ReservationForm(initial=initial_data)

    context = {
        'user': user,
        'dentistsoffice': dentistsoffice,
        'service': service,
        'dentist': dentist,
        'reservation_date': reservation_date,
        'reservation_time': reservation_time,
        'form': form
    }

    return render(request, 'reservation/create-reservation.html', context)


@login_required()
def reservation_success(request):
    reservation = Reservation.objects.get(pk=request.session['reservation_id'])
    user = UserModel.objects.get(pk=request.session['user_id'])
    dentistsoffice = DentistsofficeProfile.objects.get(slug=request.session['dentistsoffice_slug'])
    service = DentistsofficeService.objects.get(id=request.session['service_id'])
    dentist = Dentist.objects.get(id=request.session['dentist_id'])
    reservation_date_str = request.session['date']
    reservation_date = datetime.strptime(reservation_date_str, '%Y-%m-%d').date()
    reservation_time_str = request.session['reservation_time']
    reservation_time = datetime.strptime(reservation_time_str, '%H:%M:%S').time()

    del request.session['reservation_id']
    del request.session['user_id']
    del request.session['dentistsoffice_slug']
    del request.session['service_id']
    del request.session['dentist_id']
    del request.session['date']
    del request.session['reservation_time']

    context = {
        'reservation': reservation,
        'user': user,
        'dentistsoffice': dentistsoffice,
        'service': service,
        'dentist': dentist,
        'reservation_date': reservation_date,
        'reservation_time': reservation_time,
    }

    return render(request, 'reservation/reservation-success.html', context)


class ReservationsListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Reservation
    template_name = 'reservation/reservations-list.html'
    context_object_name = 'reservations'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            if hasattr(user, 'clientprofile'):
                queryset = Reservation.objects.filter(user=user.id)
            elif hasattr(user, 'dentistsofficeprofile'):
                queryset = Reservation.objects.filter(dentistsoffice=user.dentistsofficeprofile)
            else:
                queryset = Reservation.objects.none()
        else:
            queryset = Reservation.objects.none()

        user_filter = self.request.GET.get('user_filter', None)
        if user_filter:
            queryset = queryset.filter(Q(user__username__icontains=user_filter))

        date_filter = self.request.GET.get('date_filter')
        if date_filter:
            queryset = queryset.filter(date=date_filter)

        dentist_filter = self.request.GET.get('dentist_filter')
        if dentist_filter:
            queryset = queryset.filter(Q(dentist__name__icontains=dentist_filter))

        dentistsoffice_filter = self.request.GET.get('dentistsoffice_filter')
        if dentistsoffice_filter:
            queryset = queryset.filter(Q(dentistsoffice__name__icontains=dentistsoffice_filter))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_datetime = datetime.now()

        past_reservations = self.get_queryset().filter(
            Q(date__lt=current_datetime.date()) |
            Q(date=current_datetime.date(), time__lte=current_datetime.time())
        ).order_by('-date', '-time')

        upcoming_reservations = self.get_queryset().filter(
            Q(date__gt=current_datetime.date()) |
            Q(date=current_datetime.date(), time__gt=current_datetime.time())
        ).order_by('date', 'time')

        paginator_past = Paginator(past_reservations, self.paginate_by)
        page_number_past = self.request.GET.get('page_past')
        past_reservations_page = paginator_past.get_page(page_number_past)
        context['past_reservations'] = past_reservations_page

        paginator_upcoming = Paginator(upcoming_reservations, self.paginate_by)
        page_number_upcoming = self.request.GET.get('page_upcoming')
        upcoming_reservations_page = paginator_upcoming.get_page(page_number_upcoming)
        context['upcoming_reservations'] = upcoming_reservations_page

        return context


class ReservationsExcelDownloadView(auth_mixins.LoginRequiredMixin, views.View):
    def get(self, request):
        dentistsoffice_profile = get_object_or_404(DentistsofficeProfile, user=request.user)
        dentistsoffice_reservations = Reservation.objects.filter(dentistsoffice=dentistsoffice_profile)

        excel_data = [
            ['ID', 'User', 'Dentistsoffice', 'Dentist', 'Date', 'Time', 'Service', 'Price']
        ]
        for reservation in dentistsoffice_reservations:
            excel_data.append([
                reservation.id,
                reservation.user.username,
                reservation.dentistsoffice.name,
                reservation.dentist.name,
                reservation.date.strftime('%Y-%m-%d'),
                reservation.time.strftime('%H:%M:%S'),
                reservation.service.service_name,
                reservation.service.price
            ])

        response = ExcelResponse(excel_data, 'xlsx')
        response['Content-Disposition'] = f'attachment; filename="{dentistsoffice_profile.user.username}_reservations.xlsx"'

        return response


class DeleteReservationView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Reservation
    template_name = 'reservation/delete-reservation.html'

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('reservation-list', kwargs={'pk': user.pk})

    def test_func(self):
        reservation = self.get_object()
        return self.request.user == reservation.user or self.request.user == reservation.dentistsoffice.user


