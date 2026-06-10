// Logique pour l'édition de profil
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form-edition-profil");
  const prenomInput = document.getElementById("prenom");
  const nomInput = document.getElementById("nom");
  const telephoneInput = document.getElementById("telephone");
  const filiereSelect = document.getElementById("filiere");
  const niveauInput = document.getElementById("niveau");
  const bioInput = document.getElementById("bio");
  const errorPara = document.getElementById("erreur-edition");

  // Configuration niveau
  const levelBtns = document.querySelectorAll("#niveau-toggle-group .level-btn");
  levelBtns.forEach(btn => {
    btn.addEventListener("click", function() {
      levelBtns.forEach(b => b.classList.remove("active"));
      this.classList.add("active");
      niveauInput.value = this.dataset.value;
    });
  });

  // Configuration matières
  const PREDEFINED_MATIERES = [
    "React", "Node.js", "Python", "Java", "C++", "TypeScript", "SQL",
    "Machine Learning", "DevOps", "Cybersécurité", "Algorithmique", "UML",
    "Cloud AWS", "Linux", "GraphQL", "Statistiques"
  ];
  const competencesContainer = document.getElementById("competences-chips");
  const lacunesContainer = document.getElementById("lacunes-chips");

  if (competencesContainer && lacunesContainer) {
    competencesContainer.innerHTML = PREDEFINED_MATIERES.map(m => `
      <button type="button" class="chip chip-fort" data-value="${m}">
        <span class="chip-text">${m}</span>
      </button>
    `).join("");

    lacunesContainer.innerHTML = PREDEFINED_MATIERES.map(m => `
      <button type="button" class="chip chip-faible" data-value="${m}">
        <span class="chip-text">${m}</span>
      </button>
    `).join("");

    competencesContainer.querySelectorAll(".chip").forEach(chip => {
      chip.addEventListener("click", function() {
        this.classList.toggle("active");
        const val = this.dataset.value;
        if (this.classList.contains("active")) {
          // Décocher de la section lacunes
          const corresp = lacunesContainer.querySelector(`.chip[data-value="${val}"]`);
          if (corresp) corresp.classList.remove("active");
        }
      });
    });

    lacunesContainer.querySelectorAll(".chip").forEach(chip => {
      chip.addEventListener("click", function() {
        this.classList.toggle("active");
        const val = this.dataset.value;
        if (this.classList.contains("active")) {
          // Décocher de la section compétences
          const corresp = competencesContainer.querySelector(`.chip[data-value="${val}"]`);
          if (corresp) corresp.classList.remove("active");
        }
      });
    });
  }

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
        bioInput.value = u.bio || "";

        // Niveau d'études
        const activeLevel = u.niveau_raw || u.niveau || "";
        niveauInput.value = activeLevel;
        levelBtns.forEach(btn => {
          if (btn.dataset.value === activeLevel) {
            btn.classList.add("active");
          } else {
            btn.classList.remove("active");
          }
        });

        // Compétences (puces)
        const userComp = u.competences || [];
        if (competencesContainer) {
          competencesContainer.querySelectorAll(".chip").forEach(chip => {
            if (userComp.includes(chip.dataset.value)) {
              chip.classList.add("active");
            }
          });
        }

        // Lacunes (puces)
        const userLac = u.lacunes || [];
        if (lacunesContainer) {
          lacunesContainer.querySelectorAll(".chip").forEach(chip => {
            if (userLac.includes(chip.dataset.value)) {
              chip.classList.add("active");
            }
          });
        }

        // Disponibilités (grille)
        const userDispos = u.disponibilites || {};
        const checkboxes = document.querySelectorAll('.dispo-table input[type="checkbox"]');
        checkboxes.forEach(cb => cb.checked = false);

        for (let j in userDispos) {
          const day = j.toLowerCase();
          const slots = userDispos[j];
          if (Array.isArray(slots)) {
            slots.forEach(slot => {
              const cb = document.querySelector(`.dispo-table tbody tr[data-slot="${slot}"] input[data-day="${day}"]`);
              if (cb) cb.checked = true;
            });
          }
        }
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

    // Sérialiser la grille de disponibilités
    const disponibilites = {};
    const rows = document.querySelectorAll(".dispo-table tbody tr");
    rows.forEach(row => {
      const slot = row.dataset.slot;
      const checkboxes = row.querySelectorAll('input[type="checkbox"]');
      checkboxes.forEach(cb => {
        if (cb.checked) {
          const day = cb.dataset.day;
          if (!disponibilites[day]) {
            disponibilites[day] = [];
          }
          disponibilites[day].push(slot);
        }
      });
    });

    // Sérialiser les puces de matières
    const competences = competencesContainer 
      ? Array.from(competencesContainer.querySelectorAll(".chip.active")).map(c => c.dataset.value)
      : [];
    const lacunes = lacunesContainer
      ? Array.from(lacunesContainer.querySelectorAll(".chip.active")).map(c => c.dataset.value)
      : [];

    const payload = {
      prenom: prenomInput.value.trim(),
      nom: nomInput.value.trim(),
      telephone: telephoneInput.value.trim(),
      filiere: filiereSelect.value,
      niveau: niveauInput.value,
      bio: bioInput.value.trim(),
      competences: competences,
      lacunes: lacunes,
      disponibilites: disponibilites,
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
