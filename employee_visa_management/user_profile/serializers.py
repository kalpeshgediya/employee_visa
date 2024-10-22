from rest_framework import serializers
from .models import *

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['full_name', 'remarks', 'citizen_ship', 'licence_no', 'expiry_date']