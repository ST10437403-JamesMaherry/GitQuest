"use strict";

const state = {
  scenarios: [],
  selectedId: null,
  selected: null,
  result: null,
};

const elements = {
  runtimeLabel: document.querySelector("#runtime-label"),
  scenarioCount: document.querySelector("#scenario-count"),
  scenarioList: document.querySelector("#scenario-list"),
  emptyState: document.querySelector("#empty-state"),
  missionContent: document.querySelector("#mission-content"),
  missionProfile: document.querySelector("#mission-profile"),
  missionDifficulty: document.querySelector("#mission-difficulty"),
  missionCategory: document.querySelector("#mission-category"),
  missionTitle: document.querySelector("#mission-title"),
  missionSummary: document.querySelector("#mission-summary"),
  scoreValue: document.querySelector("#score-value"),
  startButton: document.querySelector("#start-button"),
  verifyButton: document.querySelector("#verify-button"),
  notice: document.querySelector("#notice"),
  workspacePath: document.querySelector("#workspace-path"),
  objectiveProgress: document.querySelector("#objective-progress"),
  objectiveList: document.querySelector("#objective-list"),
  evidencePanel: document.querySelector("#evidence-panel"),
  markdownReport: document.querySelector("#markdown-report"),
  jsonReport: document.querySelector("#json-report"),
};

async function api(path, options = {}) {
  const headers = { Accept: "application/json", ...(options.headers || {}) };
  if (options.method === "POST") {
    headers["Content-Type"] = "application/json";
    headers["X-GitQuest-Request"] = "browser-ui";
  }
  const response = await fetch(path, { ...options, headers });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || `Request failed with status ${response.status}.`);
  }
  return payload;
}

function setBusy(busy) {
  elements.startButton.disabled = busy;
  elements.verifyButton.disabled = busy;
}

function showNotice(message, tone = "info") {
  elements.notice.textContent = message;
  elements.notice.dataset.tone = tone;
  elements.notice.hidden = false;
}

function clearNotice() {
  elements.notice.hidden = true;
  elements.notice.textContent = "";
}

function scenarioButton(scenario) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "scenario-item";
  button.dataset.scenarioId = scenario.id;
  button.setAttribute("aria-pressed", String(scenario.id === state.selectedId));

  const index = document.createElement("span");
  index.className = "scenario-index";
  index.textContent = String(state.scenarios.indexOf(scenario) + 1).padStart(2, "0");

  const copy = document.createElement("span");
  const title = document.createElement("strong");
  title.textContent = scenario.title;
  const meta = document.createElement("small");
  meta.textContent = `${scenario.profile} · ${scenario.difficulty}`;
  copy.append(title, meta);

  button.append(index, copy);
  button.addEventListener("click", () => selectScenario(scenario.id));
  return button;
}

function renderScenarioList() {
  elements.scenarioList.replaceChildren(...state.scenarios.map(scenarioButton));
  elements.scenarioCount.textContent = String(state.scenarios.length);
}

function objectiveCard(objective, result) {
  const resultObjective = result?.objectives.find((item) => item.id === objective.id);
  const article = document.createElement("article");
  article.className = "objective-card";
  if (resultObjective?.passed) article.dataset.status = "passed";
  if (resultObjective && !resultObjective.passed) article.dataset.status = "pending";

  const marker = document.createElement("span");
  marker.className = "objective-marker";
  marker.textContent = resultObjective?.passed ? "✓" : "";

  const copy = document.createElement("div");
  const titleRow = document.createElement("div");
  titleRow.className = "objective-title";
  const title = document.createElement("strong");
  title.textContent = objective.title;
  const points = document.createElement("span");
  points.textContent = `${objective.points} pts`;
  titleRow.append(title, points);

  const description = document.createElement("p");
  description.textContent = objective.description;
  copy.append(titleRow, description);

  if (resultObjective && !resultObjective.passed) {
    const findings = document.createElement("ul");
    findings.className = "findings";
    resultObjective.checks
      .filter((check) => !check.passed)
      .forEach((check) => {
        const item = document.createElement("li");
        item.textContent = check.message;
        findings.append(item);
      });
    copy.append(findings);
  }

  article.append(marker, copy);
  return article;
}

