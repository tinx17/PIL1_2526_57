/**
 * IFRI_MentorLink — notifications.js
 * Logique client WebSocket pour la réception des notifications de nouveaux messages en temps réel.
 * Met à jour le badge de notification sur la barre de navigation.
 */

document.addEventListener('DOMContentLoaded', function() {
    const navMessaging = document.getElementById('nav-messaging');
    if (!navMessaging) return;

    let notificationSocket = null;
    let reconnectInterval = 5000;

    function connectNotifications() {
        const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
        const wsPath = `${wsScheme}://${window.location.host}/ws/notifications/`;

        console.log(`Tentative de connexion WebSocket pour notifications à : ${wsPath}`);
        notificationSocket = new WebSocket(wsPath);

        notificationSocket.onopen = function(e) {
            console.log('Connexion WebSocket de notification active.');
        };

        notificationSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            
            if (data.type === 'notification') {
                updateBadgeCount(data.count);
                
                // Si l'utilisateur est sur la page de conversation en cours, on ne déclenche pas d'alerte visuelle externe
                const chatWrapper = document.getElementById('chat-wrapper');
                if (chatWrapper) {
                    const activeConvId = chatWrapper.dataset.conversationId;
                    if (activeConvId === String(data.conversation_id)) {
                        // Pas de notification additionnelle si on est déjà dans le salon de chat actif
                        return;
                    }
                }
                
                // Notification sonore/visuelle discrète si disponible ou autorisée
                console.log(`Nouveau message de ${data.auteur} : ${data.message}`);
            }
        };

        notificationSocket.onclose = function(e) {
            console.warn('Canal de notification fermé. Reconnexion dans 5 secondes...');
            setTimeout(function() {
                connectNotifications();
            }, reconnectInterval);
        };

        notificationSocket.onerror = function(err) {
            console.error('Erreur du canal de notification : ', err);
            notificationSocket.close();
        };
    }

    function updateBadgeCount(count) {
        let badge = document.getElementById('unread-badge');
        
        if (count > 0) {
            if (!badge) {
                badge = document.createElement('span');
                badge.className = 'badge';
                badge.id = 'unread-badge';
                navMessaging.appendChild(badge);
            }
            badge.textContent = count;
        } else {
            if (badge) {
                badge.remove();
            }
        }
    }

    // Lancer les notifications
    connectNotifications();
});
