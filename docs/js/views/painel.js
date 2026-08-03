/* Tela PAINEL — contagem regressiva, progresso por matéria e indicadores. */

import { el, dias, fData, cartao, barraProgresso, pct, num, soma, n1, n2, nInt } from "../ui.js";
import { estado, CONCLUIDOS } from "../store.js";

export function viewPainel(d) {
  const frag = document.createDocumentFragment();

  /* ---- contadores ---- */
  const dEam = dias(estado.datas.eam);
  const dEsa = dias(estado.datas.esa);
  frag.appendChild(el("div", { class: "grade-cards", estilo: { marginBottom: "16px" } }, [
    contador("Prova da EAM · Marinha", dEam, estado.datas.eam, "eam"),
    contador("Prova da ESA · Exército", dEsa, estado.datas.esa, "esa"),
  ]));

  /* ---- progresso por matéria ---- */
  const linhas = d.ordem.map((m) => {
    const tops = d.topicos.filter((t) => t.materia === m);
    const marcados = tops.filter((t) => CONCLUIDOS.includes(estado.topicos[t.id]?.status));
    const confs = tops.map((t) => num(estado.topicos[t.id]?.confianca)).filter((x) => x !== null);
    const acs = tops.map((t) => num(estado.topicos[t.id]?.acerto)).filter((x) => x !== null);
    return {
      materia: m, total: tops.length, feitos: marcados.length,
      frac: tops.length ? marcados.length / tops.length : 0,
      conf: confs.length ? confs.reduce((a, b) => a + b, 0) / confs.length : null,
      ac: acs.length ? acs.reduce((a, b) => a + b, 0) / acs.length : null,
    };
  });
  const totTop = linhas.reduce((a, l) => a + l.total, 0);
  const totFeitos = linhas.reduce((a, l) => a + l.feitos, 0);

  const tabela = el("div", { class: "tabela-wrap" }, [
    el("table", { class: "tb" }, [
      el("thead", {}, [el("tr", {}, [
        el("th", { texto: "" }), el("th", { texto: "Matéria" }), el("th", { texto: "Serve para" }),
        el("th", { class: "cen", texto: "Tópicos" }), el("th", { class: "cen", texto: "Feitos" }),
        el("th", { texto: "Progresso", estilo: { minWidth: "170px" } }),
        el("th", { class: "cen", texto: "Confiança" }), el("th", { class: "cen", texto: "% acerto" }),
        el("th", { texto: "Situação" }),
      ])]),
      el("tbody", {}, linhas.map((l) => {
        const cor = d.materias[l.materia].barra;
        const fam = d.familias[d.materias[l.materia].familia];
        return el("tr", {}, [
          el("td", { estilo: { width: "6px", padding: "0", background: cor } }),
          el("td", {}, [el("b", { estilo: { color: cor }, texto: l.materia })]),
          el("td", { estilo: { fontSize: "11.5px", color: "var(--ink-2)" }, texto: fam.rotulo }),
          el("td", { class: "cen", texto: l.total }),
          el("td", { class: "cen", texto: l.feitos }),
          el("td", {}, [barraProgresso(l.frac, cor)]),
          el("td", { class: "cen", texto: l.conf === null ? "—" : "★".repeat(Math.round(l.conf)) }),
          el("td", { class: "cen", texto: l.ac === null ? "—" : pct(l.ac) }),
          el("td", {}, [situacao(l.feitos, l.frac)]),
        ]);
      }).concat([
        el("tr", { estilo: { fontWeight: "700" } }, [
          el("td", { estilo: { background: "var(--navy)" } }),
          el("td", { texto: "TOTAL" }), el("td"),
          el("td", { class: "cen", texto: totTop }),
          el("td", { class: "cen", texto: totFeitos }),
          el("td", {}, [barraProgresso(totTop ? totFeitos / totTop : 0, "var(--navy-2)")]),
          el("td"), el("td"), el("td"),
        ]),
      ])),
    ]),
  ]);
  frag.appendChild(cartao("Progresso do conteúdo",
    "Marque os tópicos em Conteúdo — as barras andam sozinhas.", [tabela], null, true));

  /* ---- execução ---- */
  const sem = Object.values(estado.semanas);
  const comReg = sem.filter((s) => num(s.horas) !== null);
  const horasFeitas = soma(sem.map((s) => s.horas));
  const horasPlan = comReg.length * 33;
  const q = soma(sem.map((s) => s.questoes));
  const c = soma(sem.map((s) => s.certas));
  const aulas = soma(sem.map((s) => s.aulas));
  const notas = estado.simulados.map((s) => notaSimulado(s)).filter((x) => x !== null);
  const notasRed = estado.redacoes.map((r) => num(r.nota)).filter((x) => x !== null);
  const mediaRed = notasRed.length ? notasRed.reduce((a, b) => a + b, 0) / notasRed.length : null;

  const kpis = [
    ["Semanas com registro", comReg.length, "de 52 até a prova da ESA", false],
    ["Horas próprias cumpridas", n1.format(horasFeitas), `${nInt.format(horasPlan)} h planejadas`, false],
    ["Aderência ao plano", horasPlan ? pct(horasFeitas / horasPlan) : "—",
      "mínimo aceitável: 85%", horasPlan > 0 && horasFeitas / horasPlan < 0.85],
    ["Aulas do curso", nInt.format(aulas), "5 por semana", false],
    ["Questões resolvidas", nInt.format(q), "meta: 250 por semana", false],
    ["Taxa de acerto", q ? pct(c / q) : "—", "meta: acima de 75%", q > 0 && c / q < 0.6],
    ["Simulados", estado.simulados.length, "1 por sábado", false],
    ["Média nos simulados", notas.length ? n1.format(notas.reduce((a, b) => a + b, 0) / notas.length) : "—",
      "EAM aprova com 50 — mire acima de 70", false],
    ["Redações", estado.redacoes.length, "1 a 2 por semana", false],
    ["Média das redações", mediaRed === null ? "—" : n2.format(mediaRed),
      "a ESA elimina abaixo de 5,0", mediaRed !== null && mediaRed < 5],
    ["Treinos registrados", estado.taf.length, "5 a 6 por semana", false],
  ];

  frag.appendChild(cartao("Execução e desempenho", "Alimentado por Semanas, Simulados, Redações e TAF.", [
    el("div", { class: "kpi" }, kpis.map(([rot, val, meta, alerta]) =>
      el("div", { class: `kpi__item ${alerta ? "kpi__item--alerta" : ""}` }, [
        el("div", { class: "kpi__rot", texto: rot }),
        el("div", { class: "kpi__val", texto: String(val) }),
        el("div", { class: "kpi__meta", texto: meta }),
      ]))),
  ]));

  /* ---- próximos marcos ---- */
  const futuros = d.marcos
    .map((m) => ({ ...m, faltam: dias(m.data) }))
    .filter((m) => m.faltam !== null && m.faltam >= 0)
    .sort((a, b) => a.faltam - b.faltam);

  frag.appendChild(cartao("Próximos marcos", null, [
    futuros.length
      ? el("div", {}, futuros.map((m) => el("div", {
          estilo: { display: "flex", gap: "12px", padding: "9px 0", borderBottom: "1px solid var(--line)", alignItems: "baseline", flexWrap: "wrap" },
        }, [
          el("b", { estilo: { minWidth: "78px", color: m.tag ? (m.tag === "EAM" ? "var(--fam-eam)" : "var(--fam-esa)") : "var(--ink-2)" },
                    texto: `${m.faltam} dias` }),
          el("span", { estilo: { flex: "1", minWidth: "180px" }, texto: m.nome }),
          el("span", { estilo: { fontSize: "12px", color: "var(--ink-3)" }, texto: fData(m.data) }),
        ])))
      : el("p", { texto: "Todos os marcos já passaram." }),
  ]));

  return frag;
}

