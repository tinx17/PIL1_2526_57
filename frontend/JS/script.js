const SESSION_KEY = "ifri_mentorlink_session";
const API_BASE = "http://localhost:8000";

function getSession() {
  try {
    const data = localStorage.getItem(SESSION_KEY);
    return data ? JSON.parse(data) : null;
  } catch {
    return null;
  }
}

function setSession(user) {
  localStorage.setItem(SESSION_KEY, JSON.stringify({ ...user, connecte: true }));
}

function clearSession() {
  localStorage.removeItem(SESSION_KEY);
}

function isConnecte() {
  const session = getSession();
  return Boolean(session && session.connecte);
}

function getAuthRedirectPath(page) {
  const inPages = window.location.pathname.includes("/pages/");
  if (page === "connexion") {
    return inPages ? "connexion.html" : "pages/connexion.html";
  }
  if (page === "accueil") {
    return inPages ? "../index.html" : "index.html";
  }
  if (page === "profil") {
    return inPages ? "profil.html" : "pages/profil.html";
  }
  if (page === "messagerie") {
    return inPages ? "messagerie.html" : "pages/messagerie.html";
  }
  return inPages ? "../index.html" : "index.html";
}

function requireAuth() {
  if (isConnecte()) {
    return true;
  }
  window.location.href = getAuthRedirectPath("connexion");
  return false;
}

function redirectIfConnecte() {
  if (isConnecte()) {
    window.location.href = getAuthRedirectPath("accueil");
  }
}

function initNavbarAuth() {
  const authButtons = document.getElementById("auth-buttons");
  const authUser = document.getElementById("auth-user");
  const userName = document.querySelector(".nav-user-name");
  const logoutBtn = document.getElementById("btn-deconnexion");
  const navLinks = document.querySelector(".nav-links");

  if (!authButtons && !authUser) {
    return;
  }

  const session = getSession();
  const inPages = window.location.pathname.includes("/pages/");
  const pathName = window.location.pathname.split("/").pop() || "index.html";

  if (session && session.connecte) {
    authButtons?.classList.add("d-none");
    authUser?.classList.remove("d-none");

    // Reconstruire les liens de nav pour utilisateur connecté
    if (navLinks) {
      const accueilHref = inPages ? "../index.html" : "index.html";
      const correspHref = inPages ? "correspondances.html" : "pages/correspondances.html";
      const offresHref = inPages ? "offres.html" : "pages/offres.html";
      const messagerieHref = getAuthRedirectPath("messagerie");

      const isAccueil = pathName === "index.html" || pathName === "";
      const isCorresp = pathName === "correspondances.html";
      const isOffres = pathName === "offres.html";
      const isMessages = pathName === "messagerie.html";

      navLinks.innerHTML = `
        <a href="${accueilHref}" class="nav-link ${isAccueil ? 'active' : ''}" data-tooltip="Accueil">
          <i data-lucide="home" class="nav-icon"></i>
          <span class="nav-text">Accueil</span>
        </a>
        <a href="${correspHref}" class="nav-link ${isCorresp ? 'active' : ''}" data-tooltip="Correspondances">
          <i data-lucide="handshake" class="nav-icon"></i>
          <span class="nav-text">Correspondances</span>
        </a>
        <a href="${offresHref}" class="nav-link ${isOffres ? 'active' : ''}" data-tooltip="Offres & Demandes">
          <i data-lucide="clipboard-list" class="nav-icon"></i>
          <span class="nav-text">Offres & Demandes</span>
        </a>
        <a href="${messagerieHref}" class="nav-link ${isMessages ? 'active' : ''}" id="nav-link-messagerie" data-tooltip="Messages">
          <i data-lucide="message-circle" class="nav-icon"></i>
          <span class="nav-text">Messages</span>
        </a>
      `;

      // Lancer la logique de notification de fond
      fetchInitialNotificationsCount();
      connectNotifications();
    }

    if (userName) {
      userName.textContent = session.prenom
        ? `${session.prenom} ${session.nom || ""}`.trim()
        : session.email || "Utilisateur";
      userName.style.cursor = "pointer";
      userName.style.textDecoration = "none";
      userName.style.color = "var(--blue-medium)";
      userName.style.fontWeight = "600";
      userName.addEventListener("click", function () {
        window.location.href = getAuthRedirectPath("profil");
      });
      userName.addEventListener("mouseover", function () {
        userName.style.color = "var(--blue-dark)";
      });
      userName.addEventListener("mouseout", function () {
        userName.style.color = "var(--blue-medium)";
      });
    }

    // Initialiser le dashboard sur la page d'accueil
    initDashboard(session);
  } else {
    authButtons?.classList.remove("d-none");
    authUser?.classList.add("d-none");

    // Utilisateur non connecté: masquer les nav-links, garder seulement Connexion/Inscription
    if (navLinks) {
      navLinks.innerHTML = "";
    }
  }

  if (logoutBtn) {
    logoutBtn.addEventListener("click", async function () {
      try {
        await fetch(`${API_BASE}/accounts/api/logout/`, { method: 'POST', credentials: 'include' });
      } catch (e) {
        console.error("Logout API failed", e);
      }
      clearSession();
      window.location.href = getAuthRedirectPath("accueil");
    });
  }
}

