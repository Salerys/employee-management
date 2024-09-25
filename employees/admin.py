from django.contrib import admin
from .models import PersonalDetails
from django.contrib.auth.models import User, Group
from django.contrib.admin import AdminSite


class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'get_job_position',
        'get_department',
        'get_role',
    )
    search_fields = ('first_name', 'last_name')
    list_filter = ('job_details__role',)

    def get_job_position(self, obj):
        return obj.job_details.job_position

    get_job_position.short_description = 'Job Position'

    def get_department(self, obj):
        return obj.job_details.department

    get_department.short_description = 'Department'

    def get_role(self, obj):
        return obj.job_details.role

    get_role.short_description = 'Role'


class JobDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'personal_details',
        'role',
        'department',
        'job_position',
        'is_active',
    )
    list_filter = ('role', 'department', 'is_active')

    def personal_details(self, obj):
        return f"{obj.personal_details.first_name} {obj.personal_details.last_name}"

    personal_details.short_description = 'Employee Name'


# To manage users (including admins) in the admin interface
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

    def get_queryset(self, request):
        return super().get_queryset(request)  # Show all users, including ADM

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Allow role change for ADM users
        return super().change_view(request, object_id, form_url, extra_context)


class CustomAdminSite(AdminSite):
    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff


admin_site = CustomAdminSite(name='custom_admin')

# Then register your models with this custom admin site
admin_site.register(User, UserAdmin)
admin_site.register(PersonalDetails, PersonalDetailsAdmin)
