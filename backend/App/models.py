from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings

# Create your models here.


class CandidateRegistration(models.Model):
    candidate_id = models.IntegerField(unique=True, editable=False, null=True)  # Allow null initially
    name = models.CharField(max_length=255)
    party = models.CharField(max_length=255)
    age = models.IntegerField()
    bio = models.TextField()
    photo = models.ImageField(upload_to="candidate_photos/", blank=False, null=False)
    election_position = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    election_sign = models.ImageField(upload_to="election_sign/", blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.candidate_id is None:  # Assign candidate_id only if it's missing
            last_candidate = CandidateRegistration.objects.order_by('-candidate_id').first()
            self.candidate_id = 1 if not last_candidate else last_candidate.candidate_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.candidate_id} - {self.name}"




class Voter(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="voter_profile")
    voter_id = models.CharField(max_length=100, unique=True , default="none")  
    created_at = models.DateTimeField(auto_now_add=True)
    is_voted = models.BooleanField(default=False)  



class EthereumAccount(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relationship stays
    eth_private_key = models.CharField(max_length=255)
    eth_address = models.CharField(max_length=42, unique=True)
