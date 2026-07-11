/**
 * Rovva Host — hành vi chung: dòng bảng, thông báo, gợi ý doanh thu, AI bubble.
 */

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

var hostConfirmCallback = null;

function showHostModal(el) {
  if (!el || !window.bootstrap) return;
  bootstrap.Modal.getOrCreateInstance(el).show();
}

function showHostAlert(message, title) {
  var modal = document.getElementById("hostAlertModal");
  if (!modal) return;
  var msgEl = document.getElementById("host-alert-message");
  var titleEl = document.getElementById("host-alert-title");
  if (msgEl) msgEl.textContent = message || "";
  if (titleEl) titleEl.textContent = title || "Thông báo";
  showHostModal(modal);
}

function showHostConfirm(message, onConfirm, opts) {
  opts = opts || {};
  var modal = document.getElementById("hostConfirmModal");
  if (!modal) return;
  var msgEl = document.getElementById("host-confirm-message");
  var titleEl = document.getElementById("host-confirm-title");
  var okBtn = document.getElementById("host-confirm-ok");
  if (msgEl) msgEl.textContent = message || "";
  if (titleEl) titleEl.textContent = opts.title || "Xác nhận";
  if (okBtn) {
    okBtn.textContent = opts.okText || "Xác nhận";
    okBtn.className = opts.danger ? "btn btn-danger" : "btn btn-primary";
  }
  hostConfirmCallback = onConfirm;
  showHostModal(modal);
}

function initHostDialogs() {
  var okBtn = document.getElementById("host-confirm-ok");
  var modal = document.getElementById("hostConfirmModal");
  if (!okBtn || !modal) return;
  okBtn.addEventListener("click", function () {
    bootstrap.Modal.getInstance(modal)?.hide();
    if (typeof hostConfirmCallback === "function") hostConfirmCallback();
    hostConfirmCallback = null;
  });
}

function initClickableRows() {
  document.querySelectorAll("tr[data-href]").forEach(function (row) {
    row.style.cursor = "pointer";
    row.addEventListener("click", function (e) {
      if (e.target.closest("a, button, input, select, textarea, label, .form-check")) return;
      var href = row.getAttribute("data-href");
      if (href) window.location.href = href;
    });
  });
}

function initRevenueTipsModal() {
  var trigger = document.getElementById("revenue-tips-trigger");
  var modalEl = document.getElementById("revenueTipsModal");
  if (!trigger || !modalEl || !window.bootstrap) return;
  var modal = bootstrap.Modal.getOrCreateInstance(modalEl);
  trigger.addEventListener("click", function () {
    modal.show();
  });
}

var hostAiBubbleHistory = [];
var HOST_AI_SESSIONS_KEY = "rova-host-ai-sessions";
var hostAiSessions = [];
var hostAiActiveSessionId = null;
var hostAiFullSending = false;
var hostAiBubbleSending = false;

function formatAiText(text) {
  var safe = escapeHtml(String(text || ""));
  safe = safe.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  safe = safe.replace(/\n/g, "<br>");
  return safe;
}

function getHostAiApiUrl() {
  var shell = document.getElementById("host-ai-shell");
  if (shell) return shell.getAttribute("data-api-url");
  var widget = document.getElementById("rova-ai-widget");
  return widget ? widget.getAttribute("data-api-url") : null;
}

function appendHostAiBubble(container, role, text, extra, useMarkdown) {
  var el = document.createElement("div");
  el.className =
    "rova-ai-panel__bubble" +
    (role === "user" ? " rova-ai-panel__bubble--user" : "") +
    (extra ? " " + extra : "");
  el.innerHTML = useMarkdown ? formatAiText(text) : escapeHtml(text).replace(/\n/g, "<br>");
  container.appendChild(el);
  container.scrollTop = container.scrollHeight;
}

function appendHostAiFullBubble(container, role, text, extra) {
  var el = document.createElement("div");
  el.className =
    "host-ai-bubble" +
    (role === "user" ? " host-ai-bubble--user" : "") +
    (extra ? " " + extra : "");
  el.innerHTML = role === "assistant" ? formatAiText(text) : escapeHtml(text).replace(/\n/g, "<br>");
  container.appendChild(el);
  container.scrollTop = container.scrollHeight;
}

async function fetchHostAiReply(message, history) {
  var apiUrl = getHostAiApiUrl();
  if (!apiUrl) throw new Error("API chưa cấu hình");
  var res = await fetch(apiUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: message, history: history }),
  });
  var data = await res.json().catch(function () { return {}; });
  if (!res.ok) throw new Error(data.error || "Không nhận được phản hồi từ AI.");
  return data.reply || "";
}

function loadHostAiSessions() {
  try {
    hostAiSessions = JSON.parse(localStorage.getItem(HOST_AI_SESSIONS_KEY) || "[]");
  } catch (e) {
    hostAiSessions = [];
  }
}

function saveHostAiSessions() {
  localStorage.setItem(HOST_AI_SESSIONS_KEY, JSON.stringify(hostAiSessions.slice(0, 30)));
}

function getActiveHostAiSession() {
  return hostAiSessions.find(function (s) { return s.id === hostAiActiveSessionId; }) || null;
}

function renderHostAiHistoryList() {
  var list = document.getElementById("host-ai-history-list");
  if (!list) return;
  list.innerHTML = "";
  if (!hostAiSessions.length) {
    list.innerHTML = '<p class="small text-muted px-2 mb-0">Chưa có lịch sử chat.</p>';
    return;
  }
  hostAiSessions.forEach(function (session) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "host-ai-history__item" + (session.id === hostAiActiveSessionId ? " is-active" : "");
    btn.textContent = session.title || "Cuộc trò chuyện";
    btn.title = session.title || "";
    btn.addEventListener("click", function () {
      hostAiActiveSessionId = session.id;
      renderHostAiFullConversation();
      renderHostAiHistoryList();
    });
    list.appendChild(btn);
  });
}

function clearHostAiMessagesKeepWelcome() {
  var messages = document.getElementById("host-ai-messages");
  var welcome = document.getElementById("host-ai-welcome");
  if (!messages) return;
  Array.from(messages.children).forEach(function (child) {
    if (child.id !== "host-ai-welcome") child.remove();
  });
  if (welcome) welcome.hidden = false;
}

function renderHostAiFullConversation() {
  var messages = document.getElementById("host-ai-messages");
  var welcome = document.getElementById("host-ai-welcome");
  if (!messages) return;
  var session = getActiveHostAiSession();
  clearHostAiMessagesKeepWelcome();
  if (!session || !session.messages.length) return;
  if (welcome) welcome.hidden = true;
  session.messages.forEach(function (m) {
    appendHostAiFullBubble(messages, m.role, m.content, m.role === "assistant" ? "" : "");
  });
}

var HOST_AI_BUBBLE_SESSION_KEY = "rova-host-ai-bubble-session";

