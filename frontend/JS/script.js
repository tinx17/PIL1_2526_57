document.addEventListener("DOMContentLoaded", function () {
  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");
  const pathName = window.location.pathname.split("/").pop();

  document.querySelectorAll(".nav-link").forEach((link) => {
    const href = link.getAttribute("href").split("/").pop();
    let isActive = href === pathName;
    if (!isActive) {
      if (pathName === "") {
        if (href === "index.html") {
          isActive = true;
        }
      }
    }
    if (isActive) {
      link.classList.add("active");
    }
  });

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      const isOpen = navLinks.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });
  }

  initOffresPage();

  if (window.lucide && typeof window.lucide.createIcons === "function") {
    window.lucide.createIcons();
  }
});

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

  afficherOffres(offres);

  offerForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const matiere = document.getElementById("input-matiere").value.trim();
    const description = document
      .getElementById("input-description")
      .value.trim();
    const disponibilites = document
      .getElementById("input-disponibilites")
      .value.trim();
    const format = document.getElementById("input-format").value;

    const errorElement = document.querySelector(".form-error");
    if (errorElement) {
      errorElement.textContent = "";
      errorElement.classList.remove("success");
    }

    if (!matiere || !description || !disponibilites || !format) {
      if (errorElement) {
        errorElement.textContent =
          "Veuillez remplir tous les champs du formulaire.";
      }
      return;
    }

    const nextId =
      offres.length > 0 ? Math.max(...offres.map((o) => o.id)) + 1 : 1;
    const nouvelleOffre = {
      id: nextId,
      auteur: "Vous",
      type: "offre",
      matiere,
      description,
      disponibilites,
      format,
      filiere: "IFRI/UAC",
    };

    offres.unshift(nouvelleOffre);
    afficherOffres(offres);
    offerForm.reset();

    if (errorElement) {
      errorElement.textContent = "Offre publiée avec succès.";
      errorElement.classList.add("success");
      setTimeout(() => {
        if (errorElement) {
          errorElement.textContent = "";
          errorElement.classList.remove("success");
        }
      }, 3000);
    }
  });

  if (btnFilter) {
    btnFilter.addEventListener("click", function () {
      filtrerOffres();
    });
  }

  if (btnReset) {
    btnReset.addEventListener("click", function () {
      reinitialiserFiltres();
    });
  }

  function filtrerOffres() {
    const matiereValue = filterMatiere ? filterMatiere.value.toLowerCase() : "";
    const formatValue = filterFormat ? filterFormat.value : "";

    const filtered = offres.filter((offre) => {
      const matchMatiere =
        matiereValue === "" ||
        offre.matiere.toLowerCase().includes(matiereValue) ||
        offre.description.toLowerCase().includes(matiereValue);
      const matchFormat = formatValue === "" || offre.format === formatValue;
      return matchMatiere && matchFormat;
    });

    afficherOffres(filtered);
  }

  function reinitialiserFiltres() {
    if (filterMatiere) filterMatiere.value = "";
    if (filterFormat) filterFormat.value = "";
    afficherOffres(offres);
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
    if (window.lucide && typeof window.lucide.createIcons === "function") {
      window.lucide.createIcons();
    }
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

  if (window.lucide && typeof window.lucide.createIcons === "function") {
    window.lucide.createIcons();
  }
}
