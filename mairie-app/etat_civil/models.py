from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from etat_civil.numero_utils import generer_numero


User = get_user_model()

class ActeNaissance(models.Model):
    numero = models.CharField(max_length=20, blank=True)  # permet blank=True pour générer automatiquement
    annee = models.IntegerField()
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10, choices=[("M", "Masculin"), ("F", "Féminin")])
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=150)

    nom_mere = models.CharField(max_length=100)
    nom_pere = models.CharField(max_length=100, blank=True, null=True)

    declarant = models.CharField(max_length=100)

    statut = models.CharField(
        max_length=20,
        choices=[("En attente", "En attente"), ("Validé", "Validé"), ("Refusé", "Refusé")],
        default="En attente"
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    validated_by = models.ForeignKey(User, related_name="validateur", on_delete=models.SET_NULL, null=True, blank=True)

    pdf = models.FileField(upload_to="actes/naissances/pdf/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    code_verification = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['-created_at']
    @property
    def type_document(self):
        if hasattr(self, 'type_certificat'):
            return f"Certificat de {self.type_certificat}"
        if isinstance(self, ActeNaissance):
            return "Acte de Naissance"
        if isinstance(self, ActeDeces):
            return "Acte de Décès"
        if isinstance(self, ActeMariage):
            return "Acte de Mariage"
    def __str__(self):
        return f"{self.numero}/{self.annee} - {self.nom} {self.prenom}"

    def save(self, *args, **kwargs):
        if not self.numero:  # Générer le numéro uniquement si inexistant
            self.numero = generer_numero("naissance")
        super().save(*args, **kwargs)
        
class ActeMariage(models.Model):
    numero = models.CharField(max_length=20, unique=True, blank=True, null=True)
    annee = models.IntegerField()

    epoux_nom = models.CharField(max_length=100)
    epoux_prenom = models.CharField(max_length=100)
    epouse_nom = models.CharField(max_length=100)
    epouse_prenom = models.CharField(max_length=100)

    date_mariage = models.DateField()
    lieu_mariage = models.CharField(max_length=150)

    temoins = models.TextField(blank=True)  # JSON/text list possible
    officier = models.CharField(max_length=150, blank=True)

    statut = models.CharField(
        max_length=20,
        choices=[("En attente","En attente"), ("Validé","Validé"), ("Refusé","Refusé")],
        default="En attente"
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="mariage_created")
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="mariage_validated")

    pdf = models.FileField(upload_to="actes/mariage/pdf/", blank=True, null=True)
    qr_code = models.ImageField(upload_to="actes/mariage/qr/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
    @property
    def type_document(self):
        if hasattr(self, 'type_certificat'):
            return f"Certificat de {self.type_certificat}"
        if isinstance(self, ActeNaissance):
            return "Acte de Naissance"
        if isinstance(self, ActeDeces):
            return "Acte de Décès"
        if isinstance(self, ActeMariage):
            return "Acte de Mariage"
    def __str__(self):
        return f"{self.numero or '—'}/{self.annee} — {self.epoux_nom} & {self.epouse_nom}"

    def save(self, *args, **kwargs):
        # numérotation automatique simple : incrément sur l'année
        if not self.numero:
            last = ActeMariage.objects.filter(annee=self.annee).order_by("id").last()
            if last and last.numero and last.numero.isdigit():
                try:
                    new_num = int(last.numero) + 1
                except:
                    new_num = 1
            else:
                new_num = 1
            self.numero = str(new_num)
        super().save(*args, **kwargs)


class ActeDeces(models.Model):
    numero = models.CharField(max_length=20, unique=True, blank=True, null=True)
    annee = models.IntegerField()

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10, choices=[("M","Masculin"), ("F","Féminin")])

    date_deces = models.DateField()
    lieu_deces = models.CharField(max_length=150)
    cause_deces = models.CharField(max_length=200, blank=True, null=True)

    declarant = models.CharField(max_length=150, blank=True, null=True)

    statut = models.CharField(
        max_length=20,
        choices=[("En attente","En attente"), ("Validé","Validé"), ("Refusé","Refusé")],
        default="En attente"
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="deces_created")
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="deces_validated")

    pdf = models.FileField(upload_to="actes/deces/pdf/", blank=True, null=True)
    qr_code = models.ImageField(upload_to="actes/deces/qr/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code_verification = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ["-created_at"]
    @property
    def type_document(self):
        if hasattr(self, 'type_certificat'):
            return f"Certificat de {self.type_certificat}"
        if isinstance(self, ActeNaissance):
            return "Acte de Naissance"
        if isinstance(self, ActeDeces):
            return "Acte de Décès"
        if isinstance(self, ActeMariage):
            return "Acte de Mariage"
    def __str__(self):
        return f"{self.numero or '—'}/{self.annee} — {self.nom} {self.prenom}"
 
    def save(self, *args, **kwargs):
 
        # numérotation automatique simple par année si non défini
        if not self.numero:
            last = ActeDeces.objects.filter(annee=self.annee).order_by("id").last()
            if last and last.numero and last.numero.isdigit():
                try:
                    new_num = int(last.numero) + 1
                except:
                    new_num = 1
            else:
                new_num = 1
            self.numero = str(new_num)
        super().save(*args, **kwargs)
 
class Certificat(models.Model):
    TYPES = [
        ("residence", "Certificat de résidence"),
        ("celibat", "Certificat de célibat"),
        ("mariage", "Certificat de mariage"),
        ("hebergement", "Certificat d'hébergement"),
        ("vie_individuelle", "Attestation de vie individuelle"),
    ]

    type_certificat = models.CharField(max_length=30, choices=TYPES)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100) 
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)  # optionnel selon type
    adresse = models.CharField(max_length=255, blank=True, null=True)
    motif = models.TextField(blank=True, null=True)  # info complémentaire
    numero = models.CharField(max_length=20, unique=True, blank=True, null=True)
    statut = models.CharField(
        max_length=20,
        choices=[("En attente","En attente"), ("Validé","Validé"), ("Refusé","Refusé")],
        default="En attente"
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="cert_created")
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="cert_validated")
    code_verification = models.CharField(max_length=20, unique=True)

    pdf = models.FileField(upload_to="certificats/pdf/", blank=True, null=True)
    qr_code = models.ImageField(upload_to="certificats/qr/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
    @property
    def type_document(self):
        if hasattr(self, 'type_certificat'):
            return f"Certificat de {self.type_certificat}"
        if isinstance(self, ActeNaissance):
            return "Acte de Naissance"
        if isinstance(self, ActeDeces):
            return "Acte de Décès"
        if isinstance(self, ActeMariage):
            return "Acte de Mariage"
    def __str__(self):
        return f"{self.get_type_certificat_display()} — {self.nom} {self.prenom} ({self.id})"
    def save(self, *args, **kwargs):
        if not self.numero:  # uniquement si le numéro n’existe pas
            from .utils import generer_numero  # import à l'intérieur
        self.numero = generer_numero()     # <-- correctement indenté
        super().save(*args, **kwargs)          # <-- toujours au même niveau que le if


class HistoriqueEtatCivil(models.Model):
    ACTE_TYPES = [
        ("naissance","Naissance"),
        ("mariage","Mariage"),
        ("deces","Décès"),
        ("certificat","Certificat"),
    ]
    acte_type = models.CharField(max_length=20, choices=ACTE_TYPES)
    acte_id = models.IntegerField()
    action = models.CharField(max_length=100)  # e.g. "Création", "Modification", "Validation", "Suppression"
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    details = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    code_verification = models.CharField(max_length=20)  # plus de unique=True

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.get_acte_type_display()} #{self.acte_id} — {self.action} par {self.user}"


