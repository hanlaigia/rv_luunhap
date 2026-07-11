/**
 * Nội dung tĩnh & tương tác cho các trang hỗ trợ / marketing (FAQ, đặc quyền, hướng dẫn, chính sách, AI).
 */

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/* ── FAQ ───────────────────────────────────────────────────────────── */

var FAQ_GROUPS = [
  {
    num: 1,
    title: "Đặt phòng và Hủy đặt phòng",
    icon: "bi-calendar-check",
    color: "#2784F0",
    items: [
      {
        q: "Làm thế nào để tôi tiến hành đặt phòng trên hệ thống?",
        a: "Truy cập trang chủ Rovva, nhập điểm đến, ngày nhận/trả phòng và số khách. Nhấn Tìm kiếm, chọn cơ sở lưu trú phù hợp, điền thông tin liên hệ và hoàn tất thanh toán theo hướng dẫn.",
      },
      {
        q: "Tôi có thể thay đổi ngày lưu trú hoặc hủy đặt phòng đã đặt không?",
        a: "Có. Vào Chuyến đi của tôi, chọn đơn cần thay đổi. Tùy chính sách của từng chỗ nghỉ, bạn có thể đổi ngày hoặc hủy và nhận hoàn tiền theo mức quy định.",
      },
      {
        q: "Làm sao để biết thao tác đặt phòng của tôi đã thành công?",
        a: "Sau khi thanh toán thành công, hệ thống hiển thị màn hình xác nhận và gửi email kèm mã đặt phòng. Bạn cũng xem lại trong mục Chuyến đi của tôi.",
      },
    ],
  },
  {
    num: 2,
    title: "Thanh toán và Hóa đơn",
    icon: "bi-credit-card",
    color: "#16A34A",
    items: [
      {
        q: "Hệ thống hiện đang hỗ trợ những hình thức thanh toán nào?",
        a: "Rovva hỗ trợ chuyển khoản ngân hàng, thẻ nội địa/quốc tế, ví điện tử và thanh toán tại chỗ nghỉ (nếu chỗ nghỉ cho phép).",
      },
      {
        q: "Giá phòng hiển thị trên website đã bao gồm thuế và phí chưa?",
        a: "Giá hiển thị đã bao gồm thuế VAT cơ bản. Một số phí phát sinh tại chỗ (phí giường phụ, dọn phòng muộn…) sẽ được ghi rõ trước khi bạn xác nhận đặt phòng.",
      },
      {
        q: "Tôi đi công tác và cần xuất hóa đơn đỏ (VAT) thì phải làm sao?",
        a: "Khi đặt phòng, tick mục Yêu cầu xuất hóa đơn và điền đầy đủ thông tin công ty. Hóa đơn điện tử sẽ gửi qua email trong 3–7 ngày làm việc sau khi trả phòng.",
      },
    ],
  },
  {
    num: 3,
    title: "Nhận phòng và Trả phòng",
    icon: "bi-key",
    color: "#EA580C",
    items: [
      {
        q: "Khung giờ nhận phòng và trả phòng tiêu chuẩn là mấy giờ?",
        a: "Thông thường nhận phòng từ 14:00 và trả phòng trước 12:00. Giờ cụ thể có thể khác tùy từng cơ sở — xem trong email xác nhận hoặc trang chi tiết đặt phòng.",
      },
      {
        q: "Tôi có thể yêu cầu nhận phòng sớm hoặc trả phòng muộn được không?",
        a: "Có thể, tùy tình trạng phòng trống. Liên hệ lễ tân hoặc gửi yêu cầu qua Rovva trước ngày nhận phòng. Phí phát sinh (nếu có) sẽ được thông báo trước.",
      },
      {
        q: "Khi đến quầy lễ tân, tôi cần xuất trình những giấy tờ gì?",
        a: "CMND/CCCD hoặc hộ chiếu của người đặt phòng, mã đặt phòng Rovva và thẻ thanh toán (nếu cần đặt cọc tại chỗ).",
      },
    ],
  },
  {
    num: 4,
    title: "Tài khoản và Ưu đãi",
    icon: "bi-shield-check",
    color: "#7C3AED",
    items: [
      {
        q: "Làm cách nào để tôi sử dụng mã giảm giá (Voucher/Coupon)?",
        a: "Tại bước thanh toán, nhập mã vào ô Mã giảm giá và nhấn Áp dụng. Mã hợp lệ sẽ tự động trừ vào tổng tiền.",
      },
      {
        q: "Tôi quên mật khẩu đăng nhập tài khoản, làm cách nào để khôi phục?",
        a: "Nhấn Quên mật khẩu tại trang đăng nhập, nhập email đã đăng ký. Hệ thống gửi link đặt lại mật khẩu trong vài phút.",
      },
    ],
  },
  {
    num: 5,
    title: "Tiện ích và Dịch vụ",
    icon: "bi-stars",
    color: "#0891B2",
    items: [
      {
        q: "Khách sạn có hỗ trợ kê thêm giường phụ (Extra bed) hoặc có chính sách riêng cho trẻ em không?",
        a: "Tùy từng chỗ nghỉ. Xem mục Tiện ích & Chính sách trẻ em trên trang chi tiết, hoặc ghi chú yêu cầu khi đặt phòng.",
      },
      {
        q: "Nơi lưu trú có cung cấp dịch vụ xe đưa đón sân bay không và tôi đăng ký như thế nào?",
        a: "Nhiều đối tác có dịch vụ đưa đón. Chọn thêm dịch vụ tại bước điền thông tin hoặc liên hệ lễ tân sau khi đặt phòng thành công.",
      },
    ],
  },
  {
    num: 6,
    title: "Trở thành Host",
    icon: "bi-house-door",
    color: "#92400E",
    items: [
      {
        q: "Tôi có nhà trống, căn hộ hoặc khách sạn và muốn đăng cho thuê trên nền tảng thì phải làm sao?",
        a: "Truy cập mục Trở thành Host, điền hồ sơ đăng ký. Đội ngũ Rovva sẽ liên hệ hướng dẫn niêm yết và kết nối công cụ quản lý phòng.",
      },
      {
        q: "Việc đăng ký niêm yết chỗ nghỉ trên nền tảng có mất phí không?",
        a: "Đăng ký và niêm yết miễn phí. Rovva chỉ thu hoa hồng khi có đơn đặt phòng thành công qua hệ thống.",
      },
    ],
  },
];

function renderFaq() {
  var root = document.getElementById("faq-root");
  if (!root) return;

  var html = FAQ_GROUPS.map(function (group, gi) {
    var items = group.items.map(function (item, ii) {
      var id = "faq-" + gi + "-" + ii;
      return (
        '<div class="faq-item">' +
        '<button class="faq-item__question collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#' + id + '" aria-expanded="false">' +
        "<span>" + escapeHtml(item.q) + '</span><i class="bi bi-chevron-down"></i></button>' +
        '<div class="collapse" id="' + id + '" data-bs-parent="#faq-acc-' + gi + '">' +
        '<div class="faq-item__answer">' + escapeHtml(item.a) + "</div></div></div>"
      );
    }).join("");

    return (
      '<div class="faq-group">' +
      '<div class="faq-group__head" style="--faq-color:' + group.color + '">' +
      '<span class="faq-group__badge"><i class="bi ' + group.icon + '"></i></span>' +
      '<h3 class="faq-group__title">' + group.num + ". " + escapeHtml(group.title) + "</h3></div>" +
      '<div class="faq-list" id="faq-acc-' + gi + '">' + items + "</div></div>"
    );
  }).join("");

  root.innerHTML = html;
}

/* ── Privileges & promotions ───────────────────────────────────────── */

