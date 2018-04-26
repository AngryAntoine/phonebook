from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import View
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import ContactCreateForm
from .models import (PhoneBookPerson,
                     PhoneNumber,
                     Region)


class PhoneBookPersonListView(ListView):
    model               = PhoneBookPerson
    template_name       = 'contacts/contact_list.html'
    context_object_name = 'contact_list'
    paginate_by         = 10

    def get_queryset(self):
        queryset = PhoneBookPerson.objects.filter(active=True)
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('name', 'surname', 'phone_number_1', 'phone_number_2', 'region', 'email'):
            queryset = queryset.order_by(order_by).distinct()
            if self.request.GET.get('reverse', '') == '1':
                queryset = queryset.reverse().distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PhoneBookPersonListView, self).get_context_data()
        context['head_title'] = 'Список'
        return context


class PhoneBookPersonCreateView(CreateView):
    form_class      = ContactCreateForm
    template_name   = 'forms/form.html'

    def get_context_data(self, **kwargs):
        context = super(PhoneBookPersonCreateView, self).get_context_data()
        context['head_title'] = 'Добавить контакт'
        return context


class PhoneBookPersonDetailView(DetailView):
    model               = PhoneBookPerson
    template_name       = 'contacts/contact_detail.html'
    context_object_name = 'contact'

    def get_context_data(self, **kwargs):
        context = super(PhoneBookPersonDetailView, self).get_context_data()
        obj = self.get_object()
        common_numbers_level_1 = PhoneBookPerson.objects.filter(Q(phone_number_1=obj.phone_number_1) |
                                                                Q(phone_number_1=obj.phone_number_2) |
                                                                Q(phone_number_2=obj.phone_number_1) |
                                                                Q(phone_number_2=obj.phone_number_2)
                                                                ).exclude(id=obj.id)
        common_numbers_level_2 = []
        for i in common_numbers_level_1:
            common_numbers_level_2.append(PhoneBookPerson.objects.filter(Q(phone_number_1=i.phone_number_1) |
                                                                         Q(phone_number_1=i.phone_number_2) |
                                                                         Q(phone_number_2=i.phone_number_1) |
                                                                         Q(phone_number_2=i.phone_number_2)
                                                                         ).exclude(id=i.id).exclude(id=obj.id)
                                          )
        context['head_title']             = 'Детальная информация'
        context['common_numbers_level_1'] = common_numbers_level_1
        context['common_numbers_level_2'] = common_numbers_level_2
        return context


class PhoneBookPersonUpdateView(UpdateView):
    model               = PhoneBookPerson
    form_class          = ContactCreateForm
    template_name       = 'forms/form.html'
    context_object_name = 'contact'

    def get_context_data(self, **kwargs):
        context = super(PhoneBookPersonUpdateView, self).get_context_data()
        context['head_title'] = 'Обновить данные'
        return context


class PhoneBookPersonDeleteView(DeleteView):
    model           = PhoneBookPerson
    template_name   = 'forms/form.html'
    success_url     = reverse_lazy('contacts:contact_list')

    def get_context_data(self, **kwargs):
        context = super(PhoneBookPersonDeleteView, self).get_context_data()
        context['head_title'] = 'Удалить контакт'
        return context


class RegionSelectView(View):

    def get(self, request):
        if request.is_ajax():
            regions = Region.objects.all()
            data = []
            for region in regions:
                sub_dict = {'id': region.region,
                            'text': region.region
                            }
                data.append(sub_dict)
            return JsonResponse(data, safe=False)


class PhoneSelectView(View):

    def get(self, request):
        if request.is_ajax():
            numbers = PhoneNumber.objects.all()
            data = []
            for number in numbers:
                sub_dict = {'id': number.phone_number,
                            'text': number.phone_number
                            }
                data.append(sub_dict)
            return JsonResponse(data, safe=False)
