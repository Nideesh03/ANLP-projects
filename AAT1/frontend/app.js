$("go").onclick = async () => {
  const d = await callApi({text: $("txt").value}, "summary");
  const t = $("txt").value; let html = "", last = 0;
  d.entities.forEach(e => { html += esc(t.slice(last, e.start)) + `<span class="ent ${e.label}">${esc(e.text)}<sup>${e.label}</sup></span>`; last = e.end; });
  html += esc(t.slice(last));
  $("summary").innerHTML = `<div class="stats"><div class="stat"><b>${d.words.length}</b><span>words tagged</span></div>
    <div class="stat"><b>${d.entities.length}</b><span>entities</span></div><div class="stat"><b>${d.sentences}</b><span>sentences</span></div>
    <div class="stat"><b>${d.noun_chunks.length}</b><span>noun chunks</span></div></div><p class="ents">${html}</p>
    <p class="muted">Model: ${esc(d.model)} · Tag counts: ${Object.entries(d.tag_count).map(([k,v])=>`<span class="chip alt">${k} ${v}</span>`).join("")}</p>`;
  $("ents").innerHTML = `<table><tr><th>Entity</th><th>Label</th><th>Meaning</th></tr>${d.entities.map(e=>`<tr><td>${esc(e.text)}</td><td><span class="chip">${e.label}</span></td><td>${esc(e.explain)}</td></tr>`).join("")}</table>`;
  $("pos").innerHTML = `<table><tr><th>Word</th><th>UPOS</th><th>Penn</th><th>Lemma</th></tr>${d.words.map(w=>`<tr><td>${esc(w.word)}</td><td><span class="chip">${w.upos}</span></td><td>${w.penn}</td><td>${esc(w.lemma)}</td></tr>`).join("")}</table>`;
};
