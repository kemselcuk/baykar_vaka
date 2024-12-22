from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProducedAircraft, AIRCRAFT_CHOICES
from inventory.models import Part, UsedPart, PartStock, PART_TYPES
from teams.models import Team
import json

@login_required
def assemble_aircraft(request):
    team = get_object_or_404(Team, name=request.user.team.name)
    
    if team.responsible_part != 'MONTAJ':
        messages.error(request, "Sadece montaj takımı uçak üretebilir!")
        return redirect('list_parts')
    
    if request.method == 'GET':
        from django.core import serializers
        stock_data = {}
        for a_type, _ in AIRCRAFT_CHOICES:
            stock_data[a_type] = {}
            for p_type, _ in PART_TYPES:
                stock = PartStock.objects.filter(aircraft_type=a_type, part_type=p_type).first()
                stock_data[a_type][p_type] = stock.quantity if stock else 0
        return render(request, 'aircraft/assemble.html', {
            'stock_json': json.dumps(stock_data),
        })

    if request.method == 'POST':
        aircraft_type = request.POST.get('aircraft_type')
        kanat_qty = int(request.POST.get('kanat_qty', 0))
        govde_qty = int(request.POST.get('govde_qty', 0))
        kuyruk_qty = int(request.POST.get('kuyruk_qty', 0))
        aviyonik_qty = int(request.POST.get('aviyonik_qty', 0))
        if min(kanat_qty, govde_qty, kuyruk_qty, aviyonik_qty) < 1:
            messages.error(request, "Her parçadan en az bir adet seçilmelidir.")
            return redirect('assemble_aircraft')
        try:
            required_parts = [
                ('KANAT', kanat_qty),
                ('GOVDE', govde_qty),
                ('KUYRUK', kuyruk_qty),
                ('AVIYONIK', aviyonik_qty),
            ]
            for p_type, qty in required_parts:
                stock = PartStock.objects.get(part_type=p_type, aircraft_type=aircraft_type)
                if stock.quantity < qty:
                    raise ValueError(f"Yetersiz stok: {p_type}")
            aircraft = ProducedAircraft.objects.create(aircraft_type=aircraft_type)
            for p_type, qty in required_parts:
                parts_needed = Part.objects.filter(part_type=p_type, aircraft_type=aircraft_type, used_in_aircrafts__isnull=True)[:qty]
                for p in parts_needed:
                    UsedPart.objects.create(produced_aircraft=aircraft, part=p, used_quantity=1)
            messages.success(request, f"{aircraft_type} başarıyla üretildi!")
            return redirect('list_aircraft')
        except (Part.DoesNotExist, ValueError) as e:
            messages.error(request, str(e))
            return redirect('assemble_aircraft')
    
    return render(request, 'aircraft/assemble.html')

@login_required
def list_aircraft(request):
    team = get_object_or_404(Team, name=request.user.team.name)
    if team.responsible_part != 'MONTAJ':
        messages.error(request, "Sadece montaj takımı uçakları görüntüleyebilir!")
        return redirect('list_parts')
    aircraft_list = ProducedAircraft.objects.all().order_by('-creation_date')
    for aircraft in aircraft_list:
        parts_summary = {}
        from django.db.models import Sum
        used_parts = aircraft.used_parts.values(
            'part__part_type'
        ).annotate(
            total_quantity=Sum('used_quantity')
        )
        for part in used_parts:
            part_type = dict(PART_TYPES)[part['part__part_type']]
            parts_summary[part_type] = part['total_quantity']
        aircraft.parts_summary = parts_summary
    return render(request, 'aircraft/list.html', {'aircraft': aircraft_list})

@login_required
def aircraft_details(request, aircraft_id):
    team = get_object_or_404(Team, name=request.user.team.name)
    if team.responsible_part != 'MONTAJ':
        messages.error(request, "Sadece montaj takımı uçakları görüntüleyebilir!")
        return redirect('list_parts')
    
    aircraft = get_object_or_404(ProducedAircraft, id=aircraft_id)
    used_parts = aircraft.used_parts.all().select_related('part')
    
    return render(request, 'aircraft/details.html', {
        'aircraft': aircraft,
        'used_parts': used_parts
    })
