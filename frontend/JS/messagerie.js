// Logique de messagerie instantanée en temps réel
document.addEventListener("DOMContentLoaded", function () {
  const conversationList = document.getElementById("conversation-list");
  const chatPanel = document.getElementById("chat-panel");
  const chatActive = document.getElementById("chat-active");
  const chatEmpty = document.getElementById("chat-empty");
  const activeAvatar = document.getElementById("active-avatar");
  const activeName = document.getElementById("active-name");
  const messagesBox = document.getElementById("chat-messages-box");
  const inputField = document.getElementById("chat-input-field");
  const sendBtn = document.getElementById("chat-send-btn");
  const backBtn = document.getElementById("btn-back-conversations");
  const discussionsPanel = document.getElementById("discussions-panel");

  let activeSocket = null;
  let activeConversationId = null;
  let currentUserId = null;

  // Détecter si on est sur mobile
  function isMobile() {
    return window.innerWidth <= 768;
  }

  // Initialisation responsive
  function initResponsive() {
    if (isMobile()) {
      backBtn.classList.remove("d-none");
      if (activeConversationId) {
        discussionsPanel.classList.add("d-none");
        chatPanel.classList.remove("d-none");
      } else {
        discussionsPanel.classList.remove("d-none");
        chatPanel.classList.add("d-none");
      }
    } else {
      backBtn.classList.add("d-none");
      discussionsPanel.classList.remove("d-none");
      chatPanel.classList.remove("d-none");
    }
  }

  window.addEventListener("resize", initResponsive);

  backBtn.addEventListener("click", function () {
    activeConversationId = null;
    document.querySelectorAll(".conversation-item").forEach((item) => {
      item.classList.remove("active");
    });
    if (activeSocket) {
      activeSocket.close();
      activeSocket = null;
    }
    initResponsive();
  });

  // Charger les conversations
  function chargerConversations(selectId = null) {
    fetch(`${API_BASE}/messaging/api/conversations/`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    })
      .then((res) => {
        if (!res.ok) throw new Error("Erreur de récupération.");
        return res.json();
      })
      .then((data) => {
        if (data.ok && data.conversations) {
          renderConversations(data.conversations, selectId);
        }
      })
      .catch((err) => {
        console.error("Erreur conversations:", err);
      });
  }

  function renderConversations(conversations, selectId) {
    if (conversations.length === 0) {
      conversationList.innerHTML = `
        <div style="text-align:center; padding: 40px 10px; color: var(--text-muted);">
          <p style="font-size:14px;">Aucune conversation active.</p>
        </div>
      `;
      return;
    }

    conversationList.innerHTML = conversations
      .map((c) => {
        const autre = c.autre_participant;
        const initiales = (autre.prenom.charAt(0) + autre.nom.charAt(0)).toUpperCase();
        const dernierMsg = c.dernier_message ? c.dernier_message.contenu : "Commencez la discussion !";
        const dateStr = c.dernier_message ? c.dernier_message.date : "";
        const unreadBadge = c.non_lus > 0 ? `<div class="conv-unread-badge">${c.non_lus}</div>` : "";
        const activeClass = selectId && Number(selectId) === c.id ? "active" : "";
        const unreadClass = c.non_lus > 0 ? "unread" : "";

        return `
          <div class="conversation-item ${activeClass} ${unreadClass}" data-id="${c.id}" data-name="${autre.prenom} ${autre.nom}" data-initiales="${initiales}">
            <div class="conv-avatar">${initiales}</div>
            <div class="conv-info">
              <div class="conv-name">${autre.prenom} ${autre.nom}</div>
              <div class="conv-preview">${dernierMsg}</div>
            </div>
            <div class="conv-meta">
              <div class="conv-time">${dateStr}</div>
              ${unreadBadge}
            </div>
          </div>
        `;
      })
      .join("");

    // Attacher les écouteurs de clic
    document.querySelectorAll(".conversation-item").forEach((item) => {
      item.addEventListener("click", function () {
        const id = this.getAttribute("data-id");
        ouvrirConversation(id);
      });
    });

    if (selectId) {
      const activeItem = document.querySelector(`.conversation-item[data-id="${selectId}"]`);
      if (activeItem) {
        activeItem.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }
  }

  function ouvrirConversation(id) {
    if (activeSocket) {
      activeSocket.close();
      activeSocket = null;
    }

    activeConversationId = id;

    // Activer l'élément dans la liste
    document.querySelectorAll(".conversation-item").forEach((item) => {
      item.classList.remove("active");
      if (item.getAttribute("data-id") === String(id)) {
        item.classList.add("active");
        // Enlever la classe unread et le badge
        item.classList.remove("unread");
        const badge = item.querySelector(".conv-unread-badge");
        if (badge) badge.remove();
      }
    });

    // Afficher la fenêtre active
    chatEmpty.classList.add("d-none");
    chatActive.classList.remove("d-none");

    initResponsive();

    // Récupérer les messages
    fetch(`${API_BASE}/messaging/api/conversations/${id}/messages/`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.ok && data.messages) {
          currentUserId = data.user_id;
          activeName.textContent = `${data.autre_participant.prenom} ${data.autre_participant.nom}`;
          activeAvatar.textContent = (data.autre_participant.prenom.charAt(0) + data.autre_participant.nom.charAt(0)).toUpperCase();

          renderMessages(data.messages);
          connectWebSocket(id);
        }
      })
      .catch((err) => {
        console.error("Erreur messages:", err);
      });
  }

  function renderMessages(messages) {
    if (messages.length === 0) {
      messagesBox.innerHTML = `
        <div id="no-messages-prompt" style="text-align: center; color: var(--text-muted); padding: 2rem; font-style: italic;">
          Aucun message dans cette discussion. Envoyez le premier message !
        </div>
      `;
      return;
    }

    messagesBox.innerHTML = messages
      .map((m) => {
        const bubbleClass = m.auteur_id === currentUserId ? "sent" : "received";
        return `
          <div class="chat-bubble ${bubbleClass}">
            <div class="bubble-content">${m.contenu}</div>
            <div class="bubble-meta">${m.date}</div>
          </div>
        `;
      })
      .join("");

    scrollToBottom();
  }

  function scrollToBottom() {
    messagesBox.scrollTop = messagesBox.scrollHeight;
  }

  function connectWebSocket(id) {
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    // Connecter directement au backend Django sur le port 8000
    const wsUrl = `${wsScheme}://localhost:8000/ws/chat/${id}/`;

    console.log("WebSocket connecting to:", wsUrl);
    activeSocket = new WebSocket(wsUrl);

    activeSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      if (data.type === "chat_message") {
        // Enlever le message d'invitation si présent
        const prompt = document.getElementById("no-messages-prompt");
        if (prompt) prompt.remove();

        const bubbleClass = data.auteur_id === currentUserId ? "sent" : "received";
        const bubbleHtml = `
          <div class="chat-bubble ${bubbleClass}">
            <div class="bubble-content">${data.message}</div>
            <div class="bubble-meta">${data.date}</div>
          </div>
        `;
        messagesBox.insertAdjacentHTML("beforeend", bubbleHtml);
        scrollToBottom();

        // Mettre à jour la prévisualisation dans la liste à gauche
        const item = document.querySelector(`.conversation-item[data-id="${id}"]`);
        if (item) {
          const preview = item.querySelector(".conv-preview");
          const time = item.querySelector(".conv-time");
          if (preview) preview.textContent = data.message;
          if (time) time.textContent = data.date.split(" ")[0]; // seulement la date ou heure
        }
      }
    };

    activeSocket.onclose = function (e) {
      console.log("WebSocket closed.");
    };

    activeSocket.onerror = function (err) {
      console.error("WebSocket error:", err);
    };
  }

  function sendMessage() {
    const text = inputField.value.trim();
    if (!text || !activeSocket) return;

    activeSocket.send(
      JSON.stringify({
        message: text,
      })
    );
    inputField.value = "";
    inputField.focus();
  }

  sendBtn.addEventListener("click", sendMessage);
  inputField.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  // Détection de redirection avec conversation_id en paramètre (?conv=ID)
  const urlParams = new URLSearchParams(window.location.search);
  const selectConvId = urlParams.get("conv");

  chargerConversations(selectConvId);
  initResponsive();

  if (selectConvId) {
    ouvrirConversation(selectConvId);
  }
});