var TIER_CARDS = [
  {
    key: "member",
    cls: "tier-card--member",
    name: "Thành Viên",
    condition: "Mặc định khi đăng ký",
    earn: "1% giá trị đơn đặt phòng",
    payment: "Thanh toán xu tối đa 10% hóa đơn",
    extras: ["Thưởng 5 xu cho mỗi đánh giá nơi lưu trú"],
  },
  {
    key: "silver",
    cls: "tier-card--silver",
    name: "Hạng Bạc",
    condition: "Tổng chi tiêu đạt 3.000.000 VNĐ",
    earn: "1% giá trị đơn đặt phòng",
    payment: "Thanh toán xu tối đa 12% hóa đơn",
    extras: ["Thưởng 5 xu cho mỗi đánh giá nơi lưu trú"],
  },
  {
    key: "gold",
    cls: "tier-card--gold",
    name: "Hạng Vàng",
    condition: "Tổng chi tiêu đạt 10.000.000 VNĐ",
    earn: "1,2% giá trị đơn đặt phòng",
    payment: "Thanh toán xu tối đa 15% hóa đơn",
    extras: [
      "Nhân 2 xu thưởng cho đơn đặt phòng vào tháng sinh nhật",
      "Thưởng 5 xu cho mỗi đánh giá nơi lưu trú",
    ],
  },
  {
    key: "platinum",
    cls: "tier-card--platinum",
    name: "Hạng Bạch Kim",
    condition: "Tổng chi tiêu đạt 25.000.000 VNĐ",
    earn: "1,5% giá trị đơn đặt phòng",
    payment: "Thanh toán xu tối đa 17% hóa đơn",
    extras: [
      "Nhân 3 xu thưởng cho đơn đặt phòng vào tháng sinh nhật",
      "Thưởng 10 xu cho mỗi đánh giá nơi lưu trú",
    ],
  },
  {
    key: "diamond",
    cls: "tier-card--diamond",
    name: "Hạng Kim Cương",
    condition: "Tổng chi tiêu đạt 50.000.000 VNĐ",
    earn: "2,5% giá trị đơn đặt phòng",
    payment: "Thanh toán xu tối đa 20% hóa đơn",
    extras: [
      "Giảm 20% phí dịch vụ phát sinh",
      "Tặng 01 đêm phòng miễn phí/năm (Tối đa 2.000.000 VNĐ)",
      "Thưởng 10 xu cho mỗi đánh giá nơi lưu trú",
    ],
  },
];

var TIER_RULES = [
  {
    title: "Chu kỳ ghi nhận",
    text: "Hạng thành viên được xét duyệt và có hiệu lực trong vòng 12 tháng kể từ ngày thăng hạng. Hệ thống sẽ liên tục cộng dồn các giao dịch phát sinh trong 365 ngày gần nhất.",
  },
  {
    title: "Trạng thái đơn hàng hợp lệ",
    text: 'Chỉ những hóa đơn đặt phòng ở trạng thái "Đã hoàn thành" (Check-out thành công) mới được cộng vào Tổng chi tiêu tích lũy. Các đơn hàng Hủy, Hoàn tiền hoặc Không nhận phòng sẽ không được tính.',
  },
  {
    title: "Chính sách duy trì và rớt hạng",
    text: "Hết chu kỳ 12 tháng, hệ thống sẽ kiểm tra lại tổng chi tiêu thực tế trong năm vừa qua. Nếu khách hàng không duy trì đủ hạn mức của hạng hiện tại, hệ thống sẽ tự động cập nhật về cấp hạng tương ứng với số tiền đã chi tiêu.",
  },
];

var VOUCHERS = [
  { tier: "all", discount: "Giảm ngay 50.000đ", subtitle: "Ưu đãi chào mừng (Welcome Voucher)", cond: "", expiry: "31/12/2026" },
  { tier: "all", discount: "Giảm 5%<br>(Tối đa 100.000đ)", subtitle: "", cond: "Điều kiện: Áp dụng cho các đơn có ngày nhận phòng vào Thứ 6, Thứ 7 và Chủ Nhật.", expiry: "31/08/2026" },
  { tier: "silver", discount: "Giảm 7%<br>(Tối đa 150.000đ)", subtitle: "", cond: "Điều kiện: Áp dụng cho các giao dịch đặt phòng thực hiện trên ứng dụng di động Rovva.", expiry: "31/07/2026" },
  { tier: "gold", discount: "Giảm 100.000đ", subtitle: "", cond: "Điều kiện: Áp dụng cho các hóa đơn đặt phòng có tổng giá trị từ 1.500.000đ trở lên.", expiry: "31/08/2026" },
  { tier: "silver", discount: "Giảm 250.000đ", subtitle: "", cond: "Điều kiện: Áp dụng cho các hóa đơn đặt phòng có tổng giá trị từ 3.500.000đ trở lên.", expiry: "31/08/2026" },
  { tier: "gold", discount: "Giảm 7%<br>(Tối đa 180.000đ)", subtitle: "", cond: "Điều kiện: Áp dụng riêng khi đặt các loại hình lưu trú là Homestay, Villa hoặc Căn hộ dịch vụ.", expiry: "30/09/2026" },
  { tier: "platinum", discount: "Giảm 10%<br>(Tối đa 150.000đ)", subtitle: "", cond: "Điều kiện: Các tài khoản đăng ký bằng email giáo dục", expiry: "30/09/2026" },
  { tier: "diamond", discount: "Giảm 12%<br>(Tối đa 150.000đ)", subtitle: "", cond: "Điều kiện: Các giao dịch đặt phòng được thực hiện trong khung giờ từ 22:00 đến 02:00 sáng mỗi ngày", expiry: "30/09/2026" },
];

function renderTierRow(icon, label, value, iconMod) {
  var mod = iconMod ? " tier-card__row-icon--" + iconMod : "";
  return (
    '<div class="tier-card__row">' +
    '<span class="tier-card__row-icon' + mod + '"><i class="bi ' + icon + '" aria-hidden="true"></i></span>' +
    '<div class="tier-card__row-body">' +
    '<span class="tier-card__row-label">' + escapeHtml(label) + "</span>" +
    '<span class="tier-card__row-value">' + escapeHtml(value) + "</span>" +
    "</div></div>"
  );
}

function renderTierExtraRows(icon, label, items) {
  var values = items.map(function (v) {
    return '<span class="tier-card__row-value">' + escapeHtml(v) + "</span>";
  }).join("");
  return (
    '<div class="tier-card__row tier-card__row--multi">' +
    '<span class="tier-card__row-icon tier-card__row-icon--gift"><i class="bi ' + icon + '" aria-hidden="true"></i></span>' +
    '<div class="tier-card__row-body">' +
    '<span class="tier-card__row-label">' + escapeHtml(label) + "</span>" +
    values +
    "</div></div>"
  );
}

function setupTierCarousel(wrap) {
  if (!wrap) return;
  var track = wrap.querySelector(".tier-carousel__track");
  var prev = wrap.querySelector(".tier-carousel__nav--prev");
  var next = wrap.querySelector(".tier-carousel__nav--next");
  if (!track || !prev || !next) return;

  function scrollStep() {
    var card = track.querySelector(".tier-card");
    if (!card) return 356;
    var gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap) || 19;
    return card.getBoundingClientRect().width + gap;
  }

  function updateNav() {
    var maxScroll = Math.max(0, track.scrollWidth - track.clientWidth);
    var atStart = track.scrollLeft <= 4;
    var atEnd = track.scrollLeft >= maxScroll - 4;
    var canScroll = maxScroll > 4;

    prev.hidden = !canScroll || atStart;
    next.hidden = !canScroll || atEnd;
  }

  prev.addEventListener("click", function () {
    track.scrollBy({ left: -scrollStep(), behavior: "smooth" });
    setTimeout(updateNav, 400);
  });
  next.addEventListener("click", function () {
    track.scrollBy({ left: scrollStep(), behavior: "smooth" });
    setTimeout(updateNav, 400);
  });

  track.addEventListener("scroll", updateNav, { passive: true });
  if ("onscrollend" in track) {
    track.addEventListener("scrollend", updateNav, { passive: true });
  }

  var ro = typeof ResizeObserver !== "undefined"
    ? new ResizeObserver(updateNav)
    : null;
  if (ro) ro.observe(track);

  window.addEventListener("resize", updateNav);
  requestAnimationFrame(updateNav);
  setTimeout(updateNav, 150);
  setTimeout(updateNav, 500);
}

function renderTierCard(t) {
  return (
    '<article class="tier-card ' + t.cls + '">' +
    '<div class="tier-card__inner">' +
    '<div class="tier-card__top"><span class="tier-card__brand">Rovva</span></div>' +
    '<h3 class="tier-card__name">' + escapeHtml(t.name) + "</h3>" +
    '<div class="tier-card__rows">' +
    renderTierRow("bi-patch-check-fill", "Điều kiện", t.condition, "condition") +
    renderTierRow("bi-cash-coin", "Quyền lợi tích lũy xu", t.earn, "earn") +
    renderTierRow("bi-credit-card-fill", "Thanh toán", t.payment, "payment") +
    renderTierExtraRows("bi-gift-fill", "Đặc quyền khác", t.extras) +
    "</div></div></article>"
  );
}