function appendToHostAiHistory(userMsg, assistantMsg) {
  loadHostAiSessions();
  var sid = sessionStorage.getItem(HOST_AI_BUBBLE_SESSION_KEY);
  var session = sid ? hostAiSessions.find(function (s) { return s.id === sid; }) : null;

  if (!session) {
    session = createHostAiSession(userMsg);
    sessionStorage.setItem(HOST_AI_BUBBLE_SESSION_KEY, session.id);
  } else {
    hostAiActiveSessionId = session.id;
    var idx = hostAiSessions.findIndex(function (s) { return s.id === sid; });
    if (idx > 0) {
      hostAiSessions.splice(idx, 1);
      hostAiSessions.unshift(session);
    }
  }

  session.messages.push({ role: "user", content: userMsg });
  if (assistantMsg) {
    session.messages.push({ role: "assistant", content: assistantMsg });
  }
  session.updatedAt = Date.now();
  saveHostAiSessions();
}

function createHostAiSession(firstMessage) {
  var id = "s_" + Date.now();
  var session = {
    id: id,
    title: (firstMessage || "Cuộc trò chuyện mới").slice(0, 48),
    messages: [],
    updatedAt: Date.now(),
  };
  hostAiSessions.unshift(session);
  hostAiActiveSessionId = id;
  saveHostAiSessions();
  return session;
}

function initHostAiWidget() {
  var widget = document.getElementById("rova-ai-widget");
  if (!widget) return;

  loadHostAiSessions();

  var fab = document.getElementById("rova-ai-fab");
  var panel = document.getElementById("rova-ai-panel");
  var closeBtn = document.getElementById("rova-ai-panel-close");
  var form = document.getElementById("rova-ai-panel-form");
  var messages = document.getElementById("rova-ai-panel-messages");
  var welcome = document.getElementById("rova-ai-panel-welcome");

  function openPanel() {
    if (!panel) return;
    panel.hidden = false;
    fab && fab.classList.add("is-open");
  }

  function closePanel() {
    if (!panel) return;
    panel.hidden = true;
    fab && fab.classList.remove("is-open");
  }

  fab && fab.addEventListener("click", function () {
    if (panel && panel.hidden) openPanel();
    else closePanel();
  });
  closeBtn && closeBtn.addEventListener("click", closePanel);

  document.querySelectorAll(".ai-bubble-prompt").forEach(function (chip) {
    chip.addEventListener("click", function () {
      sendHostAiMessage(chip.getAttribute("data-prompt") || chip.textContent.trim());
    });
  });

  document.querySelectorAll("[data-open-host-ai]").forEach(function (el) {
    el.addEventListener("click", function (e) {
      e.preventDefault();
      openPanel();
    });
  });

  async function sendHostAiMessage(message) {
    if (!message || !messages || hostAiBubbleSending) return;
    hostAiBubbleSending = true;
    if (welcome) welcome.hidden = true;
    appendHostAiBubble(messages, "user", message);
    hostAiBubbleHistory.push({ role: "user", content: message });
    if (hostAiBubbleHistory.length > 16) hostAiBubbleHistory = hostAiBubbleHistory.slice(-16);

    var typing = document.createElement("div");
    typing.className = "rova-ai-panel__bubble rova-ai-panel__bubble--typing";
    typing.textContent = "Đang trả lời...";
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;

    try {
      var historyForApi = hostAiBubbleHistory.slice(0, -1);
      var reply = await fetchHostAiReply(message, historyForApi);
      typing.remove();
      appendHostAiBubble(messages, "assistant", reply, "", true);
      hostAiBubbleHistory.push({ role: "assistant", content: reply });
      appendToHostAiHistory(message, reply);
    } catch (err) {
      typing.remove();
      appendHostAiBubble(messages, "assistant", err.message, "rova-ai-panel__bubble--error");
      appendToHostAiHistory(message, err.message);
    } finally {
      hostAiBubbleSending = false;
    }
  }

  form &&
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = form.querySelector("input");
      var val = input ? input.value.trim() : "";
      if (!val) return;
      if (input) input.value = "";
      sendHostAiMessage(val);
    });
}

function initHostAccTabs() {
  var tabRoot = document.getElementById("host-acc-tabs");
  var grid = document.getElementById("host-acc-grid");
  if (!tabRoot || !grid) return;

  var cards = grid.querySelectorAll("[data-acc-status]");
  var buttons = tabRoot.querySelectorAll("[data-acc-filter]");

  function applyFilter(status) {
    cards.forEach(function (card) {
      var accStatus = card.getAttribute("data-acc-status");
      var show = status === "all" || accStatus === status;
      card.style.display = show ? "" : "none";
    });
  }

  var initial = tabRoot.querySelector(".nav-link.active");
  if (initial) applyFilter(initial.getAttribute("data-acc-filter") || "all");

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      buttons.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      applyFilter(btn.getAttribute("data-acc-filter") || "all");
    });
  });
}

function initAccImageCarousel() {
  var root = document.getElementById("acc-image-carousel");
  var dataEl = document.getElementById("acc-carousel-data");
  var img = document.getElementById("acc-carousel-img");
  var prev = document.getElementById("acc-carousel-prev");
  var next = document.getElementById("acc-carousel-next");
  var counter = document.getElementById("acc-carousel-counter");
  if (!root || !dataEl || !img) return;

  var urls = [];
  try { urls = JSON.parse(dataEl.textContent || "[]"); } catch (e) { return; }
  if (urls.length <= 1) return;

  var idx = 0;
  function render() {
    img.src = urls[idx];
    if (counter) counter.textContent = (idx + 1) + " / " + urls.length;
    if (prev) prev.disabled = idx === 0;
    if (next) next.disabled = idx === urls.length - 1;
  }

  prev && prev.addEventListener("click", function () {
    if (idx > 0) { idx--; render(); }
  });
  next && next.addEventListener("click", function () {
    if (idx < urls.length - 1) { idx++; render(); }
  });
  render();
}

