from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    # image_url = serializers.ImageField(required=True)

    class Meta:
        model = Person
        fields = ('id', 'name', 'image_url')  # fields = ('id',) to use only one field
