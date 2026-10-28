// Convierte cada <pre class="editor"> en el editor de la pestaña Ejecutar SQL de
// DB Browser for SQLite: pestaña, barra con los botones de ejecutar, números de línea
// y los colores de sintaxis del programa (los mismos que se ven en las capturas).
(function () {
  const KW = new Set(("SELECT FROM WHERE AND OR NOT IN BETWEEN ORDER BY GROUP HAVING AS ASC DESC " +
    "INNER LEFT JOIN ON CREATE TABLE PRIMARY KEY FOREIGN REFERENCES NULL UNIQUE CHECK " +
    "INSERT INTO VALUES PRAGMA DROP IF EXISTS TRIGGER BEFORE AFTER UPDATE OF WHEN BEGIN END " +
    "RAISE ABORT IS INTEGER VARCHAR FLOAT DATETIME DATE NEW COUNT SUM AVG MAX MIN ROUND COALESCE").split(" "));
  const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const TOKEN = /(--.*$)|('(?:[^']|'')*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)|([\s\S])/gm;

  function resaltar(linea) {
    let html = "";
    linea.replace(TOKEN, (m, com, str, num, pal) => {
      if (com) html += `<span class="com">${esc(com)}</span>`;
      else if (str) html += `<span class="str">${esc(str)}</span>`;
      else if (num) html += `<span class="num">${num}</span>`;
      else if (pal) html += KW.has(pal.toUpperCase()) ? `<span class="kw">${pal}</span>` : `<span class="id">${pal}</span>`;
      else html += esc(m);
      return m;
    });
    return html;
  }

  const ICONO = c => `<svg width="16" height="16" viewBox="0 0 16 16"><rect x="2" y="2" width="12" height="12" rx="2" fill="${c}"/></svg>`;
  const EJECUTAR = `<svg width="16" height="16" viewBox="0 0 16 16"><path d="M4 2 L13 8 L4 14 Z" fill="#2B6CC4"/></svg>`;
  const LINEA = `<svg width="18" height="16" viewBox="0 0 18 16"><path d="M3 2 L11 8 L3 14 Z" fill="#2B6CC4"/><rect x="12" y="2" width="3" height="12" fill="#2B6CC4"/></svg>`;

  document.querySelectorAll("pre.editor").forEach(pre => {
    const lineas = pre.textContent.replace(/^\n+|\s+$/g, "").split("\n");
    const inicio = parseInt(pre.dataset.inicio || "1", 10);
    const cabecera = "compacto" in pre.dataset ? "" :
      `<div class="ed-barra">${ICONO("#9BB0C8")}${ICONO("#E3B341")}${ICONO("#9BB0C8")}<i></i>${EJECUTAR}${LINEA}<i></i></div>` +
      `<div class="ed-pestanas"><span class="ed-pestana">${esc(pre.dataset.pestana || "SQL 1")}<b></b></span></div>`;
    pre.innerHTML = cabecera +
      `<div class="ed-codigo"><div class="ed-num">${lineas.map((_, i) => i + inicio).join("<br>")}</div>` +
      `<div class="ed-txt">${lineas.map(resaltar).join("\n")}</div></div>`;
  });
})();
