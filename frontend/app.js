const API_BASE = 'http://127.0.0.1:5000/api';

// ---------------- Theme toggle: persist & apply ----------------
const THEME_KEY = 'saw_theme_pref';

function applyThemeClass(theme) {
  if (theme === 'dark') document.documentElement.classList.add('dark'), document.body.classList.add('dark');
  else document.documentElement.classList.remove('dark'), document.body.classList.remove('dark');

  // keep the checkbox in sync
  const cb = document.getElementById('themeToggle');
  if (cb) cb.checked = (theme === 'dark');

  // update small label text (optional)
  const lbl = document.querySelector('.toggle-label');
  if (lbl) lbl.textContent = (theme === 'dark' ? 'Dark' : 'Light');
}

function loadTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved) return saved;
  // auto-detect prefers-color-scheme
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  return prefersDark ? 'dark' : 'light';
}

function setTheme(theme) {
  localStorage.setItem(THEME_KEY, theme);
  applyThemeClass(theme);
  // If you want Chart.js colors to react to theme, trigger a rerender by calling render()
}

// wire toggle after DOM ready
document.addEventListener('DOMContentLoaded', () => {
  // initial theme
  const initial = loadTheme();
  applyThemeClass(initial);

  const cb = document.getElementById('themeToggle');
  if (cb) {
    cb.checked = (initial === 'dark');
    cb.addEventListener('change', (e) => {
      setTheme(e.target.checked ? 'dark' : 'light');
      // optionally re-render charts to pick up any theme changes
      if (typeof render === 'function') setTimeout(render, 120);
    });
  }
});
// ---------------------------------------------------------------

// ---------------- Existing API functions ----------------
async function fetchReports() {
  const res = await fetch(API_BASE + '/reports');
  return res.json();
}

async function fetchSummary() {
  const res = await fetch(API_BASE + '/summary');
  return res.json();
}

async function render() {
  const summary = await fetchSummary();
  const reports = await fetchReports();

  // Update reports list
  const reportsDiv = document.getElementById('reports');
  reportsDiv.innerHTML = '';
  reports.forEach(r => {
    const d = document.createElement('div');
    d.className = 'report';
    d.innerHTML = `<strong>${escapeHtml(r.title || '')}</strong> — <em>${escapeHtml(r.category || 'Uncategorized')}</em><br/>
        ${escapeHtml(r.description || '')}<br/>
        <small>Lat: ${r.latitude || 'N/A'}, Long: ${r.longitude || 'N/A'}</small>`;
    reportsDiv.appendChild(d);
  });

  // Draw category chart
  const ctx = document.getElementById('categoryChart').getContext('2d');
  const labels = Object.keys(summary.by_category || {});
  const data = Object.values(summary.by_category || {});

  // pick a theme-aware accent color for bars (don't hardcode too many colors)
  const isDark = document.body.classList.contains('dark');
  const barColor = isDark ? '#4FD1C5' : '#4CAF50';

  if (window.catChart) window.catChart.destroy();
  window.catChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Reports by Category',
        data,
        backgroundColor: barColor
      }]
    },
    options: { responsive: true, plugins: { legend: { display: false } } }
  });
}

// Simple HTML escape helper for safety (avoid XSS)
function escapeHtml(unsafe) {
  return String(unsafe)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Handle report form
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('reportForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get location from browser if available
    const submitPayload = async (coords) => {
      const payload = {
        title: form.title.value,
        description: form.description.value,
        latitude: coords ? coords.latitude : null,
        longitude: coords ? coords.longitude : null
      };
      await fetch(API_BASE + '/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      form.reset();
      await render();
    };

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (pos) => { await submitPayload(pos.coords); },
        async (err) => {
          alert("Couldn't get your location. Submitting without coordinates.");
          await submitPayload(null);
        },
        { timeout: 8000 }
      );
    } else {
      alert("Geolocation is not supported by your browser.");
      await submitPayload(null);
    }
  });

  // refresh button
  const refreshBtn = document.getElementById('refreshBtn');
  if (refreshBtn) refreshBtn.addEventListener('click', render);
});

// Initial load
render();
