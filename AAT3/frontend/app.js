$("go").onclick = async () => {
  const d = await callApi({question: $("q").value}, "ans");
  $("ans").innerHTML = `<div class="answer"><small>${esc(d.generator)}</small>${esc(d.answer)}</div>
    <p class="muted">Knowledge source: ${esc(d.source)}</p>
    <p>${d.matched.map(m=>`<span class="chip">${m.type}: ${esc(m.value)}</span>`).join("") || "<span class='muted'>No entity matched</span>"}</p>`;
  $("ctx").innerHTML = d.facts.length ? `<table><tr><th>#</th><th>Fact passed to the generator</th></tr>${d.facts.map((f,i)=>`<tr><td>${i+1}</td><td>${esc(f)}</td></tr>`).join("")}</table>` : "<p class='muted'>Nothing retrieved.</p>";
};
