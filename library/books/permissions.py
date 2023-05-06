from rest_framework.permissions import BasePermission, SAFE_METHODS


class OnlyAuthorizedUserCanChangeBooks(BasePermission):
    """ Изменение информации о книге разрешено только автору. """

    def has_object_permission(self, request, view, obj):
        """ Permission на уровне объекта. """

        if request.method not in SAFE_METHODS:
            verdict = (
                request.user.is_authenticated
                and obj.author.id == request.user.id
            )

            return verdict

        return True
