from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .decorators import manager_required
from .models import JobDetails, Performance, PersonalDetails
from .forms import EditProfileForm, RegisterForm
from .utils import (
    clear_messages,
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

            # Create an empty Performance model
            performance_model = Performance.objects.create()

            # Create a JobDetails model and assign the Performance model
            job_details_model = JobDetails.objects.create(performance=performance_model)

            # Create the PersonalDetails and associate with the user and job_details
            PersonalDetails.objects.create(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                password=user.password,
                job_details=job_details_model,
            )

            # Redirect if success
            messages.success(request, "Registration successful!")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")

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


@login_required
def update_profile(request, id):
    clear_messages(request)
    user = request.user
    personal_details = get_object_or_404(PersonalDetails, username=user.username)

    if request.method == 'POST':

        form = EditProfileForm(request.POST, instance=personal_details)

        if form.is_valid():

            form.save()

            # Update the User model data (username, email, and password)
            new_username = form.cleaned_data.get('username')
            new_email = form.cleaned_data.get('email')
            new_password = form.cleaned_data.get('new_password')

            # Update username and email if changed
            user.username = new_username
            user.email = new_email

            # If a new password is provided, hash it and update the User's password
            if new_password:
                user.password = make_password(new_password)
                user.save()

                # Reauthenticate the user with the new credentials
                updated_user = authenticate(
                    username=new_username, password=new_password
                )
                if updated_user is not None:
                    login(request, updated_user)  # Re-log the user in

            else:
                user.save()  # Save changes if no password is updated

            messages.success(request, 'Update was successful.')
            return render(request, 'main/edit-profile.html', {'form': form, 'id': id})

        else:
            messages.error(request, 'There was an error with your submission.')

    else:
        form = EditProfileForm(instance=personal_details)
    return render(request, 'main/edit-profile.html', {'form': form, 'id': id})


@login_required
@manager_required
def employees_list(request):
    current_user = request.user
    username = current_user.username
    job_details = get_job_details_by_username(username)
    self_id = job_details.id
    search_query = request.GET.get('search', '')

    # Start with the base queryset
    employees = PersonalDetails.objects.select_related('job_details')

    # Check if the current user is an ADM
    if job_details.role != 'ADM':
        # Exclude employees with the ADM role if the user is not an ADM
        employees = employees.exclude(job_details__role='ADM')

    if search_query:
        employees = employees.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(job_details__department__icontains=search_query)
        )

    return render(
        request, 'main/list.html', {'employees': employees, 'self_id': self_id}
    )
