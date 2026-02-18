from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):

        if not username or not password:
            return None

        # Admin sends username field, even if it's email
        try:
            user = User.objects.get(email__iexact=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and user.is_staff and user.is_active:
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
