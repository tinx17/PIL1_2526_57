document.addEventListener('DOMContentLoaded', () => {
    console.log("IFRI MentorLink : Les fichiers HTML, CSS et JS sont connectés avec succès !");
});
// 1. On attend que toute la page HTML soit bien chargée par le navigateur
document.addEventListener('DOMContentLoaded', () => {

    // 2. On récupère le formulaire de connexion grâce à sa classe CSS
    const formulaire = document.querySelector('.login-form');

    // 3. On écoute quand l'utilisateur clique sur le bouton pour valider le formulaire
    formulaire.addEventListener('submit', (evenement) => {
        
        // Empêche la page de se recharger automatiquement (comportement par défaut)
        evenement.preventDefault();

        // 4. On récupère ce que l'utilisateur a tapé dans les cases
        // (Le premier input c'est l'email, le deuxième c'est le mot de passe)
        const emailTape = document.querySelectorAll('input')[0].value;
        const motDePasseTape = document.querySelectorAll('input')[1].value;

        // 5. Une petite vérification de test toute simple
        if (emailTape === "admin@ifri.bj" && motDePasseTape === "1234") {
            alert("Connexion réussie ! Bienvenue sur MentorLink.");
        } else {
            alert("Identifiants incorrects. Veuillez réessayer.");
        }
    });

});