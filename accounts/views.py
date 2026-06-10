"""
Vues de l'application accounts.
Gère l'inscription, la connexion, la déconnexion,
l'affichage et l'édition du profil, et la réinitialisation
du mot de passe.
"""

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm, EditionProfilForm, ReinitialisationMotDePasseForm

UserProfile = get_user_model()


def inscription_view(request):
    """
    Vue d'inscription d'un nouvel utilisateur.
    Affiche le formulaire d'inscription et crée le compte.
    """
    if request.user.is_authenticated:
        return redirect('matching:dashboard')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Connexion automatique après inscription
            login(request, user, backend='accounts.backends.EmailOrPhoneBackend')
            messages.success(request, f'Bienvenue {user.prenom} ! Votre compte a été créé avec succès.')
            return redirect('matching:dashboard')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = InscriptionForm()

    return render(request, 'accounts/register.html', {'form': form})


def connexion_view(request):
    """
    Vue de connexion par email ou téléphone.
    Utilise le backend d'authentification personnalisé.
    """
    if request.user.is_authenticated:
        return redirect('matching:dashboard')

    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data['identifiant']
            password = form.cleaned_data['password']

            # Tenter l'authentification via le backend personnalisé
            user = authenticate(request, username=identifiant, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Bon retour, {user.prenom} !')
                # Rediriger vers la page demandée ou le dashboard
                next_url = request.GET.get('next', 'matching:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Identifiant ou mot de passe incorrect.')
    else:
        form = ConnexionForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def deconnexion_view(request):
    """Déconnecte l'utilisateur et redirige vers la page de connexion."""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('accounts:login')


@login_required
def profil_view(request, user_id):
    """
    Affiche le profil public d'un utilisateur.
    Accessible à tout utilisateur connecté.
    """
    profil = get_object_or_404(UserProfile, pk=user_id)
    est_propre_profil = (request.user.pk == profil.pk)

    # Récupérer les disponibilités formatées
    disponibilites = profil.disponibilites or {}

    context = {
        'profil': profil,
        'est_propre_profil': est_propre_profil,
        'competences': profil.competences.all(),
        'lacunes': profil.lacunes.all(),
        'disponibilites': disponibilites,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def editer_profil_view(request):
    """
    Vue d'édition du profil de l'utilisateur connecté.
    Inclut la grille de disponibilités interactive.
    """
    user = request.user

    if request.method == 'POST':
        form = EditionProfilForm(request.POST, request.FILES, instance=user)

        # Traiter les disponibilités envoyées en JSON depuis le frontend
        disponibilites_json = request.POST.get('disponibilites', '{}')
        try:
            disponibilites = json.loads(disponibilites_json)
        except json.JSONDecodeError:
            disponibilites = {}

        if form.is_valid():
            profil = form.save(commit=False)
            profil.disponibilites = disponibilites
            profil.save()
            form.save_m2m()  # Sauvegarder les relations ManyToMany
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('accounts:profil', user_id=user.pk)
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = EditionProfilForm(instance=user)

    context = {
        'form': form,
        'disponibilites_json': json.dumps(user.disponibilites or {}),
    }
    return render(request, 'accounts/edit_profile.html', context)


def reinitialiser_mdp_view(request):
    """
    Réinitialisation du mot de passe via formulaire simple.
    L'utilisateur fournit son email et un nouveau mot de passe.
    """
    if request.method == 'POST':
        form = ReinitialisationMotDePasseForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            nouveau_password = form.cleaned_data['nouveau_password']

            try:
                user = UserProfile.objects.get(email=email)
                user.set_password(nouveau_password)
                user.save()
                messages.success(
                    request,
                    'Votre mot de passe a été réinitialisé. Vous pouvez maintenant vous connecter.'
                )
                return redirect('accounts:login')
            except UserProfile.DoesNotExist:
                messages.error(request, 'Aucun compte n\'est associé à cette adresse email.')
    else:
        form = ReinitialisationMotDePasseForm()

    return render(request, 'accounts/login.html', {
        'form_reset': form,
        'show_reset': True
    })
