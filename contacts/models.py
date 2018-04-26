# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from smtplib import SMTPException
from unidecode import unidecode


class PhoneBookPerson(models.Model):
    name            = models.CharField(max_length=64, blank=False, null=False, verbose_name=u'Имя')
    surname         = models.CharField(max_length=64, blank=False, null=False, verbose_name=u'Фамилия')
    slug            = models.SlugField(max_length=128)
    phone_number_1  = models.CharField(max_length=25, blank=True, verbose_name=u'Телефон 1',
                                       help_text=u'Выберите или добавьте номер в формате (0__)___-__-__')
    phone_number_2  = models.CharField(max_length=25, blank=True, verbose_name=u'Телефон 2',
                                       help_text=u'Выберите или добавьте номер в формате (0__)___-__-__')
    email           = models.EmailField(unique=True)
    active          = models.BooleanField(default=True, verbose_name=u'Активный')
    created         = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=u'Создан')
    updated         = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=u'Обновлен')
    region          = models.CharField(max_length=50, verbose_name=u'Область',
                                       help_text=u'Выберите или добавьте область проживания. Например: Киевская область')

    class Meta:
        verbose_name        = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'
        ordering            = ('-name',)

    def __str__(self):
        return '%s %s' % (self.name, self.surname)

    def get_absolute_url(self):
        return reverse('contacts:contact_detail', kwargs={'slug': self.slug,
                                                          'pk': self.pk
                                                          })


def create_slug(instance, new_slug=None):
    slug = unidecode(u'%s-%s' % (instance.name, instance.surname))
    if new_slug is not None:
        slug = new_slug
    qs = PhoneBookPerson.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '%s-%s-%s' % (slug, instance.surname, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_phone_book_person_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    if instance.phone_number_1:
        qs = PhoneNumber.objects.filter(phone_number=instance.phone_number_1)
        exists = qs.exists()
        if not exists:
            PhoneNumber.objects.get_or_create(phone_number=instance.phone_number_1)
    if instance.phone_number_2:
        qs = PhoneNumber.objects.filter(phone_number=instance.phone_number_2)
        exists = qs.exists()
        if not exists:
            PhoneNumber.objects.get_or_create(phone_number=instance.phone_number_2)
    if instance.region:
        qs = Region.objects.filter(region=instance.region)
        exists = qs.exists()
        if not exists:
            Region.objects.get_or_create(region=instance.region)

pre_save.connect(pre_save_phone_book_person_receiver, sender=PhoneBookPerson)


def post_save_phone_book_person_receiver(sender, instance, created, *args, **kwargs):
    if created:
        subject         = 'Добавлена запись в телефонную книгу'
        from_email      = settings.EMAIL_HOST_USER
        message         = 'Ваша запись для %s %s была успешно сохранена' % (instance.name, instance.surname)
        recipient_list  = [instance.email]
        try:
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False
            )
        except SMTPException as e:
            print('Something went wrong: ', e.args[-1])

post_save.connect(post_save_phone_book_person_receiver, sender=PhoneBookPerson)


class Region(models.Model):
    region                  = models.CharField(max_length=50, blank=False, unique=True, verbose_name='Область')

    class Meta:
        ordering            = ('region',)
        verbose_name        = 'Область'
        verbose_name_plural = 'Области'

    def __str__(self):
        return '%s' % self.region


class PhoneNumber(models.Model):
    phone_number            = models.CharField(max_length=50, blank=False, unique=True, verbose_name='Номер телефона')

    class Meta:
        ordering            = ('phone_number',)
        verbose_name        = 'Номер телефона'
        verbose_name_plural = 'Номера телефонов'

    def __str__(self):
        return '%s' % self.phone_number
