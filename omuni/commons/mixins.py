from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin


class UserDataObjectMixin(SingleObjectMixin):
    """Returns a data object only if it belongs to the request user.

    This mixin is only for use with objects that have a foreign key to User.
    """
    def get_object(self, queryset=None, castable=True):
        obj = super(UserDataObjectMixin, self).get_object(queryset)
        if obj.user_id != self.request.user.id:
            raise PermissionDenied

        return obj
