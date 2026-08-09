(() => {
  const node = document.getElementById("status-data");
  const canvas = document.getElementById("statusChart");
  if (!node || !canvas || !window.Chart) return;
  const data = JSON.parse(node.textContent || "{}");
  new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: Object.keys(data),
      datasets: [{ data: Object.values(data), backgroundColor: ["#0d6efd", "#20c997", "#ffc107", "#dc3545", "#6f42c1", "#6c757d"] }]
    },
    options: { plugins: { legend: { position: "bottom" } } }
  });
})();
