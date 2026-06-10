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

  if (!authButtons && !authUser) {
    return;
  }

  const session = getSession();

  if (session && session.connecte) {
    authButtons?.classList.add("d-none");
    authUser?.classList.remove("d-none");
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
        userName.style.textDecoration = "underline";
      });
      userName.addEventListener("mouseout", function () {
        userName.style.color = "var(--blue-medium)";
        userName.style.textDecoration = "none";
      });
    }
  } else {
    authButtons?.classList.remove("d-none");
    authUser?.classList.add("d-none");
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
  const navLinks = document.querySelector(".nav-links");
  const pathName = window.location.pathname.split("/").pop();

  document.querySelectorAll(".nav-link").forEach((link) => {
    const href = link.getAttribute("href").split("/").pop();
    let isActive = href === pathName;
    if (!isActive && pathName === "" && href === "index.html") {
      isActive = true;
    }
    if (isActive) {
      link.classList.add("active");
    }
  });

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      const navActions = navLinks.closest(".nav-actions");
      const target = navActions || navLinks;
      const isOpen = target.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
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
      erreur.textContent =
        "Le mot de passe doit contenir au moins 6 caractères.";
      return false;
    }
    erreur.textContent = "";
    return true;
  }

  function validerEtape2() {
    const filiere = document.getElementById("filiere").value;
    const niveau = document.getElementById("niveau").value;
    const erreur = document.getElementById("erreur-2");

    if (!filiere || !niveau) {
      erreur.textContent = "Veuillez sélectionner une filière et un niveau.";
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

    const donnees = {
      nom: document.getElementById("nom").value.trim(),
      prenom: document.getElementById("prenom").value.trim(),
      email: document.getElementById("email").value.trim(),
      telephone: document.getElementById("telephone").value.trim(),
      motDePasse: document.getElementById("mot-de-passe").value,
      filiere: document.getElementById("filiere").value,
      niveau: document.getElementById("niveau").value,
      disponibilites: document.getElementById("disponibilites").value.trim(),
      pointsForts: document.getElementById("points-forts").value.trim(),
      pointsFaibles: document.getElementById("points-faibles").value.trim(),
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

  chargerEtAfficherOffres();

  offerForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    const matiere = document.getElementById("input-matiere").value.trim();
    const description = document.getElementById("input-description").value.trim();
    const disponibilites = document.getElementById("input-disponibilites").value.trim();
    const format = document.getElementById("input-format").value;

    const errorElement = document.querySelector(".form-error");
    if (errorElement) {
      errorElement.textContent = "";
      errorElement.classList.remove("success");
    }

    if (!matiere || !description || !disponibilites || !format) {
      if (errorElement) {
        errorElement.textContent = "Veuillez remplir tous les champs du formulaire.";
      }
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/matching/api/create-offre/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ matiere, description, disponibilites, format, type: 'offre' }),
        credentials: "include"
      });
      const resData = await response.json();
      if (resData.ok) {
        chargerEtAfficherOffres();
        offerForm.reset();
        if (errorElement) {
          errorElement.textContent = "Offre publiée avec succès.";
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
        <p>Aucune offre trouvée</p>
      </div>`;
    window.lucide?.createIcons();
    return;
  }

  conteneur.innerHTML = liste
    .map(
      (offre) => `
      <article class="offre-card">
        <div class="offre-card-header">
          <div>
            <h3>${offre.matiere}</h3>
            <p class="offre-meta">${offre.auteur} · ${offre.filiere}</p>
          </div>
          <span class="badge">${offre.format}</span>
        </div>

        <p class="offre-description">${offre.description}</p>

        <div class="offre-card-meta">
          <div>
            <i data-lucide="calendar"></i>
            <span>${offre.disponibilites}</span>
          </div>
          <div>
            <i data-lucide="map-pin"></i>
            <span>${offre.format}</span>
          </div>
        </div>

        <button class="btn btn-primary btn-sm">
          <i data-lucide="message-circle"></i>
          Répondre
        </button>
      </article>`,
    )
    .join("");

  window.lucide?.createIcons();
}
