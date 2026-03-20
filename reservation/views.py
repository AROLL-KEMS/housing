from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from .forms import *

#=============== MAKE A RESERVATION START ==================#
@login_required
def create_reservation(request, property_id):

    property = get_object_or_404(Property, id=property_id)

    if request.user == property.owner:
        return redirect("property_list")

    if request.method == "POST":

        form = ReservationForm(request.POST)

        if form.is_valid():

            reservation = form.save(commit=False)

            reservation.property = property
            reservation.seeker = request.user

            reservation.save()

            return redirect("manage_reservations")

    else:

        form = ReservationForm()

    return render(
        request,
        "reservation/create_reservation.html",
        {
            "form": form,
            "property": property
        }
    )
#=============== MAKE A RESERVATION END ==================#

#=============== MANAGE RESERVEATIONS START ==================#
@login_required
def manage_reservations(request):

    # Get reservations where user is seeker OR property owner
    reservations = Reservation.objects.filter(
        Q(seeker=request.user) |
        Q(property__owner=request.user)
    ).select_related("property", "seeker", "property__owner")

    # Handle owner actions
    if request.method == "POST":

        reservation_id = request.POST.get("reservation_id")
        action = request.POST.get("action")

        reservation = get_object_or_404(Reservation, id=reservation_id)

        # SECURITY: Only owner of the property can update
        if reservation.property.owner == request.user:

            if reservation.status == "PENDING":

                if action == "approve":
                    reservation.status = "APPROVED"

                elif action == "reject":
                    reservation.status = "REJECTED"

                reservation.save()

        return redirect("manage_reservations")

    return render(
        request,
        "reservation/reservation_list.html",
        {
            "reservations": reservations
        }
    )
#=============== MANAGE RESERVEATIONS END ==================#

#=============== PUBLIC PROPERTY LIST START ==================#
def property_list(request):

    properties = Property.objects.all()

    return render(
        request,
        "reservation/property.html",
        {"properties": properties}
    )
#=============== PUBLIC PROPERTY LIST END ==================#

#=============== PRIVATE PROPERTY LIST START ==================#
def owner_properties(request):

    properties = Property.objects.filter(owner=request.user)

    return render(
        request,
        "reservation/owner_properties.html",
        {"properties": properties}
    )
#=============== PRIVATE PROPERTY LIST END ==================#

#=============== ADD PROPERTY IMAGE START ==================#
def add_property_image(request, property_id):
    if request.user.role == "SEEKER":
        return redirect('property_list')
    property = get_object_or_404(Property, id=property_id)

    if request.method == "POST":

        image = request.FILES.get("image")

        PropertyImage.objects.create(
            property=property,
            image=image
        )

    return redirect("property_detail", property_id)
#=============== ADD PROPERTY IMAGE END ==================#

#=============== DELETE PROPERTY IMAGE END ==================#
@login_required
def delete_property_image(request, image_id):
    if request.user.role == "SEEKER":
        return redirect('property_list')
    image = get_object_or_404(PropertyImage, id=image_id, property__owner = request.user)

    property_id = image.property.id

    image.delete()

    return redirect("property_detail", pk=property_id)
#=============== DELETE PROPERTY IMAGE END ==================#

#=============== ADD AND EDIT PROPERTY START ==================#
@login_required
def property_form(request, pk=None):

    if pk:
        property = get_object_or_404(Property, pk=pk, owner=request.user)
    else:
        property = None

    if request.method == "POST":

        form = PropertyForm(request.POST,
            request.FILES,
            instance=property)

        if form.is_valid():

            property = form.save(commit=False)
            property.owner = request.user
            property.save()

            return redirect("owner_properties")

    else:

        form = PropertyForm(instance=property)

    return render(
        request,
        "reservation/property_form.html",
        {
            "form": form,
            "property": property
        }
    )
#=============== ADD AND EDIT PROPERTY END ==================#

#=============== DELETE PROPERTY START ==================#
@login_required
def delete_property(request, pk):

    if request.user.role == "SEEKER":
        return redirect('property_list')
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    property.delete()
    return redirect("owner_properties")
#=============== DELETE PROPERTY END ==================#

#=============== DETAIL PROPERTY START ==================#
@login_required
def property_detail(request, pk):

    property = get_object_or_404(Property, pk=pk)

    images = PropertyImage.objects.filter(property=property)

    context = {
        "property": property,
        "images": images
    }

    return render(
        request,
        "reservation/property_detail.html",
        context
    )
#=============== DETAIL PROPERTY END ==================#

#=============== MANAGE PROFILE START ==================#
@login_required
def profile_view(request):

    user = request.user

    if request.method == "POST":

        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=user
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:

        form = ProfileUpdateForm(instance=user)

    return render(
        request,
        "reservation/profile.html",
        {
            "form": form
        }
    )
#=============== MANAGE PROFILE END ==================#
@login_required
def dashboard(request):

    user = request.user

    # ===== OWNER DATA =====
    properties = Property.objects.filter(owner=user)

    owner_reservations = Reservation.objects.filter(
        property__owner=user
    )

    pending_reservations = owner_reservations.filter(
        status="PENDING"
    ).count()

    # ===== SEEKER DATA =====
    seeker_reservations = Reservation.objects.filter(
        seeker=user
    )

    approved_reservations = seeker_reservations.filter(
        status="APPROVED"
    ).count()

    context = {

        # OWNER DATA
        "properties_count": properties.count(),
        "owner_reservations_count": owner_reservations.count(),
        "pending_reservations": pending_reservations,
        "properties": properties[:5],
        "owner_reservations": owner_reservations[:5],

        # SEEKER DATA
        "seeker_reservations_count": seeker_reservations.count(),
        "approved_reservations": approved_reservations,
        "seeker_reservations": seeker_reservations[:5],

        # Useful flag
        "is_owner": properties.exists(),

    }

    return render(
        request,
        "reservation/dashboard.html",
        context
    )