function renderMission() {
  if (!state.selected) return;
  const scenario = state.selected;
  elements.emptyState.hidden = true;
  elements.missionContent.hidden = false;
  elements.missionProfile.textContent = `${scenario.profile} profile`;
  elements.missionDifficulty.textContent = scenario.difficulty;
  elements.missionCategory.textContent = scenario.category.replaceAll("_", " ");
  elements.missionTitle.textContent = scenario.title;
  elements.missionSummary.textContent = scenario.summary;
  elements.scoreValue.textContent = state.result ? String(state.result.score) : "—";

  const completed = state.result
    ? state.result.objectives.filter((objective) => objective.passed).length
    : 0;
  elements.objectiveProgress.textContent = `${completed} / ${scenario.objectives.length} complete`;
  elements.objectiveList.replaceChildren(
    ...scenario.objectives.map((objective) => objectiveCard(objective, state.result)),
  );

  document.querySelectorAll(".scenario-item").forEach((button) => {
    const selected = button.dataset.scenarioId === state.selectedId;
    button.setAttribute("aria-pressed", String(selected));
  });
}

async function selectScenario(scenarioId) {
  clearNotice();
  state.selectedId = scenarioId;
  state.result = null;
  state.selected = await api(`/api/scenarios/${encodeURIComponent(scenarioId)}`);
  elements.workspacePath.textContent = "Start the lab to create a workspace.";
  elements.evidencePanel.hidden = true;
  renderMission();
}

async function startSelectedScenario() {
  if (!state.selectedId) return;
  const approved = window.confirm(
    "Initialize a fresh lab? This safely resets the existing workspace for this scenario.",
  );
  if (!approved) return;
  clearNotice();
  setBusy(true);
  try {
    const payload = await api(
      `/api/scenarios/${encodeURIComponent(state.selectedId)}/start`,
      { method: "POST", body: "{}" },
    );
    state.result = null;
    elements.workspacePath.textContent = payload.workspace;
    elements.evidencePanel.hidden = true;
    showNotice("Lab initialized. Open the workspace, read INCIDENT.md, and contain the breach.", "success");
    renderMission();
  } catch (error) {
    showNotice(error.message, "error");
  } finally {
    setBusy(false);
  }
}

async function verifySelectedScenario() {
  if (!state.selectedId) return;
  clearNotice();
  setBusy(true);
  try {
    const payload = await api(
      `/api/scenarios/${encodeURIComponent(state.selectedId)}/verify`,
      { method: "POST", body: "{}" },
    );
    state.result = payload;
    elements.workspacePath.textContent = payload.workspace_path;
    elements.markdownReport.textContent = payload.reports.markdown;
    elements.jsonReport.textContent = payload.reports.json;
    elements.evidencePanel.hidden = false;
    showNotice(
      payload.passed
        ? "Incident contained. Your evidence report is ready."
        : `Verification scored ${payload.score}/100. Review the unresolved controls below.`,
      payload.passed ? "success" : "warning",
    );
    renderMission();
  } catch (error) {
    showNotice(error.message, "error");
  } finally {
    setBusy(false);
  }
}

async function boot() {
  try {
    const [health, catalog] = await Promise.all([api("/api/health"), api("/api/scenarios")]);
    elements.runtimeLabel.textContent = `Local runtime ready · v${health.version}`;
    state.scenarios = catalog.scenarios;
    renderScenarioList();
    if (state.scenarios.length) await selectScenario(state.scenarios[0].id);
  } catch (error) {
    elements.runtimeLabel.textContent = "Local runtime unavailable";
    showNotice(error.message, "error");
  }
}

elements.startButton.addEventListener("click", startSelectedScenario);
elements.verifyButton.addEventListener("click", verifySelectedScenario);
boot();
