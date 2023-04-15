from rest_framework import permissions

from Jobstler.jobstler_main.models import UserAccount


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        user_account = UserAccount.objects.get(user_owner=request.user)
        print(obj.user_owner_id, user_account.user_owner_id)
        return obj.user_owner_id == user_account.user_owner_id
