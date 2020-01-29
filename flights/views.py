from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from datetime import datetime

from .models import Flight, Booking
from .serializers import FlightSerializer, BookingSerializer, BookingDetailsSerializer, UpdateBookingSerializer, RegisterSerializer, AdminUpdateBookingSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .permissions import IsOwner, IsDate


class FlightsList(ListAPIView):
	queryset = Flight.objects.all()
	serializer_class = FlightSerializer


class BookingsList(ListAPIView):
	serializer_class = BookingSerializer

	def get_queryset(self):
		return Booking.objects.filter(user=self.request.user, date__gte=datetime.today())

	permission_classes = [IsAuthenticated ]


class BookingDetails(RetrieveAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingDetailsSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'booking_id'
	permission_classes = [IsOwner, ]


class UpdateBooking(RetrieveUpdateAPIView):
	queryset = Booking.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'booking_id'

	def get_serializer_class(self):
		if self.request.user.is_staff:
			return AdminUpdateBookingSerializer
		else:
			return UpdateBookingSerializer
	permission_classes = [IsOwner, IsDate]


class CancelBooking(DestroyAPIView):
	queryset = Booking.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'booking_id'
	permission_classes = [IsOwner, IsDate]


class BookFlight(CreateAPIView):
	serializer_class = AdminUpdateBookingSerializer

	def perform_create(self, serializer):

		serializer.save(user=self.request.user, flight_id=self.kwargs['flight_id'])

	permission_classes = [IsAuthenticated, ]



class Register(CreateAPIView):
	serializer_class = RegisterSerializer