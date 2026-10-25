$("go").onclick = async () => {
  const d = await callApi({documents: $("docs").value.split("\n"), n_topics: $("k").value, top_n: $("n").value, seed: $("seed").value}, "topics");
  $("meta").innerHTML = `<div class="stats"><div class="stat"><b>${d.n_docs}</b><span>documents</span></div><div class="stat"><b>${d.vocabulary}</b><span>vocabulary</span></div><div class="stat"><b>${d.perplexity}</b><span>perplexity</span></div></div>`;
  $("topics").innerHTML = `<div class="stats">${d.topics.map(t=>`<div class="stat"><b>Topic ${t.topic}</b>${t.words.map(w=>`<div style="display:flex;gap:8px;align-items:center;margin:4px 0"><span style="width:90px">${esc(w.word)}</span><div class="meter" style="flex:1"><i style="width:${Math.min(100,w.p*700)}%"></i></div><span class="muted">${w.p.toFixed(3)}</span></div>`).join("")}</div>`).join("")}</div>`;
  $("docsout").innerHTML = `<table><tr><th>Doc</th><th>Text</th><th>Topic</th><th>Share</th></tr>${d.documents.map(x=>`<tr><td>${x.doc}</td><td>${esc(x.text)}</td><td><span class="chip">T${x.topic}</span></td><td>${x.share}</td></tr>`).join("")}</table>`;
};
