document.addEventListener('DOMContentLoaded', () => {
    const boutonInscription = document.querySelector('.btn-google');

    boutonInscription.addEventListener('click', async () => {

        // Récupération des valeurs du formulaire
        const donnees = {
            nom: document.querySelector('#nom').value,
            prenom: document.querySelector('#prenom').value,
            telephone: document.querySelector('#telephone').value,
            email: document.querySelector('#email').value,
            filiere: document.querySelector('#filière').value,
            niveau: document.querySelector('#niveau').value,
            mot_de_passe: document.querySelector('#mot_de_passe').value,

            // Pour les selects multiples
            competences: Array.from(
                document.querySelector('#Competences').selectedOptions
            ).map(opt => opt.value),

            lacunes: Array.from(
                document.querySelector('#Lacunes').selectedOptions
            ).map(opt => opt.value),
        };

        try {
            const reponse = await fetch('http://127.0.0.1:8000/api/inscription/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(donnees)
            });

            const resultat = await reponse.json();

            if (reponse.ok) {
                alert(resultat.message); // Succès
                // window.location.href = 'page_login.html'; // Redirection
            } else {
                alert('Erreur : ' + resultat.message);
            }

        } catch (erreur) {
            alert('Impossible de joindre le serveur. Vérifiez que Django tourne.');
            console.error(erreur);
        }
    });
});