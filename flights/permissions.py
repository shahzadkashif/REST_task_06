from rest_framework.permissions import BasePermission
from datetime import date, timedelta

class IsOwner(BasePermission):
	message = "You must be the passenger!"

	def has_object_permission(self, request, view, obj):
		if request.user.is_staff or (obj.user == request.user):
			return True
		else:
			return False

class IsDate(BasePermission):
	message = "You can't modify unless you booked it more than 3 days!"

	def has_object_permission(self, request, view, obj):
		if obj.date > (date.today() + timedelta(days=3)):
			return True
		else:
			return False 