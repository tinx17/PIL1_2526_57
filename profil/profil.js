const API_URL = "http://localhost:3000";

document.getElementById("profil").innerHTML = `
    <div class="carte-profil" style="text-align:center; padding: 50px;">
        <p style="color: #3b7bc8; font-size: 16px;">⏳ Chargement du profil...</p>
    </div>
`;

fetch(`${API_URL}/api/utilisateurs/moi`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json"
    }
})
.then(function(reponse) {
    if (!reponse.ok) {
        throw new Error("Erreur serveur : " + reponse.status);
    }
    return reponse.json();
})
.then(function(utilisateur) {
    afficherProfil(utilisateur);
})
.catch(function(erreur) {
    document.getElementById("profil").innerHTML = `
        <div class="carte-profil" style="text-align:center; padding: 40px;">
            <p style="color: #c0392b; font-size: 15px;">
                ❌ Impossible de charger le profil.<br>
                <small style="color:#999;">${erreur.message}</small>
            </p>
            <p style="margin-top:15px; font-size:13px; color:#888;">
                Vérifiez que le serveur backend tourne sur <strong>${API_URL}</strong>
            </p>
        </div>
    `;
});

function afficherProfil(utilisateur) {

    const tagsForts = utilisateur.points_forts.length > 0
        ? utilisateur.points_forts.map(m => `<span class="tag-fort">${m}</span>`).join("")
        : `<p class="message-vide">Aucun point fort renseigné.</p>`;

    const tagsLacunes = utilisateur.lacunes.length > 0
        ? utilisateur.lacunes.map(m => `<span class="tag-lacune">${m}</span>`).join("")
        : `<p class="message-vide">Aucune lacune renseignée.</p>`;

    const lignesCreneaux = utilisateur.creneaux.length > 0
        ? utilisateur.creneaux.map(c => {
            const jour = c.jour.charAt(0).toUpperCase() + c.jour.slice(1);
            return `<li class="item-creneau">${jour} : ${c.heure_debut} → ${c.heure_fin}</li>`;
          }).join("")
        : `<p class="message-vide">Aucune disponibilité renseignée.</p>`;

    const initiales = utilisateur.prenom.charAt(0) + utilisateur.nom.charAt(0);

    document.getElementById("profil").innerHTML = `
        <div class="carte-profil">

            <div class="profil-haut">
                <div class="avatar">${initiales.toUpperCase()}</div>
                <div>
                    <p class="profil-nom">${utilisateur.prenom} ${utilisateur.nom}</p>
                    <p class="profil-filiere">Filière : ${utilisateur.filiere}</p>
                    <p class="profil-niveau">Niveau : ${utilisateur.niveau}</p>
                    <p class="profil-email">${utilisateur.email}</p>
                </div>
            </div>

            <hr class="separateur">

            <div class="section-profil">
                <h3 class="titre-section">À propos</h3>
                <p class="profil-bio">${utilisateur.bio_courte || "Aucune biographie renseignée."}</p>
            </div>

            <hr class="separateur">

            <div class="section-profil">
                <h3 class="titre-section">Centres d'intérêt</h3>
                <p class="profil-interets">${utilisateur.centres_interet || "Aucun centre d'intérêt renseigné."}</p>
            </div>

            <hr class="separateur">

            <div class="section-profil">
                <h3 class="titre-section">Ce que je peux enseigner</h3>
                <div class="liste-tags">${tagsForts}</div>
            </div>

            <hr class="separateur">

            <div class="section-profil">
                <h3 class="titre-section">Ce que je veux apprendre</h3>
                <div class="liste-tags">${tagsLacunes}</div>
            </div>

            <hr class="separateur">

            <div class="section-profil">
                <h3 class="titre-section">Mes disponibilités</h3>
                <ul class="liste-creneaux">${lignesCreneaux}</ul>
            </div>

        </div>
    `;
}