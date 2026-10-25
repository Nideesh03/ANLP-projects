$("go").onclick = async () => {
  const documents = $("docs").value.split("\n").filter(s => s.trim());
  const d = await callApi({question: $("q").value, documents}, "ans");
  $("ans").innerHTML = `<div class="answer"><small>Answer passage</small>${esc(d.answer)}</div>
    <p class="muted">Top-ranked sentence: ${esc(d.top_sentence)}</p>
    <p class="muted">${d.documents} documents · ${d.sentences} sentences · ${d.vocabulary} index terms</p>`;
  $("hits").innerHTML = `<table><tr><th>#</th><th>Sentence</th><th>Doc</th><th>Cosine score</th></tr>${d.hits.map(h=>`<tr><td>${h.rank}</td><td>${esc(h.sentence)}</td><td>D${h.doc}</td>
    <td><div class="meter"><i style="width:${Math.round(h.score*100)}%"></i></div>${h.score.toFixed(4)}</td></tr>`).join("")}</table>`;
};
