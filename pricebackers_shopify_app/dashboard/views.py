from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from dashboard.serializers import UserSerializer


class Profile(APIView):
	authentication_classes = [authentication.TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return Response(UserSerializer(request.user).data)

	def post(self, request):
		user = request.user
		user.first_name = request.data.get("first_name", user.first_name)
		user.last_name = request.data.get("last_name", user.last_name)
		if request.data.get("approved_marketing"):
			user.userinfo.approved_marketing = request.data.get("approved_marketing")
		user.save()
		return Response(UserSerializer(user).data)

	def delete(self, request):
		send_notification_email('user {} requesting to delete his account'.format(request.user))
		# request.user.delete()
		user = request.user
		user.is_active = False
		user.save()
		for account in user.account.socialaccount_set.all():
			account.extra_data['active'] = 'false'
			account.save()
		return Response({'success': True})