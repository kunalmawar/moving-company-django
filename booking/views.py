from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from django.views.generic.base import TemplateView
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from booking.models import Company, CompanyAvailability
from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from booking.models import Booking
from django.core.mail import EmailMessage
from dateutil import parser


def booking_index(request):
    context = dict()
    context['GOOGLE_MAP_API_KEY'] = settings.MAP_WIDGETS['GOOGLE_MAP_API_KEY']
    template = loader.get_template('booking/index.html')
    return HttpResponse(template.render(context, request))


class FindCompany(APIView):

    def post(self, request):
        lng = request.POST.get('lng', '')
        lat = request.POST.get('lat', '')
        query_date = request.POST.get('query_date', '')
        ref_location = Point(float(lng), float(lat), srid=4326)
        companies = Company.objects.filter(position__distance_lte=(ref_location, D(km=1000))).annotate(
            distance=Distance("position", ref_location)).order_by("distance")
        company_data = [{'name': c.name, 'contact_no': c.contact_no, 'license_no': c.license_no, 'rating': c.rating,
                         'schedule_link': '<a href="/booking/company_schedule/%s/?date=%s" >Check Schedule</a>' %
                                          (c.id, query_date)} for c in companies]
        if company_data:
            return JsonResponse({'status': 'success', 'msg': '', 'company_data': company_data})
        else:
            return JsonResponse({'status': 'failed', 'msg': 'No nearby company found'})


class CompanyScheduleView(TemplateView):
    template_name = 'booking/calendar.html'

    def get(self, request, company_id, *args, **kwargs):
        context = dict()
        query_date = request.GET.get('date')
        company = Company.objects.filter(id=company_id)
        if company:
            company = company[0]
            comp_aval = CompanyAvailability.objects.filter(company=company)
            business_hours_helper = {}
            business_hours = []
            for ce in comp_aval:
                business_hours.append({'start': str(ce.start_time)[:-3], 'end': str(ce.end_time)[:-3], 'dow': [ce.day]})
                business_hours_helper[ce.day] = [str(ce.start_time)[:-3], str(ce.end_time)[:-3]]
            context['business_hours'] = business_hours
            context['business_hours_helper'] = business_hours_helper
        context['company_id'] = company_id
        context['query_date'] = query_date
        return self.render_to_response(context)


class CreateBookingView(APIView):

    def post(self, request):
        booking_datetime = request.POST.get('booking_datetime')
        email = request.POST.get('email')
        company_id = request.POST.get('company_id')
        company = Company.objects.get(id=company_id)
        dt = parser.parse(booking_datetime + ':00')
        booking = Booking.objects.create(email=email, company=company, booked_for_datetime=dt)
        try:
            subject = 'Booking from %s' % company.name
            body = 'Congratulations! Your booking is confirmed for %s by %s' % (booking_datetime, company.name)
            email = EmailMessage(subject, body, to=[email])
            email.send()
            booking.booking_confirmed = True
            booking.save()
            return JsonResponse({'status': 'success', 'msg': 'Booking done'})
        except:
            return JsonResponse({'status': 'failed', 'msg': 'Email failed'})