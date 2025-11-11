from rest_framework import serializers
from qorder.models import *

class CodigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codigo
        fields = ('codigo', 'descripcion',)

