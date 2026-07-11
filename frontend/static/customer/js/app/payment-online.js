(function () {
  "use strict";

  function fmtVnd(n) {
    return Number(n).toLocaleString("vi-VN") + "đ";
  }

  function initCountdown() {
    var el = document.getElementById("payment-countdown");
    var valueEl = document.getElementById("countdown-value");
    if (!el || !valueEl) return;

    var expires = el.getAttribute("data-expires");
    if (!expires) return;

    var end = new Date(expires).getTime();

    function tick() {
      var diff = Math.max(0, end - Date.now());
      var mins = Math.floor(diff / 60000);
      var secs = Math.floor((diff % 60000) / 1000);
      valueEl.textContent =
        String(mins).padStart(2, "0") + ":" + String(secs).padStart(2, "0");
      if (diff <= 0) {
        valueEl.textContent = "00:00";
        return;
      }
      window.setTimeout(tick, 1000);
    }

    tick();
  }

  function initCopyButtons() {
    document.querySelectorAll(".online-payment__copy").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var text = btn.getAttribute("data-copy") || "";
        if (!text) return;

        var done = function () {
          var old = btn.textContent;
          btn.textContent = "Đã copy";
          window.setTimeout(function () {
            btn.textContent = old;
          }, 1500);
        };

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done).catch(function () {});
        } else {
          var ta = document.createElement("textarea");
          ta.value = text;
          document.body.appendChild(ta);
          ta.select();
          try {
            document.execCommand("copy");
            done();
          } catch (e) {}
          document.body.removeChild(ta);
        }
      });
    });
  }

  function initPaymentConfirmModal() {
    var form = document.getElementById("online-payment-form");
    var modalEl = document.getElementById("payment-verify-modal");
    if (!form || !modalEl || typeof bootstrap === "undefined") return;

    var modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    var modalContent = modalEl.querySelector(".payment-verify-modal");
    var verifyDelayMs = 3000;
    var submitting = false;
    var verifyTimer = null;

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (submitting) return;

      modalContent.classList.remove("is-verifying");
      modal.show();
    });

    modalEl.addEventListener("shown.bs.modal", function () {
      if (submitting) return;

      modalContent.classList.add("is-verifying");
      verifyTimer = window.setTimeout(function () {
        submitting = true;
        form.submit();
      }, verifyDelayMs);
    });

    modalEl.addEventListener("hidden.bs.modal", function () {
      if (submitting) return;

      modalContent.classList.remove("is-verifying");
      if (verifyTimer) {
        window.clearTimeout(verifyTimer);
        verifyTimer = null;
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initCountdown();
    initCopyButtons();
    initPaymentConfirmModal();
  });
})();
