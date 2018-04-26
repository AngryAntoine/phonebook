from django import forms
from django.forms import Select

from .models import PhoneBookPerson


class ContactCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['surname'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number_1'].widget.attrs.update({'onclick': 'get_phone_list()', 'class': 'get_phone_1 form-control'})
        self.fields['phone_number_2'].widget.attrs.update({'onclick': 'get_phone_list()', 'class': 'get_phone_2 form-control'})
        self.fields['region'].widget.attrs.update({'onclick': 'get_region_list()', 'class': 'get_region form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = PhoneBookPerson
        fields = ['name',
                  'surname',
                  'phone_number_1',
                  'phone_number_2',
                  'region',
                  'email',
                  ]
        widgets = {
            'phone_number_1': Select(),
            'phone_number_2': Select(),
            'region': Select(),
        }

        def clean_email(self):
            email = self.cleaned_data.get('email')
            email_exists = PhoneBookPerson.objects.filter(email__iexact=email).exists()
            if email_exists:
                raise forms.ValidationError('Такой email уже существует')
            return email
