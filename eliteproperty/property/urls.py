from django.urls import path
from .views import (AddPropertyView,SinglePropertyView)

urlpatterns = [
    path("add-property/", AddPropertyView.as_view(), name="add-property"),
    path("view-property/", AddPropertyView.as_view(), name="view-property"),
    path("singleproperty/<int:id>/", SinglePropertyView.as_view(), name="'single-property'"),
    
]
