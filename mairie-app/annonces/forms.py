from django import forms
from .models import Annonce

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ["titre", "contenu", "fichier_pdf"]
        widgets = {
            "titre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Titre de l'annonce"
            }),
            "contenu": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Contenu de l'annonce"
            }),
            "fichier_pdf": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
