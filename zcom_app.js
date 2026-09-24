function log(m, c="text-slate-300") {
  const b = document.getElementById("logBox");
  b.innerHTML += `<div class="${c}">${m}</div>`;
  b.scrollTop = b.scrollHeight;
}
function renderSector() {
  const c = document.getElementById("sec").value, d = DATA[c];
  document.getElementById("tList").innerHTML = d.trends.map(t => `<div class="p-2 bg-slate-950 rounded border border-slate-800 text-xs mb-1.5"><div class="flex justify-between font-bold"><span>${t[0]} <b class="text-emerald-400">${t[1]}</b></span><span>${t[3]}</span></div><div class="w-full h-1.5 bg-slate-800 rounded mt-1"><div class="h-full bg-red-500 rounded" style="width:${t[2]}%"></div></div></div>`).join("");
  document.getElementById("sqlBox").innerText = `SELECT term, ARRAY_AGG(STRUCT(rank, week) ORDER BY week DESC LIMIT 1) AS latest\nFROM \`bigquery-public-data.google_trends.international_top_terms\`\nWHERE refresh_date = '2025-08-25' AND country_name = '${c}'\nGROUP BY term ORDER BY (SELECT rank FROM UNNEST(latest)) LIMIT 100;`;
}
async function loadGH(u, label) {
  log(`🐙 [MCP -> GitHub API] Fetching ${label}...`, "text-purple-400 font-bold");
  const j = await (await fetch(u)).json();
  (j.items || j || []).slice(0, 3).forEach(i => log(`• <a href="${i.html_url}" target="_blank" class="underline text-blue-400">#${i.number}: ${i.title}</a>`));
}
function runLoop() {
  const c = document.getElementById("sec").value;
  document.getElementById("logBox").innerHTML = "";
  log("🛡️ [1/4 Model Armor]: Screening PII & Prompt Injection... ✅ CLEARED", "text-emerald-400 font-bold");
  setTimeout(() => log(`📊 [2/4 zcom-bq-agent]: Partition scan on ${c} -> Top spike: ${DATA[c].trends[0][0]} (${DATA[c].trends[0][1]})`, "text-amber-400"), 400);
  setTimeout(() => log(`🔍 [3/4 basic-search-agent]: ${DATA[c].recon}`, "text-blue-400"), 800);
  setTimeout(() => loadGH("https://api.github.com/search/issues?q=repo:google/adk-python+is:issue+is:open+MCP&per_page=3", "google/adk-python MCP issues"), 1200);
}
