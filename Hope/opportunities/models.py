from django.db import models
from accounts.models import VolunteerProfile
from organizations.models import Opportunity

class Application(models.Model):
    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name="applications")
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="applications")
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.volunteer.full_name} applied for {self.opportunity.name}"

    class Meta:
        unique_together = ("volunteer", "opportunity") 
