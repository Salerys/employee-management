from django.test import TestCase
from .models import PersonalDetails
from .forms import EditProfileForm


class PersonalDetailsTest(TestCase):
    def setUp(self):
        self.personal_detail = PersonalDetails.objects.create(
            first_name='John',
            last_name='Doe',
            username='john_doe',
            email='john@example.com',
        )

    def test_personal_details_creation(self):
        self.assertEqual(self.personal_detail.first_name, 'John')
        self.assertEqual(self.personal_detail.last_name, 'Doe')


class EditProfileFormTest(TestCase):
    def test_form_validity(self):
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'jane_doe',
            'email': 'jane@example.com',
            'phone_number': '1234567890',
            'new_password': 'newpassword',
            'confirm_new_password': 'newpassword',
        }
        form = EditProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
