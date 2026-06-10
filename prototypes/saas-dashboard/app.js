const state = { runs: [] };

const $ = (selector) => document.querySelector(selector);

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.message || "Request failed");
  }
  return payload;
}

function setStatus(text, ok = true) {
  const status = $("#service-status");
  status.textContent = text;
  status.classList.toggle("offline", !ok);
}

function setFormStatus(text, ok = true) {
  const status = $("#form-status");
  status.textContent = text;
  status.classList.toggle("error", !ok);
}

async function refreshRuns() {
  const health = await api("/api/health");
  $("#output-root").textContent = health.output_root;
  setStatus("Online");

  const payload = await api("/api/runs");
  state.runs = payload.runs || [];
  renderMetrics();
  renderLatest();
  renderRunList();
}

function renderMetrics() {
  const totals = state.runs.reduce(
    (acc, run) => {
      acc.evidence += run.counts.evidence || 0;
      acc.claims += run.counts.claims || 0;
      acc.approvals += run.counts.approvals || 0;
      return acc;
    },
    { evidence: 0, claims: 0, approvals: 0 }
  );
  $("#metric-runs").textContent = state.runs.length;
  $("#metric-evidence").textContent = totals.evidence;
  $("#metric-claims").textContent = totals.claims;
  $("#metric-approvals").textContent = totals.approvals;
}

function renderLatest() {
  const latest = state.runs[0];
  if (!latest) {
    return;
  }
  $("#latest-title").textContent = latest.run_id;
  $("#latest-domain").textContent = latest.domain;
  $("#latest-verdict").textContent =
    latest.verdict.overall_verdict || latest.summary.verdict || "Artifacts captured for review.";
  $("#latest-evidence").textContent = latest.counts.evidence || 0;
  $("#latest-claims").textContent = latest.counts.claims || 0;
  $("#latest-events").textContent = latest.counts.events || 0;
  $("#latest-approvals").textContent = latest.counts.approvals || 0;
}

function renderRunList() {
  const list = $("#run-list");
  if (!state.runs.length) {
    list.innerHTML = '<p class="muted">No local runs found.</p>';
    return;
  }
  list.replaceChildren(
    ...state.runs.map((run) => {
      const item = document.createElement("article");
      item.className = "run-item";
      const verdict = run.verdict.overall_verdict || run.summary.verdict || "Review artifact available.";
      item.innerHTML = `
        <div>
          <strong></strong>
          <span></span>
          <p></p>
        </div>
        <dl>
          <div><dt>Evidence</dt><dd>${run.counts.evidence || 0}</dd></div>
          <div><dt>Claims</dt><dd>${run.counts.claims || 0}</dd></div>
          <div><dt>Approvals</dt><dd>${run.counts.approvals || 0}</dd></div>
        </dl>
      `;
      item.querySelector("strong").textContent = run.run_id;
      item.querySelector("span").textContent = `${run.domain} - ${run.run_dir}`;
      item.querySelector("p").textContent = verdict;
      return item;
    })
  );
}

async function createRecord(event) {
  event.preventDefault();
  setFormStatus("Generating local artifacts...");
  const payload = {
    title: $("#record-title").value,
    template: $("#record-template").value,
    notes: $("#record-notes").value,
  };
  await api("/api/records", { method: "POST", body: JSON.stringify(payload) });
  setFormStatus("Record generated.");
  await refreshRuns();
}

async function runDemo(path, label) {
  setFormStatus(`Running ${label}...`);
  await api(path, { method: "POST", body: "{}" });
  setFormStatus(`${label} completed.`);
  await refreshRuns();
}

$("#record-form").addEventListener("submit", (event) => {
  createRecord(event).catch((error) => setFormStatus(error.message, false));
});

$("#refresh-runs").addEventListener("click", () => {
  refreshRuns().catch((error) => setStatus(error.message, false));
});

$("#run-agentshield").addEventListener("click", () => {
  runDemo("/api/agentshield-demo", "buyer demo").catch((error) => setFormStatus(error.message, false));
});

$("#run-energy").addEventListener("click", () => {
  runDemo("/api/energy-demo", "energy demo").catch((error) => setFormStatus(error.message, false));
});

refreshRuns().catch((error) => setStatus(error.message, false));