function initAccForm() {
  var form = document.getElementById("acc-form");
  if (!form || form.dataset.accBound) return;
  form.dataset.accBound = "1";

  var isCreate = form.getAttribute("data-is-create") === "1";
  var stayingCount = parseInt(form.getAttribute("data-staying-count") || "0", 10);
  var cancelUrl = form.getAttribute("data-cancel-url") || "/host/accommodation/accommodations/";
  var strip = document.getElementById("acc-image-strip");
  var fileInput = document.getElementById("acc-file-input");
  var uploadBox = document.getElementById("acc-upload-box");
  var uploadTrigger = document.getElementById("acc-upload-trigger");
  var fileInputsHost = document.getElementById("acc-image-file-inputs");
  var orderInput = document.getElementById("image-order-input");
  var addFeatureBtn = document.getElementById("add-custom-feature-btn");
  var featuresAnchor = document.getElementById("custom-features-anchor");
  var cancelBtn = document.getElementById("acc-cancel-btn");
  var deleteTrigger = document.getElementById("acc-delete-trigger");
  var maxImagesModal = document.getElementById("accMaxImagesModal");
  var cancelModal = document.getElementById("accCancelModal");
  var deleteModal = document.getElementById("accDeleteModal");
  var saveSuccessModal = document.getElementById("accSaveSuccessModal");
  var savedFlash = document.getElementById("acc-saved-flash");

  var MAX_IMAGES = 5;
  var imageItems = [];
  var nextFileIdx = 0;
  var formDirty = false;
  var initialImageUrls = [];

  function markDirty() { formDirty = true; }

  function showModal(el) {
    if (!el || !window.bootstrap) return;
    bootstrap.Modal.getOrCreateInstance(el).show();
  }

  if (savedFlash && saveSuccessModal) {
    showModal(saveSuccessModal);
  }

  function updateSetupProgress() {
    var basicDone = ["name", "type", "city", "district", "address"].every(function (n) {
      var el = form.querySelector('[name="' + n + '"]');
      return el && String(el.value || "").trim();
    });
    var imagesDone = imageItems.length > 0;
    var policyEl = form.querySelector('[name="cancellation_policy"]');
    var policyDone = policyEl && String(policyEl.value || "").trim();
    var legalDone = Array.from(form.querySelectorAll(".acc-legal-input")).some(function (inp) {
      return inp.files && inp.files.length > 0;
    });

    document.querySelectorAll("#acc-setup-progress .setup-step").forEach(function (step) {
      var key = step.getAttribute("data-step");
      var done = (key === "basic" && basicDone) ||
        (key === "images" && imagesDone) ||
        (key === "policy" && policyDone) ||
        (key === "legal" && legalDone);
      step.classList.toggle("done", done);
      var icon = step.querySelector("i");
      if (icon) {
        icon.className = done ? "bi bi-check-circle-fill" : "bi bi-circle";
      }
    });
  }

  function renderImageStrip() {
    if (!strip) return;
    strip.innerHTML = "";
    imageItems.forEach(function (item, i) {
      var el = document.createElement("div");
      el.className = "acc-image-item";
      el.draggable = true;
      el.dataset.idx = String(i);
      el.innerHTML =
        (i === 0 ? '<span class="acc-image-item__cover">Ảnh bìa</span>' : "") +
        '<img src="' + item.preview + '" alt="Ảnh ' + (i + 1) + '">' +
        '<button type="button" class="acc-image-item__remove" aria-label="Xóa ảnh">&times;</button>';
      el.querySelector(".acc-image-item__remove").addEventListener("click", function (e) {
        e.stopPropagation();
        imageItems.splice(i, 1);
        markDirty();
        renderImageStrip();
        updateSetupProgress();
      });
      el.addEventListener("dragstart", function (e) {
        el.classList.add("dragging");
        e.dataTransfer.setData("text/plain", String(i));
      });
      el.addEventListener("dragend", function () { el.classList.remove("dragging"); });
      el.addEventListener("dragover", function (e) { e.preventDefault(); });
      el.addEventListener("drop", function (e) {
        e.preventDefault();
        var from = parseInt(e.dataTransfer.getData("text/plain"), 10);
        var to = i;
        if (from === to || isNaN(from)) return;
        var moved = imageItems.splice(from, 1)[0];
        imageItems.splice(to, 0, moved);
        markDirty();
        renderImageStrip();
      });
      strip.appendChild(el);
    });

    if (imageItems.length < MAX_IMAGES) {
      var add = document.createElement("div");
      add.className = "acc-image-add";
      add.innerHTML = '<i class="bi bi-plus-lg mb-1"></i><span>Thêm ảnh</span>';
      add.addEventListener("click", function () { fileInput && fileInput.click(); });
      strip.appendChild(add);
    }
    updateSetupProgress();
  }

  function addImageFiles(files) {
    var remaining = MAX_IMAGES - imageItems.length;
    if (remaining <= 0) {
      showModal(maxImagesModal);
      return;
    }
    var toAdd = Array.from(files).slice(0, remaining);
    if (files.length > remaining) showModal(maxImagesModal);
    toAdd.forEach(function (file) {
      if (!file.type.startsWith("image/")) return;
      var idx = nextFileIdx++;
      imageItems.push({ type: "new", file: file, fileIdx: idx, preview: URL.createObjectURL(file) });
    });
    markDirty();
    renderImageStrip();
  }

  if (strip) {
    try {
      var existing = JSON.parse(strip.getAttribute("data-existing") || "[]");
      initialImageUrls = existing.slice();
      existing.forEach(function (url) {
        imageItems.push({ type: "existing", url: url, preview: url, fileIdx: null });
      });
    } catch (e) {}
    renderImageStrip();
  }

  uploadTrigger && uploadTrigger.addEventListener("click", function () {
    fileInput && fileInput.click();
  });
  fileInput && fileInput.addEventListener("change", function () {
    if (fileInput.files.length) addImageFiles(fileInput.files);
    fileInput.value = "";
  });
  uploadBox && uploadBox.addEventListener("dragover", function (e) {
    e.preventDefault();
    uploadBox.style.borderColor = "var(--rovva-primary-blue)";
  });
  uploadBox && uploadBox.addEventListener("dragleave", function () {
    uploadBox.style.borderColor = "";
  });
  uploadBox && uploadBox.addEventListener("drop", function (e) {
    e.preventDefault();
    uploadBox.style.borderColor = "";
    if (e.dataTransfer.files.length) addImageFiles(e.dataTransfer.files);
  });

  addFeatureBtn && featuresAnchor && addFeatureBtn.addEventListener("click", function () {
    var col = document.createElement("div");
    col.className = "col-auto custom-feature-row";
    col.setAttribute("data-custom-feature", "");
    col.innerHTML =
      '<label class="feature-check">' +
      '<input type="checkbox" class="form-check-input mt-0 acc-feature-input acc-custom-checkbox">' +
      '<input type="text" name="custom_feature_name" placeholder="Nhập Đặc điểm" class="acc-custom-name">' +
      "</label>";
    featuresAnchor.parentNode.insertBefore(col, featuresAnchor);
    col.querySelector(".acc-custom-name").addEventListener("input", markDirty);
    markDirty();
  });

  form.querySelectorAll("input, select, textarea").forEach(function (el) {
    el.addEventListener("change", function () { markDirty(); updateSetupProgress(); });
    el.addEventListener("input", function () { markDirty(); updateSetupProgress(); });
  });

  cancelBtn && cancelBtn.addEventListener("click", function () {
    if (!formDirty) {
      window.location.href = cancelUrl;
      return;
    }
    var confirmLink = document.getElementById("acc-cancel-confirm");
    if (confirmLink) confirmLink.href = cancelUrl;
    showModal(cancelModal);
  });

  deleteTrigger && deleteTrigger.addEventListener("click", function () {
    var msg = document.getElementById("acc-delete-message");
    var actions = document.getElementById("acc-delete-actions");
    var blocked = document.getElementById("acc-delete-blocked");
    var confirmBtn = document.getElementById("acc-delete-confirm");
    if (stayingCount > 0) {
      if (msg) msg.textContent = "Đang có " + stayingCount + " booking đang lưu trú, không thể xóa.";
      if (actions) actions.classList.add("d-none");
      if (blocked) blocked.classList.remove("d-none");
    } else {
      if (msg) msg.textContent = "Xóa CSLT sẽ mất toàn bộ phòng và booking. Khách đã đặt có thể được hoàn tiền. Hành động này không thể hoàn tác.";
      if (actions) actions.classList.remove("d-none");
      if (blocked) blocked.classList.add("d-none");
    }
    showModal(deleteModal);
  });

  document.querySelectorAll(".host-nav-link").forEach(function (link) {
    link.addEventListener("click", function (e) {
      if (!formDirty) return;
      e.preventDefault();
      var navModal = document.getElementById("accNavModal");
      var discard = document.getElementById("acc-nav-discard");
      var target = link.getAttribute("data-host-nav") || link.getAttribute("href");
      if (discard) discard.href = target;
      showModal(navModal);
    });
  });

  var navDiscard = document.getElementById("acc-nav-discard");
  navDiscard && navDiscard.addEventListener("click", function () {
    formDirty = false;
  });

  function cleanupCustomFeatures() {
    form.querySelectorAll(".acc-custom-checkbox").forEach(function (cb) {
      var row = cb.closest(".custom-feature-row");
      var nameInp = row && row.querySelector(".acc-custom-name");
      if (!nameInp) return;
      if (cb.checked && String(nameInp.value || "").trim()) {
        nameInp.setAttribute("name", "custom_feature_name");
      } else {
        nameInp.removeAttribute("name");
      }
    });
  }

  function currentImageUrls() {
    return imageItems.map(function (it) { return it.url || it.preview; });
  }

  function imagesChanged() {
    if (imageItems.some(function (it) { return it.type === "new"; })) return true;
    var now = currentImageUrls();
    if (now.length !== initialImageUrls.length) return true;
    for (var i = 0; i < now.length; i++) {
      if (now[i] !== initialImageUrls[i]) return true;
    }
    return false;
  }

  form.addEventListener("submit", async function (e) {
    if (imageItems.length === 0) {
      e.preventDefault();
      showHostAlert("CSLT bắt buộc có ít nhất 1 ảnh trước khi lưu.");
      return;
    }

    cleanupCustomFeatures();

    if (!imagesChanged()) return;

    e.preventDefault();
    if (fileInputsHost) fileInputsHost.innerHTML = "";
    var order = [];
    var filePromises = imageItems.map(function (item, i) {
      if (item.type === "new") {
        order.push(item.fileIdx);
        var inp = document.createElement("input");
        inp.type = "file";
        inp.name = "acc_image_" + item.fileIdx;
        inp.hidden = true;
        var dt = new DataTransfer();
        dt.items.add(item.file);
        inp.files = dt.files;
        fileInputsHost.appendChild(inp);
        return Promise.resolve();
      }
      return fetch(item.url).then(function (r) { return r.blob(); }).then(function (blob) {
        var idx = nextFileIdx++;
        order.push(idx);
        var inp = document.createElement("input");
        inp.type = "file";
        inp.name = "acc_image_" + idx;
        inp.hidden = true;
        var dt = new DataTransfer();
        dt.items.add(new File([blob], "image_" + i + ".jpg", { type: blob.type || "image/jpeg" }));
        inp.files = dt.files;
        fileInputsHost.appendChild(inp);
      });
    });

    await Promise.all(filePromises);
    if (orderInput) orderInput.value = JSON.stringify(order);
    form.submit();
  });

  updateSetupProgress();
}

