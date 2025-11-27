from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Administrateur'),
        ('agent_ec', 'Agent État Civil'),
        ('responsable_admin', 'Responsable Administratif'),
        ('agent_finances', 'Agent Financier'),
        ('citoyen', 'Citoyen'),
        ('chef_service', 'Chef de Service'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to='photos_users/', blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.get_role_display()})"

    def is_superadmin(self):
        return self.role == 'superadmin'
    
    def is_agent_ec(self):
        return self.role == 'agent_ec'

    def is_responsable_admin(self):
        return self.role == 'responsable_admin'

    def is_agent_finances(self):
        return self.role == 'agent_finances'

    def is_citoyen(self):
        return self.role == 'citoyen'

    def is_chef_service(self):
        return self.role == 'chef_service'
