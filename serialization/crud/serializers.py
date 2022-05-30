from pyexpat import model
from unicodedata import name
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.Serializer):
    name= serializers.CharField(max_length=100)
    roll= serializers.IntegerField()
    city= serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(name)
        instance.name = validated_data.get('name', instance.name)
        print(name)
        instance.roll = validated_data.get('roll', instance.roll)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance

    # FIELD LEVEL VALIDATION
    # if someone try to post request with roll>200, it will not allow to submit that.
    def validate_roll(self, value):
        if value >= 200:
            raise serializers.ValidationError("seats are full !!")
        return value

    # object LEVEL VALIDATION
    # data is python dictionary of field values
    def validate(self, data):
        nm = data.get('name')
        ct = data.get('city')
        if nm.lower() == 'nitya' and ct.lower() == 'surat':
            raise serializers.ValidationError("city is not correct !!")
        return data 



# MODELSERIALIZER insted of whole StudentSerializer class write only this
# it gives same result as StudentSerializer class

class StudSerializer(serializers.ModelSerializer):
    #name = serializers.CharField(read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll', 'city']
        #read_only_fields = ['name', 'roll']
        #extra_kwargs = {'name': {'read_only': True}}

    def validate_roll(self, value):
        if value >= 200:
            raise serializers.ValidationError("seats are full !!")
        return value