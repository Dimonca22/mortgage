from rest_framework import serializers

from .models import MortgageOffer


class MortgageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageOffer
        fields = '__all__'


class ResultSerializer(serializers.Serializer):
    bank = serializers.CharField(max_length=50)
    term_min = serializers.IntegerField(default=10)
    term_max = serializers.IntegerField(default=30)
    rate_min = serializers.FloatField(default=1.8)
    rate_max = serializers.FloatField(default=9.8)
    payment_min = serializers.IntegerField(default=1000000)
    payment_max = serializers.IntegerField(default=10000000)
    result = serializers.IntegerField(default=0)
