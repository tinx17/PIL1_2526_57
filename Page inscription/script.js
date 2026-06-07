// 1. Récupération des 3 blocs d'étapes
var etape1 = document.getElementById("step-1");
var etape2 = document.getElementById("step-2");
var etape3 = document.getElementById("step-3");

// 2. Récupération des listes de boutons Suivant et Précédent
var boutonsSuivant = document.querySelectorAll(".btn-next");
var boutonsPrecedent = document.querySelectorAll(".btn-prev");
var formulaire = document.getElementById("form-inscription");

// --- ACTIONS SUR LES BOUTONS ---

// Clic sur "Suivant" à l'étape 1
boutonsSuivant[0].addEventListener("click", function() {
    etape1.classList.remove("active-step");
    etape2.classList.add("active-step");
});

// Clic sur "Suivant" à l'étape 2
boutonsSuivant[1].addEventListener("click", function() {
    etape2.classList.remove("active-step");
    etape3.classList.add("active-step");
});

// Clic sur "Précédent" à l'étape 2
boutonsPrecedent[0].addEventListener("click", function() {
    etape2.classList.remove("active-step");
    etape1.classList.add("active-step");
});

// Clic sur "Précédent" à l'étape 3
boutonsPrecedent[1].addEventListener("click", function() {
    etape3.classList.remove("active-step");
    etape2.classList.add("active-step");
});


// --- FONCTION POUR AFFICHER/MASQUER LE MOT DE PASSE ---
function basculerMotDePasse() {
    var champPassword = document.getElementById("password");
    var iconeOeil = document.getElementById("toggle-password");

    if (champPassword.type === "password") {
        champPassword.type = "text";
        iconeOeil.classList.remove("fa-eye");
        iconeOeil.classList.add("fa-eye-slash");
    } else {
        champPassword.type = "password";
        iconeOeil.classList.remove("fa-eye-slash");
        iconeOeil.classList.add("fa-eye");
    }
}


// --- SOUMISSION FINALE DU FORMULAIRE ---
formulaire.addEventListener("submit", function(evenement) {
    evenement.preventDefault();
    alert("Inscription réussie ! Bienvenue sur IFRI MentorLink.");
});