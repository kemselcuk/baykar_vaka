from django.urls import path
from .views import assemble_aircraft, list_aircraft , aircraft_details 

urlpatterns = [
    path('assemble/', assemble_aircraft, name='assemble_aircraft'),
    path('list/', list_aircraft, name='list_aircraft'),
    path('aircraft/<int:aircraft_id>/details/', aircraft_details, name='aircraft_details'),
]