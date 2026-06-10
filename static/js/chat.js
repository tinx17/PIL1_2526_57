/**
 * IFRI_MentorLink — chat.js
 * Logique client WebSocket pour la messagerie instantanée en temps réel.
 * Gère la reconnexion automatique.
 */

document.addEventListener('DOMContentLoaded', function() {
    const chatWrapper = document.getElementById('chat-wrapper');
    if (!chatWrapper) return;

    const conversationId = chatWrapper.dataset.conversationId;
    const userId = parseInt(chatWrapper.dataset.userId);

    const messagesBox = document.getElementById('chat-messages-box');
    const inputField = document.getElementById('chat-input-field');
    const sendBtn = document.getElementById('chat-send-btn');
    const noMessagesPrompt = document.getElementById('no-messages-prompt');

    let chatSocket = null;
    let reconnectInterval = 3000; // 3 secondes

    // Faire défiler automatiquement vers le bas
    scrollToBottom();

    // Connexion au WebSocket
    function connect() {
        const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
        const wsPath = `${wsScheme}://${window.location.host}/ws/chat/${conversationId}/`;

        console.log(`Tentative de connexion WebSocket à : ${wsPath}`);
        chatSocket = new WebSocket(wsPath);

        chatSocket.onopen = function(e) {
            console.log('Connexion WebSocket établie avec succès !');
        };

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            
            // Supprimer le prompt de départ s'il existe
            if (noMessagesPrompt) {
                noMessagesPrompt.remove();
            }

            // Créer la bulle de message
            const isSentByMe = data.auteur_id === userId;
            const bubble = document.createElement('div');
            bubble.className = `chat-bubble ${isSentByMe ? 'sent' : 'received'}`;
            bubble.id = `msg-${data.message_id}`;

            bubble.innerHTML = `
                <div class="bubble-content">${escapeHTML(data.message)}</div>
                <div class="bubble-meta">${data.date}</div>
            `;

            messagesBox.appendChild(bubble);
            scrollToBottom();
        };

        chatSocket.onclose = function(e) {
            console.warn('Le canal WebSocket de discussion a été fermé. Tentative de reconnexion...');
            setTimeout(function() {
                connect();
            }, reconnectInterval);
        };

        chatSocket.onerror = function(err) {
            console.error('Erreur WebSocket de discussion : ', err);
            chatSocket.close();
        };
    }

    // Lancer la première connexion
    connect();

    // Envoi du message
    function sendMessage() {
        const messageText = inputField.value.trim();
        if (!messageText) return;

        if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.send(JSON.stringify({
                'message': messageText
            }));
            inputField.value = '';
            inputField.focus();
        } else {
            alert("Erreur de connexion : le message n'a pas pu être envoyé. Tentative de reconnexion en cours...");
        }
    }

    // Événement clic sur le bouton envoyer
    sendBtn.addEventListener('click', sendMessage);

    // Événement touche Entrée dans le champ de saisie
    inputField.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Fonction utilitaire de défilement vers le bas
    function scrollToBottom() {
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    // Sécurisation basique contre les injections XSS
    function escapeHTML(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