function initPauseModal(triggerId, modalId, formId, msgId, actionsId, blockedId, defaultMsg, blockedMsg) {
  var trigger = document.getElementById(triggerId);
  var modal = document.getElementById(modalId);
  if (!trigger || !modal) return;
  trigger.addEventListener("click", function () {
    var staying = parseInt(trigger.getAttribute("data-staying-count") || "0", 10);
    var msg = document.getElementById(msgId);
    var actions = document.getElementById(actionsId);
    var blocked = document.getElementById(blockedId);
    var pauseForm = document.getElementById(formId);
    var pauseUrl = trigger.getAttribute("data-pause-url");
    if (pauseForm && pauseUrl) pauseForm.action = pauseUrl;
    if (staying > 0) {
      if (msg) msg.textContent = blockedMsg.replace("{n}", staying);
      if (actions) actions.classList.add("d-none");
      if (blocked) blocked.classList.remove("d-none");
    } else {
      if (msg) msg.textContent = defaultMsg;
      if (actions) actions.classList.remove("d-none");
      if (blocked) blocked.classList.add("d-none");
    }
    if (window.bootstrap) bootstrap.Modal.getOrCreateInstance(modal).show();
  });
}

function initImageStripForm(opts) {
  var form = document.getElementById(opts.formId);
  var strip = document.getElementById(opts.stripId);
  if (!form || !strip || form.dataset.imgBound) return;
  form.dataset.imgBound = "1";

  var fileInput = document.getElementById(opts.fileInputId);
  var uploadBox = document.getElementById(opts.uploadBoxId);
  var uploadTrigger = document.getElementById(opts.uploadTriggerId);
  var fileInputsHost = document.getElementById(opts.fileInputsHostId);
  var orderInput = document.getElementById(opts.orderInputId);
  var maxModal = document.getElementById(opts.maxModalId);
  var prefix = opts.filePrefix || "acc_image_";
  var MAX = 5;
  var imageItems = [];
  var nextFileIdx = 0;
  var initialImageUrls = [];

  function showModal(el) {
    if (el && window.bootstrap) bootstrap.Modal.getOrCreateInstance(el).show();
  }

  function renderStrip() {
    strip.innerHTML = "";
    imageItems.forEach(function (item, i) {
      var el = document.createElement("div");
      el.className = "acc-image-item";
      el.draggable = true;
      el.innerHTML =
        (i === 0 ? '<span class="acc-image-item__cover">Ảnh bìa</span>' : "") +
        '<img src="' + item.preview + '" alt="">' +
        '<button type="button" class="acc-image-item__remove">&times;</button>';
      el.querySelector(".acc-image-item__remove").addEventListener("click", function (e) {
        e.stopPropagation();
        imageItems.splice(i, 1);
        renderStrip();
        opts.onChange && opts.onChange(imageItems.length);
      });
      el.addEventListener("dragstart", function (e) { e.dataTransfer.setData("text/plain", String(i)); });
      el.addEventListener("dragover", function (e) { e.preventDefault(); });
      el.addEventListener("drop", function (e) {
        e.preventDefault();
        var from = parseInt(e.dataTransfer.getData("text/plain"), 10);
        if (isNaN(from) || from === i) return;
        var moved = imageItems.splice(from, 1)[0];
        imageItems.splice(i, 0, moved);
        renderStrip();
      });
      strip.appendChild(el);
    });
    if (imageItems.length < MAX) {
      var add = document.createElement("div");
      add.className = "acc-image-add";
      add.innerHTML = '<i class="bi bi-plus-lg mb-1"></i><span>Thêm ảnh</span>';
      add.addEventListener("click", function () { fileInput && fileInput.click(); });
      strip.appendChild(add);
    }
    opts.onChange && opts.onChange(imageItems.length);
  }

  function addFiles(files) {
    var remaining = MAX - imageItems.length;
    if (remaining <= 0) { showModal(maxModal); return; }
    Array.from(files).slice(0, remaining).forEach(function (file) {
      if (!file.type.startsWith("image/")) return;
      var idx = nextFileIdx++;
      imageItems.push({ type: "new", file: file, fileIdx: idx, preview: URL.createObjectURL(file) });
    });
    if (files.length > remaining) showModal(maxModal);
    renderStrip();
  }

  try {
    var existing = JSON.parse(strip.getAttribute("data-existing") || "[]");
    initialImageUrls = existing.slice();
    existing.forEach(function (url) {
      imageItems.push({ type: "existing", url: url, preview: url });
    });
  } catch (e) {}
  renderStrip();

  uploadTrigger && uploadTrigger.addEventListener("click", function () { fileInput && fileInput.click(); });
  fileInput && fileInput.addEventListener("change", function () {
    if (fileInput.files.length) addFiles(fileInput.files);
    fileInput.value = "";
  });
  uploadBox && uploadBox.addEventListener("drop", function (e) {
    e.preventDefault();
    if (e.dataTransfer.files.length) addFiles(e.dataTransfer.files);
  });
  uploadBox && uploadBox.addEventListener("dragover", function (e) { e.preventDefault(); });

  form.addEventListener("submit", async function (e) {
    if (imageItems.length === 0) {
      e.preventDefault();
      showHostAlert(opts.emptyMsg || "Bắt buộc có ít nhất 1 ảnh.");
      return;
    }
    var changed = imageItems.some(function (it) { return it.type === "new"; }) ||
      imageItems.length !== initialImageUrls.length;
    if (!changed) {
      for (var i = 0; i < imageItems.length; i++) {
        if ((imageItems[i].url || imageItems[i].preview) !== initialImageUrls[i]) changed = true;
      }
    }
    if (!changed) return;
    e.preventDefault();
    if (fileInputsHost) fileInputsHost.innerHTML = "";
    var order = [];
    var promises = imageItems.map(function (item, i) {
      if (item.type === "new") {
        order.push(item.fileIdx);
        var inp = document.createElement("input");
        inp.type = "file";
        inp.name = prefix + item.fileIdx;
        inp.hidden = true;
        var dt = new DataTransfer();
        dt.items.add(item.file);
        inp.files = dt.files;
        fileInputsHost.appendChild(inp);
        return Promise.resolve();
      }
      return fetch(item.url).then(function (r) { return r.blob(); }).then(function (blob) {
        var idx = nextFileIdx++;
        order.push(idx);
        var inp = document.createElement("input");
        inp.type = "file";
        inp.name = prefix + idx;
        inp.hidden = true;
        var dt = new DataTransfer();
        dt.items.add(new File([blob], "img_" + i + ".jpg", { type: blob.type || "image/jpeg" }));
        inp.files = dt.files;
        fileInputsHost.appendChild(inp);
      });
    });
    await Promise.all(promises);
    if (orderInput) orderInput.value = JSON.stringify(order);
    form.submit();
  });

  return { getCount: function () { return imageItems.length; } };
}

