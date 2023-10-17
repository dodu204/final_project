from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import RegistrationForm, AdvertisementForm, ResponseForm
from .models import Advertisement, UserProfile, Category


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            user_profile = UserProfile(user=user)
            user_profile.generate_confirmation_code()
            user_profile.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = f'Click the link to activate your account: http://{current_site.domain}/activate/{user_profile.confirmation_code}/'
            send_mail(subject, message, 'from@example.com', [user.email])

            return render(request, 'notice_board/registration_complete.html')
    else:
        form = RegistrationForm()
    return render(request, 'notice_board/register.html', {'form': form})


def activate_account(request, confirmation_code):
    try:
        user_profile = UserProfile.objects.get(confirmation_code=confirmation_code)
    except UserProfile.DoesNotExist:
        return render(request, 'notice_board/activation_failed.html')

    user = user_profile.user
    user.is_active = True
    user.save()

    user_profile.email_confirmed = True
    user_profile.save()

    login(request, user)
    return render(request, 'notice_board/activation_success.html')


@login_required
def create_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            return redirect('advertisement_list')
    else:
        form = AdvertisementForm()

    categories = Category.objects.all()
    return render(request, 'notice_board/create_advertisement.html', {'form': form, 'categories': categories})


def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'notice_board/advertisement_list.html', {'advertisements': advertisements})


def create_response(request, advertisement_id):
    advertisement = Advertisement.objects.get(pk=advertisement_id)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = advertisement
            response.user = request.user
            response.save()

            send_mail(
                'New Response',
                'You have a new response to your advertisement.',
                'from@example.com',
                [advertisement.user.email],
                fail_silently=False,
            )

            return redirect('advertisement_list')
    else:
        form = ResponseForm()
    return render(request, 'notice_board/create_response.html', {'form': form, 'advertisement': advertisement})