async function connecterUtilisateur(email, motDePasse) {
  try {
    const response = await fetch(`${API_BASE}/accounts/api/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password: motDePasse }),
      credentials: "include"
    });
    const data = await response.json();
    if (data.ok) {
      setSession(data.user);
      return { ok: true };
    } else {
      return { ok: false, message: data.message || "Identifiants incorrects." };
    }
  } catch (error) {
    return { ok: false, message: "Erreur de connexion au serveur backend." };
  }
}

async function inscrireUtilisateur(donnees) {
  try {
    const response = await fetch(`${API_BASE}/accounts/api/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(donnees),
      credentials: "include"
    });
    const data = await response.json();
    if (data.ok) {
      setSession(data.user);
      return { ok: true };
    } else {
      return { ok: false, message: data.message || "Erreur d'inscription." };
    }
  } catch (error) {
    return { ok: false, message: "Erreur de connexion au serveur backend." };
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const navToggle = document.querySelector(".nav-toggle");

  if (navToggle) {
    navToggle.addEventListener("click", function () {
      const navActions = document.querySelector(".nav-actions");
      if (navActions) {
        const isOpen = navActions.classList.toggle("open");
        navToggle.setAttribute("aria-expanded", String(isOpen));
      }
    });
  }

  initNavbarAuth();
  initConnexionPage();
  initInscriptionPage();
  initOffresPage();

  if (window.lucide && typeof window.lucide.createIcons === "function") {
    window.lucide.createIcons();
  }
});