function renderPrivileges() {
  var root = document.getElementById("privileges-root");
  if (!root) return;

  var tiers = TIER_CARDS.map(renderTierCard).join("");

  var rules = TIER_RULES.map(function (r) {
    return (
      '<div class="tier-rules-panel__block">' +
      '<h3 class="tier-rules-panel__heading">' + escapeHtml(r.title) + "</h3>" +
      '<p class="tier-rules-panel__text">' + escapeHtml(r.text) + "</p></div>"
    );
  }).join("");

  var vouchers = VOUCHERS.map(function (v) {
    var cond = v.cond
      ? '<p class="promo-voucher-card__cond">' + escapeHtml(v.cond) + "</p>"
      : (v.subtitle ? '<p class="promo-voucher-card__cond">' + escapeHtml(v.subtitle) + "</p>" : "");
    return (
      '<div class="promo-voucher-col" data-voucher-tier="' + v.tier + '">' +
      '<article class="promo-voucher-card">' +
      '<div class="promo-voucher-card__head">' +
      '<span class="promo-voucher-card__brand">Rovva</span>' +
      '<h4 class="promo-voucher-card__discount">' + v.discount + "</h4>" +
      cond +
      "</div>" +
      '<div class="promo-voucher-card__foot">' +
      '<span class="promo-voucher-card__expiry">Hạn dùng: ' + escapeHtml(v.expiry) + "</span>" +
      '<button type="button" class="promo-voucher-card__claim">Nhận mã</button>' +
      "</div></article></div>"
    );
  }).join("");

  root.innerHTML =
    '<section class="tier-section mb-5">' +
    '<h2 class="promo-section-title text-center mb-4">Hệ thống cấp bậc thành viên</h2>' +
    '<div class="tier-carousel-wrap">' +
    '<button type="button" class="tier-carousel__nav tier-carousel__nav--prev" aria-label="Trước" hidden><i class="bi bi-chevron-left" aria-hidden="true"></i></button>' +
    '<div class="tier-carousel"><div class="tier-carousel__viewport">' +
    '<div class="tier-carousel__track">' + tiers + "</div></div></div>" +
    '<button type="button" class="tier-carousel__nav tier-carousel__nav--next" aria-label="Sau"><i class="bi bi-chevron-right" aria-hidden="true"></i></button>' +
    "</div></section>" +
    '<section class="mb-5">' +
    '<div class="tier-rules-panel">' +
    '<h2 class="tier-rules-panel__title">Quy tắc cấp bậc thành viên</h2>' +
    rules +
    "</div></section>" +
    '<section class="promo-voucher-section mb-4">' +
    '<h2 class="promo-section-title text-center mb-4">Kho voucher đặc quyền</h2>' +
    '<div class="promo-filter-wrap">' +
    '<div class="promo-filter promo-filter--pill" id="promo-voucher-filter">' +
    '<button type="button" class="promo-filter__chip is-active" data-tier="all">Tất cả</button>' +
    '<button type="button" class="promo-filter__chip" data-tier="silver">Hạng Bạc</button>' +
    '<button type="button" class="promo-filter__chip" data-tier="gold">Hạng Vàng</button>' +
    '<button type="button" class="promo-filter__chip" data-tier="platinum">Hạng Bạch Kim</button>' +
    '<button type="button" class="promo-filter__chip" data-tier="diamond">Hạng Kim Cương</button>' +
    "</div></div>" +
    '<div class="promo-voucher-grid" id="promo-voucher-grid">' + vouchers + "</div></section>";

  setupTierCarousel(root.querySelector(".tier-carousel-wrap"));

  var filter = document.getElementById("promo-voucher-filter");
  if (filter) {
    filter.addEventListener("click", function (e) {
      var chip = e.target.closest("[data-tier]");
      if (!chip) return;
      filter.querySelectorAll(".promo-filter__chip").forEach(function (c) {
        c.classList.toggle("is-active", c === chip);
      });
      var tier = chip.getAttribute("data-tier");
      document.querySelectorAll("[data-voucher-tier]").forEach(function (col) {
        var show = tier === "all" || col.getAttribute("data-voucher-tier") === tier;
        col.style.display = show ? "" : "none";
      });
    });
  }

  root.querySelectorAll(".promo-voucher-card__claim").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.textContent = "Đã nhận";
      btn.disabled = true;
    });
  });
}

/* ── Booking / cancel guides ───────────────────────────────────────── */

var GUIDE_BOOKING = [
  {
    badge: "BƯỚC 1",
    icon: "bi-search",
    title: "Tìm kiếm chỗ nghỉ",
    points: [
      "Tại trang chủ, nhập Địa điểm muốn đến (tên thành phố, khu vực hoặc tên cơ sở lưu trú).",
      "Chọn ngày nhận/trả phòng và số lượng khách (Người lớn, Trẻ em).",
      "Nhấn nút [Tìm kiếm].",
    ],
  },
  {
    badge: "BƯỚC 2",
    icon: "bi-building",
    title: "Lựa chọn cơ sở lưu trú",
    points: [
      "Sử dụng bộ lọc (mức giá, tiện ích, vị trí...) để tìm nhanh chỗ nghỉ ưng ý.",
      "Nhấp vào nơi lưu trú để xem chi tiết hình ảnh, tiện nghi, và đọc đánh giá.",
      "Nhấn chọn [Đặt phòng ngay] để tiến hành các thao tác đặt phòng.",
    ],
  },
  {
    badge: "BƯỚC 3",
    icon: "bi-card-text",
    title: "Điền thông tin",
    points: [
      "Điền chính xác thông tin Khách hàng (Họ tên, Email, Số điện thoại) để nhận mã xác nhận.",
      "Có thể chọn thêm các Dịch vụ mà nơi lưu trú cung cấp (Đưa đón sân bay, Spa,...) hoặc điền Ghi chú yêu cầu nếu cần.",
      "Đừng quên áp dụng Mã giảm giá hoặc Đổi xu để tối ưu chi phí.",
    ],
  },
  {
    badge: "BƯỚC 4",
    icon: "bi-check-circle",
    title: "Thanh toán & Nhận xác nhận",
    points: [
      "Kiểm tra lại toàn bộ Chi tiết giá và chọn Phương thức thanh toán. Nhấn [Xác nhận & Thanh toán].",
      "Nếu thanh toán trực tuyến: Tiến hành thanh toán theo hướng dẫn, sau đó nhấn nút [Tôi đã chuyển khoản]. Sau đó vui lòng chờ hệ thống xác nhận giao dịch trong khoảng 1-3 phút.",
      "Nếu chọn thanh toán khi nhận phòng: Hệ thống sẽ tự động chuyển thẳng đến bước hoàn tất.",
      'Khi màn hình hiển thị "Đặt phòng thành công!", Rovva sẽ gửi Mã đơn đặt và biên lai chi tiết qua Email của bạn.',
    ],
  },
];

var GUIDE_CANCEL = [
  {
    badge: "BƯỚC 1",
    icon: "bi-person",
    title: "Truy cập Chuyến đi của tôi",
    points: [
      "Đăng nhập vào tài khoản của bạn. Sau đó, nhấp chọn mục Chuyến đi của tôi tại menu Tài khoản.",
    ],
  },
  {
    badge: "BƯỚC 2",
    icon: "bi-journal-text",
    title: "Chọn đơn đặt phòng cần hủy",
    points: [
      "Tại màn hình Chuyến đi của tôi (tab Sắp tới), tìm đơn đặt phòng bạn muốn hủy. Nhấn trực tiếp vào nút [Hủy đặt phòng] trên thẻ thông tin.",
    ],
  },
  {
    badge: "BƯỚC 3",
    icon: "bi-shield-exclamation",
    title: "Kiểm tra chính sách & Xác nhận",
    points: [
      "Màn hình Hủy đặt phòng sẽ hiện ra. Vui lòng đọc kỹ Chính sách hoàn tiền, sau đó chọn lý do hủy đặt phòng và nhấn nút [Xác nhận hủy].",
    ],
  },
  {
    badge: "BƯỚC 4",
    icon: "bi-envelope-check",
    title: "Nhận thông báo hoàn tất",
    points: [
      "Đơn hàng sẽ tự động được chuyển sang tab Đã hủy. Hệ thống Rovva sẽ gửi Email xác nhận chi tiết đến bạn.",
    ],
  },
];

