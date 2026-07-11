(function () {
  'use strict';

  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  const toggleBtn = document.getElementById('toggle-sidebar');
  const logoutBtn = document.getElementById('logout-button');
  const navItems = document.querySelectorAll('.nav-item[data-target]');
  const views = document.querySelectorAll('.view-container');
  const entities = window.ADMIN_ENTITIES || {};
  const urls = window.ADMIN_URLS || {};

  function escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function buildAdminRoleOptions(selectedRole, includeSuper) {
    const options = window.ADMIN_ROLE_OPTIONS || [];
    const canManage = window.ADMIN_CAN_MANAGE_ROLES === true;
    return options
      .filter((opt) => canManage || opt.value !== 'super')
      .filter((opt) => includeSuper || opt.value !== 'super' || canManage)
      .map((opt) => {
        const selected = opt.value === (selectedRole || 'admin') ? ' selected' : '';
        return `<option value="${escapeHtml(opt.value)}"${selected}>${escapeHtml(opt.label)}</option>`;
      })
      .join('');
  }

  function buildAdminStatusField(edit) {
    if (edit.is_self) {
      return `<div class="form-field">
          <label>Trạng thái</label>
          <input type="text" value="Hoạt động" disabled>
          <p class="form-hint">Không thể thu hồi quyền tài khoản đang đăng nhập.</p>
        </div>`;
    }
    return `<div class="form-field">
          <label>Trạng thái</label>
          <select name="status">
            <option value="active"${!edit.is_locked ? ' selected' : ''}>Hoạt động</option>
            <option value="revoked"${edit.is_locked ? ' selected' : ''}>Thu hồi quyền</option>
          </select>
        </div>`;
  }

  function buildAdminRoleField(selectedRole, disabled) {
    const role = selectedRole || 'admin';
    if (disabled) {
      const options = window.ADMIN_ROLE_OPTIONS || [];
      const current = options.find((opt) => opt.value === role);
      return `<div class="form-field">
          <label>Phân quyền</label>
          <input type="text" value="${escapeHtml(current?.label || 'Quản trị viên')}" disabled>
          <input type="hidden" name="admin_role" value="${escapeHtml(role === 'super' && !window.ADMIN_CAN_MANAGE_ROLES ? 'admin' : role)}">
          <p class="form-hint">Chỉ quản trị cấp cao mới có thể thay đổi phân quyền.</p>
        </div>`;
    }
    return `<div class="form-field">
          <label>Phân quyền</label>
          <select name="admin_role">${buildAdminRoleOptions(role, true)}</select>
        </div>`;
  }

  function showView(target) {
    if (!target) return;
    views.forEach((v) => v.classList.toggle('active', v.id === `view-${target}`));
    navItems.forEach((n) => n.classList.toggle('active', n.dataset.target === target));
    const url = new URL(window.location.href);
    url.searchParams.set('view', target);
    window.history.replaceState({ view: target }, '', url);
    closeSidebarMobile();
  }

  function closeSidebarMobile() {
    sidebar?.classList.remove('open');
    overlay?.classList.remove('active');
    overlay?.setAttribute('aria-hidden', 'true');
  }

  function openSidebarMobile() {
    sidebar?.classList.add('open');
    overlay?.classList.add('active');
    overlay?.setAttribute('aria-hidden', 'false');
  }

  navItems.forEach((btn) => {
    btn.addEventListener('click', () => showView(btn.dataset.target));
  });

  toggleBtn?.addEventListener('click', () => {
    const isMobile = window.innerWidth <= 768;
    if (isMobile) {
      if (sidebar?.classList.contains('open')) closeSidebarMobile();
      else openSidebarMobile();
      return;
    }
    document.body.classList.toggle('sidebar-collapsed');
    const collapsed = document.body.classList.contains('sidebar-collapsed');
    if (sidebar) sidebar.classList.toggle('collapsed', collapsed);
    const main = document.querySelector('.main-layout');
    if (main) main.classList.toggle('sidebar-collapsed', collapsed);
  });

  overlay?.addEventListener('click', closeSidebarMobile);

  logoutBtn?.addEventListener('click', () => {
    const url = logoutBtn.dataset.url;
    if (url) window.location.href = url;
  });

  function applyRowFilters(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    const wrapper = table.closest('.card-body') || table.closest('section');
    const searchInput = wrapper?.querySelector(`[data-search-for="${tableId}"]`);
    const filterSelects = wrapper?.querySelectorAll(`[data-filter-for="${tableId}"]`) || [];
    const q = (searchInput?.value || '').toLowerCase().trim();

    table.querySelectorAll('tbody tr[data-id]').forEach((row) => {
      const text = row.textContent.toLowerCase();
      const textMatch = !q || text.includes(q);
      let filterMatch = true;
      filterSelects.forEach((sel) => {
        const val = sel.value;
        if (!val) return;
        const attr = sel.dataset.filterAttr || 'data-filter-status';
        const rowVal = row.getAttribute(attr) || '';
        if (sel.dataset.filterMode === 'capacity') {
          const cap = parseInt(row.getAttribute('data-filter-capacity') || '0', 10);
          if (val === '1-2' && !(cap >= 1 && cap <= 2)) filterMatch = false;
          if (val === '3-4' && !(cap >= 3 && cap <= 4)) filterMatch = false;
          if (val === '5+' && cap < 5) filterMatch = false;
        } else if (sel.dataset.filterMode === 'price') {
          const price = parseInt(row.getAttribute('data-filter-price') || '0', 10);
          if (val === '2m' && price >= 2_000_000) filterMatch = false;
          if (val === '2m-5m' && (price < 2_000_000 || price > 5_000_000)) filterMatch = false;
          if (val === '5m-10m' && (price < 5_000_000 || price > 10_000_000)) filterMatch = false;
          if (val === '10m' && price <= 10_000_000) filterMatch = false;
        } else if (rowVal !== val) {
          filterMatch = false;
        }
      });
      row.style.display = textMatch && filterMatch ? '' : 'none';
    });
  }

  window.filterTable = function filterTable(tableId, query) {
    const input = document.querySelector(`[data-search-for="${tableId}"]`);
    if (input && query !== undefined) input.value = query;
    applyRowFilters(tableId);
  };

  document.querySelectorAll('[data-search-for]').forEach((input) => {
    input.addEventListener('input', () => applyRowFilters(input.dataset.searchFor));
  });

  document.querySelectorAll('[data-filter-for]').forEach((sel) => {
    sel.addEventListener('change', () => applyRowFilters(sel.dataset.filterFor));
  });

  window.closeModal = function closeModal(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove('active');
  };

  window.openModal = function openModal(id, title, bodyHtml, footerHtml) {
    const el = document.getElementById(id);
    const titleEl = id === 'form-modal' ? document.getElementById('form-modal-title') : document.getElementById('modal-title');
    const bodyEl = id === 'form-modal' ? document.getElementById('form-modal-body') : document.getElementById('modal-body');
    const footerEl = document.getElementById('modal-footer');
    if (!el) return;
    if (titleEl && title) titleEl.textContent = title;
    if (bodyEl) bodyEl.innerHTML = bodyHtml || '';
    if (footerEl) footerEl.innerHTML = footerHtml || '<button class="btn btn-secondary" onclick="closeModal(\'detail-modal\')">Đóng</button>';
    el.classList.add('active');
  };

  function renderDetailHtml(item) {
    if (!item) return '<p>Không có dữ liệu.</p>';
    let html = '<div class="detail-grid">';
    (item.fields || []).forEach(([label, value]) => {
      html += `<div class="detail-row"><span>${label}</span><span>${value ?? '—'}</span></div>`;
    });
    html += '</div>';
    return html;
  }

  window.viewDetails = function viewDetails(type, id) {
    if (type === 'admin') {
      openAdminEditModal(id);
      return;
    }
    const item = entities[type]?.[id];
    if (!item) {
      showToast('Không tìm thấy dữ liệu.', 'info');
      return;
    }
    let footer = '<button class="btn btn-secondary" onclick="closeModal(\'detail-modal\')">Đóng</button>';
    let body = renderDetailHtml(item);

    if (type === 'booking' && item.id) {
      body += '<div class="modal-actions">';
      if (['pending', 'holding'].includes(item.status)) {
        body += `<form method="post" action="${urls.bookingStatus.replace('__ID__', item.id)}"><input type="hidden" name="status" value="confirmed"><button type="submit" class="btn btn-primary">Xác nhận</button></form>`;
      }
      if (!['cancelled', 'completed'].includes(item.status)) {
        body += `<form method="post" action="${urls.bookingStatus.replace('__ID__', item.id)}"><input type="hidden" name="status" value="cancelled"><button type="submit" class="btn btn-secondary">Hủy đặt phòng</button></form>`;
      }
      if (item.status === 'confirmed') {
        body += `<form method="post" action="${urls.bookingStatus.replace('__ID__', item.id)}"><input type="hidden" name="status" value="completed"><button type="submit" class="btn btn-primary">Hoàn thành</button></form>`;
      }
      body += '</div>';
    }

    if (type === 'dispute' && item.id && item.status !== 'resolved') {
      body += `<div class="modal-actions">
        <form method="post" action="${urls.processDispute.replace('__ID__', item.id)}"><button type="submit" class="btn btn-secondary">Đang xem xét</button></form>
        <button class="btn btn-primary" onclick="openResolveDispute(${item.id})">Giải quyết</button>
      </div>`;
    }

    openModal('detail-modal', item.title || 'Chi tiết', body, footer);
  };

  window.openResolveDispute = function openResolveDispute(id) {
    closeModal('detail-modal');
    const action = urls.resolveDispute.replace('__ID__', id);
    const html = `
      <form method="post" action="${action}" class="form-grid">
        <div class="form-field">
          <label>Nội dung xử lý</label>
          <textarea name="admin_resolution" rows="4" required placeholder="Mô tả cách giải quyết tranh chấp..."></textarea>
        </div>
        <div class="form-field">
          <label>Số tiền hoàn (VNĐ)</label>
          <input type="number" name="refund_amount" value="0" min="0" step="1000">
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" onclick="closeModal('form-modal')">Hủy</button>
          <button type="submit" class="btn btn-primary">Lưu & giải quyết</button>
        </div>
      </form>`;
    openModal('form-modal', 'Giải quyết tranh chấp', html);
  };

  window.editDetails = function editDetails(type, id) {
    if (type !== 'room') return;
    const item = entities.room?.[id];
    if (!item?.edit) {
      showToast('Không tìm thấy phòng.', 'info');
      return;
    }
    const e = item.edit;
    const action = urls.updateRoom.replace('__ID__', item.id);
    const statusLabels = {
      active: 'Hoạt động',
      pending: 'Chờ duyệt',
      paused: 'Tạm ngưng',
      draft: 'Nháp',
    };
    const statusOptions = ['active', 'pending', 'paused', 'draft'].map((s) =>
      `<option value="${s}"${e.status === s ? ' selected' : ''}>${statusLabels[s] || s}</option>`
    ).join('');
    const html = `
      <form method="post" action="${action}" class="form-grid">
        <div class="form-field"><label>Tên phòng</label><input type="text" name="name" value="${e.name}" required></div>
        <div class="form-field"><label>Sức chứa</label><input type="number" name="capacity" value="${e.capacity}" min="1" required></div>
        <div class="form-field"><label>Giá/đêm (VNĐ)</label><input type="number" name="base_price" value="${e.base_price}" min="0" step="1000" required></div>
        <div class="form-field"><label>Trạng thái</label><select name="status">${statusOptions}</select></div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" onclick="closeModal('form-modal')">Hủy</button>
          <button type="submit" class="btn btn-primary">Lưu thay đổi</button>
        </div>
      </form>`;
    openModal('form-modal', 'Chỉnh sửa phòng', html);
  };

  window.openAdminEditModal = function openAdminEditModal(id) {
    const item = entities.admin?.[id];
    if (!item?.edit) {
      showToast('Không tìm thấy quản trị viên.', 'info');
      return;
    }
    const e = item.edit;
    const action = urls.updateAdmin.replace('__ID__', item.id);
    const statusField = buildAdminStatusField(e);
    const roleField = buildAdminRoleField(
      e.admin_role,
      !window.ADMIN_CAN_MANAGE_ROLES || (e.is_self && e.admin_role === 'super')
    );

    const html = `
      <form method="post" action="${action}" class="form-grid" autocomplete="off">
        <div class="form-field">
          <label>Họ tên</label>
          <input type="text" name="full_name" value="${escapeHtml(e.full_name)}" required>
        </div>
        <div class="form-field">
          <label>Email</label>
          <input type="email" name="email" value="${escapeHtml(e.email)}" autocomplete="off" required>
        </div>
        <div class="form-field">
          <label>SĐT</label>
          <input type="text" name="phone" value="${escapeHtml(e.phone)}" autocomplete="off">
        </div>
        ${roleField}
        ${statusField}
        <div class="form-field">
          <label>Mật khẩu mới</label>
          <input type="password" name="password" autocomplete="new-password" minlength="6" placeholder="Để trống nếu không đổi">
          <p class="form-hint">Chỉ nhập khi muốn đặt lại mật khẩu (tối thiểu 6 ký tự).</p>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" onclick="closeModal('form-modal')">Hủy</button>
          <button type="submit" class="btn btn-primary">Lưu thay đổi</button>
        </div>
      </form>`;
    openModal('form-modal', 'Chỉnh sửa quản trị viên', html);
  };

  window.openAddModal = function openAddModal(type) {
    if (type === 'promotion') {
      const hostOptions = (window.ADMIN_HOSTS || []).map((h) => `<option value="${h.id}">${h.name}</option>`).join('');
      const html = `
        <form method="post" action="${urls.createPromotion}" class="form-grid">
          <div class="form-field"><label>Tên khuyến mãi</label><input type="text" name="name" required></div>
          <div class="form-field"><label>Loại</label>
            <select name="type">
              <option value="Phiếu giảm giá">Phiếu giảm giá</option>
              <option value="Flash Sale">Giảm giá nhanh</option>
              <option value="Promo">Khuyến mãi</option>
            </select>
          </div>
          <div class="form-field"><label>Giảm giá (vd: 15% hoặc 100000)</label><input type="text" name="discount_value" required></div>
          <div class="form-field"><label>Từ ngày</label><input type="date" name="start_date"></div>
          <div class="form-field"><label>Đến ngày</label><input type="date" name="end_date"></div>
          <div class="form-field"><label>Chủ cơ sở lưu trú</label><select name="host_id">${hostOptions}</select></div>
          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" onclick="closeModal('form-modal')">Hủy</button>
            <button type="submit" class="btn btn-primary">Tạo khuyến mãi</button>
          </div>
        </form>`;
      openModal('form-modal', 'Tạo khuyến mãi', html);
      return;
    }
    if (type === 'admin') {
      const roleField = buildAdminRoleField('admin', !window.ADMIN_CAN_MANAGE_ROLES);
      const html = `
        <form method="post" action="${urls.createAdmin}" class="form-grid" autocomplete="off">
          <div class="form-field">
            <label>Họ tên</label>
            <input type="text" name="full_name" autocomplete="off" placeholder="Nhập họ tên" required>
          </div>
          <div class="form-field">
            <label>Email</label>
            <input type="email" name="email" autocomplete="off" placeholder="Nhập email" required>
          </div>
          <div class="form-field">
            <label>SĐT</label>
            <input type="text" name="phone" autocomplete="off" placeholder="Nhập số điện thoại (tuỳ chọn)">
          </div>
          ${roleField}
          <div class="form-field">
            <label>Mật khẩu</label>
            <input type="password" name="password" autocomplete="new-password" placeholder="Nhập mật khẩu (tối thiểu 6 ký tự)" required minlength="6">
          </div>
          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" onclick="closeModal('form-modal')">Hủy</button>
            <button type="submit" class="btn btn-primary">Tạo tài khoản</button>
          </div>
        </form>`;
      openModal('form-modal', 'Tạo quản trị viên', html);
    }
  };

  window.triggerReportExport = function triggerReportExport(name) {
    const url = urls.exportReport.replace('__TYPE__', encodeURIComponent(name));
    window.location.href = url;
    showToast(`Đang tải báo cáo: ${name}`, 'info');
  };

  window.togglePromoSwitch = function togglePromoSwitch(id, checked) {
    const form = document.getElementById(`promo-form-${id}`);
    if (form) {
      const hidden = form.querySelector('input[name="enabled"]');
      if (hidden) hidden.value = checked ? '1' : '0';
      form.submit();
    }
  };

  window.showToast = function showToast(message, type) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type || 'info'}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3200);
  };

  document.querySelectorAll('.modal-backdrop').forEach((backdrop) => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) backdrop.classList.remove('active');
    });
  });

  const initialView = document.body.dataset.activeView || 'dashboard';
  showView(initialView);

  const flashMessages = window.ADMIN_FLASH || [];
  flashMessages.forEach((msg) => showToast(msg.text, msg.category === 'error' ? 'error' : 'success'));

  const chartDb = window.ADMIN_CHART_DB;
  if (chartDb && typeof Chart !== 'undefined') {
    initDashboardCharts(chartDb);
  }
})();

