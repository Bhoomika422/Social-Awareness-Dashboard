// static/js/app.js
const API_BASE = '/api';

function toast(msg, t = 3000) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.style.display = 'block';
  setTimeout(()=> el.style.display = 'none', t);
}

async function fetchReports() {
  const res = await fetch('/api/reports');
  return res.json();
}

// Render reports & category chart
async function render() {
  const reports = await fetchReports();
  const reportsDiv = document.getElementById('reports');
  reportsDiv.innerHTML = '';
  const counts = {};
  reports.forEach(r => {
    const d = document.createElement('div');
    d.className = 'report';
    d.innerHTML = `<strong>${escapeHtml(r.title)}</strong> — <em>${escapeHtml(r.category||'Uncategorized')}</em>
      <div>${escapeHtml(r.description)}</div>
      ${r.image_path ? `<img src="/uploads/${r.image_path}" style="max-width:120px;margin-top:8px;border-radius:6px">` : ''}
      <small>${r.date_reported ? new Date(r.date_reported).toLocaleString() : ''}</small>`;
    reportsDiv.appendChild(d);

    const cat = r.category || 'Other';
    counts[cat] = (counts[cat]||0) + 1;
  });

  // Chart
  const ctx = document.getElementById('categoryChart').getContext('2d');
  const labels = Object.keys(counts);
  const data = Object.values(counts);
  if (window.catChart) window.catChart.destroy();
  window.catChart = new Chart(ctx, {
    type: 'bar',
    data: { labels, datasets: [{ label: 'Reports', data }] },
    options: { responsive: true }
  });
}

function escapeHtml(s){ return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

// handle form submit
document.getElementById('reportForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  // try geolocation if inputs empty
  const lat = form.latitude.value;
  const lon = form.longitude.value;
  if ((!lat || !lon) && navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(async (pos) => {
      form.latitude.value = pos.coords.latitude;
      form.longitude.value = pos.coords.longitude;
      await submitForm();
    }, async () => {
      toast("Couldn't get location, submitting without coords");
      await submitForm();
    }, {timeout:8000});
  } else {
    await submitForm();
  }

  async function submitForm(){
    const fd = new FormData(form);
    const res = await fetch('/api/report', { method: 'POST', body: fd });
    if (res.ok) {
      const json = await res.json();
      toast('Submitted — pending approval');
      form.reset();
    } else {
      toast('Submission failed');
    }
    // refresh (pending -> not visible until approved)
  }
});

render();