function initRoomForm() {
  var form = document.getElementById("room-form");
  if (!form || form.dataset.roomBound) return;
  form.dataset.roomBound = "1";

  var cancelUrl = form.getAttribute("data-cancel-url") || "/host/accommodation/";
  var cancelBtn = document.getElementById("room-cancel-btn");
  var deleteTrigger = document.getElementById("room-delete-trigger");
  var imgApi;

  function updateRoomProgress(imgCount) {
    var basic = !!form.querySelector('[name="name"]')?.value?.trim();
    var amenities = form.querySelectorAll('[name="features"]:checked').length > 0 ||
      Array.from(form.querySelectorAll(".acc-custom-name")).some(function (i) { return i.value.trim(); });
    var price = !!form.querySelector('[name="base_price"]')?.value;
    document.querySelectorAll("#room-setup-progress .setup-step").forEach(function (step) {
      var key = step.getAttribute("data-step");
      var done = (key === "basic" && basic) || (key === "images" && imgCount > 0) ||
        (key === "amenities" && amenities) || (key === "price" && price);
      step.classList.toggle("done", done);
      var icon = step.querySelector("i");
      if (icon) icon.className = done ? "bi bi-check-circle-fill" : "bi bi-circle";
    });
  }

  imgApi = initImageStripForm({
    formId: "room-form",
    stripId: "room-image-strip",
    fileInputId: "room-file-input",
    uploadBoxId: "room-upload-box",
    uploadTriggerId: "room-upload-trigger",
    fileInputsHostId: "room-image-file-inputs",
    orderInputId: "room-image-order-input",
    maxModalId: "accMaxImagesModal",
    filePrefix: "room_image_",
    emptyMsg: "Phòng bắt buộc có ít nhất 1 ảnh trước khi lưu.",
    onChange: updateRoomProgress,
  });

  document.getElementById("room-add-feature-btn")?.addEventListener("click", function () {
    var anchor = document.getElementById("room-custom-features-anchor");
    if (!anchor) return;
    var col = document.createElement("div");
    col.className = "col-md-4 col-sm-6 custom-feature-row";
    col.innerHTML =
      '<label class="feature-check w-100">' +
      '<input type="checkbox" class="form-check-input mt-0 acc-custom-checkbox">' +
      '<input type="text" placeholder="Nhập tiện ích" class="acc-custom-name">' +
      "</label>";
    anchor.parentNode.insertBefore(col, anchor);
    updateRoomProgress(imgApi ? imgApi.getCount() : 0);
  });

  document.getElementById("room-add-service-btn")?.addEventListener("click", function () {
    var list = document.getElementById("room-services-list");
    if (!list) return;
    var row = document.createElement("div");
    row.className = "row g-2 align-items-end mb-2 service-row";
    row.innerHTML =
      '<div class="col-md-5"><small class="text-muted">Tên dịch vụ</small><input type="text" name="service_name" class="form-control"></div>' +
      '<div class="col-md-3"><small class="text-muted">Giá</small><input type="text" name="service_price" class="form-control"></div>' +
      '<div class="col-md-3"><small class="text-muted">Ghi chú (Đơn vị)</small><input type="text" name="service_note" class="form-control"></div>' +
      '<div class="col-md-1"><button type="button" class="btn btn-link text-danger p-0 remove-service-btn">&times;</button></div>';
    list.appendChild(row);
    row.querySelector(".remove-service-btn").addEventListener("click", function () { row.remove(); });
  });

  document.getElementById("room-services-list")?.addEventListener("click", function (e) {
    if (e.target.classList.contains("remove-service-btn")) e.target.closest(".service-row")?.remove();
  });

  form.querySelectorAll(".room-progress-input, [name='features']").forEach(function (el) {
    el.addEventListener("change", function () { updateRoomProgress(imgApi ? imgApi.getCount() : 0); });
    el.addEventListener("input", function () { updateRoomProgress(imgApi ? imgApi.getCount() : 0); });
  });

  form.addEventListener("submit", function () {
    form.querySelectorAll(".acc-custom-checkbox").forEach(function (cb) {
      var nameInp = cb.closest(".custom-feature-row")?.querySelector(".acc-custom-name");
      if (!nameInp) return;
      if (cb.checked && nameInp.value.trim()) nameInp.setAttribute("name", "custom_feature_name");
      else nameInp.removeAttribute("name");
    });
  });

  cancelBtn && cancelBtn.addEventListener("click", function () {
    showHostConfirm("Thay đổi không được lưu. Rời khỏi trang?", function () {
      window.location.href = cancelUrl;
    }, { title: "Rời khỏi trang", okText: "Rời khỏi" });
  });

  deleteTrigger && deleteTrigger.addEventListener("click", function () {
    showHostConfirm("Xóa phòng sẽ không thể hoàn tác. Tiếp tục?", function () {
      document.getElementById("deleteRoomForm")?.submit();
    }, { title: "Xóa phòng", okText: "Xóa", danger: true });
  });

  updateRoomProgress(imgApi ? imgApi.getCount() : 0);
}

