from django.test import TestCase
from ..forms import ContactCreateForm
from ..models import PhoneBookPerson


class ContactCreateFormTest(TestCase):

    def test_contact_create_form_phone_number_1_label(self):
        form        = ContactCreateForm()
        self.assertTrue(form.fields['phone_number_1'].label,
                        'Телефон 1:')

    def test_contact_create_form_phone_number_1_help_text(self):
        form        = ContactCreateForm()
        self.assertTrue(form.fields['phone_number_1'].help_text,
                        'Выберите или добавьте номер в формате (0__)___-__-__')

    def test_contact_create_form_phone_number_2_label(self):
        form        = ContactCreateForm()
        self.assertTrue(form.fields['phone_number_2'].label,
                        'Телефон 2:')

    def test_contact_create_form_phone_number_2_help_text(self):
        form        = ContactCreateForm()
        self.assertTrue(form.fields['phone_number_2'].help_text,
                        'Выберите или добавьте номер в формате (0__)___-__-__')

    def test_contact_create_form_region_help_text(self):
        form        = ContactCreateForm()
        self.assertTrue(form.fields['region'].help_text,
                        'Выберите или добавьте область проживания. Например: Киевская область')

    def test_contact_create_form_is_valid(self):
        form_data   = {'name': 'John',
                       'surname': 'Deere',
                       'phone_number_1': '(066)336-20-33',
                       'phone_number_2': '(066)400-60-70',
                       'region': 'Запорожская область',
                       'email': 'tractor@gmail.com'
                       }
        form        = ContactCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_create_form_create_person(self):
        form_data   = {'name': 'John',
                       'surname': 'Deere',
                       'phone_number_1': '(066)336-20-33',
                       'phone_number_2': '(066)400-60-70',
                       'region': 'Запорожская область',
                       'email': 'tractor@gmail.com'
                       }
        form        = ContactCreateForm(data=form_data)
        form.save()
        exists      = PhoneBookPerson.objects.filter(name__iexact='john', surname__iexact='dEere').exists()
        self.assertTrue(exists)

