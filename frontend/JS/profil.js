// API_BASE est déjà défini dans script.js

// Affichage immédiat du message de chargement
document.getElementById("profil").innerHTML = `
    <div class="carte-profil" style="text-align:center; padding: 50px;">
        <p style="color: var(--blue-medium); font-size: 16px;">⏳ Chargement du profil...</p>
    </div>
`;

// Appel de l'API avec partage des cookies de session
fetch(`${API_BASE}/accounts/api/user/`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json"
    },
    credentials: "include"
})
.then(function(reponse) {
    if (!reponse.ok) {
        throw new Error("Erreur serveur : " + reponse.status);
    }
    return reponse.json();
})
.then(function(data) {
    if (data.ok && data.user) {
        afficherProfil(data.user);
    } else {
        throw new Error(data.message || "Impossible de récupérer les données utilisateur.");
    }
})
.catch(function(erreur) {
    document.getElementById("profil").innerHTML = `
        <div class="carte-profil" style="text-align:center; padding: 40px;">
            <p style="color: #dc2626; font-size: 15px; font-weight: 600;">
                ❌ Impossible de charger le profil.
            </p>
            <p style="color:#6b7280; font-size:13px; margin-top:8px;">
                ${erreur.message}
            </p>
            <p style="margin-top:15px; font-size:13px; color:#6b7280;">
                Vérifiez que vous êtes bien connecté à votre compte.
            </p>
        </div>
    `;
});

function afficherProfil(utilisateur) {
    // Gestion des compétences (points forts)
    const tagsForts = utilisateur.competences && utilisateur.competences.length > 0
        ? utilisateur.competences.map(m => `<span class="tag tag-competence">${m}</span>`).join("")
        : `<p class="message-vide">Aucune compétence renseignée.</p>`;

    // Gestion des lacunes (points faibles)
    const tagsLacunes = utilisateur.lacunes && utilisateur.lacunes.length > 0
        ? utilisateur.lacunes.map(m => `<span class="tag tag-lacune">${m}</span>`).join("")
        : `<p class="message-vide">Aucune lacune renseignée.</p>`;

    // Gestion des créneaux de disponibilités
    let lignesCreneaux = "";
    if (utilisateur.disponibilites && typeof utilisateur.disponibilites === "object") {
        let parts = [];
        for (let j in utilisateur.disponibilites) {
            const jour = j.charAt(0).toUpperCase() + j.slice(1);
            const slots = utilisateur.disponibilites[j].join(", ");
            parts.push(`<li class="item-creneau"><strong>${jour}</strong> : ${slots}</li>`);
        }
        lignesCreneaux = parts.join("") || `<li class="message-vide">Aucune disponibilité renseignée.</li>`;
    } else {
        lignesCreneaux = `<li class="message-vide">Aucune disponibilité renseignée.</li>`;
    }

    // Gestion des initiales de l'avatar
    const prenom = utilisateur.prenom || "";
    const nom = utilisateur.nom || "";
    let initiales = "U";
    if (prenom || nom) {
        initiales = (prenom.charAt(0) + nom.charAt(0)).toUpperCase();
    }

    document.getElementById("profil").innerHTML = `
        <div class="carte-profil">
            <div class="profil-haut">
                <div class="avatar">${initiales}</div>
                <div class="profil-textes">
                    <h2 class="profil-nom">${prenom} ${nom}</h2>
                    <p class="profil-filiere"><strong>Filière :</strong> ${utilisateur.filiere || "Non renseignée"}</p>
                    <p class="profil-niveau"><strong>Niveau d'études :</strong> ${utilisateur.niveau || "Non renseigné"}</p>
                    <p class="profil-email"><strong>Email :</strong> ${utilisateur.email || "Non renseigné"}</p>
                </div>
                <div class="profil-actions">
                    <a href="editer_profil.html" class="btn btn-secondary btn-sm" style="display: flex; align-items: center; gap: 8px;">
                        <i data-lucide="edit-3"></i> Modifier le profil
                    </a>
                </div>
            </div>

            <hr class="separateur">

            <div class="section-profil">
                <h3 class="titre-section">Biographie</h3>
                <p class="profil-bio">${utilisateur.bio || "Aucune biographie renseignée."}</p>
            </div>

            <hr class="separateur">

            <div class="section-profil">
                <h3 class="titre-section">Matières maîtrisées (Points forts)</h3>
                <div class="tags">${tagsForts}</div>
            </div>

            <hr class="separateur">

            <div class="section-profil">
                <h3 class="titre-section">Matières à améliorer (Points faibles)</h3>
                <div class="tags">${tagsLacunes}</div>
            </div>

            <hr class="separateur">

            <div class="section-profil">
                <h3 class="titre-section">Mes disponibilités</h3>
                <ul class="liste-creneaux">${lignesCreneaux}</ul>
            </div>
        </div>
    `;

    if (window.lucide) {
        window.lucide.createIcons();
    }
}