from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsRideOfferAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.driver == request.user
      
class IsRideOfferOwner(BasePermission):
    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return (
            obj.ride_offer.driver
            == request.user
        )