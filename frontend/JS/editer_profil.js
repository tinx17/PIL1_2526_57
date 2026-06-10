// Logique pour l'édition de profil
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form-edition-profil");
  const prenomInput = document.getElementById("prenom");
  const nomInput = document.getElementById("nom");
  const telephoneInput = document.getElementById("telephone");
  const filiereSelect = document.getElementById("filiere");
  const niveauSelect = document.getElementById("niveau");
  const bioInput = document.getElementById("bio");
  const competencesInput = document.getElementById("competences");
  const lacunesInput = document.getElementById("lacunes");
  const disponibilitesInput = document.getElementById("disponibilites");
  const errorPara = document.getElementById("erreur-edition");

  // Charger les données utilisateur courantes
  fetch(`${API_BASE}/accounts/api/user/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  })
    .then((res) => {
      if (!res.ok) throw new Error("Erreur serveur.");
      return res.json();
    })
    .then((data) => {
      if (data.ok && data.user) {
        const u = data.user;
        prenomInput.value = u.prenom || "";
        nomInput.value = u.nom || "";
        telephoneInput.value = u.telephone || "";
        filiereSelect.value = u.filiere_raw || "";
        niveauSelect.value = u.niveau_raw || "";
        bioInput.value = u.bio || "";
        competencesInput.value = (u.competences || []).join(", ");
        lacunesInput.value = (u.lacunes || []).join(", ");

        // Formater les disponibilités en chaîne lisible
        let dispoText = "";
        if (u.disponibilites && typeof u.disponibilites === "object") {
          let parts = [];
          for (let j in u.disponibilites) {
            const jour = j.charAt(0).toUpperCase() + j.slice(1);
            const slots = u.disponibilites[j].join(", ");
            parts.push(`${jour} ${slots}`);
          }
          dispoText = parts.join(", ");
        }
        disponibilitesInput.value = dispoText;
      } else {
        throw new Error(data.message || "Impossible de charger vos données.");
      }
    })
    .catch((err) => {
      errorPara.textContent = `❌ ${err.message}`;
    });

  // Soumission du formulaire
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    errorPara.textContent = "";

    const payload = {
      prenom: prenomInput.value.trim(),
      nom: nomInput.value.trim(),
      telephone: telephoneInput.value.trim(),
      filiere: filiereSelect.value,
      niveau: niveauSelect.value,
      bio: bioInput.value.trim(),
      competences: competencesInput.value.trim(),
      lacunes: lacunesInput.value.trim(),
      disponibilites: disponibilitesInput.value.trim(),
    };

    if (!payload.prenom || !payload.nom || !payload.telephone) {
      errorPara.textContent = "❌ Veuillez remplir les champs obligatoires.";
      return;
    }

    fetch(`${API_BASE}/accounts/api/user/update/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.ok) {
          // Succès: retour au profil
          window.location.href = "profil.html";
        } else {
          errorPara.textContent = `❌ ${data.message || "Une erreur est survenue."}`;
        }
      })
      .catch((err) => {
        errorPara.textContent = `❌ Erreur de connexion : ${err.message}`;
      });
  });
});
