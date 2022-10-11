from django.db import models
from django.core import validators


class MortgageOffer(models.Model):
    bank_name = models.CharField(max_length=150, verbose_name='Название банка')
    term_min = models.IntegerField(validators=[validators.MinValueValidator(10)],
                                   default=10, verbose_name='Срок ипотеки, от ')
    term_max = models.IntegerField(validators=[validators.MaxValueValidator(30)],
                                   default=30, verbose_name='Срок ипотеки, до')
    rate_min = models.FloatField(default=1.8, verbose_name='Ставка от (%)')
    rate_max = models.FloatField(default=9.8, verbose_name='Ставка до (%)')
    payment_min = models.IntegerField(default=1000000, verbose_name='Сумма кредита, от')
    payment_max = models.IntegerField(default=10000000, verbose_name='Сумма кредита, до')

    class Meta:
        verbose_name = 'Предложение по ипотеке'
        verbose_name_plural = 'Предложения по ипотеке'

    def __str__(self):
        return self.bank_name
