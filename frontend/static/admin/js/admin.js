(function () {
  const sidebar = document.getElementById('admin-sidebar');
  const overlay = document.getElementById('admin-overlay');
  const toggle = document.getElementById('admin-sidebar-toggle');

  if (sidebar && toggle && overlay) {
    const open = () => {
      sidebar.classList.add('is-open');
      overlay.classList.add('is-open');
    };
    const close = () => {
      sidebar.classList.remove('is-open');
      overlay.classList.remove('is-open');
    };
    toggle.addEventListener('click', () => {
      sidebar.classList.contains('is-open') ? close() : open();
    });
    overlay.addEventListener('click', close);
  }

  const dateEl = document.getElementById('admin-date');
  if (dateEl) {
    dateEl.textContent = new Date().toLocaleDateString('vi-VN', {
      weekday: 'short',
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    });
  }

  window.adminFilterTable = function (targetId, query) {
    const q = (query || '').toLowerCase().trim();
    const table = document.getElementById(targetId);
    if (table) {
      table.querySelectorAll('tbody tr').forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = !q || text.includes(q) ? '' : 'none';
      });
      return;
    }
    const container = document.getElementById(targetId);
    if (!container) return;
    container.querySelectorAll('.admin-dispute-card').forEach((card) => {
      const text = card.textContent.toLowerCase();
      card.style.display = !q || text.includes(q) ? '' : 'none';
    });
  };

  document.querySelectorAll('[data-admin-filter]').forEach((input) => {
    const tableId = input.getAttribute('data-admin-filter');
    const handler = () => window.adminFilterTable(tableId, input.value);
    input.addEventListener('input', handler);
    input.addEventListener('keyup', handler);
  });

  document.querySelectorAll('[data-admin-status-filter]').forEach((select) => {
    select.addEventListener('change', () => {
      const tableId = select.getAttribute('data-admin-status-filter');
      const table = document.getElementById(tableId);
      if (!table) return;
      const value = select.value;
      table.querySelectorAll('tbody tr').forEach((row) => {
        if (!value) {
          row.style.display = '';
          return;
        }
        const status = row.getAttribute('data-status') || '';
        row.style.display = status === value ? '' : 'none';
      });
    });
  });

  const chartRoot = document.getElementById('admin-dashboard-charts');
  if (chartRoot && window.Chart) {
    const payload = JSON.parse(chartRoot.textContent || '{}');
    const mixCtx = document.getElementById('adminRevenueBookingChart');
    if (mixCtx) {
      new Chart(mixCtx, {
        type: 'line',
        data: {
          labels: payload.labels || [],
          datasets: [
            {
              label: 'Doanh thu (triệu ₫)',
              type: 'bar',
              data: payload.revenue || [],
              backgroundColor: 'rgba(21, 101, 192, 0.82)',
              borderRadius: 6,
              yAxisID: 'y',
            },
            {
              label: 'Lượt đặt phòng',
              type: 'line',
              data: payload.bookings || [],
              borderColor: '#00BFA5',
              backgroundColor: '#00BFA5',
              borderWidth: 3,
              tension: 0.35,
              yAxisID: 'y1',
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: { legend: { position: 'top' } },
          scales: {
            y: { type: 'linear', display: true, position: 'left' },
            y1: {
              type: 'linear',
              display: true,
              position: 'right',
              grid: { drawOnChartArea: false },
            },
          },
        },
      });
    }

    const statusCtx = document.getElementById('adminBookingStatusChart');
    if (statusCtx) {
      new Chart(statusCtx, {
        type: 'doughnut',
        data: {
          labels: ['Hoàn thành', 'Đang xử lý', 'Đã hủy'],
          datasets: [
            {
              data: payload.status || [0, 0, 0],
              backgroundColor: ['#10B981', '#F59E0B', '#EF4444'],
              borderWidth: 0,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '68%',
          plugins: { legend: { position: 'bottom' } },
        },
      });
    }

    const topCtx = document.getElementById('adminTopHotelsChart');
    if (topCtx && payload.top_hotels) {
      new Chart(topCtx, {
        type: 'bar',
        data: {
          labels: payload.top_hotels.map((h) => h.name),
          datasets: [
            {
              label: 'Doanh thu (triệu ₫)',
              data: payload.top_hotels.map((h) => h.revenue),
              backgroundColor: 'rgba(21, 101, 192, 0.85)',
              borderRadius: 6,
            },
          ],
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
        },
      });
    }
  }
})();
