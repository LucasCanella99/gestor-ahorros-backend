from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class ResgisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required= True, validators = [UniqueValidator(queryset=User.objects.all())]) # Revisa la db que no este registrado el mail con otro user
    password = serializers.CharField(required= True, write_only= True) # no va la lenght max pero si la min  para que despues se pueda hashear

    class Meta:
        model = User
        fields = ['id','username','email','password']
        read_only_fields = ['id'] # Esto nose si es necesario especificar

    def create(self,validated_data):
        return User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        ) # aca llamamos y creamos el user, pero como sabe como tomar lo previamente "exigido"? email y password y en el create del model hashea la pass?