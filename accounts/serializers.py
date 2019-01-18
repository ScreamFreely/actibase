from rest_framework import serializers

# from django.contrib.auth.models import User
from opencivicdata.core.models import Jurisdiction, Organization
from .models import User, UserJurisdictions, Organizer, ActivistOrgs

############
## Events ##
############

class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)


	class Meta:
		model = User
		fields = ('id', 'username', 'user_type', 'password')


	def create(self, validated_data):
		print(validated_data)
		user = super(UserSerializer, self).create(validated_data)
		user.set_password(validated_data['password'])
		user.save()
		return user
      


class JurisSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserJurisdictions
		fields = ('id', 'activist', 'jurisdiction', 'info_level')


	def create(self, validated_data):
		print('vdt', validated_data)
		userj = super(JurisSerializer, self).create(validated_data)
		userj.save()
		return userj


class MiniJurisSerializer(serializers.ModelSerializer):

	class Meta:
		model = Jurisdiction
		fields = ('id', 'name')


class ProfileJurisSerializer(serializers.ModelSerializer):
	jurisdiction = MiniJurisSerializer()

	class Meta:
		model = UserJurisdictions
		fields = ('id','jurisdiction')
		# depth = 1


class UserProfileSerializer(serializers.ModelSerializer):
	userjurisdictions_set = ProfileJurisSerializer(many=True)


	class Meta:
		model = User
		fields = ('id', 'username', 'user_type', 'email', 'phone_number', 'userjurisdictions_set')
		# depth = 2



class OrganizerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Organizer
		fields = ('id', 'organizer', 'organization', 'admin_level')


	def create(self, validated_data):
		print('vdt', validated_data)
		userj = super(OrganizerSerializer, self).create(validated_data)
		userj.save()
		return userj


class OrgFollowersSerializer(serializers.ModelSerializer):

	class Meta:
		model = ActivistOrgs
		fields = ('id', 'activist', 'organization', 'phone', 'email')

	def create(self, validated_data):
		print('vdt', validated_data)
		userj = super(OrgFollowersSerializer, self).create(validated_data)
		userj.save()
		return userj