from django import forms
from .models import MortgageOffer
from django.db.models import Max

max_term = MortgageOffer.objects.aggregate(Max('term_max')).get('term_max__max')


class BankForm(forms.Form):
    price = forms.IntegerField(label='Цена объекта недвижимости', required=True)
    deposit = forms.FloatField(label='Первоначальный взнос, в (%)', required=True, max_value=100)
    term = forms.IntegerField(label='Количество лет ипотечного рабства', max_value=max_term, required=True, )
