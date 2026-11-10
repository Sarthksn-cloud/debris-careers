/**
 * DEBRIS CAREERS — ChatGPT Interface Client Controller
 * Natural free-form career consultation, auto-resizing textarea,
 * dark/light theme switching, model selector, markdown formatting.
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

document.addEventListener("DOMContentLoaded", () => {
  const conversationStream = document.getElementById("conversationStream");
  const heroView = document.getElementById("heroView");
  const chatScrollContainer = document.getElementById("chatScrollContainer");
  const chatForm = document.getElementById("chatForm");
  const userInput = document.getElementById("userInput");
  const btnSend = document.getElementById("btnSend");
  const activeConvId = window.ACTIVE_CONV_ID;

  // --- Theme Controller ---
  const THEME_KEY = "chatgpt_theme";
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
    const themeToggleText = document.getElementById("themeToggleText");
    if (themeToggleText) {
      themeToggleText.textContent = theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode";
    }
  }
  const savedTheme = localStorage.getItem(THEME_KEY) || "dark";
  applyTheme(savedTheme);

  const btnThemeToggle = document.getElementById("btnThemeToggle");
  if (btnThemeToggle) {
    btnThemeToggle.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme") || "dark";
      applyTheme(current === "dark" ? "light" : "dark");
    });
  }

  // --- Format Existing Server-Rendered Bot Messages ---
  document.querySelectorAll(".bot-bubble-markdown").forEach(el => {
    const raw = el.getAttribute("data-raw");
    if (raw) {
      el.innerHTML = formatMarkdown(raw);
    }
  });

  // --- Auto-Scroll to Bottom ---
  function scrollToBottom() {
    if (chatScrollContainer) {
      chatScrollContainer.scrollTop = chatScrollContainer.scrollHeight;
    }
  }
  scrollToBottom();

  // --- Textarea Auto-Resize & Send Button Enable/Disable ---
  if (userInput && btnSend) {
    userInput.addEventListener("input", () => {
      // Auto resize height
      userInput.style.height = "auto";
      userInput.style.height = Math.min(userInput.scrollHeight, 180) + "px";

      // Enable/disable send button
      const hasText = userInput.value.trim().length > 0;
      btnSend.disabled = !hasText;
      btnSend.classList.toggle("active", hasText);
    });

    // Handle Enter to send, Shift+Enter for newline
    userInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        if (userInput.value.trim().length > 0) {
          sendMessage(userInput.value);
        }
      }
    });
  }

  // --- Send Message Function ---
  async function sendMessage(text) {
    const cleanText = text.trim();
    if (!cleanText) return;

    // Hide hero view
    if (heroView) heroView.classList.add("hidden");

    // Append user message immediately
    appendUserMessage(cleanText);

    // Reset textarea
    if (userInput) {
      userInput.value = "";
      userInput.style.height = "auto";
    }
    if (btnSend) {
      btnSend.disabled = true;
      btnSend.classList.remove("active");
    }
    scrollToBottom();

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
        appendBotMessage(data.bot_message);
      } else {
        appendBotMessage("An error occurred while analyzing career pathways. Please try again.");
      }
    } catch (err) {
      console.error("Chat error:", err);
      appendBotMessage("Communication error. Please ensure the local server is running.");
    } finally {
      scrollToBottom();
      if (userInput) userInput.focus();
    }
  }

  function appendUserMessage(text) {
    const row = document.createElement("div");
    row.className = "message-row user-row";
    row.innerHTML = `<div class="user-bubble">${escapeHtml(text)}</div>`;
    conversationStream.appendChild(row);
  }

  function appendBotMessage(rawText) {
    const row = document.createElement("div");
    row.className = "message-row bot-row";
    row.innerHTML = `
      <div class="bot-spark-avatar">
        <img src="/static/images/chatgpt_spark.svg" alt="Debris Spark" class="spark-svg">
      </div>
      <div class="bot-content-wrap">
        <div class="bot-bubble-markdown">${formatMarkdown(rawText)}</div>
        <div class="bot-action-bar">
          <button type="button" class="btn-action-copy" title="Copy response">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
          </button>
          <button type="button" class="btn-action-thumb" title="Good response">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
            </svg>
          </button>
          <button type="button" class="btn-action-thumb" title="Bad response">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-3"></path>
            </svg>
          </button>
          <button type="button" class="btn-action-retry" title="Regenerate response">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="23 4 23 10 17 10"></polyline>
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
            </svg>
          </button>
        </div>
      </div>
    `;
    conversationStream.appendChild(row);
    bindBotActionEvents(row);
  }

  // --- Form Submit ---
  if (chatForm) {
    chatForm.addEventListener("submit", (e) => {
      e.preventDefault();
      if (userInput && userInput.value.trim().length > 0) {
        sendMessage(userInput.value);
      }
    });
  }

  // --- Prompt Suggestion Cards (Hero 2x2 Grid) ---
  document.querySelectorAll(".prompt-card").forEach(card => {
    card.addEventListener("click", () => {
      const prompt = card.getAttribute("data-prompt");
      if (prompt) {
        sendMessage(prompt);
      }
    });
  });

  // --- Sidebar Collapse & Open ---
  const sidebar = document.getElementById("sidebar");
  const btnCloseSidebar = document.getElementById("btnCloseSidebar");
  const btnOpenSidebar = document.getElementById("btnOpenSidebar");

  if (btnCloseSidebar && sidebar) {
    btnCloseSidebar.addEventListener("click", () => {
      sidebar.classList.add("collapsed");
    });
  }
  if (btnOpenSidebar && sidebar) {
    btnOpenSidebar.addEventListener("click", () => {
      sidebar.classList.remove("collapsed");
    });
  }

  // --- User Profile Popup Menu ---
  const btnUserMenuToggle = document.getElementById("btnUserMenuToggle");
  const userPopupMenu = document.getElementById("userPopupMenu");
  if (btnUserMenuToggle && userPopupMenu) {
    btnUserMenuToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      userPopupMenu.classList.toggle("show");
    });
    document.addEventListener("click", () => {
      userPopupMenu.classList.remove("show");
    });
  }

  // --- Model Selector Dropdown ---
  const btnModelDropdown = document.getElementById("btnModelDropdown");
  const modelDropdownMenu = document.getElementById("modelDropdownMenu");
  const currentModelLabel = document.getElementById("currentModelLabel");
  if (btnModelDropdown && modelDropdownMenu) {
    btnModelDropdown.addEventListener("click", (e) => {
      e.stopPropagation();
      modelDropdownMenu.classList.toggle("show");
    });
    document.addEventListener("click", () => {
      modelDropdownMenu.classList.remove("show");
    });

    document.querySelectorAll(".model-dropdown-item").forEach(item => {
      item.addEventListener("click", () => {
        document.querySelectorAll(".model-dropdown-item").forEach(i => i.classList.remove("active"));
        item.classList.add("active");
        if (currentModelLabel) currentModelLabel.textContent = item.getAttribute("data-model");
        modelDropdownMenu.classList.remove("show");
      });
    });
  }

  // --- Attachment Plus Button Action ---
  const btnAttach = document.getElementById("btnAttach");
  if (btnAttach && userInput) {
    btnAttach.addEventListener("click", () => {
      userInput.placeholder = "Describe your marks, dream stream, or target colleges...";
      userInput.focus();
    });
  }

  // --- Bot Action Bar Handlers (Copy, Thumbs, Retry) ---
  function bindBotActionEvents(container) {
    const copyBtn = container.querySelector(".btn-action-copy");
    const markdownBody = container.querySelector(".bot-bubble-markdown");
    if (copyBtn && markdownBody) {
      copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(markdownBody.innerText).then(() => {
          copyBtn.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10a37f" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          `;
          setTimeout(() => {
            copyBtn.innerHTML = `
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            `;
          }, 2000);
        });
      });
    }

    const retryBtn = container.querySelector(".btn-action-retry");
    if (retryBtn) {
      retryBtn.addEventListener("click", () => {
        const userBubbles = document.querySelectorAll(".user-bubble");
        if (userBubbles.length > 0) {
          const lastUserText = userBubbles[userBubbles.length - 1].innerText;
          sendMessage(lastUserText);
        }
      });
    }
  }

  // Bind existing bot action bars
  document.querySelectorAll(".message-row.bot-row").forEach(bindBotActionEvents);

  function escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
});
