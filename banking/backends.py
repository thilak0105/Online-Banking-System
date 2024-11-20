from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from banking.models import CustomUser  # Assuming you want to use CustomUser instead of customer_credentials

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, user_id=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(user_id=user_id)  # Fetch the user from CustomUser
            if user.check_password(password):  # Use check_password for hashed passwords
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
