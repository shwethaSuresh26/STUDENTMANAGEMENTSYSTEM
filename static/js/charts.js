// ===================================================================
// DASHBOARD CHARTS & ANALYTICS VISUALIZER
// ===================================================================

document.addEventListener('DOMContentLoaded', () => {
  const attendanceCanvas = document.getElementById('attendanceDoughnut');
  const feeCanvas = document.getElementById('feeProgressBar');

  // Fetch stats from API
  fetch('/api/dashboard-stats')
    .then(res => res.json())
    .then(data => {
      renderAttendanceChart(data.attendance);
      renderDeptBars(data.departments);
    })
    .catch(err => console.log('Chart data load note:', err));
});

function renderAttendanceChart(att) {
  const canvas = document.getElementById('attendanceChartCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const total = (att.present || 0) + (att.absent || 0) + (att.excused || 0);
  
  if (total === 0) {
    ctx.font = '14px Plus Jakarta Sans, sans-serif';
    ctx.fillStyle = '#94a3b8';
    ctx.textAlign = 'center';
    ctx.fillText('No attendance recorded yet', canvas.width / 2, canvas.height / 2);
    return;
  }

  const values = [att.present || 0, att.absent || 0, att.excused || 0];
  const colors = ['#10b981', '#ef4444', '#94a3b8'];
  
  let startAngle = -0.5 * Math.PI;
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = Math.min(centerX, centerY) - 15;
  const innerRadius = radius * 0.65;

  values.forEach((val, i) => {
    const sliceAngle = (val / total) * 2 * Math.PI;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
    ctx.arc(centerX, centerY, innerRadius, startAngle + sliceAngle, startAngle, true);
    ctx.closePath();
    ctx.fillStyle = colors[i];
    ctx.fill();
    startAngle += sliceAngle;
  });

  // Center text
  const pct = Math.round(((att.present || 0) / total) * 100);
  ctx.font = 'bold 22px Plus Jakarta Sans, sans-serif';
  ctx.fillStyle = '#0f172a';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(`${pct}%`, centerX, centerY - 8);

  ctx.font = '11px Plus Jakarta Sans, sans-serif';
  ctx.fillStyle = '#64748b';
  ctx.fillText('Present', centerX, centerY + 14);
}

function renderDeptBars(depts) {
  const container = document.getElementById('deptBarsContainer');
  if (!container || !depts || !depts.labels) return;

  const maxVal = Math.max(...depts.data, 1);
  let html = '';

  depts.labels.forEach((label, i) => {
    const count = depts.data[i];
    const pct = Math.round((count / maxVal) * 100);
    html += `
      <div style="margin-bottom: 0.85rem;">
        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.25rem;">
          <span>${label}</span>
          <span style="color: var(--text-muted);">${count} Students</span>
        </div>
        <div style="background-color: var(--surface-alt); height: 8px; border-radius: 9999px; overflow: hidden;">
          <div style="background: linear-gradient(90deg, #2563eb, #3b82f6); width: ${pct}%; height: 100%; border-radius: 9999px; transition: width 0.6s ease;"></div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}
