const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const messages = document.getElementById("messages");
const conversationList = document.getElementById("conversationList");

let sessionId = null;
let lastAIResponse = "";


/* ============================================================
   MESSAGE UI
============================================================ */

function addMessage(sender, text, type) {

    const message = document.createElement("div");
    message.className = "message " + type;

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = sender;

    const box = document.createElement("div");
    box.className = "message-box";
    box.textContent = text;

    message.appendChild(label);
    message.appendChild(box);

    messages.appendChild(message);

    scrollToBottom();
}


/* ============================================================
   WELCOME
============================================================ */

function removeWelcome() {

    const welcome = document.getElementById("welcome");

    if (welcome) {
        welcome.remove();
    }
}


function showWelcome() {

    messages.innerHTML = "";

    const welcome = document.createElement("div");

    welcome.className = "welcome";
    welcome.id = "welcome";

    welcome.innerHTML =
        '<div class="welcome-logo">RETRO-AI</div>' +
        '<div class="welcome-subtitle">' +
        'Your classic computer-style AI assistant.' +
        '</div>' +
        '<div class="welcome-line"></div>' +
        '<p>SYSTEM READY.</p>' +
        '<br>' +
        '<span class="command-hint">' +
        'TYPE YOUR COMMAND BELOW...' +
        '</span>';

    messages.appendChild(welcome);
}


/* ============================================================
   TYPING INDICATOR
============================================================ */

function showTyping() {

    removeTyping();

    const typing = document.createElement("div");

    typing.className = "message ai";
    typing.id = "typing";

    const label = document.createElement("div");

    label.className = "message-label";
    label.textContent = "RETRO-AI";

    const box = document.createElement("div");

    box.className = "message-box";

    const dots = document.createElement("div");

    dots.className = "typing";

    for (let i = 0; i < 3; i++) {

        const dot = document.createElement("span");

        dots.appendChild(dot);
    }

    box.appendChild(dots);

    typing.appendChild(label);
    typing.appendChild(box);

    messages.appendChild(typing);

    scrollToBottom();
}


function removeTyping() {

    const typing = document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}


/* ============================================================
   SEND MESSAGE
============================================================ */

async function sendMessage() {

    const text = input.value.trim();

    if (!text) {
        return;
    }

    removeWelcome();

    addMessage(
        "YOU",
        text,
        "user"
    );

    input.value = "";

    input.disabled = true;
    sendBtn.disabled = true;

    showTyping();

    updateStatus("THINKING");

    try {

        const response = await fetch(
            "/api/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: text,
                    session_id: sessionId
                })
            }
        );

        const data = await response.json();

        removeTyping();

        if (!response.ok || !data.success) {

            throw new Error(
                data.error || "Server error"
            );
        }

        sessionId = data.session_id;

        const aiResponse =
            data.response ||
            "No response received.";

        lastAIResponse = aiResponse;

        addMessage(
            "RETRO-AI",
            aiResponse,
            "ai"
        );

        updateStatus("READY");

        await loadSessions();

    }

    catch (error) {

        removeTyping();

        /*
         * IMPORTANT:
         * Backend/system error ko chat me expose nahi karna.
         */

        addMessage(
            "RETRO-AI",
            "Sorry, I could not process that request.",
            "ai"
        );

        updateStatus("ERROR");

        console.error(
            "RETRO-AI:",
            error
        );
    }

    finally {

        input.disabled = false;
        sendBtn.disabled = false;

        input.focus();
    }
}


/* ============================================================
   CLEAR CURRENT CHAT
============================================================ */

function clearChat() {

    sessionId = null;
    lastAIResponse = "";

    showWelcome();

    updateStatus("READY");

    document
        .querySelectorAll(".conversation")
        .forEach(function (item) {
            item.classList.remove("active");
        });

    input.focus();
}


/* ============================================================
   NEW CHAT
============================================================ */

function newChat() {

    clearChat();

    input.focus();
}


/* ============================================================
   COPY LAST RESPONSE
============================================================ */

async function copyLastResponse() {

    if (!lastAIResponse) {

        alert(
            "NO AI RESPONSE AVAILABLE."
        );

        return;
    }

    try {

        await navigator.clipboard.writeText(
            lastAIResponse
        );

        alert(
            "RESPONSE COPIED."
        );

    }

    catch (error) {

        const textArea =
            document.createElement("textarea");

        textArea.value =
            lastAIResponse;

        document.body.appendChild(
            textArea
        );

        textArea.select();

        document.execCommand(
            "copy"
        );

        textArea.remove();

        alert(
            "RESPONSE COPIED."
        );
    }
}


