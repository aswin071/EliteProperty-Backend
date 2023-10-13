from django.urls import path
from .views import (VendorRegistrationApprovalView,BlockUnblockUserView,PublishUnpublishProperty,
AdminTransactionDetails,AdminDashboard)

urlpatterns = [
   path("block-unblock-user/<int:user_id>/", BlockUnblockUserView.as_view(), name="block-unblock-user"),
   path("block-unblock-vendor/<int:user_id>/", BlockUnblockUserView.as_view(), name="block-unblock-vendor"),
   path('vendor/approve/<int:vendor_id>/', VendorRegistrationApprovalView.as_view(), name='approve-registration'),
   path("properties/", PublishUnpublishProperty.as_view(), name="approve-property"),
   path("property/approve/<int:prop_id>/", PublishUnpublishProperty.as_view(), name="approve-property"),
   path("commission-view/", AdminTransactionDetails.as_view(), name="approve-property"),
   path("dashboard/", AdminDashboard.as_view(), name="dashboard"),
]