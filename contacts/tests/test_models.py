from django.test import TestCase
from django.db import IntegrityError
from ..models import PhoneBookPerson, PhoneNumber, Region


class PhoneBookPersonTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        PhoneBookPerson.objects.create(name='Дин',
                                       surname='Кунц',
                                       phone_number_1='(066)666-66-77',
                                       phone_number_2='(066)777-77-66',
                                       region='Киевская область',
                                       email='kuntz@gmail.com')

    def test_name_label(self):
        person          = PhoneBookPerson.objects.get(id=1)
        field_label     = person._meta.get_field('name').verbose_name
        self.assertEqual(field_label, u'Имя')

    def test_surname_label(self):
        person          = PhoneBookPerson.objects.get(id=1)
        field_label     = person._meta.get_field('surname').verbose_name
        self.assertEqual(field_label, u'Фамилия')

    def test_name_max_length(self):
        person          = PhoneBookPerson.objects.get(id=1)
        max_length      = person._meta.get_field('name').max_length
        self.assertEqual(max_length, 64)

    def test_if_phone_number_1_is_saved_after_person_model_saved_via_pre_save_signal(self):
        person          = PhoneBookPerson.objects.get(id=1)
        phone_number    = PhoneNumber.objects.get(phone_number=person.phone_number_1)
        self.assertEqual(str(phone_number), person.phone_number_1)

    def test_phone_number_1_is_not_duplicated_after_editing_or_saving_new_person_model(self):
        person          = PhoneBookPerson.objects.get(id=1)
        person2         = PhoneBookPerson.objects.create(name='George',
                                                         surname='Orwell',
                                                         phone_number_1=person.phone_number_1)
        numbers         = PhoneNumber.objects.filter(phone_number=person2.phone_number_1).count()
        self.assertEqual(numbers, 1)

    def test_if_phone_number_2_is_saved_after_person_model_saved_via_pre_save_signal(self):
        person          = PhoneBookPerson.objects.get(id=1)
        phone_number    = PhoneNumber.objects.get(phone_number=person.phone_number_2)
        self.assertEqual(str(phone_number), person.phone_number_2)

    def test_phone_number_2_is_not_duplicated_after_editing_or_saving_new_person_model(self):
        person          = PhoneBookPerson.objects.get(id=1)
        person2         = PhoneBookPerson.objects.create(name='George',
                                                         surname='Orwell',
                                                         phone_number_2=person.phone_number_2)
        numbers         = PhoneNumber.objects.filter(phone_number=person2.phone_number_2).count()
        self.assertEqual(numbers, 1)

    def test_phone_number_is_unique(self):
        person          = PhoneBookPerson.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            PhoneNumber.objects.create(phone_number=person.phone_number_1)
            PhoneNumber.objects.create(phone_number=person.phone_number_2)

    def test_if_region_is_saved_after_person_model_saved_via_pre_save_signal(self):
        person          = PhoneBookPerson.objects.get(id=1)
        region          = Region.objects.get(region=person.region)
        self.assertEqual(str(region), person.region)

    def test_email_is_unique(self):
        with self.assertRaises(IntegrityError):
            PhoneBookPerson.objects.create(name='Stephen',
                                           surname='King',
                                           email='kuntz@gmail.com')

    def test_person_absolute_url(self):
        person          = PhoneBookPerson.objects.get(id=1)
        self.assertEqual(person.get_absolute_url(), '/Din-Kunts/1/')
