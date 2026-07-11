/**
 * Rovva customer — tương tác UI tối giản.
 */

import { initSupportPages } from "./support-pages.js";
import { initAiChat } from "./ai-chat.js";

(function () {
  "use strict";

  function autoDismissAlerts() {
    document.querySelectorAll(".alert-dismissible, [data-rova-flash]").forEach(function (el) {
      window.setTimeout(function () {
        el.classList.add("fade");
        el.style.transition = "opacity .4s ease";
        el.style.opacity = "0";
        window.setTimeout(function () { el.remove(); }, 400);
      }, 4000);
    });
  }

  function setFavoriteUi(btn, saved) {
    btn.classList.toggle("is-active", saved);
    btn.setAttribute("aria-pressed", saved ? "true" : "false");
    var icon = btn.querySelector("i");
    if (icon) {
      icon.classList.toggle("bi-heart-fill", saved);
      icon.classList.toggle("bi-heart", !saved);
    }
    btn.classList.toggle("text-danger", saved);
  }

  function toggleFavorite(accommodationId) {
    return fetch("/customer/favorites/toggle", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ accommodation_id: accommodationId }),
      credentials: "same-origin",
    });
  }

  function bindFavoriteButtons() {
    document.querySelectorAll(".favorite-btn[data-accommodation-id]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        var accId = parseInt(btn.getAttribute("data-accommodation-id"), 10);
        if (!accId) return;

        toggleFavorite(accId)
          .then(function (res) {
            if (res.status === 401) {
              window.location.href = "/login?next=" + encodeURIComponent(window.location.pathname);
              return null;
            }
            return res.json();
          })
          .then(function (data) {
            if (!data) return;
            setFavoriteUi(btn, !!data.saved);
          })
          .catch(function () {});
      });
    });

    document.querySelectorAll(".favorite-btn:not([data-accommodation-id])").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        var icon = btn.querySelector("i");
        if (!icon) return;
        var active = icon.classList.toggle("bi-heart-fill");
        icon.classList.toggle("bi-heart", !active);
        btn.classList.toggle("text-danger", active);
      });
    });
  }

  function bindAccommodationFavorite() {
    document.querySelectorAll('[data-rova-action="favorite"]').forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var accId = parseInt(btn.getAttribute("data-rova-id"), 10);
        if (!accId) return;

        toggleFavorite(accId)
          .then(function (res) {
            if (res.status === 401) {
              window.location.href = "/login?next=" + encodeURIComponent(window.location.pathname);
              return null;
            }
            if (!res.ok) return null;
            return res.json();
          })
          .then(function (data) {
            if (!data) return;
            setFavoriteUi(btn, !!data.saved);
          })
          .catch(function () {});
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    autoDismissAlerts();
    bindFavoriteButtons();
    bindAccommodationFavorite();
    initSupportPages();
    initAiChat();
  });
})();