function renderGuideSteps(steps) {
  return (
    '<ol class="guide-steps">' +
    steps.map(function (s) {
      var pts = s.points.map(function (p) { return "<li>" + escapeHtml(p) + "</li>"; }).join("");
      return (
        '<li class="guide-step">' +
        '<div class="guide-step__badge"><i class="bi ' + s.icon + ' d-block mb-1"></i>' + escapeHtml(s.badge) + "</div>" +
        '<div class="guide-step__body">' +
        '<h3 class="guide-step__title">' + escapeHtml(s.title) + "</h3>" +
        '<ul class="guide-step__points">' + pts + "</ul></div></li>"
      );
    }).join("") +
    "</ol>"
  );
}

function initGuide() {
  var root = document.getElementById("guide-root");
  if (!root) return;

  var defaultTab = document.body.getAttribute("data-guide-tab") || "booking";
  var isBooking = defaultTab === "booking";
  var bookingUrl = root.getAttribute("data-booking-url") || "#";
  var cancelUrl = root.getAttribute("data-cancel-url") || "#";

  root.innerHTML =
    '<nav class="guide-tabs mb-4" role="tablist">' +
    '<a class="guide-tab' + (isBooking ? " is-active" : "") + '" href="' + escapeHtml(bookingUrl) + '">Hướng dẫn Đặt phòng</a>' +
    '<a class="guide-tab' + (!isBooking ? " is-active" : "") + '" href="' + escapeHtml(cancelUrl) + '">Hướng dẫn Hủy đặt phòng</a>' +
    "</nav>" +
    '<div class="page-card">' +
    '<h2 class="guide-heading">' + (isBooking ? "Các bước Đặt phòng:" : "Các bước Hủy đặt phòng:") + "</h2>" +
    renderGuideSteps(isBooking ? GUIDE_BOOKING : GUIDE_CANCEL) +
    "</div>";
}

/* ── Policy pages ──────────────────────────────────────────────────── */