function initRoomDetail() {
  document.querySelectorAll("#roomTabs [data-room-tab]").forEach(function (tab) {
    tab.addEventListener("click", function (e) {
      e.preventDefault();
      var target = tab.getAttribute("data-room-tab");
      document.querySelectorAll("#roomTabs .nav-link").forEach(function (t) {
        t.classList.remove("active");
      });
      tab.classList.add("active");
      document.querySelectorAll(".room-tab-pane").forEach(function (p) { p.classList.add("d-none"); });
      var pane = document.getElementById(target);
      if (pane) pane.classList.remove("d-none");
    });
  });

  if (window.location.hash === "#tab-reviews") {
    document.querySelector('#roomTabs [data-room-tab="tab-reviews"]')?.click();
  }

  var list = document.getElementById("review-list");
  if (!list) return;
  var cards = Array.from(list.querySelectorAll(".review-card"));
  var sortEl = document.getElementById("review-sort");
  var activeStar = "all";

  function applyReviewFilters() {
    var sort = sortEl ? sortEl.value : "newest";
    cards.forEach(function (card) {
      var rating = String(card.getAttribute("data-rating"));
      var match = activeStar === "all" || rating === activeStar;
      card.classList.toggle("hidden", !match);
    });
    var visible = cards.filter(function (c) { return !c.classList.contains("hidden"); });
    visible.sort(function (a, b) {
      var ta = parseFloat(a.getAttribute("data-ts") || "0");
      var tb = parseFloat(b.getAttribute("data-ts") || "0");
      return sort === "oldest" ? ta - tb : tb - ta;
    });
    visible.forEach(function (c) { list.appendChild(c); });
  }

  sortEl && sortEl.addEventListener("change", applyReviewFilters);
  document.querySelectorAll(".filter-star").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll(".filter-star").forEach(function (b) {
        b.classList.remove("active", "btn-primary");
        b.classList.add("btn-outline-secondary");
      });
      btn.classList.add("active", "btn-primary");
      btn.classList.remove("btn-outline-secondary");
      activeStar = btn.getAttribute("data-star") || "all";
      applyReviewFilters();
    });
  });
}

function initHostConfirmForms() {
  document.querySelectorAll("form[data-host-confirm-delete]").forEach(function (form) {
    if (form.dataset.confirmBound) return;
    form.dataset.confirmBound = "1";
    form.addEventListener("submit", function (e) {
      if (form.dataset.confirmed === "1") {
        form.dataset.confirmed = "";
        return;
      }
      e.preventDefault();
      var message = form.getAttribute("data-host-confirm-delete") || "Bạn có chắc chắn muốn xóa?";
      showHostConfirm(message, function () {
        form.dataset.confirmed = "1";
        if (typeof form.requestSubmit === "function") form.requestSubmit();
        else form.submit();
      }, { title: "Xác nhận xóa", okText: "Xóa", danger: true });
    });
  });
}

function initHostRoomTabs() {
  var tabRoot = document.getElementById("host-room-tabs");
  var grid = document.getElementById("host-room-grid");
  if (!tabRoot || !grid) return;

  var cards = grid.querySelectorAll("[data-room-status]");
  var buttons = tabRoot.querySelectorAll("[data-room-filter]");

  function applyFilter(status) {
    cards.forEach(function (card) {
      var roomStatus = card.getAttribute("data-room-status");
      var show = status === "all" || roomStatus === status;
      card.style.display = show ? "" : "none";
    });
  }

  var initial = tabRoot.querySelector(".nav-link.active");
  if (initial) applyFilter(initial.getAttribute("data-room-filter") || "all");

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      buttons.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      applyFilter(btn.getAttribute("data-room-filter") || "all");
    });
  });
}

function formatRuleAdjust(type, value) {
  var v = String(value || "").trim();
  if (!v) return "—";
  if (type === "percent_up") return "+" + v + "%";
  if (type === "percent_down") return "-" + v + "%";
  if (type === "fixed_up") return "+" + v + "đ";
  return "-" + v + "đ";
}

