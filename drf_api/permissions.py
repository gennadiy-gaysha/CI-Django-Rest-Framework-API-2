from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    # The method checks if the request's HTTP method is in permissions.SAFE_METHODS
    # (which includes GET, HEAD, and OPTIONS methods). These methods are considered
    # "safe" because they don't modify data.
    # If the request method is safe, the method returns True, allowing the request
    # to proceed. This means any user can view or retrieve the Profile data.
    if request.method in permissions.SAFE_METHODS:
      return True
    # If the request method is not a safe method (meaning it's a method that modifies
    # data, like POST, PUT, PATCH, DELETE), the method checks if the Profile
    # instance's owner is the same as the request.user (the user making the request).
    # If obj.owner is equal to request.user, it returns True, allowing the request to
    # proceed. This means the owner of the Profile can modify it.
    # If they are not the same, it returns False, denying the request.
    return obj.owner == request.user