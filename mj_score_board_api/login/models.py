from django.db import models
from django.db import transaction

class UserManager(models.Manager):
    @transaction.atomic
    def create(self, email):
        email = self.normalize_email(email=email)
        user = self.model(mail_address=email)
        user.save()
        return user

    def is_valid_email(self, email):
        email = self.normalize_email(email=email)
        return self.model.objects.all().filter(mail_address=email).exists()

    def normalize_email(self, email):
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email

class User(models.Model):
    mail_address = models.EmailField(unique=True)
    objects = UserManager()
