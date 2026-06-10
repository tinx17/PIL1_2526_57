"""
Vues de l'application matching.
Gère le dashboard, la création d'offres/demandes,
la recherche et le contact.
"""

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import OffreMentorat, Matching
from .forms import OffreMentoratForm, RechercheForm
from .matching_engine import get_suggestions, calculate_score
from accounts.models import Matiere
from messaging.models import Conversation


@login_required
def dashboard_view(request):
    """
    Tableau de bord principal.
    Affiche les suggestions de matching avec score visuel
    et les offres/demandes de l'utilisateur.
    """
    user = request.user

    # Obtenir les suggestions de matching
    suggestions = get_suggestions(user, limit=10)

    # Récupérer les offres/demandes de l'utilisateur
    mes_offres = OffreMentorat.objects.filter(auteur=user, statut='active')

    # Statistiques rapides
    stats = {
        'total_offres': OffreMentorat.objects.filter(auteur=user, type='offre').count(),
        'total_demandes': OffreMentorat.objects.filter(auteur=user, type='demande').count(),
        'total_matchings': Matching.objects.filter(
            Q(mentor=user) | Q(mentore=user)
        ).count(),
    }

    context = {
        'suggestions': suggestions,
        'mes_offres': mes_offres,
        'stats': stats,
    }
    return render(request, 'matching/dashboard.html', context)


@login_required
def creer_offre_view(request):
    """
    Créer une nouvelle offre de mentorat.
    L'utilisateur propose ses compétences.
    """
    if request.method == 'POST':
        form = OffreMentoratForm(request.POST)
        # Traiter les disponibilités JSON
        disponibilites_json = request.POST.get('disponibilites', '{}')
        try:
            disponibilites = json.loads(disponibilites_json)
        except json.JSONDecodeError:
            disponibilites = {}

        if form.is_valid():
            offre = form.save(commit=False)
            offre.auteur = request.user
            offre.type = 'offre'
            offre.disponibilites = disponibilites
            offre.save()
            form.save_m2m()  # Sauvegarder les matières
            messages.success(request, 'Votre offre de mentorat a été publiée avec succès !')
            return redirect('matching:dashboard')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = OffreMentoratForm()

    context = {
        'form': form,
        'type_publication': 'offre',
        'disponibilites_json': json.dumps(request.user.disponibilites or {}),
    }
    return render(request, 'matching/create_offer.html', context)


@login_required
def creer_demande_view(request):
    """
    Créer une nouvelle demande de mentorat.
    L'utilisateur exprime ses besoins d'aide.
    """
    if request.method == 'POST':
        form = OffreMentoratForm(request.POST)
        disponibilites_json = request.POST.get('disponibilites', '{}')
        try:
            disponibilites = json.loads(disponibilites_json)
        except json.JSONDecodeError:
            disponibilites = {}

        if form.is_valid():
            demande = form.save(commit=False)
            demande.auteur = request.user
            demande.type = 'demande'
            demande.disponibilites = disponibilites
            demande.save()
            form.save_m2m()
            messages.success(request, 'Votre demande de mentorat a été publiée avec succès !')
            return redirect('matching:dashboard')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = OffreMentoratForm()

    context = {
        'form': form,
        'type_publication': 'demande',
        'disponibilites_json': json.dumps(request.user.disponibilites or {}),
    }
    return render(request, 'matching/create_request.html', context)


@login_required
def recherche_view(request):
    """
    Page de recherche d'offres et demandes de mentorat.
    Filtre par matière, type, format et disponibilités.
    """
    form = RechercheForm(request.GET or None)

    context = {
        'form': form,
    }
    return render(request, 'matching/search.html', context)


@login_required
def resultats_view(request):
    """
    Affiche les résultats de recherche filtrés.
    """
    form = RechercheForm(request.GET)
    offres = OffreMentorat.objects.filter(statut='active').exclude(auteur=request.user)

    if form.is_valid():
        # Filtre par texte libre (nom de l'auteur ou matière)
        q = form.cleaned_data.get('q')
        if q:
            offres = offres.filter(
                Q(matieres__nom__icontains=q) |
                Q(auteur__nom__icontains=q) |
                Q(auteur__prenom__icontains=q) |
                Q(description__icontains=q)
            ).distinct()

        # Filtre par type
        type_filtre = form.cleaned_data.get('type')
        if type_filtre:
            offres = offres.filter(type=type_filtre)

        # Filtre par matière
        matiere = form.cleaned_data.get('matiere')
        if matiere:
            offres = offres.filter(matieres=matiere)

        # Filtre par format
        format_filtre = form.cleaned_data.get('format')
        if format_filtre:
            offres = offres.filter(format=format_filtre)

        # Filtre par jour de disponibilité
        jour = form.cleaned_data.get('jour')
        if jour:
            offres = offres.filter(disponibilites__has_key=jour)

    # Précharger les relations pour optimiser les requêtes
    offres = offres.select_related('auteur').prefetch_related('matieres')

    context = {
        'form': form,
        'offres': offres,
        'total_resultats': offres.count(),
    }
    return render(request, 'matching/results.html', context)


@login_required
def contacter_view(request, user_id):
    """
    Contacter un utilisateur.
    Crée ou récupère une conversation existante et redirige
    vers la messagerie.
    """
    autre_utilisateur = get_object_or_404(
        get_user_model(), pk=user_id
    )

    if autre_utilisateur == request.user:
        messages.warning(request, 'Vous ne pouvez pas vous contacter vous-même.')
        return redirect('matching:dashboard')

    # Chercher une conversation existante entre les deux utilisateurs
    conversations = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=autre_utilisateur
    )

    if conversations.exists():
        conversation = conversations.first()
    else:
        # Créer une nouvelle conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, autre_utilisateur)

        # Optionnel : créer un matching si les scores sont bons
        resultat = calculate_score(request.user, autre_utilisateur)
        if resultat['score'] > 0.1:
            matching, created = Matching.objects.get_or_create(
                mentor=request.user,
                mentore=autre_utilisateur,
                defaults={
                    'score_compatibilite': resultat['score'],
                    'disponibilites_communes': resultat['disponibilites_communes'],
                }
            )
            if created and resultat['matieres_communes_ids']:
                matching.matieres_communes.set(resultat['matieres_communes_ids'])

    messages.info(
        request,
        f'Conversation ouverte avec {autre_utilisateur.get_full_name()}.'
    )
    return redirect('messaging:conversation', conversation_id=conversation.pk)


@login_required
def fermer_offre_view(request, offre_id):
    """Fermer une offre ou demande de mentorat."""
    offre = get_object_or_404(OffreMentorat, pk=offre_id, auteur=request.user)
    offre.statut = 'fermee'
    offre.save()
    messages.success(request, 'L\'offre a été fermée.')
    return redirect('matching:dashboard')


# Import nécessaire pour contacter_view
from django.contrib.auth import get_user_model
