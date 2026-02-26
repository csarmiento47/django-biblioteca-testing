from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class AuthRequiredMixin(LoginRequiredMixin):
    login_url = 'login'

class EditRequiredMixin(PermissionRequiredMixin):
    permission_required = [
        'core.add_libro',
        'core.change_libro'
    ]

class AdminRequiredMixin(PermissionRequiredMixin):
    permission_required = [
        'core.add_libro',
        'core.change_libro',
        'core.delete_libro'
    ]