from django.db import models
from django.utils import timezone

class Annonce(models.Model):
    STATUTS = [
        ("brouillon", "Brouillon"),
        ("publie", "Publié"),
        ("archive", "Archivé"),
    ]

    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    date_publication = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default="brouillon")
    fichier_pdf = models.FileField(upload_to="annonces_pdfs/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def publier(self):
        self.statut = "publie"
        self.date_publication = timezone.now()
        self.save()

    def archiver(self):
        self.statut = "archive"
        self.save()

    def restaurer(self):
        self.statut = "brouillon"
        self.save()

    def __str__(self):
        return self.titre