function initConnexionPage() {
  const form = document.getElementById("form-connexion");
  if (!form) {
    return;
  }

  redirectIfConnecte();

  const toggleBtn = document.getElementById("toggle-mdp");
  const champMdp = document.getElementById("mot-de-passe");
  if (toggleBtn && champMdp) {
    toggleBtn.addEventListener("click", function () {
      const visible = champMdp.type === "text";
      champMdp.type = visible ? "password" : "text";
      toggleBtn.setAttribute(
        "aria-label",
        visible ? "Afficher le mot de passe" : "Masquer le mot de passe",
      );
      toggleBtn.innerHTML = visible
        ? '<i data-lucide="eye"></i>'
        : '<i data-lucide="eye-off"></i>';
      window.lucide?.createIcons();
    });
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    const email = document.getElementById("email").value.trim();
    const mdp = document.getElementById("mot-de-passe").value;
    const erreur = document.getElementById("erreur-connexion");

    if (!email || !mdp) {
      erreur.textContent = "Veuillez remplir tous les champs.";
      return;
    }

    const resultat = await connecterUtilisateur(email, mdp);
    if (!resultat.ok) {
      erreur.textContent = resultat.message;
      return;
    }

    erreur.textContent = "";
    window.location.href = getAuthRedirectPath("accueil");
  });
}
function initInscriptionPage() {
  const form = document.getElementById("form-inscription");
  if (!form) {
    return;
  }

  redirectIfConnecte();

  let etapeActuelle = 1;
  const totalEtapes = 3;

  // Configuration niveau
  const niveauInput = document.getElementById("niveau");
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
  const fortsContainer = document.getElementById("points-forts-chips");
  const faiblesContainer = document.getElementById("points-faibles-chips");

  if (fortsContainer && faiblesContainer) {
    fortsContainer.innerHTML = PREDEFINED_MATIERES.map(m => `
      <button type="button" class="chip chip-fort" data-value="${m}">
        <span class="chip-text">${m}</span>
      </button>
    `).join("");

    faiblesContainer.innerHTML = PREDEFINED_MATIERES.map(m => `
      <button type="button" class="chip chip-faible" data-value="${m}">
        <span class="chip-text">${m}</span>
      </button>
    `).join("");

    fortsContainer.querySelectorAll(".chip").forEach(chip => {
      chip.addEventListener("click", function() {
        this.classList.toggle("active");
        const val = this.dataset.value;
        if (this.classList.contains("active")) {
          // Décocher en faible
          const corresp = faiblesContainer.querySelector(`.chip[data-value="${val}"]`);
          if (corresp) corresp.classList.remove("active");
        }
      });
    });

    faiblesContainer.querySelectorAll(".chip").forEach(chip => {
      chip.addEventListener("click", function() {
        this.classList.toggle("active");
        const val = this.dataset.value;
        if (this.classList.contains("active")) {
          // Décocher en fort
          const corresp = fortsContainer.querySelector(`.chip[data-value="${val}"]`);
          if (corresp) corresp.classList.remove("active");
        }
      });
    });
  }

  function allerEtape(n) {
    for (let i = 1; i <= totalEtapes; i++) {
      document.getElementById("step-" + i).classList.remove("active-step");
    }
    document.getElementById("step-" + n).classList.add("active-step");

    for (let i = 1; i <= totalEtapes; i++) {
      const point = document.getElementById("point-" + i);
      point.classList.remove("active", "complete");
      if (i < n) point.classList.add("complete");
      if (i === n) point.classList.add("active");
    }

    for (let i = 1; i < totalEtapes; i++) {
      const trait = document.getElementById("trait-" + i);
      trait.classList.toggle("complete", i < n);
    }

    window.lucide?.createIcons();
    etapeActuelle = n;
  }

  function validerEtape1() {
    const nom = document.getElementById("nom").value.trim();
    const prenom = document.getElementById("prenom").value.trim();
    const email = document.getElementById("email").value.trim();
    const tel = document.getElementById("telephone").value.trim();
    const mdp = document.getElementById("mot-de-passe").value;
    const erreur = document.getElementById("erreur-1");

    if (!nom || !prenom || !email || !tel || !mdp) {
      erreur.textContent = "Veuillez remplir tous les champs.";
      return false;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      erreur.textContent = "Adresse e-mail invalide.";
      return false;
    }
    if (mdp.length < 6) {
      erreur.textContent = "Le mot de passe doit contenir au moins 6 caractères.";
      return false;
    }
    erreur.textContent = "";
    return true;
  }

  function validerEtape2() {
    const filiere = document.getElementById("filiere").value;
    const niveau = document.getElementById("niveau").value;
    const erreur = document.getElementById("erreur-2");

    if (!filiere) {
      erreur.textContent = "Veuillez sélectionner une filière.";
      return false;
    }
    if (!niveau) {
      erreur.textContent = "Veuillez sélectionner un niveau d'études.";
      return false;
    }
    erreur.textContent = "";
    return true;
  }

  const toggleBtn = document.getElementById("toggle-mdp");
  const champMdp = document.getElementById("mot-de-passe");
  if (toggleBtn && champMdp) {
    toggleBtn.addEventListener("click", function () {
      const visible = champMdp.type === "text";
      champMdp.type = visible ? "password" : "text";
      toggleBtn.innerHTML = visible
        ? '<i data-lucide="eye"></i>'
        : '<i data-lucide="eye-off"></i>';
      window.lucide?.createIcons();
    });
  }

  document.getElementById("btn-suivant-1").addEventListener("click", function () {
    if (validerEtape1()) allerEtape(2);
  });

  document.getElementById("btn-retour-2").addEventListener("click", function () {
    allerEtape(1);
  });

  document.getElementById("btn-suivant-2").addEventListener("click", function () {
    if (validerEtape2()) allerEtape(3);
  });

  document.getElementById("btn-retour-3").addEventListener("click", function () {
    allerEtape(2);
  });

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    const erreur = document.getElementById("erreur-3");
    erreur.style.color = "#dc2626";
    erreur.textContent = "";

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
    const pointsForts = Array.from(fortsContainer.querySelectorAll(".chip.active")).map(c => c.dataset.value);
    const pointsFaibles = Array.from(faiblesContainer.querySelectorAll(".chip.active")).map(c => c.dataset.value);

    const donnees = {
      nom: document.getElementById("nom").value.trim(),
      prenom: document.getElementById("prenom").value.trim(),
      email: document.getElementById("email").value.trim(),
      telephone: document.getElementById("telephone").value.trim(),
      motDePasse: document.getElementById("mot-de-passe").value,
      filiere: document.getElementById("filiere").value,
      niveau: document.getElementById("niveau").value,
      disponibilites: disponibilites,
      pointsForts: pointsForts,
      pointsFaibles: pointsFaibles,
    };

    const resultat = await inscrireUtilisateur(donnees);
    if (!resultat.ok) {
      erreur.textContent = resultat.message;
      return;
    }

    erreur.style.color = "#166534";
    erreur.textContent = "Inscription réussie ! Redirection…";
    setTimeout(function () {
      window.location.href = getAuthRedirectPath("accueil");
    }, 1200);
  });
}