/* ============================================================
   LOAD CHAT HISTORY
============================================================ */

async function loadSessions() {

    try {

        const response =
            await fetch(
                "/api/sessions"
            );

        const data =
            await response.json();

        if (
            !response.ok ||
            !data.success
        ) {
            return;
        }

        conversationList.innerHTML = "";

        data.sessions.forEach(
            function (session) {

                const item =
                    document.createElement("div");

                item.className =
                    "conversation";

                item.dataset.id =
                    session.id;

                const title =
                    document.createElement("div");

                title.className =
                    "conversation-title";

                title.textContent =
                    session.title ||
                    "New Chat";

                const time =
                    document.createElement("div");

                time.className =
                    "conversation-time";

                time.textContent =
                    formatDate(
                        session.updated_at ||
                        session.created_at
                    );

                item.appendChild(title);
                item.appendChild(time);

                item.addEventListener(
                    "click",
                    function () {

                        document
                            .querySelectorAll(
                                ".conversation"
                            )
                            .forEach(
                                function (conversation) {

                                    conversation
                                        .classList
                                        .remove(
                                            "active"
                                        );
                                }
                            );

                        item.classList.add(
                            "active"
                        );

                        loadConversation(
                            session.id
                        );
                    }
                );

                conversationList.appendChild(
                    item
                );
            }
        );

    }

    catch (error) {

        console.error(
            "History loading error:",
            error
        );
    }
}


/* ============================================================
   LOAD PARTICULAR CONVERSATION
============================================================ */

async function loadConversation(id) {

    if (!id) {
        return;
    }

    try {

        const response =
            await fetch(
                "/api/conversations/" +
                id
            );

        const data =
            await response.json();

        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.error ||
                "Unable to load conversation"
            );
        }

        messages.innerHTML = "";

        sessionId =
            data.session_id;

        lastAIResponse = "";

        data.messages.forEach(
            function (message) {

                const isUser =
                    message.role === "user";

                const sender =
                    isUser
                        ? "YOU"
                        : "RETRO-AI";

                const type =
                    isUser
                        ? "user"
                        : "ai";

                addMessage(
                    sender,
                    message.content,
                    type
                );

                if (
                    !isUser
                ) {

                    lastAIResponse =
                        message.content;
                }
            }
        );

        if (
            data.messages.length === 0
        ) {

            showWelcome();
        }

        updateStatus(
            "READY"
        );

    }

    catch (error) {

        console.error(
            "Conversation loading error:",
            error
        );

        showWelcome();

        updateStatus(
            "ERROR"
        );
    }
}


/* ============================================================
   DATE FORMAT
============================================================ */

function formatDate(value) {

    if (!value) {
        return "";
    }

    const date =
        new Date(value);

    if (
        Number.isNaN(
            date.getTime()
        )
    ) {
        return "";
    }

    const now =
        new Date();

    const difference =
        now.getTime() -
        date.getTime();

    const minutes =
        Math.floor(
            difference /
            60000
        );

    if (minutes < 1) {
        return "Just now";
    }

    if (minutes < 60) {
        return minutes + " min ago";
    }

    const hours =
        Math.floor(
            minutes / 60
        );

    if (hours < 24) {
        return hours + " hr ago";
    }

    const days =
        Math.floor(
            hours / 24
        );

    if (days === 1) {
        return "Yesterday";
    }

    if (days < 7) {
        return days + " days ago";
    }

    return date.toLocaleDateString();
}


/* ============================================================
   STATUS BAR
============================================================ */

function updateStatus(status) {

    const statusElements =
        document.querySelectorAll(
            ".status-bar span"
        );

    statusElements.forEach(
        function (element) {

            if (
                element.textContent.includes(
                    "STATUS:"
                )
            ) {

                element.textContent =
                    "STATUS: " +
                    status;
            }
        }
    );
}


/* ============================================================
   SCROLL
============================================================ */

function scrollToBottom() {

    messages.scrollTop =
        messages.scrollHeight;
}


/* ============================================================
   SEND BUTTON
============================================================ */

if (sendBtn) {

    sendBtn.addEventListener(
        "click",
        sendMessage
    );
}


/* ============================================================
   ENTER TO SEND
============================================================ */

if (input) {

    input.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendMessage();
            }
        }
    );
}


/* ============================================================
   INITIALIZE
============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    async function () {

        updateStatus(
            "READY"
        );

        await loadSessions();

        input.focus();
    }
);