/**
 * Trợ lý Rovva AI — bubble widget + fullscreen + xAI API.
 */

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

var chatHistory = [];

function appendBubbleMessage(container, role, text, extraClass) {
  var el = document.createElement("div");
  el.className = "rova-ai-panel__bubble" + (role === "user" ? " rova-ai-panel__bubble--user" : "") + (extraClass ? " " + extraClass : "");
  el.innerHTML = escapeHtml(text).replace(/\n/g, "<br>");
  container.appendChild(el);
  container.scrollTop = container.scrollHeight;
}

async function fetchAiReply(message) {
  var widget = document.getElementById("rova-ai-widget");
  var shell = document.querySelector(".ai-shell");
  var apiUrl =
    (widget && widget.getAttribute("data-api-url")) ||
    (shell && shell.getAttribute("data-api-url")) ||
    null;
  if (!apiUrl) throw new Error("API chưa cấu hình");

  var res = await fetch(apiUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: message, history: chatHistory }),
  });

  var data = await res.json().catch(function () { return {}; });
  if (!res.ok) throw new Error(data.error || "Không nhận được phản hồi từ AI.");
  return data.reply || "";
}

function pushHistory(role, content) {
  chatHistory.push({ role: role, content: content });
  if (chatHistory.length > 16) chatHistory = chatHistory.slice(-16);
}

export async function sendAiMessage(container, welcome, message) {
  if (!message || !container) return;

  if (welcome) welcome.hidden = true;
  appendBubbleMessage(container, "user", message);
  pushHistory("user", message);

  var typing = document.createElement("div");
  typing.className = "rova-ai-panel__bubble rova-ai-panel__bubble--typing";
  typing.textContent = "Đang trả lời...";
  container.appendChild(typing);
  container.scrollTop = container.scrollHeight;

  try {
    var reply = await fetchAiReply(message);
    typing.remove();
    appendBubbleMessage(container, "assistant", reply);
    pushHistory("assistant", reply);
  } catch (err) {
    typing.remove();
    appendBubbleMessage(container, "assistant", err.message || "Lỗi kết nối AI.", "rova-ai-panel__bubble--error");
  }
}

export function initAiBubble() {
  var widget = document.getElementById("rova-ai-widget");
  var panel = document.getElementById("rova-ai-panel");
  var fab = document.getElementById("rova-ai-fab");
  var closeBtn = document.getElementById("rova-ai-panel-close");
  var form = document.getElementById("rova-ai-panel-form");
  var messages = document.getElementById("rova-ai-panel-messages");
  var welcome = document.getElementById("rova-ai-panel-welcome");

  if (!widget || !panel || !fab) return;

  fab.addEventListener("click", function () {
    var open = !panel.hidden;
    panel.hidden = open;
    fab.classList.toggle("is-open", !open);
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      panel.hidden = true;
      fab.classList.remove("is-open");
    });
  }

  function handleSend(text) {
    sendAiMessage(messages, welcome, text);
  }

  if (form) {
    var input = form.querySelector("input");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var val = (input.value || "").trim();
      if (!val) return;
      input.value = "";
      handleSend(val);
    });
  }

  document.querySelectorAll(".ai-bubble-prompt").forEach(function (btn) {
    btn.addEventListener("click", function () {
      handleSend(btn.getAttribute("data-prompt") || btn.textContent.trim());
    });
  });
}

export function initAiChat() {
  initAiBubble();

  var shell = document.querySelector(".ai-shell");
  if (!shell) return;

  var messages = document.getElementById("ai-messages");
  var welcome = document.getElementById("ai-welcome");
  var form = document.getElementById("ai-chat-form");
  var input = form ? form.querySelector("input") : null;

  function appendFullMessage(role, text) {
    var el = document.createElement("div");
    el.className = role === "user" ? "ai-msg ai-msg--user" : "ai-msg ai-msg--bot";
    el.innerHTML = "<p>" + escapeHtml(text).replace(/\n/g, "<br>") + "</p>";
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
  }

  async function sendFull(text) {
    if (!text || !messages) return;
    if (welcome) welcome.style.display = "none";
    appendFullMessage("user", text);
    pushHistory("user", text);

    var typing = document.createElement("div");
    typing.className = "ai-msg ai-msg--bot ai-msg--typing";
    typing.innerHTML = "<p>Đang trả lời...</p>";
    messages.appendChild(typing);

    try {
      var reply = await fetchAiReply(text);
      typing.remove();
      appendFullMessage("bot", reply);
      pushHistory("assistant", reply);
    } catch (err) {
      typing.remove();
      appendFullMessage("bot", err.message || "Lỗi kết nối AI.");
    }
  }

  if (form && input) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var val = input.value.trim();
      if (!val) return;
      sendFull(val);
      input.value = "";
    });
  }

  document.querySelectorAll(".ai-suggestion").forEach(function (btn) {
    btn.addEventListener("click", function () {
      sendFull(btn.getAttribute("data-prompt") || btn.textContent.trim());
    });
  });

  var newChat = document.getElementById("ai-new-chat");
  if (newChat && messages) {
    newChat.addEventListener("click", function () {
      messages.querySelectorAll(".ai-msg").forEach(function (m) { m.remove(); });
      chatHistory = [];
      if (welcome) welcome.style.display = "";
    });
  }
}
