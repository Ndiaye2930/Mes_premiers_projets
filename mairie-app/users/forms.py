from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    # Ajout des widgets Bootstrap aux champs supplémentaires
    nom = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de famille'})
    )
    prenom = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom(s)'})
    )
    telephone = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone (optionnel)'})
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = (
            'nom',
            'prenom',
            'username',
            'email',
            'telephone',
            'photo',
            'role', # Assurez-vous que le champ 'role' est un SelectField dans le modèle pour utiliser form-select
        )
        widgets = {
            # Application des classes aux champs de base de UserCreationForm
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur unique'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse e-mail'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            # Note: password1 et password2 sont gérés par UserCreationForm mais nécessitent un rendu manuel dans le template
        }
    
    # Ajout des widgets pour les champs de mot de passe qui sont générés par la classe parente
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajout des classes Bootstrap aux champs de mot de passe générés par UserCreationForm
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nouveau mot de passe'})


# ----------------------------------------------------------------------------------------------------------------------

class CustomUserChangeForm(UserChangeForm):
    password = None  # Masquer le champ mot de passe dans le formulaire édition

    # Ajout des widgets Bootstrap aux champs supplémentaires
    nom = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    prenom = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telephone = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = (
            'nom',
            'prenom',
            'username',
            'email',
            'telephone',
            'photo',
            'role',
        )
        widgets = {
            # Application des classes aux champs de base
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

# ----------------------------------------------------------------------------------------------------------------------

class CustomAuthenticationForm(AuthenticationForm):
    # Les champs username et password étaient déjà définis, j'ai juste mis à jour la classe
    # pour s'assurer qu'ils sont cohérents et bien stylisés.
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg', # Utiliser form-control-lg pour plus d'impact sur la page de login
            'placeholder': 'Nom d’utilisateur ou E-mail'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg', # Utiliser form-control-lg
            'placeholder': 'Mot de passe'
        })
    )