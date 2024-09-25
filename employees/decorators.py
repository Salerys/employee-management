from employees.models import PersonalDetails
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied


def manager_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        username = request.user
        personal_details = PersonalDetails.objects.get(username=username)
        job_details = personal_details.job_details
        # Check if the user is authenticated and has the MNG role
        if job_details.role == 'MNG' or job_details.role == 'ADM':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")

    return _wrapped_view


def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        try:
            # Fetch the user's role from the PersonalDetails model
            personal_details = PersonalDetails.objects.get(username=user.username)
            if personal_details.job_details.role == 'ADM':  # Check if the role is 'ADM'
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied  # Deny access if the user is not an admin
        except PersonalDetails.DoesNotExist:
            raise PermissionDenied  # Deny access if the user's details are not found

    return _wrapped_view
