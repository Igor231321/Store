from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q


class EmailOrPhoneNumberAuthlBackend(BaseBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """
    def authenticate(self, request, identifier=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(Q(email=identifier) | Q(phone_number=identifier))
            if user.check_password(password):
                return user

        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
