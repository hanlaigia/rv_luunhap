/**
 * Trang Bảo mật — đổi mật khẩu & xóa tài khoản.
 */

(function () {
  "use strict";

  function showFormError(el, message) {
    if (!el) return;
    if (!message) {
      el.hidden = true;
      el.textContent = "";
      return;
    }
    el.hidden = false;
    el.textContent = message;
  }

  function bindPasswordForm() {
    var form = document.getElementById("security-form");
    if (!form) return;

    var errorEl = document.getElementById("security-form-error");
    var currentInput = document.getElementById("sec-current");
    var newInput = document.getElementById("sec-new");
    var confirmInput = document.getElementById("sec-confirm");

    function clearError() {
      showFormError(errorEl, "");
    }

    [currentInput, newInput, confirmInput].forEach(function (input) {
      if (input) {
        input.addEventListener("input", clearError);
      }
    });

    form.addEventListener("submit", function (e) {
      var current = (currentInput && currentInput.value) || "";
      var newPass = (newInput && newInput.value) || "";
      var confirm = (confirmInput && confirmInput.value) || "";

      if (!current.trim() || !newPass.trim() || !confirm.trim()) {
        e.preventDefault();
        showFormError(errorEl, "Vui lòng điền đầy đủ thông tin.");
        return;
      }

      if (newPass === current) {
        e.preventDefault();
        showFormError(errorEl, "Mật khẩu mới phải khác mật khẩu hiện tại.");
        return;
      }

      if (newPass !== confirm) {
        e.preventDefault();
        showFormError(errorEl, "Xác nhận mật khẩu không khớp.");
        return;
      }
    });
  }

  function bindDeleteAccount() {
    var agreeCheckbox = document.getElementById("deleteAccountAgree");
    var confirmBtn = document.getElementById("deleteAccountConfirm");
    var step1El = document.getElementById("modalDeleteAccountStep1");
    var step2El = document.getElementById("modalDeleteAccountStep2");

    if (!confirmBtn || !step1El) return;

    if (agreeCheckbox && confirmBtn) {
      agreeCheckbox.addEventListener("change", function () {
        confirmBtn.disabled = !agreeCheckbox.checked;
      });
    }

    confirmBtn.addEventListener("click", function () {
      if (agreeCheckbox && !agreeCheckbox.checked) return;

      confirmBtn.disabled = true;

      fetch("/customer/account/security/delete", {
        method: "POST",
        credentials: "same-origin",
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then(function (res) {
          return res.json().then(function (data) {
            return { ok: res.ok, data: data };
          });
        })
        .then(function (result) {
          if (!result.ok || !result.data.ok) {
            var msg = (result.data && result.data.error) || "Không thể xóa tài khoản. Vui lòng thử lại.";
            window.alert(msg);
            confirmBtn.disabled = !(agreeCheckbox && agreeCheckbox.checked);
            return;
          }

          var step1 = window.bootstrap.Modal.getInstance(step1El)
            || new window.bootstrap.Modal(step1El);
          step1.hide();

          if (step2El) {
            var step2 = new window.bootstrap.Modal(step2El);
            step2.show();
            window.setTimeout(function () {
              window.location.href = "/customer/";
            }, 2200);
          } else {
            window.location.href = "/customer/";
          }
        })
        .catch(function () {
          window.alert("Không thể xóa tài khoản. Vui lòng thử lại.");
          confirmBtn.disabled = !(agreeCheckbox && agreeCheckbox.checked);
        });
    });

    step1El.addEventListener("hidden.bs.modal", function () {
      if (agreeCheckbox) {
        agreeCheckbox.checked = false;
      }
      confirmBtn.disabled = true;
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindPasswordForm();
    bindDeleteAccount();
  });
})();