function initPriceSuggestionsPage() {
  var page = document.getElementById("price-suggestions-page");
  if (!page || page.dataset.priceBound) return;
  page.dataset.priceBound = "1";

  var rulesDataEl = document.getElementById("pricing-rules-data");
  var tbody = document.getElementById("pricing-rules-tbody");
  var detailPanel = document.getElementById("rule-detail-panel");
  if (!rulesDataEl || !tbody) return;

  var rules = [];
  try { rules = JSON.parse(rulesDataEl.textContent || "[]"); } catch (e) { rules = []; }
  var nextId = rules.reduce(function (m, r) { return Math.max(m, r.id || 0); }, 0) + 1;
  var selectedId = null;

  function showRuleDetail(rule) {
    if (!detailPanel || !rule) return;
    selectedId = rule.id;
    document.getElementById("rule-detail-name").textContent = rule.name;
    document.getElementById("rule-detail-condition").textContent = rule.condition;
    var adjEl = document.getElementById("rule-detail-adjust");
    adjEl.textContent = rule.adjust;
    adjEl.className = "fw-bold " + (String(rule.adjust).startsWith("+") ? "text-success" : "text-danger");
    document.getElementById("rule-detail-status").textContent = rule.active ? "Đang bật" : "Đã tắt";
    document.getElementById("rule-detail-note").textContent = rule.note || "Không có ghi chú.";
    detailPanel.classList.remove("d-none");
  }

  function renderRules() {
    tbody.innerHTML = "";
    if (!rules.length) {
      tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted py-4">Chưa có quy tắc nào.</td></tr>';
      detailPanel && detailPanel.classList.add("d-none");
      return;
    }
    rules.forEach(function (rule) {
      var tr = document.createElement("tr");
      tr.className = "rule-row" + (selectedId === rule.id ? " is-selected" : "");
      tr.innerHTML =
        '<td class="fw-bold">' + escapeHtml(rule.name) + "</td>" +
        "<td>" + escapeHtml(rule.condition) + "</td>" +
        '<td class="fw-bold ' + (String(rule.adjust).startsWith("+") ? "text-success" : "text-danger") + '">' + escapeHtml(rule.adjust) + "</td>" +
        '<td><div class="form-check form-switch m-0"><input class="form-check-input rule-active-toggle" type="checkbox" data-rule-id="' + rule.id + '"' + (rule.active ? " checked" : "") + "></div></td>";
      tr.addEventListener("click", function (e) {
        if (e.target.closest(".rule-active-toggle")) return;
        tbody.querySelectorAll(".rule-row").forEach(function (r) { r.classList.remove("is-selected"); });
        tr.classList.add("is-selected");
        showRuleDetail(rule);
      });
      tr.querySelector(".rule-active-toggle").addEventListener("change", function (e) {
        e.stopPropagation();
        rule.active = e.target.checked;
        if (selectedId === rule.id) showRuleDetail(rule);
      });
      tbody.appendChild(tr);
    });
    if (selectedId) {
      var current = rules.find(function (r) { return r.id === selectedId; });
      if (current) showRuleDetail(current);
    }
  }

  document.getElementById("rule-save-btn")?.addEventListener("click", function () {
    var name = document.getElementById("rule-name-input")?.value.trim();
    var condition = document.getElementById("rule-condition-input")?.value.trim();
    var adjustType = document.getElementById("rule-adjust-type")?.value;
    var adjustValue = document.getElementById("rule-adjust-value")?.value.trim();
    var note = document.getElementById("rule-note-input")?.value.trim();
    var active = document.getElementById("rule-active-input")?.checked;
    if (!name || !condition || !adjustValue) {
      showHostAlert("Vui lòng nhập đầy đủ tên, điều kiện và giá trị điều chỉnh.");
      return;
    }
    var rule = {
      id: nextId++,
      name: name,
      condition: condition,
      adjust: formatRuleAdjust(adjustType, adjustValue),
      adjust_type: adjustType,
      adjust_value: adjustValue,
      active: !!active,
      note: note || "",
    };
    rules.push(rule);
    selectedId = rule.id;
    renderRules();
    showRuleDetail(rule);
    document.getElementById("rule-name-input").value = "";
    document.getElementById("rule-condition-input").value = "";
    document.getElementById("rule-adjust-value").value = "";
    document.getElementById("rule-note-input").value = "";
    document.getElementById("rule-active-input").checked = true;
    var modal = document.getElementById("addRuleModal");
    if (modal && window.bootstrap) bootstrap.Modal.getInstance(modal)?.hide();
  });

  renderRules();
  if (rules.length) {
    selectedId = rules[0].id;
    renderRules();
  }

  var chartEl = document.getElementById("priceRevenueChart");
  if (chartEl && window.Chart) {
    var labels = JSON.parse(page.getAttribute("data-revenue-labels") || "[]");
    var actual = JSON.parse(page.getAttribute("data-revenue-actual") || "[]");
    var predicted = JSON.parse(page.getAttribute("data-revenue-predicted") || "[]");
    new Chart(chartEl.getContext("2d"), {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Thực tế",
            data: actual,
            borderColor: "#2784f0",
            backgroundColor: "rgba(39, 132, 240, 0.08)",
            fill: true,
            tension: 0.35,
            pointRadius: 2,
          },
          {
            label: "Dự đoán",
            data: predicted,
            borderColor: "#10b981",
            backgroundColor: "transparent",
            borderDash: [6, 4],
            tension: 0.35,
            pointRadius: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { display: true, position: "bottom" },
        },
        scales: {
          x: { grid: { display: false }, ticks: { maxTicksLimit: 10, font: { size: 11 } } },
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (v) {
                if (v >= 1000000) return (v / 1000000).toFixed(1) + "tr";
                if (v >= 1000) return (v / 1000).toFixed(0) + "k";
                return v;
              },
            },
          },
        },
      },
    });
  }
}

function initDisputeRoomFilter() {
  var accSelect = document.getElementById("dispute-filter-acc");
  var roomSelect = document.getElementById("dispute-filter-room");
  if (!accSelect || !roomSelect || roomSelect.dataset.bound) return;
  roomSelect.dataset.bound = "1";

  var allOptions = Array.from(roomSelect.querySelectorAll("option[data-acc-id]"));

  function filterRooms() {
    var accId = accSelect.value;
    allOptions.forEach(function (opt) {
      var show = !accId || opt.getAttribute("data-acc-id") === accId;
      opt.hidden = !show;
      opt.disabled = !show;
    });
    if (roomSelect.value) {
      var selected = roomSelect.querySelector('option[value="' + roomSelect.value + '"]');
      if (selected && selected.disabled) roomSelect.value = "";
    }
  }

  accSelect.addEventListener("change", filterRooms);
  filterRooms();
}

function initNotificationBell() {
  var btn = document.getElementById("host-noti-btn");
  var modalEl = document.getElementById("hostNotiModal");
  if (!btn || !modalEl || !window.bootstrap) return;
  btn.addEventListener("click", function () {
    bootstrap.Modal.getOrCreateInstance(modalEl).show();
  });

  modalEl.querySelectorAll(".host-noti-item[data-href]").forEach(function (item) {
    item.addEventListener("click", function (e) {
      if (e.target.closest("button, form")) return;
      var href = item.getAttribute("data-href");
      if (href) window.location.href = href;
    });
  });
}

function formatVnd(n) {
  return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ".") + "đ";
}