# etat_civil/models.py
class Registre(models.Model):
    ACTE_TYPES = [
        ("naissance", "Acte de Naissance"),
        ("mariage", "Acte de Mariage"),
        ("deces", "Acte de Décès"),
        ("certificat", "Certificat"),
    ]

    type_acte = models.CharField(max_length=20, choices=ACTE_TYPES)
    annee = models.IntegerField()
    dernier_numero = models.IntegerField(default=0)
    code_verification = models.CharField(max_length=20, unique=True)

    class Meta:
        unique_together = ("type_acte", "annee")

    def __str__(self):
        return f"{self.type_acte} - {self.annee} : {self.dernier_numero}"


class HistoriqueVerification(models.Model):
    code = models.CharField(max_length=20)
    type_document = models.CharField(max_length=50)
    resultat = models.BooleanField(default=False)  # trouvé ou non
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.type_document} - {'OK' if self.resultat else 'Non trouvé'}"




class ParametreMairie(models.Model):
    nom_mairie = models.CharField(max_length=200)
    nom_maire = models.CharField(max_length=150)
    commune = models.CharField(max_length=100)
    departement = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    adresse = models.CharField(max_length=250, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    site_web = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="mairie/logo/", blank=True, null=True)
    slogan = models.CharField(max_length=250, blank=True, null=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom_mairie