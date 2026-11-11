/**
 * DEBRIS CAREERS — AI Career Consultant Frontend Controller
 * Minimalist, Reactive, Lavender Glassmorphism Client Experience.
 */

// Markdown to HTML converter
function formatMarkdown(text) {
  if (!text) return "";

  let html = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Headers
  html = html.replace(/^#### (.*$)/gim, "<h4>$1</h4>");
  html = html.replace(/^### (.*$)/gim, "<h3>$1</h3>");
  html = html.replace(/^## (.*$)/gim, "<h2>$1</h2>");
  html = html.replace(/^# (.*$)/gim, "<h1>$1</h1>");

  // Bold & Italic
  html = html.replace(/\*\*\*(.*?)\*\*\*/gim, "<strong><em>$1</em></strong>");
  html = html.replace(/\*\*(.*?)\*\*/gim, "<strong>$1</strong>");
  html = html.replace(/\*(.*?)\*/gim, "<em>$1</em>");

  // Inline Code
  html = html.replace(/`([^`]+)`/gim, "<code>$1</code>");

  // Blockquotes
  html = html.replace(/^\> (.*$)/gim, "<blockquote>$1</blockquote>");

  // Horizontal rules
  html = html.replace(/^\-\-\-$/gim, "<hr/>");

  // Markdown Tables
  const lines = html.split("\n");
  let inTable = false;
  let tableHtml = "";
  const newLines = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line.startsWith("|") && line.endsWith("|")) {
      if (line.includes("---")) {
        continue;
      }
      if (!inTable) {
        inTable = true;
        tableHtml = "<table><tbody>";
      }
      const cells = line.split("|").slice(1, -1);
      const isHeader = !tableHtml.includes("<tr>");
      const tag = isHeader ? "th" : "td";
      tableHtml += "<tr>" + cells.map(c => `<${tag}>${c.trim()}</${tag}>`).join("") + "</tr>";
    } else {
      if (inTable) {
        inTable = false;
        tableHtml += "</tbody></table>";
        newLines.push(tableHtml);
        tableHtml = "";
      }
      newLines.push(lines[i]);
    }
  }
  if (inTable) {
    tableHtml += "</tbody></table>";
    newLines.push(tableHtml);
  }
  html = newLines.join("\n");

  // Bullet points
  html = html.replace(/^[•\-] (.*$)/gim, "<li>$1</li>");
  html = html.replace(/(<li>.*<\/li>)/gims, "<ul>$1</ul>");
  html = html.replace(/<\/ul>\s*<ul>/gim, "");

  // Paragraphs
  const paragraphs = html.split(/\n\s*\n/);
  html = paragraphs
    .map(p => {
      p = p.trim();
      if (!p) return "";
      if (p.startsWith("<h") || p.startsWith("<ul") || p.startsWith("<blockquote") || p.startsWith("<hr") || p.startsWith("<table")) {
        return p;
      }
      return `<p>${p.replace(/\n/g, "<br/>")}</p>`;
    })
    .join("\n");

  return html;
}

// Format current time as '10:45 AM'
function getNowTimeString() {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }).replace(/^0/, '');
}

document.addEventListener("DOMContentLoaded", () => {
  const chatViewport = document.getElementById("chatViewport");
  const emptyWelcomeState = document.getElementById("emptyWelcomeState");
  const conversationStream = document.getElementById("conversationStream");
  const bottomInputBar = document.getElementById("bottomInputBar");
  const thinkingIndicator = document.getElementById("thinkingIndicator");

  const heroInputForm = document.getElementById("heroInputForm");
  const heroInputText = document.getElementById("heroInputText");
  const chatForm = document.getElementById("chatForm");
  const userInput = document.getElementById("userInput");

  const activeConvId = window.ACTIVE_CONV_ID;

  // Format existing server-rendered bot messages on load
  document.querySelectorAll(".msg-markdown-body").forEach(el => {
    const raw = el.getAttribute("data-raw");
    if (raw) {
      el.innerHTML = formatMarkdown(raw);
    }
  });

  // Auto-scroll to bottom
  function scrollToBottom() {
    if (chatViewport) {
      chatViewport.scrollTop = chatViewport.scrollHeight;
    }
  }
  scrollToBottom();

  // Send message function
  async function sendMessage(text) {
    const cleanText = text.trim();
    if (!cleanText) return;

    // Transition from Empty Center Welcome to Active Stream
    if (emptyWelcomeState) emptyWelcomeState.classList.add("hidden");
    if (conversationStream) conversationStream.classList.remove("hidden");
    if (bottomInputBar) bottomInputBar.classList.remove("hidden");

    // Append User Message to UI
    const timeStr = getNowTimeString();
    appendUserMessage(cleanText, timeStr);

    // Reset inputs
    if (heroInputText) {
      heroInputText.value = "";
      heroInputText.style.height = "auto";
    }
    if (userInput) {
      userInput.value = "";
      userInput.style.height = "auto";
    }

    // Show Thinking Indicator
    if (thinkingIndicator) {
      thinkingIndicator.classList.remove("hidden");
      conversationStream.appendChild(thinkingIndicator);
    }
    scrollToBottom();

    // Disable send buttons while waiting
    const sendBtns = document.querySelectorAll(".btn-send-purple");
    sendBtns.forEach(b => { b.disabled = true; });

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          conversation_id: activeConvId,
          message: cleanText
        })
      });

      const data = await response.json();
      if (data.status === "success") {
        if (thinkingIndicator) thinkingIndicator.classList.add("hidden");
        appendBotMessage(data.bot_message, data.bot_time || getNowTimeString());
      } else {
        if (thinkingIndicator) thinkingIndicator.classList.add("hidden");
        appendBotMessage("An error occurred while generating career guidance. Please try again.", getNowTimeString());
      }
    } catch (err) {
      console.error("Chat error:", err);
      if (thinkingIndicator) thinkingIndicator.classList.add("hidden");
      appendBotMessage("Connection error. Please verify the local server is running.", getNowTimeString());
    } finally {
      sendBtns.forEach(b => { b.disabled = false; });
      scrollToBottom();
      if (userInput) userInput.focus();
    }
  }

  function appendUserMessage(text, timeStr) {
    const row = document.createElement("div");
    row.className = "chat-msg-row user-row";
    row.innerHTML = `
      <div class="msg-bubble user-bubble">
        <div class="msg-content-text">${escapeHtml(text)}</div>
        <span class="msg-timestamp">${escapeHtml(timeStr)}</span>
      </div>
    `;
    if (thinkingIndicator && thinkingIndicator.parentNode === conversationStream) {
      conversationStream.insertBefore(row, thinkingIndicator);
    } else {
      conversationStream.appendChild(row);
    }
  }

  function appendBotMessage(rawText, timeStr) {
    const row = document.createElement("div");
    row.className = "chat-msg-row ai-row";
    row.innerHTML = `
      <div class="ai-avatar-badge">
        <img src="/static/images/debris_symbol.svg" alt="Debris AI" class="ai-badge-svg">
      </div>
      <div class="msg-bubble ai-bubble glass-panel">
        <div class="msg-markdown-body">${formatMarkdown(rawText)}</div>
        <span class="msg-timestamp">${escapeHtml(timeStr)}</span>
      </div>
    `;
    conversationStream.appendChild(row);
  }

  // --- Form & Textarea Event Listeners ---
  function setupTextarea(textarea, form) {
    if (!textarea || !form) return;

    // Auto-expand textarea
    textarea.addEventListener("input", () => {
      textarea.style.height = "auto";
      textarea.style.height = Math.min(textarea.scrollHeight, 160) + "px";
    });

    // Enter to send, Shift+Enter for newline
    textarea.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        if (textarea.value.trim().length > 0) {
          sendMessage(textarea.value);
        }
      }
    });

    // Form submit
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (textarea.value.trim().length > 0) {
        sendMessage(textarea.value);
      }
    });
  }

  setupTextarea(heroInputText, heroInputForm);
  setupTextarea(userInput, chatForm);

  // --- Sidebar Collapse & Mobile Drawer Controller ---
  const chatSidebar = document.getElementById("chatSidebar");
  const btnCollapseSidebar = document.getElementById("btnCollapseSidebar");
  const btnToggleDrawer = document.getElementById("btnToggleDrawer");
  const sidebarOverlay = document.getElementById("sidebarOverlay");

  function toggleSidebar() {
    if (!chatSidebar) return;
    const isMobile = window.innerWidth <= 860;
    if (isMobile) {
      const isOpen = chatSidebar.classList.contains("drawer-open");
      chatSidebar.classList.toggle("drawer-open", !isOpen);
      if (sidebarOverlay) sidebarOverlay.classList.toggle("hidden", isOpen);
    } else {
      chatSidebar.classList.toggle("collapsed");
    }
  }

  function closeMobileDrawer() {
    if (chatSidebar) chatSidebar.classList.remove("drawer-open");
    if (sidebarOverlay) sidebarOverlay.classList.add("hidden");
  }

  if (btnCollapseSidebar) btnCollapseSidebar.addEventListener("click", toggleSidebar);
  if (btnToggleDrawer) btnToggleDrawer.addEventListener("click", toggleSidebar);
  if (sidebarOverlay) sidebarOverlay.addEventListener("click", closeMobileDrawer);

  // --- User Profile Dropdown Popover ---
  const btnUserMenu = document.getElementById("btnUserMenu");
  const userDropdown = document.getElementById("userDropdown");

  if (btnUserMenu && userDropdown) {
    btnUserMenu.addEventListener("click", (e) => {
      e.stopPropagation();
      userDropdown.classList.toggle("hidden");
    });
    document.addEventListener("click", () => {
      userDropdown.classList.add("hidden");
    });
  }

  // --- Delete Chat Confirmation Modal ---
  const confirmDeleteModal = document.getElementById("confirmDeleteModal");
  const modalDialogTitle = document.getElementById("modalDialogTitle");
  const modalDialogText = document.getElementById("modalDialogText");
  const btnCancelModal = document.getElementById("btnCancelModal");
  const btnDismissDelete = document.getElementById("btnDismissDelete");
  const btnConfirmDelete = document.getElementById("btnConfirmDelete");
  const btnPromptClearAll = document.getElementById("btnPromptClearAll");

  let pendingDeleteType = null; // 'single' or 'all'
  let pendingDeleteId = null;

  function openDeleteModal(title, text, type, id = null) {
    if (!confirmDeleteModal) return;
    modalDialogTitle.textContent = title;
    modalDialogText.textContent = text;
    pendingDeleteType = type;
    pendingDeleteId = id;
    confirmDeleteModal.classList.remove("hidden");
  }

  function closeModal() {
    if (confirmDeleteModal) confirmDeleteModal.classList.add("hidden");
    pendingDeleteType = null;
    pendingDeleteId = null;
  }

  if (btnCancelModal) btnCancelModal.addEventListener("click", closeModal);
  if (btnDismissDelete) btnDismissDelete.addEventListener("click", closeModal);
  if (confirmDeleteModal) {
    confirmDeleteModal.addEventListener("click", (e) => {
      if (e.target === confirmDeleteModal) closeModal();
    });
  }

  // Bind individual delete buttons in sidebar
  document.querySelectorAll(".btn-delete-item").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      const id = btn.getAttribute("data-id");
      const title = btn.getAttribute("data-title") || "this chat";
      openDeleteModal(
        "Delete Conversation",
        `Are you sure you want to delete "${title}"? This action cannot be undone.`,
        "single",
        id
      );
    });
  });

  // Bind clear all button
  if (btnPromptClearAll) {
    btnPromptClearAll.addEventListener("click", (e) => {
      e.preventDefault();
      openDeleteModal(
        "Clear All Chat History",
        "Are you sure you want to delete all past conversations? This action cannot be undone.",
        "all"
      );
    });
  }

  // Confirm delete handler
  if (btnConfirmDelete) {
    btnConfirmDelete.addEventListener("click", async () => {
      btnConfirmDelete.disabled = true;
      try {
        if (pendingDeleteType === "single" && pendingDeleteId) {
          const res = await fetch(`/chat/delete/${pendingDeleteId}`, {
            method: "POST",
            headers: { "X-Requested-With": "XMLHttpRequest" }
          });
          const result = await res.json();
          if (result.status === "success") {
            // Remove row from sidebar DOM immediately
            const row = document.querySelector(`.history-item-row[data-id="${pendingDeleteId}"]`);
            if (row) row.remove();

            // If active conversation was deleted, redirect to home
            if (pendingDeleteId === activeConvId) {
              window.location.href = "/";
            }
          }
        } else if (pendingDeleteType === "all") {
          const res = await fetch("/chat/clear_all", {
            method: "POST",
            headers: { "X-Requested-With": "XMLHttpRequest" }
          });
          const result = await res.json();
          if (result.status === "success") {
            window.location.href = "/";
          }
        }
      } catch (err) {
        console.error("Delete error:", err);
      } finally {
        btnConfirmDelete.disabled = false;
        closeModal();
      }
    });
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
});
