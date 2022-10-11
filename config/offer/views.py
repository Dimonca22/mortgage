from django.shortcuts import render
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from .models import MortgageOffer
from .serializers import MortgageSerializer, ResultSerializer
from .forms import BankForm
from .utils import calculator
from django_filters.rest_framework import DjangoFilterBackend


class MortgageViewSet(viewsets.ModelViewSet):
    queryset = MortgageOffer.objects.all()
    serializer_class = MortgageSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_fields = ['term_min', 'term_max', 'rate_min', 'rate_max', 'payment_min', 'payment_max', ]
    ordering_fields = ['rate_min', ]

    def list(self, request, *args, **kwargs):
        price = request.query_params.get('price')
        deposit = request.query_params.get('deposit')
        term = request.query_params.get('term')
        ordering = request.query_params.get('ordering')
        if price and deposit and term:
            serializer = ResultSerializer
            result = calculator(int(price), int(deposit), int(term), api=True, ordering=ordering)
            return Response(serializer(result, many=True).data, status=status.HTTP_200_OK)
        else:
            queryset = MortgageOffer.objects.all()
            return Response(self.serializer_class(queryset, many=True).data, status=status.HTTP_200_OK)


def calculatorOffer(request):
    form = BankForm()
    res = []
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data
            res = calculator(
                response['price'],
                response['deposit'],
                response['term']
            )
        else:
            form = BankForm()
    return render(request, {'form': form, 'offers': res})