function initRevenueLineChart() {
  var root = document.getElementById("revenue-line-chart");
  if (!root) return;

  var labels = JSON.parse(root.getAttribute("data-labels") || "[]");
  var values = JSON.parse(root.getAttribute("data-values") || "[]");
  var avg = parseFloat(root.getAttribute("data-avg") || "0");
  var svg = document.getElementById("revenue-line-svg");
  var labelsEl = document.getElementById("revenue-line-labels");
  var tooltip = document.getElementById("revenue-line-tooltip");
  if (!svg || !values.length) return;

  var w = 800;
  var h = 180;
  var padX = 24;
  var padY = 16;
  var maxVal = Math.max.apply(null, values.concat([avg, 1]));
  var step = values.length > 1 ? (w - padX * 2) / (values.length - 1) : 0;

  function yPos(v) {
    return h - padY - (v / maxVal) * (h - padY * 2);
  }

  var points = values.map(function (v, i) {
    return { x: padX + i * step, y: yPos(v), v: v, label: labels[i] || "" };
  });

  var linePath = points.map(function (p, i) {
    return (i === 0 ? "M" : "L") + p.x + "," + p.y;
  }).join(" ");

  var areaPath = linePath + " L" + points[points.length - 1].x + "," + (h - padY) +
    " L" + points[0].x + "," + (h - padY) + " Z";

  var avgY = yPos(avg);
  svg.innerHTML =
    '<defs><linearGradient id="revFill" x1="0" y1="0" x2="0" y2="1">' +
    '<stop offset="0%" stop-color="#2784f0" stop-opacity="0.18"/>' +
    '<stop offset="100%" stop-color="#2784f0" stop-opacity="0"/></linearGradient></defs>' +
    '<line x1="' + padX + '" y1="' + avgY + '" x2="' + (w - padX) + '" y2="' + avgY + '" stroke="#ef4444" stroke-width="2" stroke-dasharray="8 6"/>' +
    '<path d="' + areaPath + '" fill="url(#revFill)"/>' +
    '<path d="' + linePath + '" fill="none" stroke="#2784f0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>';

  points.forEach(function (p) {
    var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", p.x);
    circle.setAttribute("cy", p.y);
    circle.setAttribute("r", 5);
    circle.setAttribute("fill", "#2784f0");
    circle.setAttribute("stroke", "#fff");
    circle.setAttribute("stroke-width", "2");
    circle.style.cursor = "pointer";
    circle.addEventListener("mouseenter", function (ev) {
      if (!tooltip) return;
      tooltip.hidden = false;
      tooltip.textContent = (p.label ? p.label + ": " : "") + formatVnd(p.v);
      var rect = root.getBoundingClientRect();
      var sx = (p.x / w) * rect.width;
      tooltip.style.left = sx + "px";
      tooltip.style.top = (p.y / h) * 180 + "px";
    });
    circle.addEventListener("mouseleave", function () {
      if (tooltip) tooltip.hidden = true;
    });
    svg.appendChild(circle);
  });

  if (labelsEl) {
    labelsEl.innerHTML = "";
    var showEvery = values.length > 14 ? Math.ceil(values.length / 10) : 1;
    labels.forEach(function (lbl, i) {
      if (i % showEvery !== 0 && i !== labels.length - 1) return;
      var span = document.createElement("span");
      span.textContent = lbl;
      labelsEl.appendChild(span);
    });
  }
}

function initHostAiFullPage() {
  var form = document.getElementById("host-ai-full-form");
  var messages = document.getElementById("host-ai-messages");
  var welcome = document.getElementById("host-ai-welcome");
  var newChat = document.getElementById("host-ai-new-chat");
  if (!form || !messages || form.dataset.aiBound) return;
  form.dataset.aiBound = "1";

  loadHostAiSessions();
  if (hostAiSessions.length) {
    hostAiActiveSessionId = hostAiSessions[0].id;
    renderHostAiFullConversation();
  }
  renderHostAiHistoryList();

  async function send(message) {
    if (!message || hostAiFullSending) return;
    hostAiFullSending = true;

    var session = getActiveHostAiSession();
    if (!session) session = createHostAiSession(message);
    if (!session.title || session.title === "Cuộc trò chuyện mới") {
      session.title = message.slice(0, 48);
    }

    if (welcome) welcome.hidden = true;
    appendHostAiFullBubble(messages, "user", message);
    session.messages.push({ role: "user", content: message });

    var typing = document.createElement("div");
    typing.className = "host-ai-bubble";
    typing.textContent = "Đang trả lời...";
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;

    try {
      var historyForApi = session.messages.slice(0, -1);
      var reply = await fetchHostAiReply(message, historyForApi);
      typing.remove();
      appendHostAiFullBubble(messages, "assistant", reply);
      session.messages.push({ role: "assistant", content: reply });
      session.updatedAt = Date.now();
      saveHostAiSessions();
      renderHostAiHistoryList();
    } catch (err) {
      typing.remove();
      appendHostAiFullBubble(messages, "assistant", err.message, " text-danger");
    } finally {
      hostAiFullSending = false;
    }
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var input = form.querySelector("input");
    var val = input ? input.value.trim() : "";
    if (!val) return;
    if (input) input.value = "";
    send(val);
  });

  document.querySelectorAll(".host-ai-suggestion").forEach(function (btn) {
    btn.addEventListener("click", function () {
      send(btn.getAttribute("data-prompt") || btn.textContent.trim());
    });
  });

  if (newChat) {
    newChat.addEventListener("click", function () {
      hostAiActiveSessionId = null;
      sessionStorage.removeItem(HOST_AI_BUBBLE_SESSION_KEY);
      clearHostAiMessagesKeepWelcome();
      renderHostAiHistoryList();
    });
  }
}

document.addEventListener("DOMContentLoaded", function () {
  initHostDialogs();
  initHostConfirmForms();
  initClickableRows();
  initRevenueTipsModal();
  initRevenueLineChart();
  initHostAiWidget();
  initHostAccTabs();
  initHostRoomTabs();
  initAccImageCarousel();
  initAccForm();
  initRoomForm();
  initRoomDetail();
  initPriceSuggestionsPage();
  initDisputeRoomFilter();
  initPauseModal("acc-pause-trigger", "accPauseModal", "accPauseForm", "acc-pause-message", "acc-pause-actions", "acc-pause-blocked",
    "Tạm ngưng sẽ ẩn CSLT khỏi tìm kiếm. Khách đã đặt có thể được hoàn tiền.",
    "Đang có {n} booking đang lưu trú, không thể tạm ngưng.");
  initPauseModal("room-pause-trigger", "roomPauseModal", "roomPauseForm", "room-pause-message", "room-pause-actions", "room-pause-blocked",
    "Tạm ngưng sẽ ẩn phòng khỏi tìm kiếm.",
    "Đang có {n} booking đang lưu trú, không thể tạm ngưng.");
  initNotificationBell();
  initHostAiFullPage();
});
