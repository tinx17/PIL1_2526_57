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

  // Photo de profil
  const photoInput = document.getElementById("photo_profil");
  const avatarImg = document.getElementById("avatar-preview-img");
  const avatarInitials = document.getElementById("avatar-preview-initials");
  const btnSupprimerPhoto = document.getElementById("btn-supprimer-photo");
  let supprimerPhotoFlag = false;

  if (photoInput) {
    photoInput.addEventListener("change", function () {
      const file = this.files[0];
      if (file) {
        if (file.size > 2 * 1024 * 1024) {
          errorPara.textContent = "❌ L'image ne doit pas dépasser 2 Mo.";
          this.value = "";
          return;
        }
        const reader = new FileReader();
        reader.onload = function (e) {
          avatarImg.src = e.target.result;
          avatarImg.style.display = "block";
          avatarInitials.style.display = "none";
          btnSupprimerPhoto.style.display = "inline-flex";
          supprimerPhotoFlag = false;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  if (btnSupprimerPhoto) {
    btnSupprimerPhoto.addEventListener("click", function () {
      avatarImg.style.display = "none";
      avatarInitials.style.display = "flex";
      btnSupprimerPhoto.style.display = "none";
      if (photoInput) photoInput.value = "";
      supprimerPhotoFlag = true;
    });
  }

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

        // Afficher l'avatar ou les initiales
        const initials = ((u.prenom || "").charAt(0) + (u.nom || "").charAt(0)).toUpperCase() || "U";
        avatarInitials.textContent = initials;
        if (u.photo_profil) {
          avatarImg.src = u.photo_profil;
          avatarImg.style.display = "block";
          avatarInitials.style.display = "none";
          btnSupprimerPhoto.style.display = "inline-flex";
        } else {
          avatarImg.style.display = "none";
          avatarInitials.style.display = "flex";
          btnSupprimerPhoto.style.display = "none";
        }

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

    const prenom = prenomInput.value.trim();
    const nom = nomInput.value.trim();
    const telephone = telephoneInput.value.trim();

    if (!prenom || !nom || !telephone) {
      errorPara.textContent = "❌ Veuillez remplir les champs obligatoires.";
      return;
    }

    const formData = new FormData();
    formData.append("prenom", prenom);
    formData.append("nom", nom);
    formData.append("telephone", telephone);
    formData.append("filiere", filiereSelect.value);
    formData.append("niveau", niveauInput.value);
    formData.append("bio", bioInput.value.trim());
    formData.append("competences", JSON.stringify(competences));
    formData.append("lacunes", JSON.stringify(lacunes));
    formData.append("disponibilites", JSON.stringify(disponibilites));
    formData.append("supprimer_photo", supprimerPhotoFlag);

    if (photoInput && photoInput.files && photoInput.files[0]) {
      formData.append("photo_profil", photoInput.files[0]);
    }

    fetch(`${API_BASE}/accounts/api/user/update/`, {
      method: "POST",
      body: formData,
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
