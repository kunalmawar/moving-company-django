from django.urls import path, include, re_path
from booking.views import booking_index, FindCompany, CompanyScheduleView, CreateBookingView


urlpatterns = [
    # Booking Home page
    re_path(r'^$', booking_index, name='booking-index'),
    re_path(r'^find_companies/$', FindCompany.as_view(), name='submit-query'),
    re_path(r'^company_schedule/(?P<company_id>[0-9]+)/$', CompanyScheduleView.as_view(), name='company-schedule'),
    re_path(r'^confirm_booking/$', CreateBookingView.as_view(), name='confirm-booking'),
]