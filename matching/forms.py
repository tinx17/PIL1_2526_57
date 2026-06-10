"""
Formulaires de l'application matching.
Gère la création d'offres/demandes et la recherche.
"""

from django import forms
from .models import OffreMentorat
from accounts.models import Matiere


class OffreMentoratForm(forms.ModelForm):
    """Formulaire de création d'une offre ou demande de mentorat."""

    matieres = forms.ModelMultipleChoiceField(
        queryset=Matiere.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        label='Matières concernées',
        help_text='Sélectionnez une ou plusieurs matières'
    )

    class Meta:
        model = OffreMentorat
        fields = ['matieres', 'format', 'description']
        widgets = {
            'format': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_format'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Décrivez votre offre ou demande...',
                'rows': 4,
                'id': 'id_description'
            }),
        }


class RechercheForm(forms.Form):
    """Formulaire de recherche d'offres et demandes de mentorat."""

    TYPE_CHOICES = [
        ('', 'Tous les types'),
        ('offre', 'Offres de mentorat'),
        ('demande', 'Demandes de mentorat'),
    ]

    FORMAT_CHOICES = [
        ('', 'Tous les formats'),
        ('presentiel', 'En présentiel'),
        ('en_ligne', 'En ligne'),
        ('les_deux', 'Présentiel et en ligne'),
    ]

    JOUR_CHOICES = [
        ('', 'Tous les jours'),
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
        ('vendredi', 'Vendredi'),
        ('samedi', 'Samedi'),
        ('dimanche', 'Dimanche'),
    ]

    q = forms.CharField(
        required=False,
        label='Rechercher',
        widget=forms.TextInput(attrs={
            'class': 'form-input search-input',
            'placeholder': 'Rechercher par matière, nom...',
            'id': 'id_recherche'
        })
    )
    type = forms.ChoiceField(
        required=False,
        choices=TYPE_CHOICES,
        label='Type',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_type'
        })
    )
    matiere = forms.ModelChoiceField(
        queryset=Matiere.objects.all(),
        required=False,
        label='Matière',
        empty_label='Toutes les matières',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_matiere'
        })
    )
    format = forms.ChoiceField(
        required=False,
        choices=FORMAT_CHOICES,
        label='Format',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_format_recherche'
        })
    )
    jour = forms.ChoiceField(
        required=False,
        choices=JOUR_CHOICES,
        label='Jour de disponibilité',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_jour'
        })
    )
