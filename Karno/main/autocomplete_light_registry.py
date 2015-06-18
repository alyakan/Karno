import autocomplete_light
from django.contrib.auth.models import User


class UserAutoComplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['username']
    choices = User.objects.all()
    model = User
autocomplete_light.register(User, UserAutoComplete)
