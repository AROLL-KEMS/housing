from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path(
        "property/create/",
        views.property_form,
        name="create_property"
    ),# OK

    path(
        "property/<int:pk>/update/",
        views.property_form,
        name="update_property"
    ),# OK

    path(
        "properties/",
        views.property_list,
        name="property_list"
    ),# OK

    path(
    "owner/properties/",
    views.owner_properties,
    name="owner_properties"
    ), # OK
    
    path(
        "property/<int:pk>/",
        views.property_detail,
        name="property_detail"
    ),# OK

    path(
        "property/<int:pk>/delete/",
        views.delete_property,
        name="delete_property"
    ),# OK

    path(
        "property/<int:property_id>/add-image/",
        views.add_property_image,
        name="add_property_image"
    ),# OK

    path(
        "image/<int:image_id>/delete/",
        views.delete_property_image,
        name="delete_property_image"
    ),# OK

    path(
        "reservations/",
        views.manage_reservations,
        name="manage_reservations"
    ), # OK

    path(
        "book/<int:property_id>/",
        views.create_reservation,
        name="create_reservation"
    ),# OK  

    path(
        "profile/",
        views.profile_view,
        name="profile"
    ),

    path("",
        views.dashboard,
        name="dashboard"
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)