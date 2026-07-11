(function () {
  function normalizeText(value) {
    return (value || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function initHostFaqSearch() {
    var root = document.querySelector('[data-support-page="faq"]');
    if (!root) return;

    var input = document.getElementById("host-faq-search");
    var items = root.querySelectorAll("[data-faq-item]");
    var sections = root.querySelectorAll("[data-faq-section]");
    var empty = document.getElementById("host-faq-empty");
    if (!input || !items.length) return;

    function applyFilter() {
      var query = normalizeText(input.value.trim());
      var visibleCount = 0;

      items.forEach(function (item) {
        var text = normalizeText(item.textContent);
        var match = !query || text.indexOf(query) !== -1;
        item.classList.toggle("is-hidden", !match);
        if (match) visibleCount += 1;
      });

      sections.forEach(function (section) {
        var visibleInSection = section.querySelectorAll("[data-faq-item]:not(.is-hidden)").length;
        section.style.display = visibleInSection ? "" : "none";
      });

      if (empty) {
        empty.classList.toggle("is-visible", query.length > 0 && visibleCount === 0);
      }
    }

    input.addEventListener("input", applyFilter);
  }

  function initHostSupportToc() {
    document.querySelectorAll(".host-support-toc__link").forEach(function (link) {
      link.addEventListener("click", function (e) {
        var href = link.getAttribute("href");
        if (!href || href.charAt(0) !== "#") return;
        var target = document.querySelector(href);
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }

  function initHostPolicySearch() {
    var root = document.querySelector('[data-support-page="policy"]');
    if (!root) return;

    var input = document.getElementById("host-policy-search");
    var sections = root.querySelectorAll("[data-policy-section]");
    if (!input || !sections.length) return;

    function applyFilter() {
      var query = normalizeText(input.value.trim());

      sections.forEach(function (section) {
        var text = normalizeText(section.textContent);
        var match = !query || text.indexOf(query) !== -1;
        section.classList.toggle("is-hidden", !match);
      });
    }

    input.addEventListener("input", applyFilter);
  }

  document.addEventListener("DOMContentLoaded", function () {
    initHostFaqSearch();
    initHostPolicySearch();
    initHostSupportToc();
  });
})();
