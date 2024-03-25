import datetime
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.shortcuts import render
from DentistBook.dentistsoffice.models import DentistsofficeProfile
from DentistBook.reservation.models import Reservation


def home_page(request):
    dentistsoffices_count = DentistsofficeProfile.objects.all().count()
    reservations_count = Reservation.objects.all().count()

    user = request.user

    client_message = None
    if user.is_authenticated and hasattr(user, 'clientprofile'):
        total_reservations = Reservation.objects.filter(user=user).count()
        if total_reservations == 1:
            client_message = f"Total {total_reservations} booked appointment with us"
        else:
            client_message = f"Total {total_reservations} booked appointments with us"

    dentistsoffice_message = None
    if user.is_authenticated and hasattr(user, 'dentistsofficeprofile'):
        today_reservations = Reservation.objects.filter(dentistsoffice=user.dentistsofficeprofile, date=datetime.date.today()).count()
        if today_reservations == 1:
            dentistsoffice_message = f"You have {today_reservations} reservation for today"
        else:
            dentistsoffice_message = f"You have {today_reservations} reservations for today"

    context = {
        'dentistsoffices_count': dentistsoffices_count,
        'reservations_count': reservations_count,
        'client_message': client_message,
        'dentistsoffice_message': dentistsoffice_message,
    }
    return render(request, 'common/home.html', context)


def map_page(request):
    dentistsoffices = DentistsofficeProfile.objects.all()
    dentistsoffices = dentistsoffices.annotate(avg_rating=Avg('review__rating'))
    dentistsoffices = dentistsoffices.annotate(reviews_count=Count('review'))
    context = {
        'dentistsoffices': dentistsoffices
    }
    return render(request, 'common/map-all-dentistsoffices.html', context)


def search_view(request):
    if request.method == 'GET' and 'q' in request.GET:
        query = request.GET.get('q', '')
        results = DentistsofficeProfile.objects.filter(
            Q(name__icontains=query) | Q(city__icontains=query)
        )
        data = [{'name': result.name, 'address': result.address, 'city': result.city, 'slug': result.slug} for result in results]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


def about_page(request):
    return render(request, 'common/about.html')