var POLICIES = {
  privacy: {
    title: "CHÍNH SÁCH BẢO MẬT",
    tocTitle: "Mục lục chính sách",
    updated: "01 tháng 6, 2026",
    intro: "Chào mừng quý khách đến với Rovva Smart Stay Platform. Việc bảo vệ dữ liệu cá nhân và quyền riêng tư của bạn là ưu tiên hàng đầu của chúng tôi. Vui lòng đọc kỹ chính sách dưới đây để hiểu rõ cách chúng tôi thu thập, sử dụng và bảo vệ thông tin của bạn.",
    sections: [
      {
        id: "scope",
        title: "1. Đối tượng và phạm vi áp dụng",
        html:
          '<p class="policy-subheading">1.1 Đối tượng áp dụng</p>' +
          '<p class="policy-text">Chính sách này áp dụng cho mọi Khách hàng trải nghiệm và sử dụng dịch vụ trên nền tảng Rovva, bao gồm:</p>' +
          '<ul class="policy-list"><li><strong>Thành viên:</strong> Cá nhân đã đăng nhập tài khoản trên hệ thống.</li>' +
          "<li><strong>Khách vãng lai:</strong> Cá nhân truy cập, tìm kiếm thông tin hoặc tương tác với nền tảng nhưng chưa đăng ký hoặc chưa đăng nhập.</li></ul>" +
          '<p class="policy-subheading">1.2 Phạm vi áp dụng</p>' +
          '<p class="policy-text">Chính sách này áp dụng cho các hoạt động thu thập, lưu trữ, xử lý và bảo vệ dữ liệu cá nhân phát sinh khi Khách hàng (bao gồm cả Thành viên và Khách vãng lai) tương tác trên hệ sinh thái Rovva, cụ thể:</p>' +
          "<ul class=\"policy-list\"><li>Truy cập, duyệt thông tin trên website và ứng dụng di động Rovva.</li>" +
          "<li>Tìm kiếm, xem thông tin và thực hiện đặt phòng trực tuyến.</li>" +
          "<li>Thực hiện các luồng giao dịch thanh toán và đặt phòng trực tuyến.</li></ul>",
      },
      {
        id: "data",
        title: "2. Các loại dữ liệu thu thập",
        html:
          '<ul class="policy-list">' +
          "<li><strong>Dữ liệu định danh:</strong> Họ tên, số điện thoại, địa chỉ email (được thu thập khi bạn đăng ký tài khoản hoặc khi điền thông tin đặt phòng dành cho Khách vãng lai).</li>" +
          "<li><strong>Dữ liệu giao dịch:</strong> Thông tin đặt phòng, ngày nhận/trả phòng và lịch sử thanh toán (Rovva không lưu trữ dữ liệu thẻ tín dụng nhạy cảm của bạn).</li>" +
          "<li><strong>Dữ liệu tương tác AI:</strong> Nội dung các cuộc hội thoại, lịch trình dự kiến và sở thích cá nhân mà Thành viên cung cấp khi trò chuyện với Trợ lý Rovva AI. Đối với Khách vãng lai, dữ liệu hội thoại AI không được lưu trữ.</li></ul>",
      },
      {
        id: "purpose",
        title: "3. Mục đích sử dụng dữ liệu",
        html:
          '<p class="policy-text">Rovva chỉ sử dụng dữ liệu của Khách hàng cho các mục đích thiết thực sau:</p>' +
          '<ul class="policy-list">' +
          "<li><strong>Xử lý dịch vụ:</strong> Gửi email xác nhận đặt phòng, cập nhật trạng thái chuyến đi và hỗ trợ các yêu cầu trong quá trình lưu trú.</li>" +
          "<li><strong>Cá nhân hóa trải nghiệm:</strong> Gợi ý các điểm đến, resort hoặc homestay phù hợp với thói quen và ngân sách của bạn.</li>" +
          "<li><strong>Huấn luyện Trợ lý AI:</strong> Sử dụng các dữ liệu hội thoại (đã được ẩn danh hoàn toàn) để cải thiện khả năng thấu hiểu, giúp Rovva AI tư vấn lịch trình ngày càng chính xác hơn.</li></ul>",
      },
      {
        id: "sharing",
        title: "4. Chia sẻ dữ liệu với bên thứ ba",
        html:
          '<p class="policy-text">Dữ liệu chỉ được chia sẻ trong các trường hợp phục vụ trực tiếp cho chuyến đi của bạn:</p>' +
          '<ul class="policy-list">' +
          "<li><strong>Với Nhà cung cấp (Host):</strong> Rovva chỉ cung cấp Họ tên, Số điện thoại và yêu cầu đặc biệt của Khách hàng để Host có thể chuẩn bị phòng và liên hệ đón tiếp.</li>" +
          "<li><strong>Với Cổng thanh toán:</strong> Truyền tải thông tin mã đơn hàng đến các đối tác thanh toán hợp tác để hoàn tất giao dịch an toàn.</li></ul>",
      },
      {
        id: "security",
        title: "5. Lưu trữ và Bảo mật dữ liệu",
        html:
          '<p class="policy-subheading">Biện pháp bảo mật</p>' +
          '<p class="policy-text">Toàn bộ dữ liệu truyền tải trên nền tảng đều được mã hóa bằng công nghệ tiên tiến. Chúng tôi áp dụng các hệ thống tường lửa để chống lại các rủi ro an ninh mạng.</p>' +
          '<p class="policy-subheading">Thời gian lưu trữ</p>' +
          '<p class="policy-text">Đối với Thành viên, dữ liệu được lưu trữ trong suốt thời gian tài khoản hoạt động. Đối với Khách vãng lai có phát sinh giao dịch, thông tin đơn hàng được lưu trữ để phục vụ đối soát và hỗ trợ sau chuyến đi.</p>',
      },
      {
        id: "rights",
        title: "6. Quyền lợi và Quyền kiểm soát",
        html:
          '<p class="policy-text">Với tư cách là Khách hàng, bạn có toàn quyền thao tác với thông tin của mình:</p>' +
          '<ul class="policy-list">' +
          "<li><strong>Quyền truy cập &amp; chỉnh sửa:</strong> Thành viên có thể cập nhật thông tin trong phần Tài khoản. Khách vãng lai có thể liên hệ bộ phận hỗ trợ để được trợ giúp cập nhật thông tin cá nhân.</li>" +
          "<li><strong>Quyền xóa bỏ:</strong> Khách hàng là Thành viên có quyền yêu cầu Rovva xóa vĩnh viễn tài khoản hoặc thông tin lưu trữ cá nhân (bao gồm cả lịch sử chat với AI) khỏi hệ thống.</li></ul>",
      },
      {
        id: "cookies",
        title: "7. Chính sách Cookie",
        html:
          '<p class="policy-text">Rovva sử dụng cookie để ghi nhớ trạng thái đăng nhập, lưu trữ tùy chọn ngôn ngữ và theo dõi luồng truy cập nhằm tối ưu hóa giao diện. Bạn có thể chủ động tắt cookie trong phần Cài đặt của trình duyệt.</p>',
      },
      {
        id: "contact",
        title: "8. Thông tin liên hệ",
        html:
          '<p class="policy-subheading">8.1 Kênh hỗ trợ</p>' +
          '<p class="policy-text">Nếu Khách hàng có bất kỳ thắc mắc nào liên quan đến việc bảo mật dữ liệu, vui lòng liên hệ với bộ phận hỗ trợ, qua:</p>' +
          '<ul class="policy-list">' +
          "<li><strong>Email hỗ trợ:</strong> support@rovva.com</li>" +
          "<li><strong>Hotline:</strong> 1900 2005</li>" +
          "<li><strong>Biểu mẫu trực tuyến:</strong> Truy cập mục Hỗ trợ và chọn Trợ giúp &amp; Yêu cầu trên website hoặc ứng dụng Rovva.</li></ul>" +
          '<p class="policy-subheading">8.2 Thời gian xử lý</p>' +
          '<p class="policy-text">Rovva sẽ phản hồi trong vòng 03 ngày làm việc kể từ ngày tiếp nhận.</p>',
      },
    ],
  },
  operation: {
    title: "CHÍNH SÁCH HOẠT ĐỘNG",
    tocTitle: "Mục lục chính sách",
    updated: "01 tháng 6, 2026",
    intro: "Chào mừng quý khách đến với Rovva Smart Stay Platform. Vui lòng đọc kỹ các chính sách hoạt động của chúng tôi để có trải nghiệm lưu trú tuyệt vời nhất.",
    sections: [
      {
        id: "scope",
        title: "1. Đối tượng và Phạm vi áp dụng",
        html:
          '<p class="policy-subheading">1.1 Đối tượng áp dụng</p>' +
          '<p class="policy-text">Chính sách này áp dụng cho mọi Khách hàng trải nghiệm và sử dụng dịch vụ trên nền tảng Rovva, bao gồm:</p>' +
          '<ul class="policy-list"><li><strong>Thành viên:</strong> Cá nhân đã đăng nhập tài khoản trên hệ thống.</li>' +
          "<li><strong>Khách vãng lai:</strong> Cá nhân truy cập, tìm kiếm thông tin hoặc tương tác với nền tảng nhưng chưa đăng ký hoặc chưa đăng nhập.</li></ul>" +
          '<p class="policy-subheading">1.2 Phạm vi áp dụng</p>' +
          '<p class="policy-text">Chính sách này áp dụng cho các hoạt động của Khách hàng trên nền tảng Rovva, bao gồm:</p>' +
          "<ul class=\"policy-list\"><li>Đăng ký, xác thực và quản lý tài khoản cá nhân.</li>" +
          "<li>Tìm kiếm, xem thông tin và thực hiện đặt phòng trực tuyến.</li>" +
          "<li>Thanh toán, hủy đặt phòng và yêu cầu hoàn tiền.</li>" +
          "<li>Thực hiện nhận phòng, trả phòng và lưu trú tại cơ sở lưu trú.</li>" +
          "<li>Đánh giá chất lượng dịch vụ sau lưu trú.</li>" +
          "<li>Gửi khiếu nại và yêu cầu hỗ trợ.</li></ul>",
      },
      {
        id: "definitions",
        title: "2. Định nghĩa",
        html:
          '<dl class="policy-defs">' +
          "<dt>Nền tảng</dt><dd>Rovva Smart Stay Platform, bao gồm website và ứng dụng di động, là nơi kết nối Khách hàng với các Nhà cung cấp dịch vụ lưu trú.</dd>" +
          "<dt>Khách hàng</dt><dd>Bao gồm Thành viên (cá nhân đã đăng nhập tài khoản) và Khách vãng lai (cá nhân đặt phòng trực tiếp thông qua email mà không cần tài khoản).</dd>" +
          "<dt>Nhà cung cấp</dt><dd>Cá nhân hoặc tổ chức đăng ký và được Rovva phê duyệt để đăng tải, quản lý và cho thuê cơ sở lưu trú trên nền tảng.</dd>" +
          "<dt>Cơ sở lưu trú</dt><dd>Địa điểm vật lý do Nhà cung cấp đăng ký trên nền tảng, bao gồm phòng, căn hộ, homestay hoặc khách sạn được cho thuê thông qua Rovva.</dd>" +
          "<dt>Đặt phòng</dt><dd>Giao dịch đặt chỗ lưu trú được thực hiện bởi Khách hàng thông qua nền tảng Rovva, bao gồm thông tin người đặt phòng, thông tin phòng, thời gian lưu trú.</dd>" +
          "<dt>Chính sách hủy</dt><dd>Quy định của Nhà cung cấp về điều kiện hủy đặt phòng và mức hoàn tiền tương ứng, được hiển thị công khai trên trang chi tiết phòng trước khi Khách hàng xác nhận đặt.</dd></dl>",
      },
      {
        id: "booking",
        title: "3. Đặt phòng",
        html:
          '<p class="policy-subheading">3.1 Điều kiện đặt phòng</p>' +
          '<p class="policy-text">Khách hàng có tài khoản có thể thực hiện đặt phòng thông qua tài khoản cá nhân. Khách hàng vãng lai có thể thực hiện đặt phòng bằng cách cung cấp thông tin liên hệ (Email, SĐT) trực tiếp trên nền tảng.</p>' +
          '<p class="policy-subheading">3.2 Xác nhận đặt phòng</p>' +
          '<p class="policy-text">Đặt phòng được xác nhận theo cơ chế và điều kiện thanh toán do từng Nhà cung cấp quy định. Thông tin xác nhận đặt phòng sẽ được gửi qua email và được lưu trữ trong mục “Chuyến đi của tôi” ở tài khoản Thành viên. Đối với Khách vãng lai, xác nhận đặt phòng được gửi qua email.</p>',
      },
      {
        id: "payment",
        title: "4. Thanh toán",
        html:
          '<p class="policy-subheading">4.1 Phương thức thanh toán</p>' +
          '<p class="policy-text">Tùy theo chính sách của từng Nhà cung cấp, Khách hàng có thể lựa chọn:</p>' +
          "<ul class=\"policy-list\"><li>Thanh toán trực tuyến.</li><li>Thanh toán khi nhận phòng.</li></ul>" +
          '<p class="policy-subheading">4.2 Bảo mật thanh toán</p>' +
          '<p class="policy-text">Rovva không lưu trữ thông tin thẻ hoặc dữ liệu thanh toán nhạy cảm của Khách hàng.</p>' +
          '<p class="policy-subheading">4.3 Hóa đơn và chứng từ</p>' +
          '<p class="policy-text">Thông tin giao dịch được lưu trên hệ thống và hiển thị trong mục “Chuyến đi của tôi” ở tài khoản Thành viên. Đối với Khách vãng lai, thông tin giao dịch, hóa đơn và các chứng từ liên quan sẽ được gửi trực tiếp đến địa chỉ email đã đăng ký khi đặt phòng.</p>',
      },
      {
        id: "cancel",
        title: "5. Hủy đặt phòng và Hoàn tiền",
        html:
          '<p class="policy-subheading">5.1 Chính sách hủy</p>' +
          '<p class="policy-text">Mỗi Nhà cung cấp được quyền thiết lập chính sách hủy riêng. Chính sách hủy được hiển thị trên trang chi tiết phòng trước khi Khách hàng đặt phòng.</p>' +
          '<p class="policy-subheading">5.2 Hủy đặt phòng</p>' +
          '<p class="policy-text">Khách hàng là Thành viên có thể thực hiện hủy đặt phòng thông qua mục “Chuyến đi của tôi” ở tài khoản cá nhân. Đối với Khách vãng lai, có thể thực hiện hủy đặt phòng thông qua đường dẫn được gửi kèm trong email xác nhận đặt phòng.</p>' +
          '<p class="policy-subheading">5.3 Hoàn tiền</p>' +
          '<p class="policy-text">Tiền hoàn được xử lý trong vòng 5-10 ngày làm việc kể từ ngày hủy hợp lệ, thông qua phương thức thanh toán gốc. Khách hàng sẽ nhận thông báo qua email khi tiền hoàn được xử lý thành công.</p>' +
          '<p class="policy-subheading">5.4 Trường hợp Nhà cung cấp hủy đặt phòng</p>' +
          '<p class="policy-text">Nếu Nhà cung cấp chủ động hủy booking đã xác nhận, Khách hàng được hoàn 100% số tiền đã thanh toán, không phụ thuộc vào chính sách hủy đã công bố.</p>' +
          '<p class="policy-subheading">5.5 Trường hợp Khách hàng không nhận phòng</p>' +
          '<p class="policy-text">Nếu Khách hàng không đến nhận phòng đúng thời gian quy định mà không thông báo trước, đặt phòng được xem là không nhận phòng. Việc hoàn tiền được áp dụng theo chính sách của Nhà cung cấp.</p>',
      },
      {
        id: "checkin",
        title: "6. Nhận phòng và Trả phòng",
        html:
          '<p class="policy-subheading">6.1 Thời gian nhận và trả phòng</p>' +
          '<p class="policy-text">Thời gian nhận phòng và trả phòng được quy định bởi từng Nhà cung cấp và hiển thị trên trang chi tiết cơ sở lưu trú.</p>' +
          '<p class="policy-subheading">6.2 Thông tin người lưu trú</p>' +
          '<p class="policy-text">Khách hàng có trách nhiệm cung cấp thông tin người lưu trú chính xác theo yêu cầu của Nhà cung cấp và pháp luật hiện hành. Rovva không chịu trách nhiệm về các sự cố phát sinh do thông tin không trung thực.</p>' +
          '<p class="policy-subheading">6.3 Số lượng khách</p>' +
          '<p class="policy-text">Số lượng khách thực tế lưu trú không được vượt quá số lượng tối đa được ghi nhận trong booking. Nhà cung cấp có quyền từ chối nhận phòng nếu số lượng khách vượt mức cho phép.</p>',
      },
      {
        id: "reviews",
        title: "7. Đánh giá",
        html:
          '<p class="policy-subheading">7.1 Điều kiện đánh giá</p>' +
          '<p class="policy-text">Chỉ Khách hàng là Thành viên và đã hoàn tất lưu trú mới được phép đánh giá cơ sở lưu trú.</p>' +
          '<p class="policy-subheading">7.2 Nội dung đánh giá</p>' +
          '<p class="policy-text">Đánh giá phải trung thực và phản ánh trải nghiệm thực tế tại cơ sở lưu trú.</p>' +
          '<p class="policy-subheading">7.3 Xử lý vi phạm</p>' +
          '<p class="policy-text">Rovva có quyền ẩn hoặc xóa các đánh giá vi phạm tiêu chuẩn cộng đồng.</p>',
      },
      {
        id: "support",
        title: "8. Hỗ trợ và Khiếu nại",
        html:
          '<p class="policy-subheading">8.1 Kênh hỗ trợ</p>' +
          '<p class="policy-text">Khách hàng có thể nhận hỗ trợ thông qua các kênh: AI Chatbot, email hỗ trợ chính thức, hotline hoặc biểu mẫu liên hệ trên nền tảng.</p>' +
          '<ul class="policy-list">' +
          "<li><strong>Email hỗ trợ:</strong> support@rovva.com</li>" +
          "<li><strong>Hotline:</strong> 1900 2005</li>" +
          "<li><strong>Biểu mẫu trực tuyến:</strong> Truy cập mục Hỗ trợ và chọn Trợ giúp &amp; Yêu cầu trên website hoặc ứng dụng Rovva.</li></ul>" +
          '<p class="policy-subheading">8.2 Khiếu nại</p>' +
          '<p class="policy-text">Khách hàng có thể thực hiện gửi yêu cầu khiếu nại chính thức qua các kênh hỗ trợ.</p>' +
          '<p class="policy-text">Khiếu nại liên quan đến đặt phòng, giao dịch thanh toán hoặc chất lượng dịch vụ thực tế tại cơ sở lưu trú cần được gửi đến Rovva trong vòng 07 ngày kể từ ngày trả phòng (hoặc ngày dự kiến trả phòng đối với trường hợp không nhận phòng).</p>' +
          '<p class="policy-text">AI Chatbot hỗ trợ giải đáp thắc mắc mang tính tham khảo và không có thẩm quyền xác nhận, thay đổi hoặc hủy đặt phòng. Với các vấn đề phức tạp hoặc khiếu nại chính thức, Khách hàng cần liên hệ bộ phận hỗ trợ trực tiếp.</p>' +
          '<p class="policy-subheading">8.3 Thời gian xử lý</p>' +
          '<p class="policy-text">Rovva sẽ phản hồi khiếu nại hợp lệ trong vòng 03 ngày làm việc kể từ ngày tiếp nhận.</p>',
      },
    ],
  },
  terms: {
    title: "Điều khoản & Điều kiện",
    tocTitle: "Mục lục",
    updated: "01 tháng 6, 2026",
    intro: "Chào mừng quý khách đến với Rovva Smart Stay Platform. Vui lòng đọc kỹ các điều khoản dưới đây trước khi bắt đầu hành trình của bạn.",
    sections: [
      {
        id: "intro",
        title: "1. Giới thiệu",
        html:
          '<p class="policy-text">Chào mừng bạn đến với Rovva Smart Stay Platform - gọi tắt là "Rovva", được sở hữu và vận hành bởi Công ty TNHH Rovva Việt Nam. Bằng việc truy cập, tạo tài khoản hoặc thực hiện giao dịch đặt phòng trên nền tảng, bạn xác nhận đã đọc, hiểu và đồng ý tuân thủ toàn bộ nội dung của Điều khoản &amp; Điều kiện này, cũng như Chính sách hoạt động và Chính sách bảo mật của chúng tôi.</p>' +
          '<p class="policy-text">Rovva là nền tảng công nghệ đóng vai trò trung gian kết nối Khách hàng với các Nhà cung cấp dịch vụ lưu trú. Rovva không trực tiếp sở hữu, quản lý hay cung cấp dịch vụ lưu trú và không chịu trách nhiệm pháp lý về chất lượng thực tế cũng như sự an toàn tại cơ sở lưu trú.</p>',
      },
      {
        id: "scope",
        title: "2. Đối tượng và Phạm vi áp dụng",
        html:
          '<p class="policy-subheading">2.1 Đối tượng áp dụng</p>' +
          '<p class="policy-text">Điều khoản này áp dụng cho mọi Khách hàng trải nghiệm và sử dụng dịch vụ trên nền tảng Rovva, bao gồm:</p>' +
          '<ul class="policy-list"><li><strong>Thành viên:</strong> Cá nhân đã đăng nhập tài khoản trên hệ thống.</li>' +
          "<li><strong>Khách vãng lai:</strong> Cá nhân truy cập, tìm kiếm thông tin hoặc tương tác với nền tảng nhưng chưa đăng ký hoặc chưa đăng nhập.</li></ul>" +
          '<p class="policy-subheading">2.2 Phạm vi áp dụng</p>' +
          '<p class="policy-text">Điều khoản này áp dụng cho toàn bộ hoạt động của Khách hàng trên nền tảng ROVVA, bao gồm website và ứng dụng di động.</p>',
      },
      {
        id: "definitions",
        title: "3. Định nghĩa",
        html:
          '<dl class="policy-defs">' +
          "<dt>Nền tảng</dt><dd>Rovva Smart Stay Platform, bao gồm website và ứng dụng di động, là nơi kết nối Khách hàng với các Nhà cung cấp dịch vụ lưu trú.</dd>" +
          "<dt>Khách hàng</dt><dd>Bao gồm Thành viên (cá nhân đã đăng nhập tài khoản) và Khách vãng lai (cá nhân đặt phòng trực tiếp thông qua email mà không cần tài khoản).</dd>" +
          "<dt>Nhà cung cấp</dt><dd>Cá nhân hoặc tổ chức đăng ký và được Rovva phê duyệt để đăng tải, quản lý và cho thuê cơ sở lưu trú trên nền tảng.</dd>" +
          "<dt>Cơ sở lưu trú</dt><dd>Địa điểm vật lý do Nhà cung cấp đăng ký trên nền tảng, bao gồm phòng, căn hộ, homestay hoặc khách sạn được cho thuê thông qua Rovva.</dd>" +
          "<dt>Đặt phòng</dt><dd>Giao dịch đặt chỗ lưu trú được thực hiện bởi Khách hàng thông qua nền tảng Rovva, bao gồm thông tin người đặt phòng, thông tin phòng, thời gian lưu trú.</dd>" +
          "<dt>Tài khoản</dt><dd>Hồ sơ cá nhân của Khách hàng được tạo sau khi đăng ký và xác thực email thành công trên nền tảng.</dd></dl>",
      },
      {
        id: "account",
        title: "4. Tài khoản",
        html:
          '<p class="policy-subheading">4.1 Đăng ký</p>' +
          '<p class="policy-text">Mỗi địa chỉ email chỉ được đăng ký một tài khoản duy nhất. Thông tin cung cấp khi đăng ký phải trung thực và chính xác. Tài khoản chỉ có thể đăng nhập sau khi xác thực email thành công.</p>' +
          '<p class="policy-subheading">4.2 Bảo mật tài khoản</p>' +
          '<p class="policy-text">Khách hàng chịu hoàn toàn trách nhiệm bảo mật thông tin đăng nhập. Mọi hoạt động phát sinh từ tài khoản được xem là do chủ tài khoản thực hiện. Vui lòng thông báo ngay cho Rovva nếu phát hiện tài khoản bị truy cập trái phép.</p>' +
          '<p class="policy-subheading">4.3 Chấm dứt tài khoản</p>' +
          '<p class="policy-text">Rovva có quyền tạm khóa hoặc xóa tài khoản khi phát hiện hành vi gian lận, vi phạm điều khoản hoặc gây ảnh hưởng xấu đến người dùng khác và nền tảng. Khách hàng sẽ được thông báo trước khi tài khoản bị chấm dứt, trừ trường hợp vi phạm nghiêm trọng.</p>',
      },
      {
        id: "customer-rights",
        title: "5. Quyền và nghĩa vụ của Khách hàng",
        html:
          '<p class="policy-subheading">5.1 Quyền của Khách hàng</p>' +
          "<ul class=\"policy-list\"><li>Được trải nghiệm các dịch vụ trên nền tảng. Trong đó, Thành viên sẽ được mở rộng thêm quyền quản lý chuyến đi, tích lũy xu và nhận các ưu đãi riêng biệt.</li>" +
          "<li>Được tiếp cận các thông tin về cơ sở lưu trú do Nhà cung cấp đăng tải trên nền tảng trước khi đặt phòng.</li>" +
          "<li>Được bảo vệ thông tin cá nhân theo Chính sách bảo mật dữ liệu của Rovva.</li>" +
          "<li>Được hỗ trợ giải quyết khiếu nại theo quy trình của nền tảng.</li></ul>" +
          '<p class="policy-subheading">5.2 Nghĩa vụ của Khách hàng</p>' +
          "<ul class=\"policy-list\"><li>Cung cấp thông tin đặt phòng và thông tin cá nhân trung thực, chính xác.</li>" +
          "<li>Tuân thủ nội quy và chính sách của Nhà cung cấp trong suốt thời gian lưu trú.</li>" +
          "<li>Thanh toán đầy đủ theo giá trị đặt phòng đã xác nhận.</li>" +
          "<li>Không sử dụng nền tảng vào các mục đích trái pháp luật hoặc gây hại cho người dùng khác.</li></ul>",
      },
      {
        id: "rovva-rights",
        title: "6. Quyền và nghĩa vụ của Rovva",
        html:
          '<p class="policy-subheading">6.1 Quyền của Rovva</p>' +
          "<ul class=\"policy-list\"><li>Từ chối hoặc hủy đặt phòng trong trường hợp phát hiện gian lận hoặc vi phạm điều khoản.</li>" +
          "<li>Tạm khóa hoặc chấm dứt tài khoản vi phạm chính sách nền tảng.</li>" +
          "<li>Sửa đổi, cập nhật Điều khoản này khi cần thiết.</li>" +
          "<li>Kiểm duyệt nội dung đánh giá không đạt tiêu chuẩn cộng đồng.</li></ul>" +
          '<p class="policy-subheading">6.2 Nghĩa vụ của Rovva</p>' +
          "<ul class=\"policy-list\"><li>Duy trì nền tảng hoạt động ổn định và bảo mật.</li>" +
          "<li>Kiểm duyệt thông tin cơ sở lưu trú trước khi hiển thị công khai.</li>" +
          "<li>Bảo vệ thông tin cá nhân của Khách hàng theo quy định pháp luật.</li>" +
          "<li>Hỗ trợ xử lý khiếu nại trong phạm vi trách nhiệm của nền tảng.</li>" +
          "<li>Thông báo kịp thời các thay đổi quan trọng ảnh hưởng đến Khách hàng.</li></ul>",
      },
      {
        id: "booking-payment",
        title: "7. Đặt phòng và Thanh toán",
        html:
          '<p class="policy-subheading">7.1 Xác nhận đặt phòng</p>' +
          '<p class="policy-text">Hợp đồng dịch vụ lưu trú được hình thành trực tiếp giữa Khách hàng và Nhà cung cấp tại thời điểm Rovva gửi thông báo Xác nhận đặt phòng thành công đến email của Khách hàng và hiển thị trong mục “Chuyến đi của tôi” đối với khách hàng là Thành viên. Rovva đóng vai trò trung gian cung cấp nền tảng công nghệ và hỗ trợ xử lý giao dịch, không phải là bên ký kết hợp đồng lưu trú.</p>' +
          '<p class="policy-subheading">7.2 Phương thức và thời điểm thanh toán</p>' +
          '<p class="policy-text">Khách hàng có thể lựa chọn các phương thức thanh toán được hệ thống hỗ trợ tùy thuộc vào chính sách của từng Cơ sở lưu trú:</p>' +
          "<ul class=\"policy-list\"><li><strong>Trường hợp Thanh toán trực tuyến:</strong> Giao dịch đặt phòng chỉ được xác nhận chính thức sau khi Khách hàng thanh toán thành công qua cổng thanh toán trên nền tảng Rovva.</li>" +
          "<li><strong>Trường hợp Thanh toán tại Cơ sở lưu trú khi nhận phòng:</strong> Giao dịch đặt phòng được xác nhận ngay sau khi Khách hàng hoàn tất các bước đặt chỗ trên nền tảng. Khách hàng có nghĩa vụ tự thanh toán đầy đủ giá trị đặt phòng trực tiếp cho Nhà cung cấp khi đến nhận phòng theo đúng quy định.</li></ul>" +
          '<p class="policy-subheading">7.3 Bảo mật thanh toán</p>' +
          '<p class="policy-text">Đối với các giao dịch thanh toán trực tuyến, toàn bộ thông tin thẻ và tài khoản ngân hàng của Khách hàng được xử lý, bảo mật bởi đối tác cổng thanh toán bên thứ ba. Rovva không trực tiếp thu thập hay lưu trữ các dữ liệu thanh toán nhạy cảm này của Khách hàng.</p>',
      },
      {
        id: "usage",
        title: "8. Quy định sử dụng nền tảng",
        html:
          '<p class="policy-text">Khách hàng không được thực hiện các hành vi sau trên nền tảng:</p>' +
          "<ul class=\"policy-list\"><li>Cung cấp thông tin giả mạo khi đăng ký tài khoản hoặc đặt phòng.</li>" +
          "<li>Đăng đánh giá giả mạo hoặc thao túng hệ thống đánh giá.</li>" +
          "<li>Sử dụng nền tảng vào mục đích trái pháp luật hoặc gây hại cho người dùng khác.</li>" +
          "<li>Cố tình khai thác lỗi hệ thống để trục lợi.</li>" +
          "<li>Sao chép, phân phối hoặc khai thác thương mại bất kỳ nội dung nào của nền tảng mà không có sự đồng ý bằng văn bản của Rovva.</li></ul>",
      },
      {
        id: "ip",
        title: "9. Sở hữu trí tuệ",
        html:
          '<p class="policy-subheading">9.1 Quyền sở hữu của nền tảng</p>' +
          '<p class="policy-text">Toàn bộ nội dung, thiết kế, logo, tên thương hiệu, mã nguồn và phần mềm của Rovva là tài sản trí tuệ thuộc quyền sở hữu độc quyền của Rovva Smart Stay Platform. Khách hàng không được phép sao chép, phân phối, chỉnh sửa, hoặc khai thác thương mại bất kỳ phần nào của nền tảng dưới mọi hình thức mà không có sự chấp thuận trước bằng văn bản của Rovva.</p>' +
          '<p class="policy-subheading">9.2 Quyền đối với nội dung của người dùng</p>' +
          '<p class="policy-text">Các nội dung do Khách hàng đăng tải trên nền tảng (bao gồm nhưng không giới hạn ở đánh giá, bình luận, hình ảnh thực tế) vẫn thuộc quyền sở hữu của Khách hàng. Khách hàng cam kết chịu trách nhiệm pháp lý đối với nội dung mình đăng tải và đảm bảo không vi phạm bản quyền của bất kỳ bên thứ ba nào.</p>' +
          '<p class="policy-text">Bằng việc đăng tải nội dung lên Rovva, Khách hàng đồng ý cấp cho Rovva một quyền sử dụng không độc quyền, miễn phí bản quyền, vĩnh viễn và trên phạm vi toàn cầu để hiển thị, phân phối, điều chỉnh và sử dụng các nội dung này nhằm mục đích vận hành, cải thiện dịch vụ và phục vụ cho các hoạt động tiếp thị, truyền thông của nền tảng.</p>',
      },
      {
        id: "liability",
        title: "10. Giới hạn trách nhiệm Của Rovva",
        html:
          '<p class="policy-text">ROVVA không chịu trách nhiệm về:</p>' +
          "<ul class=\"policy-list\"><li>Chất lượng dịch vụ thực tế của Nhà cung cấp tại cơ sở lưu trú.</li>" +
          "<li>Tranh chấp phát sinh trực tiếp giữa Khách hàng và Nhà cung cấp.</li>" +
          "<li>Thiệt hại do sự cố kỹ thuật ngoài tầm kiểm soát của nền tảng.</li>" +
          "<li>Mọi thông tin sai lệch, thiếu sót hoặc không chính xác về cơ sở lưu trú do Nhà cung cấp tự cập nhật trên hệ thống.</li></ul>",
      },
      {
        id: "changes",
        title: "11. Thay Đổi Điều Khoản",
        html:
          '<p class="policy-text">Rovva có quyền sửa đổi Điều khoản này bất cứ lúc nào. Thông báo thay đổi sẽ được hiển thị trên nền tảng và gửi qua email trước khi có hiệu lực. Việc tiếp tục sử dụng nền tảng sau khi thay đổi có hiệu lực được xem là Khách hàng đã chấp thuận điều khoản mới.</p>',
      },
      {
        id: "law",
        title: "12. Luật áp dụng",
        html:
          '<p class="policy-text">Điều khoản này được điều chỉnh bởi pháp luật Việt Nam. Trong trường hợp phát sinh tranh chấp, các bên ưu tiên giải quyết thông qua thương lượng. Nếu thương lượng không thành, tranh chấp sẽ được giải quyết tại tòa án có thẩm quyền tại Việt Nam.</p>',
      },
    ],
  },
};

