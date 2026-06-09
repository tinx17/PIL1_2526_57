# Ce que le backend doit faire pour la page Profil

## Le principe en deux mots

La page profil est prête côté frontend.
Dès que quelqu'un ouvre la page, elle va automatiquement appeler votre serveur pour demander les infos de la personne connectée.
Votre boulot c'est de répondre à cet appel avec les bonnes données.

---

## Ce que le frontend va appeler

La page va envoyer une requête à cette adresse :

```
GET /api/utilisateurs/moi
```

Rien de plus. Pas de paramètres, pas de body. Juste un appel GET à cette route.

---

## Ce que vous devez renvoyer

Vous devez renvoyer un JSON qui ressemble exactement à ça :

```json
{
  "id": 1,
  "nom": "AHOUANDJINOU",
  "prenom": "Koffi",
  "email": "koffi@ifri.uac.bj",
  "filiere": "Génie Logiciel",
  "niveau": "Licence 1",
  "bio_courte": "Passionné par la prog...",
  "centres_interet": "Dev web, IA, Jeux vidéo",
  "points_forts": ["Algorithmique", "Python", "HTML / CSS"],
  "lacunes": ["Réseaux", "Java", "Base de données"],
  "creneaux": [
    { "jour": "lundi",    "heure_debut": "18:00", "heure_fin": "20:00" },
    { "jour": "mercredi", "heure_debut": "17:00", "heure_fin": "19:00" }
  ]
}
```

D'où viennent ces données dans la base ?

| Champ JSON       | Table base de données | Colonne          |
|------------------|-----------------------|------------------|
| nom, prenom, email, filiere, niveau, bio_courte, centres_interet | users | colonnes directes |
| points_forts     | points_forts          | colonne `matiere` (tous les enregistrements liés à cet utilisateur) |
| lacunes          | lacunes               | colonne `matiere` (tous les enregistrements liés à cet utilisateur) |
| creneaux         | users_creneaux        | colonnes `jour`, `heure_debut`, `heure_fin` |

---

## Comment savoir quel utilisateur est connecté ?

C'est vous qui gérez ça avec votre système de session ou de token.
Le frontend ne vous envoie pas l'id dans l'URL. C'est votre serveur qui sait qui est connecté et qui va chercher SES données.

Si vous utilisez des tokens JWT, le frontend peut envoyer le token dans les headers.
Dites-nous juste comment vous voulez qu'on le transmette et on s'adapte.

---

## Ce qui se passe si ça marche pas

Si votre serveur ne répond pas ou renvoie une erreur, la page affiche un message rouge à l'utilisateur.
Rien ne plante côté frontend, on gère ça proprement.

---

## En résumé

1. Créez la route `GET /api/utilisateurs/moi`
2. Elle renvoie les données de la personne connectée au format JSON ci-dessus
3. Le frontend fait le reste tout seul