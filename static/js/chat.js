/**
 * IFRI MentorLink — Moteur de Messagerie Instantanée (Spécification Technique)
 * 
 * Ce script gère l'extraction des données du DOM, la publication de messages dans
 * Supabase, l'écoute en temps réel des nouveautés et l'injection dynamique
 * des bulles de discussion en respectant la charte graphique CSS de l'application.
 */

(function () {
    'use strict';

    // --- 1. CONFIGURATION DES IDENTIFIANTS SUPABASE ---
    // À remplacer par vos véritables identifiants de projet Supabase
    const SUPABASE_URL = "https://supabase.co"; 
    const SUPABASE_ANON_KEY = "votre-cle-anonyme-supabase";

    if (!window.supabase) {
        console.error("[MentorLink] Le SDK Supabase est introuvable. Chargement arrêté.");
        return;
    }

    // Initialisation du client Supabase
    const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

    // --- 2. SÉLECTION DES ÉLÉMENTS DU DOM ---
    const metadataNode = document.getElementById('chat-metadata');
    const chatBody = document.getElementById('chat-messages-container');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');

    if (!metadataNode || !chatBody || !chatForm || !messageInput) {
        console.warn("[MentorLink] Certains éléments requis sont absents du DOM actuel.");
        return;
    }

    // --- 3. RÉCUPÉRATION DU CONTEXTE APPLICATIF (Spécification 1) ---
    const context = {
        userId:         metadataNode.getAttribute('data-user-id'),
        roomId:         metadataNode.getAttribute('data-room-id'),
        userInitials:   metadataNode.getAttribute('data-user-initials') || 'ML',
        userAvatar:     metadataNode.getAttribute('data-user-avatar') || '',
        targetInitials: metadataNode.getAttribute('data-target-initials') || 'DM',
        targetAvatar:   metadataNode.getAttribute('data-target-avatar') || ''
    };

    /**
     * Force le défilement automatique du conteneur vers le bas.
     * (Spécification 5)
     */
    function performAutoScroll() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    /**
     * Sécurise le contenu textuel pour bloquer les failles XSS.
     */
    function sanitizeText(text) {
        const shield = document.createElement('div');
        shield.innerText = text;
        return shield.innerHTML;
    }

    /**
     * Crée et injecte dynamiquement la structure HTML d'une bulle de message.
     * (Spécification 4 & 5)
     */
    function injectMessageBubble(msg) {
        // Supprime le conteneur de chat vide s'il existe à l'écran
        const emptyStatePlaceholder = chatBody.querySelector('.empty-chat');
        if (emptyStatePlaceholder) {
            emptyStatePlaceholder.remove();
        }

        // Identification de l'expéditeur pour l'affichage visuel (Spécification 5)
        const isMe = String(msg.sender_id) === String(context.userId);
        const dynamicClass = isMe ? 'moi' : 'autre';

        // Association des bonnes métadonnées d'avatar
        const resolvedAvatar = isMe ? context.userAvatar : context.targetAvatar;
        const resolvedInitials = isMe ? context.userInitials : context.targetInitials;

        // Formatage de l'horodatage en format 24h (HH:MM)
        const parseTimestamp = msg.created_at ? new Date(msg.created_at) : new Date();
        const displayTime = parseTimestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        // Création du conteneur parent .message-row
        const messageRow = document.createElement('div');
        messageRow.className = `message-row ${dynamicClass}`;

        // Construction du bloc avatar ou initiales textuelles
        const avatarHTML = resolvedAvatar 
            ? `<img src="${resolvedAvatar}" alt="Profil">` 
            : `<span>${resolvedInitials}</span>`;

        // Injection du balisage CSS exact du fichier HTML
        messageRow.innerHTML = `
            <div class="mini-avatar ${dynamicClass}">
                ${avatarHTML}
            </div>
            <div class="bubble ${dynamicClass}">
                ${sanitizeText(msg.content)}
                <div class="bubble-time">${displayTime}</div>
            </div>
        `;

        // Ajout final au DOM et défilement de l'écran
        chatBody.appendChild(messageRow);
        performAutoScroll();
    }

    // --- 4. GESTIONNAIRE D'ENVOI ET VALIDATION (Spécification 2 & 3) ---
    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Annule le rafraîchissement natif de la page

        const rawContent = messageInput.value.trim();

        // Spécification 5 : Blocage si la chaîne est vide
        if (!rawContent) return;

        // Réinitialisation de l'interface et focus instantané
        messageInput.value = '';
        messageInput.focus();
        messageInput.style.height = '44px'; // Reset de la hauteur suite à l'auto-resize

        try {
            // Insertion asynchrone dans la table des messages de Supabase
            const { error } = await supabaseClient
                .from('messages')
                .insert([
                    {
                        room_id: context.roomId,
                        sender_id: context.userId,
                        content: rawContent
                    }
                ]);

            if (error) throw error;

        } catch (err) {
            console.error("[Supabase] Erreur d'envoi du message :", err.message);
            alert("Impossible d'envoyer le message pour le moment. Veuillez réessayer.");
        }
    });

    // Envoi via la touche "Entrée" (sauf si la touche Maj est pressée)
    messageInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            chatForm.requestSubmit();
        }
    });

    // Ajustement automatique de la hauteur du champ selon la longueur du texte
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // --- 5. SYNCHRONISATION EN TEMPS RÉEL (Spécification 3) ---
    function initializeRealtimeStream() {
        if (!context.roomId) return;

        supabaseClient
            .channel(`room_stream_${context.roomId}`)
            .on(
                'postgres_changes',
                {
                    event: 'INSERT',
                    schema: 'public',
                    table: 'messages',
                    filter: `room_id=eq.${context.roomId}` // Écoute filtrée sur cette discussion
                },
                (payload) => {
                    // Réception et traitement immédiat du nouveau message
                    injectMessageBubble(payload.new);
                }
            )
            .subscribe((connectionStatus) => {
                if (connectionStatus === 'SUBSCRIBED') {
                    console.log(`[MentorLink] Flux temps réel connecté sur la room : ${context.roomId}`);
                }
            });
    }

    // --- 6. DEMARRAGE AU CHARGEMENT ---
    document.addEventListener('DOMContentLoaded', () => {
        performAutoScroll();
        initializeRealtimeStream();
    });

})();