function initOffresPage() {
  const offerForm = document.querySelector(".offer-form");
  const offresItems = document.getElementById("offres-items");
  const filterMatiere = document.getElementById("offre-filter-matiere");
  const filterFormat = document.getElementById("offre-filter-format");
  const btnFilter = document.getElementById("btn-filter-offres");
  const btnReset = document.getElementById("btn-reset-offres");

  if (!offresItems || !offerForm) {
    return;
  }

  if (!requireAuth()) {
    return;
  }

  const PREDEFINED_MATIERES = [
    "React", "Node.js", "Python", "Java", "C++", "TypeScript", "SQL",
    "Machine Learning", "DevOps", "Cybersécurité", "Algorithmique", "UML",
    "Cloud AWS", "Linux", "GraphQL", "Statistiques"
  ];

  // Générer les puces de matières pour le formulaire
  const chipsContainer = document.getElementById("points-offres-chips");
  if (chipsContainer) {
    chipsContainer.innerHTML = PREDEFINED_MATIERES.map(m => `
      <button type="button" class="chip chip-fort" data-value="${m}">
        <span class="chip-text">${m}</span>
      </button>
    `).join("");

    chipsContainer.querySelectorAll(".chip").forEach(chip => {
      chip.addEventListener("click", function() {
        chipsContainer.querySelectorAll(".chip").forEach(c => {
          if (c !== this) c.classList.remove("active");
        });
        this.classList.toggle("active");
      });
    });
  }

  // Remplir le select de filtre de matière
  if (filterMatiere) {
    filterMatiere.innerHTML = '<option value="">Toutes les matières</option>' +
      PREDEFINED_MATIERES.map(m => `<option value="${m}">${m}</option>`).join("");
  }

  chargerEtAfficherOffres();

  offerForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    
    const activeChip = chipsContainer ? chipsContainer.querySelector(".chip.active") : null;
    const matiere = activeChip ? activeChip.dataset.value : "";
    const description = document.getElementById("input-description").value.trim();
    const format = document.getElementById("input-format").value;
    const type = document.getElementById("input-type").value;

    const errorElement = document.querySelector(".form-error");
    if (errorElement) {
      errorElement.textContent = "";
      errorElement.classList.remove("success");
    }

    // Sérialiser la grille de disponibilités
    const disponibilites = {};
    let dispoCheckedCount = 0;
    const rows = offerForm.querySelectorAll(".dispo-table tbody tr");
    rows.forEach(row => {
      const slot = row.dataset.slot;
      const checkboxes = row.querySelectorAll('input[type="checkbox"]');
      checkboxes.forEach(cb => {
        if (cb.checked) {
          dispoCheckedCount++;
          const day = cb.dataset.day;
          if (!disponibilites[day]) {
            disponibilites[day] = [];
          }
          disponibilites[day].push(slot);
        }
      });
    });

    if (!matiere) {
      if (errorElement) errorElement.textContent = "Veuillez sélectionner une matière.";
      return;
    }

    if (!description || !format || !type) {
      if (errorElement) errorElement.textContent = "Veuillez remplir tous les champs.";
      return;
    }

    if (dispoCheckedCount === 0) {
      if (errorElement) errorElement.textContent = "Veuillez cocher au moins un créneau horaire dans la grille.";
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/matching/api/create-offre/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ matiere, description, disponibilites, format, type }),
        credentials: "include"
      });
      const resData = await response.json();
      if (resData.ok) {
        chargerEtAfficherOffres();
        offerForm.reset();
        
        // Réinitialiser les chips
        if (chipsContainer) {
          chipsContainer.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
        }
        // Réinitialiser les checkboxes
        offerForm.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);

        if (errorElement) {
          errorElement.textContent = resData.message || "Publication publiée avec succès.";
          errorElement.classList.add("success");
          setTimeout(function () {
            errorElement.textContent = "";
            errorElement.classList.remove("success");
          }, 3000);
        }
      } else {
        if (errorElement) errorElement.textContent = resData.message || "Erreur de publication.";
      }
    } catch (e) {
      if (errorElement) errorElement.textContent = "Erreur de connexion au serveur.";
    }
  });

  if (btnFilter) {
    btnFilter.addEventListener("click", chargerEtAfficherOffres);
  }

  if (btnReset) {
    btnReset.addEventListener("click", function() {
      if (filterMatiere) filterMatiere.value = "";
      if (filterFormat) filterFormat.value = "";
      chargerEtAfficherOffres();
    });
  }

  async function chargerEtAfficherOffres() {
    const matiereValue = filterMatiere ? filterMatiere.value.toLowerCase() : "";
    const formatValue = filterFormat ? filterFormat.value : "";
    
    let url = `${API_BASE}/matching/api/offres/?`;
    if (matiereValue) url += `matiere=${encodeURIComponent(matiereValue)}&`;
    if (formatValue) url += `format=${encodeURIComponent(formatValue)}&`;

    try {
      const response = await fetch(url, { credentials: "include" });
      const data = await response.json();
      if (data.ok) {
        afficherOffres(data.offres);
      }
    } catch (e) {
      console.error("Failed to load offers", e);
    }
  }
}

