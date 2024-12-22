from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from inventory.models import Part, PartStock
from .models import Team, PART_TYPES
from django.contrib import messages
from aircraft.models import AIRCRAFT_CHOICES

@login_required
def list_parts(request):
    team = get_object_or_404(Team, name=request.user.team.name)
    aircraft_type = request.GET.get('aircraft_type', '')
    
    parts = Part.objects.all() if team.responsible_part == 'MONTAJ' else Part.objects.filter(part_type=team.responsible_part)
    
    if aircraft_type:
        parts = parts.filter(aircraft_type=aircraft_type)
    
    # Add mapping dictionary for part types that use Turkish characters
    part_type_mapping = {
        'GÖVDE': 'GOVDE',
        'AVİYONİK': 'AVIYONIK'
    }
    
    # Prepare stock summary data
    stock_summary = {}
    if team.responsible_part == 'MONTAJ':
        for a_type, a_name in AIRCRAFT_CHOICES:
            if not aircraft_type or aircraft_type == a_type:
                stock_summary[a_name] = {}
                for p_type, p_name in PART_TYPES:
                    db_part_type = part_type_mapping.get(p_type, p_type)
                    stock = PartStock.objects.filter(part_type=db_part_type, aircraft_type=a_type).first()
                    stock_summary[a_name][p_name] = stock.quantity if stock else 0
    else:
        # Map the team's responsible parts
        team_part_type = part_type_mapping.get(team.responsible_part, team.responsible_part)
        for p in parts:
            aircraft_name = p.get_aircraft_type_display()
            if aircraft_name not in stock_summary:
                stock_summary[aircraft_name] = {}
                stock = PartStock.objects.filter(
                    part_type=team_part_type,
                    aircraft_type=p.aircraft_type
                ).first()
                stock_summary[aircraft_name][p.get_part_type_display()] = stock.quantity if stock else 0

    context = {
        'parts': parts.order_by('aircraft_type'),
        'stock_summary': stock_summary,
    }
    return render(request, 'teams/parts_list.html', context)

@login_required
def create_part(request):
    team = get_object_or_404(Team, name=request.user.team.name)
    
    if team.responsible_part == 'MONTAJ':
        messages.error(request, "Montaj takımı parça üretemez!")
        return redirect('list_parts')
    
    if request.method == 'POST':
        aircraft_type = request.POST.get('aircraft_type')
        quantity = int(request.POST.get('quantity', 1))
        
        stock, _ = PartStock.objects.get_or_create(
            part_type=team.responsible_part, 
            aircraft_type=aircraft_type
        )
        stock.quantity += quantity
        stock.save()

        from uuid import uuid4
        for i in range(quantity):
            Part.objects.create(
                part_type=team.responsible_part,
                aircraft_type=aircraft_type,
                serial_number=f"{team.responsible_part}-{uuid4().hex[:6]}"
            )

        messages.success(request, f"{team.responsible_part} parçası başarıyla üretildi.")
        return redirect('list_parts')
    
    return render(request, 'teams/create_part.html')

@login_required
def delete_part(request, part_id):
    team = get_object_or_404(Team, name=request.user.team.name)
    part = get_object_or_404(Part, id=part_id)
    
    if team.responsible_part != part.part_type:
        messages.error(request, "Bu parçayı silme yetkiniz yok!")
        return redirect('list_parts')
    
    if part.used_in_aircrafts.exists():
        messages.error(request, "Bu parça bir uçakta kullanıldığı için silinemez!")
        return redirect('list_parts')
    
    stock = PartStock.objects.filter(
        part_type=part.part_type,
        aircraft_type=part.aircraft_type
    ).first()
    if stock and stock.quantity > 0:
        stock.quantity -= 1
        stock.save()
    part.delete()
    messages.success(request, "Parça başarıyla silindi.")
    return redirect('list_parts')
