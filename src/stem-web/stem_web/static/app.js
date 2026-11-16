"use strict";

const POLL_MS = 2000;
const UNFINISHED = ["queued", "running"];

function hasUnfinishedJob(jobs) {
  return jobs.some((job) => UNFINISHED.includes(job.status));
}

function renderJob(job) {
  const item = document.createElement("li");
  item.className = "job job-" + job.status;
  const heading = document.createElement("p");
  heading.className = "job-heading";
  heading.textContent = job.id + " " + job.status;
  item.appendChild(heading);
  if (job.error) {
    const error = document.createElement("p");
    error.className = "job-error";
    error.textContent = job.error;
    item.appendChild(error);
  }
  return item;
}

function renderJobs(list, jobs) {
  list.replaceChildren();
  if (jobs.length === 0) {
    const empty = document.createElement("li");
    empty.className = "empty";
    empty.textContent = "No jobs yet.";
    list.appendChild(empty);
    return;
  }
  jobs.forEach((job) => list.appendChild(renderJob(job)));
}

if (typeof document !== "undefined") {
  const form = document.getElementById("upload-form");
  const status = document.getElementById("status");
  const list = document.getElementById("jobs");
  let timer = null;

  async function refresh() {
    clearTimeout(timer);
    try {
      const response = await fetch("/jobs");
      const jobs = await response.json();
      renderJobs(list, jobs);
      if (hasUnfinishedJob(jobs)) {
        timer = setTimeout(refresh, POLL_MS);
      }
    } catch (error) {
      status.textContent = "The service is not reachable.";
    }
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData();
    data.append("file", form.elements.file.files[0]);
    data.append("full_stems", form.elements.full_stems.checked ? "true" : "false");
    status.textContent = "Sending the file.";
    try {
      const response = await fetch("/jobs", { method: "POST", body: data });
      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        status.textContent = typeof body.detail === "string" ? body.detail : "The upload failed.";
        return;
      }
      status.textContent = "The job is queued.";
      form.reset();
      refresh();
    } catch (error) {
      status.textContent = "The service is not reachable.";
    }
  });

  refresh();
}
