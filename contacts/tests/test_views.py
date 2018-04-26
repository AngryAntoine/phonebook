from django.urls import reverse
from django.test import TestCase

from ..models import PhoneBookPerson


class PhoneBookPersonListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create 12 persons for pagination test
        number_of_contacts = 12
        for number in range(number_of_contacts):
            PhoneBookPerson.objects.create(name='Michael%s' % number,
                                           surname='Jackson%s' % number,
                                           email='email%s@gmail.com' % number)

    def test_view_url_accessible_by_name(self):
        response    = self.client.get(reverse('contacts:contact_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response    = self.client.get(reverse('contacts:contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts/contact_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('contacts:contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'], True)
        self.assertTrue(len(response.context['contact_list']), 10)

    def test_pagination_remaining_3_contacts(self):
        response = self.client.get(reverse('contacts:contact_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'], True)
        self.assertTrue(len(response.context['contact_list']), 2)


class PhoneBookPersonCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        PhoneBookPerson.objects.create(name='Michael',
                                       surname='Jackson',
                                       email='thriller@gmail.com')

    def test_view_url_accessible_by_name(self):
        response    = self.client.get(reverse('contacts:contact_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response    = self.client.get(reverse('contacts:contact_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forms/form.html')


class PhoneBookPersonDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        PhoneBookPerson.objects.create(name='Michael',
                                       surname='Jackson',
                                       email='thriller@gmail.com')

    def test_view_url_accessible_by_name(self):
        person      = PhoneBookPerson.objects.get(id=1)
        response    = self.client.get(reverse('contacts:contact_detail', args=[person.slug, person.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        person      = PhoneBookPerson.objects.get(id=1)
        response    = self.client.get(person.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts/contact_detail.html')


class PhoneBookPersonDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        PhoneBookPerson.objects.create(name='Michael',
                                       surname='Jackson',
                                       email='thriller@gmail.com')

    def test_view_url_accessible_by_name(self):
        person      = PhoneBookPerson.objects.get(id=1)
        response    = self.client.get(reverse('contacts:contact_delete', args=[person.slug, person.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        person      = PhoneBookPerson.objects.get(id=1)
        response    = self.client.get(reverse('contacts:contact_delete', args=[person.slug, person.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forms/form.html')

    def test_view_can_delete_person(self):
        person      = PhoneBookPerson.objects.get(id=1)
        PhoneBookPerson.delete(person)
        persons     = PhoneBookPerson.objects.all().count()
        self.assertEqual(persons, 0)