function afficherOffres(liste) {
  const conteneur = document.getElementById("offres-items");
  if (!conteneur) {
    return;
  }

  if (liste.length === 0) {
    conteneur.innerHTML = `
      <div class="vide">
        <i data-lucide="search-x"></i>
        <p>Aucune offre ou demande trouvée</p>
      </div>`;
    window.lucide?.createIcons();
    return;
  }

  conteneur.innerHTML = liste
    .map(
      (offre) => {
        const isOffre = offre.type === 'offre';
        const typeClass = isOffre ? 'badge-offre' : 'badge-demande';
        const typeText = isOffre ? 'Offre (Mentor)' : 'Demande (Mentoré)';
        
        return `
        <article class="offre-card">
          <div class="offre-card-header">
            <div>
              <span class="badge ${typeClass}" style="margin-bottom: 8px;">${typeText}</span>
              <h3 style="margin-top: 4px; font-weight: 700; color: var(--blue-dark); font-size: 1.1rem;">${offre.matiere}</h3>
              <p class="offre-meta" style="font-size: 0.8rem; margin: 4px 0 0 0;">${offre.auteur} · ${offre.filiere}</p>
            </div>
            <span class="badge" style="background: var(--blue-xlight); color: var(--blue-dark); border: 1px solid var(--blue-light);">${offre.format}</span>
          </div>

          <p class="offre-description" style="margin: 12px 0; font-size: 0.9rem; line-height: 1.5; color: var(--text-dark);">${offre.description}</p>

          <div class="offre-card-meta" style="border-top: 1px solid var(--gray-200); padding-top: 12px; margin-bottom: 16px;">
            <div style="font-size: 0.8rem; color: var(--text-muted); display: flex; align-items: center; gap: 6px;">
              <i data-lucide="calendar" style="width: 14px; height: 14px;"></i>
              <span>${offre.disponibilites}</span>
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); display: flex; align-items: center; gap: 6px; margin-top: 6px;">
              <i data-lucide="map-pin" style="width: 14px; height: 14px;"></i>
              <span>${offre.format}</span>
            </div>
          </div>

          <button class="btn btn-primary btn-sm" style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px;" onclick="contacterUtilisateur(${offre.auteur_id})">
            <i data-lucide="message-circle" style="width: 14px; height: 14px;"></i>
            Répondre
          </button>
        </article>`;
      }
    )
    .join("");

  window.lucide?.createIcons();
}

function connectNotifications() {
  const session = getSession();
  if (!session || !session.connecte) return;

  const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
  const wsUrl = `${wsScheme}://localhost:8000/ws/notifications/`;

  console.log("Connecting background notification socket to:", wsUrl);
  const socket = new WebSocket(wsUrl);

  socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (data.type === 'notification') {
      updateNavbarBadge(data.count);
    }
  };

  socket.onclose = function () {
    // Tenter de reconnecter après 5 secondes
    setTimeout(connectNotifications, 5000);
  };
}

