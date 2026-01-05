const output = document.getElementById("output");

const studentForm = document.getElementById("studentForm");
const studentsTableBody = document.querySelector("#studentsTable tbody");
const pairsTableBody = document.querySelector("#pairsTable tbody");

const refreshStudentsBtn = document.getElementById("refreshStudentsBtn");
const generatePairsBtn = document.getElementById("generatePairsBtn");
const refreshPairsBtn = document.getElementById("refreshPairsBtn");

/* Utility */
function show(data) {
  output.textContent =
    typeof data === "string" ? data : JSON.stringify(data, null, 2);
}

/* ---------- STUDENTS ---------- */

function renderStudents(students) {
  studentsTableBody.innerHTML = "";
  for (const s of students) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${s.id}</td>
      <td>${s.name}</td>
      <td>${s.role}</td>
      <td>${s.subject}</td>
    `;
    studentsTableBody.appendChild(tr);
  }
}

async function loadStudents() {
  const res = await fetch("/students");
  const data = await res.json();
  renderStudents(data);
}

/* Create student */
studentForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const student = {
    name: document.getElementById("name").value.trim(),
    role: document.getElementById("role").value,
    subject: document.getElementById("subject").value.trim().toLowerCase(),
  };

  const res = await fetch("/students", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(student),
  });

  const data = await res.json();
  show(data);

  studentForm.reset();
  await loadStudents();
});

refreshStudentsBtn.addEventListener("click", async () => {
  await loadStudents();
  show("Students refreshed.");
});

/* ---------- PAIRS ---------- */

function renderPairs(pairs) {
  pairsTableBody.innerHTML = "";
  for (const p of pairs) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${p.mentor}</td>
      <td>${p.mentee}</td>
      <td>${p.subject}</td>
    `;
    pairsTableBody.appendChild(tr);
  }
}

async function loadPairs() {
  const res = await fetch("/pairs");
  const data = await res.json();
  renderPairs(data);
}

generatePairsBtn.addEventListener("click", async () => {
  const res = await fetch("/pairs/generate", { method: "POST" });
  const data = await res.json();
  show(data);
  await loadPairs();
});

refreshPairsBtn.addEventListener("click", async () => {
  await loadPairs();
  show("Pairs refreshed.");
});

/* ---------- INITIAL LOAD ---------- */
loadStudents();
loadPairs();
