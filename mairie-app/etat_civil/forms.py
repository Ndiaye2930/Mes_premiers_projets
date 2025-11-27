from django import forms
from .models import ActeNaissance, ActeMariage, ActeDeces, Certificat, ParametreMairie


class ParametreMairieForm(forms.ModelForm):
    class Meta:
        model = ParametreMairie
        fields = [
            "nom_mairie", "nom_maire", "commune", "departement", "region",
            "adresse", "telephone", "email", "site_web", "logo", "slogan"
        ]
        widgets = {
            # Tous les champs de texte/URL/Email reçoivent la classe form-control
            "nom_mairie": forms.TextInput(attrs={"class": "form-control"}),
            "nom_maire": forms.TextInput(attrs={"class": "form-control"}),
            "commune": forms.TextInput(attrs={"class": "form-control"}),
            "departement": forms.TextInput(attrs={"class": "form-control"}),
            "region": forms.TextInput(attrs={"class": "form-control"}),
            "adresse": forms.TextInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "site_web": forms.URLInput(attrs={"class": "form-control"}),
            "slogan": forms.TextInput(attrs={"class": "form-control"}),
            # Le champ 'logo' est géré par Django par défaut, souvent un FileInput.
        }


class CertificatForm(forms.ModelForm):
    class Meta:
        model = Certificat
        fields = [
            "type_certificat",
            "nom",
            "prenom",
            "email",
            "telephone",
            "date_naissance",
            "adresse",
            "motif",
            "statut",
        ]
        widgets = {
            # Ajout de form-control à tous les champs de texte/saisie
            "type_certificat": forms.Select(attrs={"class": "form-select"}), # Utiliser form-select pour les Selects
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "adresse": forms.TextInput(attrs={"class": "form-control"}),
            "statut": forms.Select(attrs={"class": "form-select"}),
            
            "date_naissance": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "motif": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }

class ActeDecesForm(forms.ModelForm):
    class Meta:
        model = ActeDeces
        fields = [
            "annee",
            "nom", "prenom", "sexe",
            "date_deces", "lieu_deces", "cause_deces",
            "declarant", "statut"
        ]
        widgets = {
            # Ajout de form-control/form-select
            "annee": forms.NumberInput(attrs={"class": "form-control"}),
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "sexe": forms.Select(attrs={"class": "form-select"}),
            "lieu_deces": forms.TextInput(attrs={"class": "form-control"}),
            "declarant": forms.TextInput(attrs={"class": "form-control"}),
            "statut": forms.Select(attrs={"class": "form-select"}),
            
            "date_deces": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "cause_deces": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }

class ActeMariageForm(forms.ModelForm):
    class Meta:
        model = ActeMariage
        fields = [
            "annee",
            "epoux_nom", "epoux_prenom",
            "epouse_nom", "epouse_prenom",
            "date_mariage", "lieu_mariage",
            "temoins", "officier",
            "statut",
        ]
        widgets = {
            # Ajout de form-control/form-select
            "annee": forms.NumberInput(attrs={"class": "form-control"}),
            "epoux_nom": forms.TextInput(attrs={"class": "form-control"}),
            "epoux_prenom": forms.TextInput(attrs={"class": "form-control"}),
            "epouse_nom": forms.TextInput(attrs={"class": "form-control"}),
            "epouse_prenom": forms.TextInput(attrs={"class": "form-control"}),
            "lieu_mariage": forms.TextInput(attrs={"class": "form-control"}),
            "officier": forms.TextInput(attrs={"class": "form-control"}),
            "statut": forms.Select(attrs={"class": "form-select"}),
            
            "date_mariage": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "temoins": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }

class ActeNaissanceForm(forms.ModelForm):
    class Meta:
        model = ActeNaissance
        fields = "__all__"
        exclude = ('created_by', 'validated_by', 'pdf', 'statut')

        widgets = {
            # Ajout de form-control à tous les champs
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
            'nom_enfant': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom_enfant': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe_enfant': forms.Select(attrs={'class': 'form-select'}),
            'lieu_naissance': forms.TextInput(attrs={'class': 'form-control'}),
            'pere_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'pere_prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'mere_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'mere_prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'declarant': forms.TextInput(attrs={'class': 'form-control'}),
            'officier': forms.TextInput(attrs={'class': 'form-control'}),

            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }