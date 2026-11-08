/**
 * Debris Careers — Frontend Client Interaction & UI Controls
 * Inspired by Reference Assistant UI: Clean, Reactive, Zero MCQ constraints
 */

// Markdown to HTML converter for client-side display
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

  // Inline Code / Badges
  html = html.replace(/`([^`]+)`/gim, "<code>$1</code>");

  // Blockquotes
  html = html.replace(/^\> (.*$)/gim, "<blockquote>$1</blockquote>");

  // Horizontal rules
  html = html.replace(/^\-\-\-$/gim, "<hr/>");

  // Markdown Tables: rows starting with |
  const lines = html.split("\n");
  let inTable = false;
  let tableHtml = "";
  const newLines = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line.startsWith("|") && line.endsWith("|")) {
      // Skip separator row like | :--- | :--- |
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
  const messagesContainer = document.getElementById("messagesContainer");
  const heroWelcomeSection = document.getElementById("heroWelcomeSection");
  const cardScrollBody = document.getElementById("cardScrollBody");
  const chatForm = document.getElementById("chatForm");
  const userInput = document.getElementById("userInput");
  const activeConvId = window.ACTIVE_CONV_ID;

  // Drawer Elements
  const historyDrawer = document.getElementById("historyDrawer");
  const historyOverlay = document.getElementById("historyOverlay");
  const btnDockHistory = document.getElementById("btnDockHistory");
  const btnCloseDrawer = document.getElementById("btnCloseDrawer");
  const btnDockSearch = document.getElementById("btnDockSearch");
  const btnDockExplore = document.getElementById("btnDockExplore");
  const btnDockCategories = document.getElementById("btnDockCategories");
  const btnMicAction = document.getElementById("btnMicAction");
  const btnPlusAction = document.getElementById("btnPlusAction");

  // Drawer open / close handlers
  function openHistoryDrawer() {
    if (historyDrawer && historyOverlay) {
      historyDrawer.classList.add("open");
      historyOverlay.classList.add("active");
    }
  }

  function closeHistoryDrawer() {
    if (historyDrawer && historyOverlay) {
      historyDrawer.classList.remove("open");
      historyOverlay.classList.remove("active");
    }
  }

  if (btnDockHistory) btnDockHistory.addEventListener("click", openHistoryDrawer);
  if (btnCloseDrawer) btnCloseDrawer.addEventListener("click", closeHistoryDrawer);
  if (historyOverlay) historyOverlay.addEventListener("click", closeHistoryDrawer);

  if (btnDockSearch && userInput) {
    btnDockSearch.addEventListener("click", () => {
      userInput.focus();
    });
  }

  if (btnDockExplore && userInput) {
    btnDockExplore.addEventListener("click", () => {
      sendMessage("Give me a comprehensive overview of all 4 streams: Medical, Non-Medical, Commerce, and Humanities.");
    });
  }

  if (btnDockCategories) {
    btnDockCategories.addEventListener("click", openHistoryDrawer);
  }

  if (btnPlusAction && userInput) {
    btnPlusAction.addEventListener("click", () => {
      userInput.focus();
      userInput.placeholder = "Describe your favorite subjects, hobbies, or career goals...";
    });
  }

  // Format existing server-rendered bot messages on load
  document.querySelectorAll(".bot-bubble").forEach(el => {
    const raw = el.getAttribute("data-raw");
    if (raw) {
      el.innerHTML = formatMarkdown(raw);
    }
  });

  // Scroll to bottom
  function scrollToBottom() {
    if (cardScrollBody) {
      cardScrollBody.scrollTop = cardScrollBody.scrollHeight;
    }
  }
  scrollToBottom();

  // Send message function
  async function sendMessage(text) {
    const cleanText = text.trim();
    if (!cleanText) return;

    // Hide hero welcome card when conversation starts
    if (heroWelcomeSection) {
      heroWelcomeSection.classList.add("hidden");
    }

    // Append User Message to UI immediately
    appendUserMessage(cleanText);
    if (userInput) userInput.value = "";
    scrollToBottom();

    // Disable send button while awaiting response
    const submitBtn = document.querySelector(".btn-input-send");
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
        appendBotMessage(data.bot_message);
      } else {
        appendBotMessage("An error occurred processing your consultation request. Please try again.");
      }
    } catch (err) {
      console.error("Chat error:", err);
      appendBotMessage("Communication error. Please ensure the local server is running.");
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
      <div class="bubble user-bubble">${escapeHtml(text)}</div>
    `;
    messagesContainer.appendChild(row);
  }

  function appendBotMessage(rawText) {
    const row = document.createElement("div");
    row.className = "message-row bot-row";
    row.innerHTML = `
      <div class="sender-tag">Debris Careers AI Consultant</div>
      <div class="bubble bot-bubble">${formatMarkdown(rawText)}</div>
    `;
    messagesContainer.appendChild(row);
  }

  // Form submit
  if (chatForm) {
    chatForm.addEventListener("submit", (e) => {
      e.preventDefault();
      sendMessage(userInput.value);
    });
  }

  // Feature Cards Click Listeners (Hero Welcome Cards)
  document.querySelectorAll(".feature-card").forEach(card => {
    card.addEventListener("click", () => {
      const prompt = card.getAttribute("data-prompt");
      if (prompt) {
        sendMessage(prompt);
      }
    });
  });

  // Quick Action Chips Listeners (Pills beneath the input)
  document.querySelectorAll(".action-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const query = chip.getAttribute("data-query");
      if (query) {
        sendMessage(query);
      }
    });
  });

  // Mic Button Action (Friendly voice interaction hint)
  if (btnMicAction && userInput) {
    btnMicAction.addEventListener("click", () => {
      userInput.placeholder = "Listening... (or type your career interests)";
      userInput.focus();
      setTimeout(() => {
        userInput.placeholder = 'Example : "I like mathematics, computers, and want a high-paying job"';
      }, 3000);
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
