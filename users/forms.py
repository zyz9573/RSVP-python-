from django.contrib.auth.forms import UserCreationForm
from .models import user

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = user
        fields = ("username","email")
