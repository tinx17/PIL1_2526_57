document.addEventListener('DOMContentLoaded', async () => {

    // 1. Récupérer les infos utilisateur depuis localStorage
    const userId = localStorage.getItem('user_id');
    const prenom = localStorage.getItem('user_prenom') || 'Étudiant';

    // Afficher le prénom et l'initiale dans l'avatar
    document.getElementById('prenomUtilisateur').textContent = prenom;
    document.getElementById('avatarInitiales').textContent = prenom.charAt(0).toUpperCase();

    // 2. Si l'utilisateur n'est pas connecté → redirection
    if (!userId) {
        window.location.href = '../connexion/page_connexion.html';
        return;
    }

    // 3. Charger les statistiques depuis l'API Django
    // (À décommenter quand les APIs seront prêtes)
    /*
    try {
        const reponse = await fetch(`http://127.0.0.1:8000/api/stats/?user_id=${userId}`);
        const data = await reponse.json();

        document.getElementById('nbOffres').textContent        = data.nb_offres        || 0;
        document.getElementById('nbDemandes').textContent      = data.nb_demandes      || 0;
        document.getElementById('nbMatchings').textContent     = data.nb_matchings     || 0;
        document.getElementById('nbConversations').textContent = data.nb_conversations || 0;

        // Badge de notification
        const badge = document.getElementById('notifBadge');
        if (data.messages_non_lus > 0) {
            badge.textContent = data.messages_non_lus;
            badge.style.display = 'inline-block';
        } else {
            badge.style.display = 'none';
        }

    } catch (erreur) {
        console.error('Impossible de charger les statistiques :', erreur);
    }
    */

    // 4. Menu mobile — toggle sidebar
    const menuToggle = document.getElementById('menuToggle');
    const sidebar    = document.getElementById('sidebar');
    const overlay    = document.getElementById('overlay');

    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('show');
    });

    overlay.addEventListener('click', () => {
        sidebar.classList.remove('open');
        overlay.classList.remove('show');
    });

});
