from rest_framework import serializers


class UserSerializer(serializers.Serializer):
	email = serializers.EmailField()
	username = serializers.CharField(max_length=100)
	first_name = serializers.CharField(max_length=100)
	last_name = serializers.CharField(max_length=100)
	date_joined = serializers.CharField(max_length=100)
	# approved_marketing = serializers.SerializerMethodField()