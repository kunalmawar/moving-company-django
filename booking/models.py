from django.db import models
from django.contrib.gis.db import models as gis_models


DAYS = (
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday')
)


class Company(models.Model):
    name = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=30)
    license_no = models.CharField(max_length=100)
    position = gis_models.PointField(null=True, blank=True)
    active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CompanyAvailability(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    day = models.PositiveIntegerField(choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s: %s (%s-%s)' % (self.company.name, DAYS[self.day-1][1], self.start_time, self.end_time)

    class Meta:
        ordering = ['company']


class Booking(models.Model):
    email = models.CharField(max_length=200, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    source_position = gis_models.PointField(null=True, blank=True)
    source_name = models.CharField(max_length=255, null=True, blank=True)
    destination_position = gis_models.PointField(null=True, blank=True)
    destination_name = models.CharField(max_length=255, null=True, blank=True)
    booked_for_datetime = models.DateTimeField()
    booking_confirmed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Booking of %s, Company: %s. Source: %s' % (self.email, self.company.name, self.source_name)