function renderPolicy() {
  var key = document.body.getAttribute("data-policy");
  if (!key || !POLICIES[key]) return;
  var root = document.getElementById("policy-root");
  if (!root) return;

  var policy = POLICIES[key];
  var homeUrl = root.getAttribute("data-home-url") || "/";
  var tocTitle = policy.tocTitle || "Mục lục chính sách";

  var toc = policy.sections.map(function (s, i) {
    return (
      '<a class="policy-toc__link' + (i === 0 ? " is-active" : "") + '" href="#' + s.id + '" data-policy-link="' + s.id + '">' +
      escapeHtml(s.title) + "</a>"
    );
  }).join("");

  var sections = policy.sections.map(function (s) {
    return (
      '<section class="policy-section" id="' + s.id + '">' +
      '<h2 class="policy-heading">' + escapeHtml(s.title) + "</h2>" + s.html + "</section>"
    );
  }).join("");

  root.innerHTML =
    '<section class="policy-hero"><div class="container-xxl">' +
    '<h1 class="policy-hero__title">' + escapeHtml(policy.title) + "</h1>" +
    '<p class="policy-hero__intro">' + escapeHtml(policy.intro) + "</p>" +
    '<p class="policy-hero__updated">Cập nhật lần cuối: ' + escapeHtml(policy.updated) + "</p></div></section>" +
    '<div class="container-xxl"><div class="policy-layout">' +
    '<aside class="policy-toc"><h2 class="policy-toc__title">' + escapeHtml(tocTitle) + '</h2><nav class="policy-toc__nav">' + toc + "</nav></aside>" +
    '<div class="policy-content">' + sections +
    '<div class="policy-back"><a class="btn btn-rova-primary" href="' + escapeHtml(homeUrl) + '"><i class="bi bi-house"></i> Quay lại Trang chủ</a></div>' +
    "</div></div></div>";

  var links = root.querySelectorAll("[data-policy-link]");
  links.forEach(function (link) {
    link.addEventListener("click", function () {
      links.forEach(function (l) { l.classList.remove("is-active"); });
      link.classList.add("is-active");
    });
  });
}

