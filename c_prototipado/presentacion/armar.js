// Completa el pie de cada diapositiva: materia, fase activa y número de diapositiva.
(function () {
  const diapos = [...document.querySelectorAll(".slide")];
  const FASES = ["I", "II", "III", "IV"];
  const NOMBRES = { I: "I · Investigación", II: "II · Planificación", III: "III · Construcción", IV: "IV · Consulta" };
  const MATERIA = "Informática Industrial · TP Nº 3 · Grupo Nº 4";
  diapos.forEach((s, i) => {
    const numero = `${i + 1} / ${diapos.length}`;
    const apertura = s.querySelector(".pie.a-pie");
    if (apertura) apertura.innerHTML = `${MATERIA}<span style="margin-left:auto">${numero}</span>`;
    const pie = s.querySelector(".pie[data-fase]");
    if (!pie) return;
    const fase = pie.dataset.fase;
    pie.innerHTML = MATERIA +
      `<div class="fases">${FASES.map(f => f === fase ? `<span class="on">${NOMBRES[f]}</span>` : `<span>${f}</span>`).join("")}</div>` +
      numero;
  });
})();
