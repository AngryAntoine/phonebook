from django.contrib import admin

from .models import (PhoneBookPerson,
                     PhoneNumber,
                     Region)


class PhoneBookPersonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", "surname")}
    list_display_links = ['name', 'surname']
    list_display = ('name', 'surname', 'email', 'active')
    list_editable = ('email', 'active',)


admin.site.register(PhoneBookPerson, PhoneBookPersonAdmin)
admin.site.register(PhoneNumber)
admin.site.register(Region)
