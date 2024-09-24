from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import JobDetails, Performance, PersonalDetails
from .forms import RegisterForm
from .utils import (
    get_job_details_by_username,
    get_performance_by_username,
    get_personal_details_by_username,
)


def index(request):
    return render(request, 'base.html')


# user registration
def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Step 1: Create an empty Performance instance
            performance_model = Performance.objects.create()

            # Step 2: Create a JobDetails instance and assign the performance
            job_details_model = JobDetails.objects.create(performance=performance_model)

            # Step 3: Create the PersonalDetails and associate with the user and job_details
            PersonalDetails.objects.create(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                password=user.password,  # Assuming password is already hashed by the form
                job_details=job_details_model,
            )

            messages.success(request, "Registration successful!")  # Success message
            return redirect('/')  # Redirect to a success page after registration
        else:
            messages.error(
                request, "There was an error with your submission."
            )  # Error message

    else:
        form = RegisterForm()

    return render(
        request,
        'register/register.html',
        {'form': form},
    )


@login_required
def home(request):
    current_user = request.user
    username = current_user.username
    job_details = get_job_details_by_username(username)
    personal_details = get_personal_details_by_username(username)
    first_name = personal_details.first_name

    return render(
        request, 'main/home.html', {'job': job_details, 'first_name': first_name}
    )


@login_required
def get_profile_data(request, id):
    current_user = request.user
    username = current_user.username

    personal_details = get_personal_details_by_username(username)
    job_details = get_job_details_by_username(username)
    performance = get_performance_by_username(username)

    return render(
        request,
        'main/profile.html',
        {
            'personal_details': personal_details,
            'job_details': job_details,
            'performance': performance,
        },
    )
