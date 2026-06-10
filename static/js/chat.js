/**
 * IFRI MentorLink - Messagerie (avec notifications)
 */

document.addEventListener("DOMContentLoaded", () => {
    const workspaceCard = document.getElementById("chatWorkspaceCard");
    if (!workspaceCard) return;

    const chatBodyStream = document.getElementById("chatBodyStream");
    const messageInput = document.getElementById("chatMessageInput");
    const charCounter = document.getElementById("charCounter");
    const btnSend = document.getElementById("btnSendMessage");

    const currentUserId = parseInt(workspaceCard.dataset.expediteurId);
    const activeDestinataireId = parseInt(workspaceCard.dataset.destinataireId);
    const MAX_CHARS = 2000;

    let lastMessageId = null;
    let isSending = false;

    // Demander la permission pour les notifications
    if (Notification.permission === "default") {
        Notification.requestPermission();
    }

    function showNotification(message, senderName) {
        if (Notification.permission === "granted" && document.hidden) {
            new Notification("💬 Nouveau message de " + senderName, {
                body: message.substring(0, 100),
                icon: "/static/img/IFRI MentorLink.png"
            });
        }
    }

    function performAutoscroll() {
        chatBodyStream.scrollTop = chatBodyStream.scrollHeight;
    }
    performAutoscroll();

    async function checkNewMessages() {
        try {
            const response = await fetch(`/messagerie/api/nouveaux_messages?depuis=${lastMessageId || ''}&avec=${activeDestinataireId}`);
            const data = await response.json();
            
            if (data.success && data.messages && data.messages.length > 0) {
                for (const msg of data.messages) {
                    const existingMsg = document.querySelector(`.msg-row[data-message-id="${msg.id}"]`);
                    if (!existingMsg) {
                        appendMessageToChat(msg);
                        if (msg.expediteur_id !== currentUserId && !document.hasFocus()) {
                            showNotification(msg.contenu, msg.prenom_expediteur || "Quelqu'un");
                        }
                    }
                    if (msg.id > (lastMessageId || 0)) {
                        lastMessageId = msg.id;
                    }
                }
                performAutoscroll();
            }
        } catch (err) {
            console.error("Erreur polling:", err);
        }
    }

    function appendMessageToChat(msg, isTemp = false) {
        if (msg.id && document.querySelector(`.msg-row[data-message-id="${msg.id}"]`)) {
            return;
        }

        const emptyState = chatBodyStream.querySelector('.empty-stream-state');
        if (emptyState) emptyState.remove();

        const isSent = (msg.expediteur_id === currentUserId);
        const date = msg.date_envoi ? new Date(msg.date_envoi) : new Date();
        const formattedTime = String(date.getHours()).padStart(2, '0') + ':' + String(date.getMinutes()).padStart(2, '0');

        const msgDiv = document.createElement('div');
        msgDiv.className = `msg-row ${isSent ? 'sent' : 'received'}`;
        if (msg.id) {
            msgDiv.setAttribute('data-message-id', msg.id);
        }
        if (isTemp) {
            msgDiv.setAttribute('data-temp', 'true');
        }
        msgDiv.innerHTML = `
            <div class="msg-bubble">
                ${escapeHtml(msg.contenu)}
                <span class="msg-timestamp">${formattedTime}</span>
            </div>
        `;
        chatBodyStream.appendChild(msgDiv);
    }

    async function loadInitialMessages() {
        try {
            const response = await fetch(`/messagerie/api/historique?avec=${activeDestinataireId}`);
            const data = await response.json();
            
            if (data.success && data.messages) {
                chatBodyStream.innerHTML = '';
                for (const msg of data.messages) {
                    appendMessageToChat(msg);
                    if (msg.id > (lastMessageId || 0)) {
                        lastMessageId = msg.id;
                    }
                }
                performAutoscroll();
            }
        } catch (err) {
            console.error("Erreur chargement historique:", err);
        }
    }

    messageInput.addEventListener("input", function() {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
        const remainingChars = MAX_CHARS - this.value.length;
        charCounter.textContent = `${remainingChars} caractères restants`;
        charCounter.style.color = remainingChars < 100 ? "#dc3545" : "";
    });

    async function sendMessage() {
        const rawContent = messageInput.value.trim();
        if (!rawContent) return;
        if (isSending) return;

        isSending = true;
        messageInput.disabled = true;
        btnSend.disabled = true;

        const tempMsg = {
            id: null,
            expediteur_id: currentUserId,
            destinataire_id: activeDestinataireId,
            contenu: rawContent,
            date_envoi: new Date().toISOString()
        };
        appendMessageToChat(tempMsg, true);
        performAutoscroll();

        try {
            const response = await fetch('/messagerie/api/envoyer', {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    destinataire_id: activeDestinataireId,
                    contenu: rawContent
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                const tempDiv = chatBodyStream.querySelector('.msg-row[data-temp="true"]');
                if (tempDiv) tempDiv.remove();
                
                const realMsg = {
                    id: data.message_id,
                    expediteur_id: currentUserId,
                    destinataire_id: activeDestinataireId,
                    contenu: rawContent,
                    date_envoi: data.date_envoi || new Date().toISOString()
                };
                appendMessageToChat(realMsg);
                if (realMsg.id > (lastMessageId || 0)) {
                    lastMessageId = realMsg.id;
                }
                performAutoscroll();
                
                messageInput.value = "";
                messageInput.style.height = "auto";
                charCounter.textContent = `${MAX_CHARS} caractères restants`;
            } else {
                const tempDiv = chatBodyStream.querySelector('.msg-row[data-temp="true"]');
                if (tempDiv) tempDiv.remove();
                alert(`Erreur : ${data.erreur || 'Échec de l\'envoi'}`);
            }
        } catch (err) {
            console.error("Erreur réseau:", err);
            const tempDiv = chatBodyStream.querySelector('.msg-row[data-temp="true"]');
            if (tempDiv) tempDiv.remove();
            alert("Erreur de connexion. Votre message n'a pas été envoyé.");
        } finally {
            isSending = false;
            messageInput.disabled = false;
            btnSend.disabled = false;
            messageInput.focus();
        }
    }

    btnSend.addEventListener("click", sendMessage);
    messageInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, (m) => map[m]);
    }

    loadInitialMessages();
    setInterval(checkNewMessages, 3000);
});