function formatVnd(amount) {
  const n = Number(amount || 0);
  return n.toLocaleString('vi-VN') + ' ₫';
}

function initDashboardCharts(mockDatabase) {
  const typeSelect = document.getElementById('dashboard-filter-type');
  const monthSelect = document.getElementById('dashboard-filter-month');
  const yearSelect = document.getElementById('dashboard-filter-year');
  if (!typeSelect || !yearSelect) return;

  let currentYear = yearSelect.value;
  let currentMonth = monthSelect?.value || '1';
  let currentData = mockDatabase[currentYear]?.months?.[currentMonth] || mockDatabase[currentYear]?.yearly;

  let revenueBookingChart;
  let bookingStatusChart;
  let topHotelsChart;

  const ctxMix = document.getElementById('revenueBookingChart');
  if (ctxMix) {
    revenueBookingChart = new Chart(ctxMix.getContext('2d'), {
      type: 'line',
      data: {
        labels: currentData.chartLabels,
        datasets: [
          { label: 'Doanh thu (VNĐ)', type: 'bar', data: currentData.chartRevenue, backgroundColor: 'rgba(21, 101, 192, 0.8)', borderRadius: 4, yAxisID: 'y' },
          { label: 'Lượt đặt phòng', type: 'line', data: currentData.chartBookings, borderColor: '#00BFA5', backgroundColor: '#00BFA5', borderWidth: 3, tension: 0.4, yAxisID: 'y1' },
        ],
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: { legend: { position: 'top' } },
        scales: {
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            ticks: {
              callback: (value) => formatVnd(value),
            },
          },
          y1: { type: 'linear', display: true, position: 'right', grid: { drawOnChartArea: false } },
        },
      },
    });
  }

  const ctxStatus = document.getElementById('bookingStatusChart');
  if (ctxStatus) {
    bookingStatusChart = new Chart(ctxStatus.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: ['Hoàn thành', 'Chờ xác nhận', 'Đã hủy'],
        datasets: [{ data: currentData.status, backgroundColor: ['#10B981', '#F59E0B', '#EF4444'], borderWidth: 0, hoverOffset: 4 }],
      },
      options: {
        responsive: true, maintainAspectRatio: false, cutout: '70%',
        plugins: { legend: { position: 'bottom', labels: { padding: 20, usePointStyle: true } } },
      },
    });
  }

  const hotelNames = (currentData.topHotelsDetail || []).map((h) => h.name);
  const ctxTop = document.getElementById('topHotelsChart');
  if (ctxTop) {
    topHotelsChart = new Chart(ctxTop.getContext('2d'), {
      type: 'bar',
      data: {
        labels: hotelNames.length ? hotelNames : ['—'],
        datasets: [{ label: 'Doanh thu (VNĐ)', data: currentData.topHotels, backgroundColor: 'rgba(21, 101, 192, 0.85)', borderRadius: 4, barThickness: 24 }],
      },
      options: {
        indexAxis: 'y', responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: {
            grid: { display: true, drawBorder: false, color: '#E2E8F0' },
            ticks: {
              callback: (value) => formatVnd(value),
            },
          },
          y: { grid: { display: false, drawBorder: false } },
        },
      },
    });
  }

  function updateAllCharts() {
    const filterType = typeSelect.value;
    const yearVal = yearSelect.value;
    if (filterType === 'year') {
      if (monthSelect) monthSelect.style.display = 'none';
    } else if (monthSelect) {
      monthSelect.style.display = 'inline-block';
    }
    let newData;
    if (filterType === 'year') newData = mockDatabase[yearVal]?.yearly;
    else newData = mockDatabase[yearVal]?.months?.[monthSelect?.value];
    if (!newData) return;

    const setText = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
    setText('dash-stat-revenue', newData.kpis.revenue);
    setText('dash-stat-bookings', newData.kpis.bookings);
    setText('dash-stat-users', newData.kpis.users);
    setText('dash-stat-hosts', newData.kpis.hosts);
    setText('dash-stat-disputes', newData.kpis.disputes);
    setText('dash-stat-completion', newData.kpis.completion);
    const labelBookings = document.getElementById('dash-label-bookings');
    if (labelBookings) labelBookings.innerText = filterType === 'year' ? 'Đặt phòng trong năm' : 'Đặt phòng trong tháng';

    if (revenueBookingChart) {
      revenueBookingChart.data.labels = newData.chartLabels;
      revenueBookingChart.data.datasets[0].data = newData.chartRevenue;
      revenueBookingChart.data.datasets[1].data = newData.chartBookings;
      revenueBookingChart.update();
    }
    if (bookingStatusChart) {
      bookingStatusChart.data.datasets[0].data = newData.status;
      bookingStatusChart.update();
    }
    if (topHotelsChart) {
      const names = (newData.topHotelsDetail || []).map((h) => h.name);
      topHotelsChart.data.labels = names.length ? names : ['—'];
      topHotelsChart.data.datasets[0].data = newData.topHotels;
      topHotelsChart.update();
    }
    const hotelsListContainer = document.getElementById('dashboard-hotels-list');
    if (hotelsListContainer && newData.topHotelsDetail) {
      hotelsListContainer.innerHTML = newData.topHotelsDetail.map((hotel) => `
        <div class="list-item">
          <div class="list-item-content">
            <div class="list-item-text">${hotel.name}</div>
            <div class="list-item-subtext">${hotel.bookings} đơn đặt</div>
          </div>
          <div class="list-item-right cell-highlight">${hotel.revenue_display || formatVnd(hotel.revenue)}</div>
        </div>`).join('') || '<div class="list-item"><div class="list-item-text">Chưa có dữ liệu</div></div>';
    }
  }

  typeSelect.addEventListener('change', updateAllCharts);
  monthSelect?.addEventListener('change', updateAllCharts);
  yearSelect.addEventListener('change', updateAllCharts);
  updateAllCharts();
}
