const routes = new Map([
  ["/", "home"],
  ["/learn", "learn"],
  ["/guide", "guide"],
]);

let curriculumLoaded = false;

function setRoute(pathname, replace = false) {
  const viewName = routes.get(pathname) || "not-found";
  document.querySelectorAll("[data-view]").forEach((view) => {
    view.hidden = view.dataset.view !== viewName;
  });
  document.querySelectorAll("nav a").forEach((link) => {
    const current = link.getAttribute("href") === pathname;
    if (current) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
  if (!replace) window.history.pushState({}, "", pathname);
  document.title = viewName === "home" ? "GitQuest — Learn Git by doing" : `GitQuest — ${viewName}`;
  document.querySelector("#content").focus({ preventScroll: true });
  window.scrollTo(0, 0);
  if (viewName === "learn" && !curriculumLoaded) loadCurriculum();
}

function missionItem(mission) {
  const item = document.createElement("li");
  const number = document.createElement("span");
  number.textContent = String(mission.id).padStart(2, "0");
  const title = document.createElement("strong");
  title.textContent = mission.title;
  const command = document.createElement("code");
  command.textContent = mission.command;
  item.append(number, title, command);
  return item;
}

function areaCard(area) {
  const article = document.createElement("article");
  article.className = "area";
  const summary = document.createElement("div");
  const status = document.createElement("span");
  status.className = "status";
  status.textContent = area.status;
  const heading = document.createElement("h2");
  heading.textContent = area.name;
  const description = document.createElement("p");
  description.textContent = area.description;
  summary.append(status, heading, description);

  if (area.missions.length) {
    const list = document.createElement("ol");
    list.className = "mission-list";
    area.missions.forEach((mission) => list.append(missionItem(mission)));
    article.append(summary, list);
  } else {
    const empty = document.createElement("p");
    empty.className = "empty";
    empty.textContent = "Lessons will be added in the execution plan.";
    article.append(summary, empty);
  }
  return article;
}

async function loadCurriculum() {
  const container = document.querySelector("#curriculum");
  try {
    const response = await fetch("/api/curriculum");
    if (!response.ok) throw new Error("Curriculum request failed");
    const data = await response.json();
    container.replaceChildren(...data.areas.map(areaCard));
    curriculumLoaded = true;
  } catch (_error) {
    container.textContent = "The curriculum could not be loaded. Restart the local server and try again.";
  }
}

async function loadVersion() {
  try {
    const response = await fetch("/api/health");
    const data = await response.json();
    document.querySelector("#version").textContent = `Local server · v${data.version}`;
  } catch (_error) {
    document.querySelector("#version").textContent = "Local server unavailable";
  }
}

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[data-link]");
  if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  event.preventDefault();
  setRoute(new URL(link.href).pathname);
});

window.addEventListener("popstate", () => setRoute(window.location.pathname, true));
setRoute(window.location.pathname, true);
loadVersion();
