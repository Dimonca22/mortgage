from .models import MortgageOffer
from operator import itemgetter


def calculator(price, deposit, term, api=False, ordering=None):
    total = int(price - price * (deposit / 100))  # всего
    mes = term * 12  # срок кредита (месяцах)
    offers = MortgageOffer.objects.filter(
        term_min__lte=term,
        term_max__gte=term,
        payment_min__lte=total,
        payment_max__gte=total,
    )
    prize = []
    for offer in offers:
        bank = offer.bank_name
        of_p_min = offer.rate_min  # мин ставка по кредиту (месяц)
        of_p_max = offer.rate_max  # макс ставка по кредиту (месяц)
        r_min = of_p_min / 12 / 100  # мин (%) ставка за год /на 12 месяцев
        r_max = of_p_max / 12 / 100  # макс (%) ставка за год / на 12 месяцев
        min_gen_rate = (1 + r_min) ** mes  # мин общая (%) ставка
        max_gen_rate = (1 + r_max) ** mes  # макс общая (%) ставка
        min_monthly_payment = total * r_min * min_gen_rate / (min_gen_rate - 1)  # мин ежемесячный платеж
        max_monthly_payment = total * r_max * max_gen_rate / (max_gen_rate - 1)  # макс ежемесячный платеж
        min_over = min_monthly_payment * mes - total
        max_over = max_monthly_payment * mes - total
        if api:
            res_sentence = {
                "bank": bank,
                "term_min": offer.term_min,
                "term_max": offer.term_max,
                "rate_min": offer.rate_min,
                "rate_max": offer.rate_max,
                "payment_min": offer.payment_min,
                "payment_max": offer.payment_max,
                "result": int(min_monthly_payment),
            }
        else:
            res_sentence = {
                'bank': bank,
                'min_rate': of_p_min,
                'max_rate': of_p_max,
                'min_payment': int(min_monthly_payment),
                'max_payment': int(max_monthly_payment),
                'min_over': int(min_over),
                'max_over': int(max_over),
            }
        prize.append(res_sentence)
    if ordering == 'rate_min':
        prize = sorted(prize, key=itemgetter('rate_min'))
    elif ordering == '-rate_min':
        prize = sorted(prize, key=itemgetter('rate_min'), reverse=True)
    return prize