export function notaSimulado(s) {
  const ac = soma(Object.values(s.acertos || {}));
  const q = num(s.questoes);
  if (!q) return null;
  return (ac / q) * 100;
}

function contador(rot, n, data, tipo) {
  const corpo = n === null ? "—" : (n < 0 ? "✔" : String(n));
  return el("div", { class: `contador contador--${tipo}` }, [
    el("div", { class: "contador__rot", texto: rot }),
    el("div", { class: "contador__n", texto: corpo }),
    el("div", { class: "contador__u", texto: n === null ? "" : (n < 0 ? "prova realizada" : "dias restantes") }),
    el("div", { class: "contador__pe",
      texto: n === null || n < 0 ? fData(data) : `${Math.round(n / 7)} semanas · ${fData(data)}` }),
  ]);
}

function situacao(feitos, frac) {
  if (!feitos) return el("span", { class: "chip", texto: "◻ não iniciado" });
  if (frac >= 0.9) return el("span", { class: "chip chip--ok", texto: "● dominado" });
  if (frac >= 0.6) return el("span", { class: "chip", texto: "● em ritmo" });
  if (frac >= 0.3) return el("span", { class: "chip", texto: "◐ atenção" });
  return el("span", { class: "chip chip--bad", texto: "◔ atrasado" });
}
