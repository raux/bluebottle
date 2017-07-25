from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'parent'):
            obj = obj.parent

        return self.check_object_permission(
            request.method, request.user, view, obj
        )

    def has_permission(self, request, view, obj=None):
        if obj and hasattr(obj, 'parent'):
            obj = obj.parent

        return self.check_permission(
            request.method, request.user, view, obj
        )

    def check_object_permission(self, method, user, view, obj):
        """ Check if user has permission to access method on obj for the view

        Used by both the DRF permission system and for returning permissions to the user
        """
        raise NotImplementedError('check_object_permission() must be implemented')

    def check_permission(self, method, user, view, obj=None):
        """ Check if user has permission to access method for the view

        Used by both the DRF permission system and for returning permissions to the user
        """
        raise NotImplementedError('check_permission() must be implemented')


class IsUser(BasePermission):
    pass


class IsOwner(BasePermission):
    """
    Allows access only to obj owner.
    """

    owner_field = 'owner'

    def get_parent_from_request(self, request):
        """ For requests to list endpoints, eg when creating an object then
        get_parent needs to be defined to use this permission class

        """
        raise NotImplementedError('get_parent_from_request() must be implemented')

    def get_owner(self, obj):
        return getattr(obj, self.owner_field, None)

    def check_object_permission(self, method, user, view, obj):
        """ If the object has a parent then the user needs to be the
        owner of the parent object
        """
        if hasattr(obj, 'parent'):
            obj = obj.parent

        return user == self.get_owner(obj)

    def has_permission(self, request, view):
        try:
            obj = view.get_object()
        except AssertionError:
            obj = None

        if obj and hasattr(obj, 'parent'):
            obj = obj.parent
        else:
            # Get the obj (parent) from the request
            obj = self.get_parent_from_request(request)

        print("IsOwner::has_permission > ", obj)
        # If we don't have an obj then don't complain.
        if not obj:
            return True

        return request.user == self.get_owner(obj)


class ResourcePermissions(BasePermission, permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.api_read_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.api_add_%(model_name)s'],
        'PUT': ['%(app_label)s.api_change_%(model_name)s'],
        'PATCH': ['%(app_label)s.api_change_%(model_name)s'],
        'DELETE': ['%(app_label)s.api_delete_%(model_name)s'],
    }

    def check_permission(self, method, user, view, obj=None):
        queryset = None
        if hasattr(view, 'queryset'):
            queryset = view.queryset
        elif hasattr(view, 'get_queryset'):
            queryset = view.get_queryset()

        assert queryset is not None, (
            'Cannot apply DjangoModelPermissions on a view that '
            'does not set `.queryset` or have a `.get_queryset()` method.'
        )

        perms = self.get_required_permissions(method, queryset.model)
        print("ResourcePermissions::check_permission > ", perms)
        return user.has_perms(perms)

    def check_object_permission(self, method, user, view, obj=None):
        return self.check_permission(method, user, view)
