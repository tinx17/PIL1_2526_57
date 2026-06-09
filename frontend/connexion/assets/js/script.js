document.addEventListener('DOMContentLoaded', () => {
    console.log("IFRI MentorLink : Prêt !");

    const formulaire = document.querySelector('.login-form');

    formulaire.addEventListener('submit', async (evenement) => {
        evenement.preventDefault();

        const email = document.querySelector('#email').value;
        const mot_de_passe = document.querySelector('#mot_de_passe').value;

        // Désactiver le bouton pendant la requête
        const bouton = document.querySelector('.btn-login');
        bouton.disabled = true;
        bouton.textContent = 'Connexion en cours...';

        try {
            const reponse = await fetch('http://127.0.0.1:8000/api/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, mot_de_passe })
            });

            const resultat = await reponse.json();

            if (reponse.ok) {
                // Sauvegarder l'utilisateur connecté
                localStorage.setItem('user_id', resultat.user_id);
                localStorage.setItem('user_prenom', resultat.message);

                alert(resultat.message);
                // Rediriger vers le tableau de bord
                // window.location.href = '../dashboard/dashboard.html';
            } else {
                alert('Erreur : ' + resultat.message);
            }

        } catch (erreur) {
            alert('Impossible de joindre le serveur. Vérifiez que Django tourne.');
            console.error(erreur);
        } finally {
            bouton.disabled = false;
            bouton.textContent = 'Se connecter';
        }
    });
});