from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        resource = getattr(view, 'basename', None)

        if resource not in ['user', 'role', 'product', 'order']:
            return False

        user = request.user
        role = user.role

        method = request.method
        if method == 'GET':
            # Мне лень делать отдельные поля в ролях под псевдобизнес
            return role.get

        if method == 'POST':
            if resource == 'user':
                return role.postusers
            elif resource == 'role':
                return role.postroles
            # Мне лень делать отдельные поля в ролях под псевдобизнес
            elif resource == 'product':
                return role.postusers
            elif resource == 'order':
                return role.postroles

        if method == 'DELETE':
            if resource == 'user':
                return role.delete
            elif resource == 'role':
                return role.delete
            elif resource == 'product':
                return role.delete
            elif resource == 'order':
                return role.delete
        return True