/* ── Help form ─────────────────────────────────────────────────────── */

function initHelpForm() {
  var form = document.getElementById("help-request-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var btn = form.querySelector('[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<i class="bi bi-check-circle"></i> Đã gửi yêu cầu';
    }
    window.setTimeout(function () {
      form.reset();
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-send"></i> Gửi yêu cầu hỗ trợ';
      }
    }, 3000);
  });
}

/* ── Blog filters ──────────────────────────────────────────────────── */

function initBlogFilters() {
  var chips = document.querySelectorAll(".blog-page-filter__chip, .blog-filter__chip");
  var cards = document.querySelectorAll("#blog-grid .blog-page-card, #blog-grid .col-sm-6");
  if (!chips.length || !cards.length) return;

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      chips.forEach(function (c) { c.classList.remove("is-active"); });
      chip.classList.add("is-active");
      var label = chip.textContent.trim();
      cards.forEach(function (card) {
        if (label === "Tất cả") {
          card.style.display = "";
          return;
        }
        var category = card.getAttribute("data-category");
        if (category) {
          var match = category === label
            || category.indexOf(label) !== -1
            || label.indexOf(category) !== -1;
          card.style.display = match ? "" : "none";
          return;
        }
        var meta = card.querySelector(".blog-card__meta span, .blog-page-card__date");
        var show = meta && meta.textContent.indexOf(label) !== -1;
        card.style.display = show ? "" : "none";
      });
    });
  });
}

/* ── Blog newsletter ───────────────────────────────────────────────── */

function initBlogNewsletter() {
  var form = document.getElementById("blog-newsletter-form");
  var modalEl = document.getElementById("blogNewsletterModal");
  if (!form || !modalEl || typeof bootstrap === "undefined") return;

  var modal = bootstrap.Modal.getOrCreateInstance(modalEl);
  var emailOut = document.getElementById("blogNewsletterEmail");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var input = form.querySelector('input[type="email"]');
    if (!input || !input.value.trim()) {
      input && input.focus();
      return;
    }
    if (!input.checkValidity()) {
      input.reportValidity();
      return;
    }
    if (emailOut) {
      emailOut.textContent = input.value.trim();
    }
    modal.show();
    form.reset();
  });
}

/* ── Entry ─────────────────────────────────────────────────────────── */

export function initSupportPages() {
  renderFaq();
  renderPrivileges();
  initGuide();
  renderPolicy();
  initHelpForm();
  initBlogFilters();
  initBlogNewsletter();
}