function updateNavbarBadge(count) {
  const navMsg = document.getElementById("nav-link-messagerie");
  if (!navMsg) return;

  let badge = document.getElementById("nav-unread-badge");
  if (count > 0) {
    if (!badge) {
      badge = document.createElement("span");
      badge.id = "nav-unread-badge";
      // Style premium pour le badge
      badge.style.background = "#3b91bc"; // var(--blue-medium)
      badge.style.color = "#ffffff";
      badge.style.fontSize = "10px";
      badge.style.fontWeight = "700";
      badge.style.borderRadius = "50%";
      badge.style.minWidth = "16px";
      badge.style.height = "16px";
      badge.style.display = "inline-flex";
      badge.style.alignItems = "center";
      badge.style.justifyContent = "center";
      badge.style.marginLeft = "6px";
      badge.style.padding = "2px";
      navMsg.appendChild(badge);
    }
    badge.textContent = count;
  } else {
    if (badge) badge.remove();
  }
}

function fetchInitialNotificationsCount() {
  fetch(`${API_BASE}/messaging/api/conversations/`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.ok && data.conversations) {
        const totalUnread = data.conversations.reduce((sum, c) => sum + c.non_lus, 0);
        updateNavbarBadge(totalUnread);
      }
    })
    .catch((err) => console.error("Initial notification fetch failed", err));
}

function contacterUtilisateur(userId) {
  fetch(`${API_BASE}/messaging/api/conversations/start/${userId}/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
  })
    .then((res) => {
      if (!res.ok) throw new Error("Erreur serveur.");
      return res.json();
    })
    .then((data) => {
      if (data.ok && data.conversation_id) {
        const inPages = window.location.pathname.includes("/pages/");
        const targetUrl = inPages ? `messagerie.html?conv=${data.conversation_id}` : `pages/messagerie.html?conv=${data.conversation_id}`;
        window.location.href = targetUrl;
      } else {
        alert("Impossible d'ouvrir la discussion : " + (data.message || "Erreur inconnue"));
      }
    })
    .catch((err) => {
      console.error("Error starting conversation:", err);
      alert("Erreur de connexion : " + err.message);
    });
}

function initDashboard(session) {
  // Dashboard uniquement sur la page d'accueil
  const pathName = window.location.pathname.split("/").pop() || "index.html";
  if (pathName !== "index.html" && pathName !== "") return;

  const dashboardSection = document.getElementById("dashboard-section");
  const heroSection = document.querySelector(".hero");
  const howItWorksSection = document.querySelector(".how-it-works");
  const navCardsSection = document.querySelector(".nav-cards");

  if (!dashboardSection) return;

  if (session && session.connecte) {
    // Masquer les sections publiques
    if (heroSection) heroSection.style.display = "none";
    if (howItWorksSection) howItWorksSection.style.display = "none";
    if (navCardsSection) navCardsSection.style.display = "none";

    // Afficher le dashboard
    dashboardSection.classList.add("active");

    // Personnaliser l'en-tête
    const dashName = document.getElementById("dashboard-user-name");
    if (dashName) {
      dashName.textContent = session.prenom || session.email || "Utilisateur";
    }

    // Récupérer les statistiques depuis l'API
    fetchDashboardStats();
  }
}

async function fetchDashboardStats() {
  // Récupérer le nombre de messages non lus
  try {
    const convRes = await fetch(`${API_BASE}/messaging/api/conversations/`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    });
    const convData = await convRes.json();
    if (convData.ok && convData.conversations) {
      const totalUnread = convData.conversations.reduce((sum, c) => sum + c.non_lus, 0);
      const totalConversations = convData.conversations.length;
      const unreadEl = document.getElementById("stat-unread");
      const convEl = document.getElementById("stat-conversations");
      if (unreadEl) unreadEl.textContent = totalUnread;
      if (convEl) convEl.textContent = totalConversations;
    }
  } catch (e) {
    console.error("Dashboard stats fetch failed:", e);
  }

  // Récupérer le nombre d'offres
  try {
    const offresRes = await fetch(`${API_BASE}/matching/api/offres/`, {
      credentials: "include",
    });
    const offresData = await offresRes.json();
    if (offresData.ok && offresData.offres) {
      const offresEl = document.getElementById("stat-offres");
      if (offresEl) offresEl.textContent = offresData.offres.length;
    }
  } catch (e) {
    console.error("Dashboard offres fetch failed:", e);
  }
}
