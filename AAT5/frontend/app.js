const SAMPLES = {"bat": [{"word": "bat", "pos": "n", "sentence": "A bat flew out of the dark cave at night to hunt insects."}, {"word": "bat", "pos": "n", "sentence": "He gripped the wooden cricket bat and hit the ball over the boundary."}], "crane": [{"word": "crane", "pos": "n", "sentence": "A tall crane lifted the heavy steel beams at the construction site."}, {"word": "crane", "pos": "n", "sentence": "The crane stood on one leg in the shallow lake waiting for a fish."}], "light": [{"word": "light", "pos": "n", "sentence": "Please switch on the light because the room is too dark to read."}, {"word": "light", "pos": "a", "sentence": "The bag is light enough for a small child to carry."}]};
document.querySelectorAll(".examples button").forEach(b => b.addEventListener("click", () => {
  const rows = SAMPLES[b.textContent] || [];
  $("ctxs").innerHTML = "<tr><th>Sentence</th><th style='width:80px'>POS</th></tr>" + rows.map(c => `<tr><td><input class="ctx" value="${esc(c.sentence)}"></td><td><select class="pos"><option value="">auto</option>${["n","v","a","r"].map(p=>`<option value="${p}" ${p===c.pos?"selected":""}>${p}</option>`).join("")}</select></td></tr>`).join("");
}));
$("go").onclick = async () => {
  const ctx = [...document.querySelectorAll(".ctx")].map((el, i) => ({sentence: el.value, pos: document.querySelectorAll(".pos")[i].value}));
  const d = await callApi({word: $("w").value, contexts: ctx}, "syn");
  $("syn").innerHTML = `<div class="stats"><div class="stat"><b>${d.sense_count}</b><span>senses</span></div><div class="stat"><b>${d.all_synonyms.length}</b><span>synonyms</span></div></div>
    <p>${d.all_synonyms.map(s=>`<span class="chip alt">${esc(s)}</span>`).join("")}</p>`;
  $("ctxout").innerHTML = `<table><tr><th>Sentence</th><th>POS</th><th>NLTK Lesk</th><th>Extended Lesk (overlap)</th></tr>${d.contexts.map(c=>`<tr><td>${esc(c.sentence)}</td><td>${c.pos_hint}</td>
    <td><span class="chip alt">${c.synset}</span><br>${esc(c.definition)}</td><td><span class="chip">${c.ext_synset}</span><br>${esc(c.ext_definition)}<br><span class="muted">overlap: ${esc(c.overlap.join(", "))}</span></td></tr>`).join("")}</table>`;
  $("senses").innerHTML = `<table><tr><th>Synset</th><th>POS</th><th>Definition</th><th>Synonyms</th></tr>${d.senses.map(s=>`<tr><td>${s.synset}</td><td>${s.pos}</td><td>${esc(s.definition)}</td><td>${esc(s.synonyms.join(", "))}</td></tr>`).join("")}</table>`;
};
