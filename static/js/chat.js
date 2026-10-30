/**
 * Debris Careers - Frontend Client Interaction
 */

// Simple lightweight Markdown to HTML converter for client-side display
function formatMarkdown(text) {
  if (!text) return "";
  
  let html = text
    // Escape basic HTML
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Headers
  html = html.replace(/^### (.*$)/gim, "<h3>$1</h3>");
  html = html.replace(/^#### (.*$)/gim, "<h4>$1</h4>");
  html = html.replace(/^## (.*$)/gim, "<h2>$1</h2>");
  html = html.replace(/^# (.*$)/gim, "<h1>$1</h1>");

  // Bold & Italic
  html = html.replace(/\*\*\*(.*?)\*\*\*/gim, "<strong><em>$1</em></strong>");
  html = html.replace(/\*\*(.*?)\*\*/gim, "<strong>$1</strong>");
  html = html.replace(/\*(.*?)\*/gim, "<em>$1</em>");

  // Blockquotes
  html = html.replace(/^\> (.*$)/gim, "<blockquote>$1</blockquote>");

  // Horizontal rules
  html = html.replace(/^\-\-\-$/gim, "<hr/>");

  // Bullet points
  html = html.replace(/^[•\-] (.*$)/gim, "<li>$1</li>");
  html = html.replace(/(<li>.*<\/li>)/gims, "<ul>$1</ul>");

  // Clean double ul tags
  html = html.replace(/<\/ul>\s*<ul>/gim, "");

  // Line breaks to paragraphs
  const paragraphs = html.split(/\n\s*\n/);
  html = paragraphs
    .map(p => {
      p = p.trim();
      if (!p) return "";
      if (p.startsWith("<h") || p.startsWith("<ul") || p.startsWith("<blockquote") || p.startsWith("<hr")) {
        return p;
      }
      return `<p>${p.replace(/\n/g, "<br/>")}</p>`;
    })
    .join("\n");

  return html;
}

document.addEventListener("DOMContentLoaded", () => {
  const messagesContainer = document.getElementById("messagesContainer");
  const chatForm = document.getElementById("chatForm");
  const userInput = document.getElementById("userInput");
  const activeConvId = window.ACTIVE_CONV_ID;

  // Format existing server-rendered bot messages on load
  document.querySelectorAll(".bot-row .bubble").forEach(el => {
    const raw = el.getAttribute("data-raw");
    if (raw) {
      el.innerHTML = formatMarkdown(raw);
    }
  });

  // Scroll to bottom
  function scrollToBottom() {
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  }
  scrollToBottom();

  // Send message function
  async function sendMessage(text) {
    const cleanText = text.trim();
    if (!cleanText) return;

    // Append User Message to UI immediately
    appendUserMessage(cleanText);
    if (userInput) userInput.value = "";
    scrollToBottom();

    // Disable send button while awaiting response
    const submitBtn = document.querySelector(".chat-submit-btn");
    if (submitBtn) submitBtn.disabled = true;

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
        appendBotMessage(data.bot_message, data.options);
      } else {
        appendBotMessage("An error occurred processing your consultation request. Please try again.", ["Restart"]);
      }
    } catch (err) {
      console.error("Chat error:", err);
      appendBotMessage("Communication error. Please ensure the server is active.", ["Restart"]);
    } finally {
      if (submitBtn) submitBtn.disabled = false;
      scrollToBottom();
      if (userInput) userInput.focus();
    }
  }

  function appendUserMessage(text) {
    const row = document.createElement("div");
    row.className = "message-row user-row";
    row.innerHTML = `
      <div class="sender-tag">You</div>
      <div class="bubble">${escapeHtml(text)}</div>
    `;
    messagesContainer.appendChild(row);
  }

  function appendBotMessage(rawText, options) {
    const row = document.createElement("div");
    row.className = "message-row bot-row";

    let optionsHtml = "";
    if (options && options.length > 0) {
      const btns = options.map(opt => `<button type="button" class="option-btn" data-val="${escapeHtml(opt)}">${escapeHtml(opt)}</button>`).join("");
      optionsHtml = `<div class="quick-options">${btns}</div>`;
    }

    row.innerHTML = `
      <div class="sender-tag">Debris Careers Consultant</div>
      <div class="bubble">${formatMarkdown(rawText)}</div>
      ${optionsHtml}
    `;

    messagesContainer.appendChild(row);
    attachOptionListeners(row);
  }

  function attachOptionListeners(scope) {
    const buttons = scope.querySelectorAll(".option-btn");
    buttons.forEach(btn => {
      btn.addEventListener("click", () => {
        const val = btn.getAttribute("data-val");
        sendMessage(val);
      });
    });
  }

  // Attach listeners to initial option buttons on the page
  attachOptionListeners(document);

  // Form submit
  if (chatForm) {
    chatForm.addEventListener("submit", (e) => {
      e.preventDefault();
      sendMessage(userInput.value);
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
