from django.db import models
from encrypted_model_fields.fields import EncryptedCharField
from users.models import CustomUser

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id_number = EncryptedCharField(max_length=20)
    insurance_number = EncryptedCharField(max_length=20)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.get_full_name()