from .models import PersonalDetails
from django.contrib import messages


def get_personal_details_by_username(username):
    personal_details = PersonalDetails.objects.get(username=username)
    return personal_details


def get_job_details_by_username(username):
    personal_details = PersonalDetails.objects.get(username=username)
    job_details = personal_details.job_details
    return job_details


def get_performance_by_username(username):
    personal_details = PersonalDetails.objects.get(username=username)
    job_details = personal_details.job_details
    performance = job_details.performance
    return performance


def clear_messages(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass
