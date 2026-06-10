"""
Formulaires de l'application accounts.
Gère l'inscription, la connexion, l'édition de profil
et la réinitialisation du mot de passe.
"""

from django import forms
from django.contrib.auth import get_user_model
from .models import Matiere

UserProfile = get_user_model()


class InscriptionForm(forms.ModelForm):
    """Formulaire d'inscription d'un nouvel utilisateur."""

    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Créez un mot de passe sécurisé',
            'id': 'id_password'
        }),
        min_length=8,
        help_text='Minimum 8 caractères'
    )
    password_confirm = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirmez votre mot de passe',
            'id': 'id_password_confirm'
        })
    )
    competences = forms.ModelMultipleChoiceField(
        queryset=Matiere.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        required=False,
        label='Mes compétences'
    )
    lacunes = forms.ModelMultipleChoiceField(
        queryset=Matiere.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        required=False,
        label='Mes lacunes'
    )

    class Meta:
        model = UserProfile
        fields = [
            'nom', 'prenom', 'email', 'telephone',
            'filiere', 'niveau', 'competences', 'lacunes', 'bio'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Votre nom de famille', 'id': 'id_nom'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Votre prénom', 'id': 'id_prenom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input', 'placeholder': 'votre@email.com', 'id': 'id_email'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': '+229XXXXXXXX', 'id': 'id_telephone'
            }),
            'filiere': forms.Select(attrs={
                'class': 'form-select', 'id': 'id_filiere'
            }),
            'niveau': forms.Select(attrs={
                'class': 'form-select', 'id': 'id_niveau'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea', 'placeholder': 'Parlez-nous de vous...',
                'rows': 3, 'id': 'id_bio'
            }),
        }

    def clean(self):
        """Validation croisée des champs."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')

        return cleaned_data

    def clean_email(self):
        """Vérifier l'unicité de l'email."""
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('Cette adresse email est déjà utilisée.')
        return email

    def clean_telephone(self):
        """Vérifier l'unicité du téléphone."""
        telephone = self.cleaned_data.get('telephone')
        if UserProfile.objects.filter(telephone=telephone).exists():
            raise forms.ValidationError('Ce numéro de téléphone est déjà utilisé.')
        return telephone

    def save(self, commit=True):
        """Créer l'utilisateur avec un mot de passe hashé."""
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Utiliser l'email comme username
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Sauvegarder les relations ManyToMany
            self.save_m2m()
        return user


class ConnexionForm(forms.Form):
    """Formulaire de connexion par email ou téléphone."""

    identifiant = forms.CharField(
        label='Email ou Téléphone',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Votre email ou numéro de téléphone',
            'id': 'id_identifiant',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Votre mot de passe',
            'id': 'id_password'
        })
    )


class EditionProfilForm(forms.ModelForm):
    """Formulaire d'édition du profil utilisateur."""

    competences = forms.ModelMultipleChoiceField(
        queryset=Matiere.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        required=False,
        label='Mes compétences'
    )
    lacunes = forms.ModelMultipleChoiceField(
        queryset=Matiere.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        required=False,
        label='Mes lacunes'
    )

    class Meta:
        model = UserProfile
        fields = [
            'nom', 'prenom', 'telephone', 'photo_profil',
            'filiere', 'niveau', 'competences', 'lacunes',
            'disponibilites', 'bio'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-input', 'id': 'id_nom'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-input', 'id': 'id_prenom'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-input', 'id': 'id_telephone'
            }),
            'photo_profil': forms.ClearableFileInput(attrs={
                'class': 'form-file', 'id': 'id_photo_profil'
            }),
            'filiere': forms.Select(attrs={
                'class': 'form-select', 'id': 'id_filiere'
            }),
            'niveau': forms.Select(attrs={
                'class': 'form-select', 'id': 'id_niveau'
            }),
            'disponibilites': forms.HiddenInput(attrs={
                'id': 'id_disponibilites'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea', 'rows': 3, 'id': 'id_bio'
            }),
        }

    def clean_telephone(self):
        """Vérifier l'unicité du téléphone (sauf pour l'utilisateur courant)."""
        telephone = self.cleaned_data.get('telephone')
        if UserProfile.objects.filter(telephone=telephone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Ce numéro de téléphone est déjà utilisé.')
        return telephone


class ReinitialisationMotDePasseForm(forms.Form):
    """Formulaire de réinitialisation du mot de passe."""

    email = forms.EmailField(
        label='Adresse email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Votre adresse email',
            'id': 'id_email'
        })
    )
    nouveau_password = forms.CharField(
        label='Nouveau mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nouveau mot de passe',
            'id': 'id_nouveau_password'
        }),
        min_length=8
    )
    confirmer_password = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirmez le nouveau mot de passe',
            'id': 'id_confirmer_password'
        })
    )

    def clean(self):
        """Vérifier que les mots de passe correspondent."""
        cleaned_data = super().clean()
        nouveau = cleaned_data.get('nouveau_password')
        confirmer = cleaned_data.get('confirmer_password')
        if nouveau and confirmer and nouveau != confirmer:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cleaned_data
