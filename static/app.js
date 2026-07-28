const input = document.querySelector("#expression");
const result = document.querySelector("#result");
const history = document.querySelector("#history");

document.querySelector("#keys").addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;
  if (button.dataset.action === "clear") {
    input.value = "";
    result.textContent = "Ready";
  } else if (button.dataset.action === "calculate") {
    calculate();
  } else if (button.dataset.value) {
    input.value += button.dataset.value;
    input.focus();
  }
});

document.querySelector("[data-example]").addEventListener("click", (event) => {
  input.value = event.currentTarget.dataset.example;
  calculate();
});

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter") calculate();
});

async function calculate() {
  if (!input.value.trim()) return;
  result.textContent = "Calculating…";
  const response = await fetch("api/calculate", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({expression: input.value}),
  });
  const data = await response.json();
  if (!response.ok) {
    result.textContent = data.detail || "Unable to calculate";
    return;
  }
  result.textContent = Number.isInteger(data.result) ? data.result : Number(data.result.toFixed(8));
  loadHistory();
}

async function loadHistory() {
  const response = await fetch("api/history");
  const rows = await response.json();
  if (!rows.length) return;
  history.innerHTML = rows.map((row) =>
    `<article><code>${escapeHtml(row.expression)}</code><span>=</span><strong>${row.result}</strong></article>`
  ).join("");
}

function escapeHtml(value) {
  const node = document.createElement("span");
  node.textContent = value;
  return node.innerHTML;
}

loadHistory();

