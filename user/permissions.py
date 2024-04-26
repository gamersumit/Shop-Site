from django_graphene_permissions.permissions import BasePermission

class AdminPermission(BasePermission):

    @staticmethod
    def has_permission(context):
        return context.user and context.user.is_authenticated and context.user.is_superuser

    @staticmethod
    def has_object_permission(context, obj):
        return True