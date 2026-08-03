/* Telas de registro: SIMULADOS, REDAÇÕES e TAF. */

import { el, cartao, campoEditavel, fData, iso, HOJE, pct, num, soma, n1, n2, chip, vazio, toast } from "../ui.js";
import { estado, mudar } from "../store.js";

const novoId = () => `${Date.now().toString(36)}${Math.random().toString(36).slice(2, 7)}`;

function botaoNovo(rot, ao) {
  return el("button", { class: "btn btn--primario", type: "button", onclick: ao }, [
    el("span", { class: "btn__ic", texto: "+" }), rot,
  ]);
}

function botaoApagar(ao) {
  return el("button", {
    class: "btn btn--peq btn--fantasma", type: "button", title: "Excluir",
    estilo: { color: "var(--bad-fg)" },
    onclick: () => { if (confirm("Excluir este registro?")) ao(); },
  }, ["✕"]);
}

/* ═══════════════════════════════════════════════════════════ SIMULADOS */
export function viewSimulados(d) {
  const frag = document.createDocumentFragment();
  const MATS = ["Português", "Matemática", "Física", "Química", "História", "Geografia", "Inglês"];
  const corpo = el("div");

  function novo() {
    mudar((s) => {
      s.simulados.unshift({ id: novoId(), data: iso(HOJE()), origem: "", alvo: "EAM",
                            acertos: {}, questoes: 50, fracos: "", acao: "" });
    });
    pintar(); toast("Simulado adicionado");
  }

  function pintar() {
    corpo.innerHTML = "";
    if (!estado.simulados.length) {
      corpo.appendChild(vazio("📝", "Nenhum simulado registrado. Faça um todo sábado, das 08h às 12h, cronometrado."));
      return;
    }
    const tb = el("table", { class: "tb" }, [
      el("thead", {}, [el("tr", {}, [
        el("th", { texto: "Data" }), el("th", { texto: "Origem" }), el("th", { class: "cen", texto: "Alvo" }),
        ...MATS.map((m) => el("th", { class: "cen", texto: m.slice(0, 4) + ".",
          estilo: { borderTop: `3px solid ${d.materias[m].barra}` } })),
        el("th", { class: "cen", texto: "Acertos" }), el("th", { class: "cen", texto: "Questões" }),
        el("th", { class: "cen", texto: "% acerto" }), el("th", { class: "cen", texto: "Nota" }),
        el("th", { texto: "Mais fracas" }), el("th", { texto: "Ação da semana" }), el("th"),
      ])]),
    ]);
    const tbody = el("tbody");
    for (const s of estado.simulados) {
      const set = (c) => (v) => mudar((st) => {
        const alvo = st.simulados.find((x) => x.id === s.id); if (alvo) alvo[c] = v;
      });
      const setAcerto = (m) => (v) => { mudar((st) => {
        const alvo = st.simulados.find((x) => x.id === s.id);
        if (alvo) { alvo.acertos = { ...alvo.acertos }; alvo.acertos[m] = v; }
      }); pintar(); };

      const ac = soma(MATS.map((m) => s.acertos?.[m]));
      const q = num(s.questoes);
      const p = q ? ac / q : null;
      const nota = p === null ? null : p * 100;

      tbody.appendChild(el("tr", {}, [
        el("td", {}, [campoEditavel({ valor: s.data, tipo: "date", ao: set("data") })]),
        el("td", {}, [campoEditavel({ valor: s.origem, ao: set("origem"), placeholder: "banca / ano" })]),
        el("td", { class: "cen" }, [campoEditavel({ valor: s.alvo, opcoes: ["EAM", "ESA"], ao: set("alvo") })]),
        ...MATS.map((m) => el("td", { class: "cen" }, [campoEditavel({
          valor: s.acertos?.[m] ?? "", tipo: "number", largura: "mini", ao: setAcerto(m),
        })])),
        el("td", { class: "cen", estilo: { fontWeight: "700" }, texto: ac || "—" }),
        el("td", { class: "cen" }, [campoEditavel({ valor: s.questoes, tipo: "number", largura: "mini", ao: (v) => { set("questoes")(v); pintar(); } })]),
        el("td", { class: "cen", estilo: { fontWeight: "650" }, texto: p === null ? "—" : pct(p) }),
        el("td", { class: "cen", estilo: notaCor(nota), texto: nota === null ? "—" : n1.format(nota) }),
        el("td", {}, [campoEditavel({ valor: s.fracos, ao: set("fracos") })]),
        el("td", {}, [campoEditavel({ valor: s.acao, ao: set("acao") })]),
        el("td", {}, [botaoApagar(() => { mudar((st) => { st.simulados = st.simulados.filter((x) => x.id !== s.id); }); pintar(); })]),
      ]));
    }
    tb.appendChild(tbody);
    corpo.appendChild(el("div", { class: "tabela-wrap" }, [tb]));

    const notas = estado.simulados.map((s) => {
      const q = num(s.questoes); if (!q) return null;
      return (soma(MATS.map((m) => s.acertos?.[m])) / q) * 100;
    }).filter((x) => x !== null);
    if (notas.length) {
      const media = notas.reduce((a, b) => a + b, 0) / notas.length;
      corpo.appendChild(el("div", { estilo: { padding: "12px 16px", borderTop: "1px solid var(--line)", fontSize: "13px" } }, [
        "Média geral: ", el("b", { texto: n1.format(media) }), " de 100 · ",
        media >= 70 ? chip("classificando", "ok") : media >= 50 ? chip("passa, sem folga") : chip("abaixo do corte", "bad"),
      ]));
    }
  }

  frag.appendChild(el("div", { class: "aviso" }, [
    el("div", {}, [
      el("b", { texto: "O corte da EAM" }),
      "Aprova com 50 pontos, exigindo mais de 10 em Português, Matemática e Ciências, sem zerar Inglês. Para classificar de verdade — não só passar — mire acima de 70.",
    ]),
  ]));
  frag.appendChild(cartao("Simulados", "Digite os acertos por matéria; o resto é calculado.",
    [corpo], [botaoNovo("Novo simulado", novo)], true));
  pintar();
  return frag;
}

const notaCor = (n) => n === null ? {}
  : n >= 70 ? { background: "var(--ok-bg)", color: "var(--ok-fg)", fontWeight: "700" }
  : n < 50 ? { background: "var(--bad-bg)", color: "var(--bad-fg)", fontWeight: "700" }
  : { fontWeight: "650" };

/* ═══════════════════════════════════════════════════════════ REDAÇÕES */
export function viewRedacoes(d) {
  const frag = document.createDocumentFragment();
  const CRIT = [["estrutura", "Estrutura", 2], ["argumentacao", "Argumentação", 3],
                ["coesao", "Coesão", 2], ["gramatica", "Gramática", 2], ["proposta", "Proposta", 1]];
  const corpo = el("div");
  const resumo = el("div");

  function novo() {
    mudar((s) => {
      s.redacoes.unshift({ id: novoId(), data: iso(HOJE()), tema: "", tempo: 60, nota: "",
                           criterios: {}, erros: "", acao: "" });
    });
    pintar(); toast("Redação adicionada");
  }

  function pintar() {
    corpo.innerHTML = ""; resumo.innerHTML = "";
    if (!estado.redacoes.length) {
      corpo.appendChild(vazio("✍", "Nenhuma redação registrada. São duas por semana: quarta às 19h40 e sábado às 14h15."));
      return;
    }
    const tb = el("table", { class: "tb" }, [
      el("thead", {}, [el("tr", {}, [
        el("th", { texto: "Data" }), el("th", { texto: "Tema", estilo: { minWidth: "220px" } }),
        el("th", { class: "cen", texto: "Tempo" }), el("th", { class: "cen", texto: "NOTA" }),
        ...CRIT.map(([, r, mx]) => el("th", { class: "cen", texto: `${r} (${mx})` })),
        el("th", { class: "cen", texto: "Soma" }),
        el("th", { texto: "Erros principais", estilo: { minWidth: "180px" } }),
        el("th", { texto: "Próxima vez", estilo: { minWidth: "180px" } }), el("th"),
      ])]),
    ]);
    const tbody = el("tbody");
    for (const r of estado.redacoes) {
      const set = (c) => (v) => mudar((st) => {
        const a = st.redacoes.find((x) => x.id === r.id); if (a) a[c] = v;
      });
      const setCrit = (k) => (v) => { mudar((st) => {
        const a = st.redacoes.find((x) => x.id === r.id);
        if (a) { a.criterios = { ...a.criterios }; a.criterios[k] = v; }
      }); pintar(); };
      const somaCrit = soma(CRIT.map(([k]) => r.criterios?.[k]));
      const nota = num(r.nota);

      tbody.appendChild(el("tr", {}, [
        el("td", {}, [campoEditavel({ valor: r.data, tipo: "date", ao: set("data") })]),
        el("td", {}, [campoEditavel({ valor: r.tema, ao: set("tema"), placeholder: "tema proposto" })]),
        el("td", { class: "cen" }, [campoEditavel({ valor: r.tempo, tipo: "number", largura: "mini", ao: set("tempo") })]),
        el("td", { class: "cen", estilo: redCor(nota) }, [campoEditavel({
          valor: r.nota, tipo: "number", passo: "0.5", largura: "mini", ao: (v) => { set("nota")(v); pintar(); },
        })]),
        ...CRIT.map(([k]) => el("td", { class: "cen" }, [campoEditavel({
          valor: r.criterios?.[k] ?? "", tipo: "number", passo: "0.5", largura: "mini", ao: setCrit(k),
        })])),
        el("td", { class: "cen", estilo: { fontWeight: "650" }, texto: somaCrit ? n1.format(somaCrit) : "—" }),
        el("td", {}, [campoEditavel({ valor: r.erros, ao: set("erros") })]),
        el("td", {}, [campoEditavel({ valor: r.acao, ao: set("acao") })]),
        el("td", {}, [botaoApagar(() => { mudar((st) => { st.redacoes = st.redacoes.filter((x) => x.id !== r.id); }); pintar(); })]),
      ]));
    }
    tb.appendChild(tbody);
    corpo.appendChild(el("div", { class: "tabela-wrap" }, [tb]));

    const notas = estado.redacoes.map((r) => num(r.nota)).filter((x) => x !== null);
    if (notas.length) {
      const m = notas.reduce((a, b) => a + b, 0) / notas.length;
      resumo.appendChild(el("div", {
        class: `aviso ${m >= 7 ? "aviso--ok" : m >= 5 ? "aviso--info" : ""}`,
        estilo: { marginTop: "14px" },
      }, [
        el("div", {}, [
          el("b", { texto: `Média atual: ${n2.format(m)}` }),
          m >= 7 ? "Zona segura. Mantenha o ritmo."
            : m >= 5 ? "Passa, mas sem margem — uma redação ruim no dia da prova elimina."
            : "RISCO DE ELIMINAÇÃO. Priorize redação sobre qualquer outra matéria até subir de 5,0.",
        ]),
      ]));
    }
  }

  frag.appendChild(el("div", { class: "aviso" }, [
    el("div", {}, [
      el("b", { texto: "A redação da ESA elimina sozinha" }),
      "Nota abaixo de 5,0 reprova, por melhor que seja o resto da prova. Não cai na EAM.",
    ]),
  ]));
  frag.appendChild(cartao("Redações", null, [corpo], [botaoNovo("Nova redação", novo)], true));
  frag.appendChild(resumo);
  pintar();
  return frag;
}

const redCor = (n) => n === null ? {}
  : n < 5 ? { background: "var(--bad-bg)" }
  : n >= 7 ? { background: "var(--ok-bg)" } : {};

/* ════════════════════════════════════════════════════════════════ TAF */
export function viewTaf(d) {
  const frag = document.createDocumentFragment();
  const metaCorrida = d.taf.corrida_min, metaNatacao = d.taf.natacao_seg;
  const corpo = el("div");

  function novo() {
    mudar((s) => {
      s.taf.unshift({ id: novoId(), data: iso(HOJE()), corrida: "", natacao: "",
                      barra: "", abdominais: "", flexoes: "", peso: "", obs: "" });
    });
    pintar(); toast("Treino adicionado");
  }

  function pintar() {
    corpo.innerHTML = "";
    if (!estado.taf.length) {
      corpo.appendChild(vazio("🏃", "Nenhum treino registrado. O treino é diário, às 17h40."));
      return;
    }
    const tb = el("table", { class: "tb" }, [
      el("thead", {}, [el("tr", {}, [
        el("th", { texto: "Data" }),
        el("th", { class: "cen", texto: "Corrida 2.400 m (min)" }),
        el("th", { class: "cen", texto: "Natação 50 m (s)" }),
        el("th", { class: "cen", texto: "Barra" }), el("th", { class: "cen", texto: "Abdominais" }),
        el("th", { class: "cen", texto: "Flexões" }), el("th", { class: "cen", texto: "Peso (kg)" }),
        el("th", { class: "cen", texto: "No índice?" }), el("th", { texto: "Observações" }), el("th"),
      ])]),
    ]);
    const tbody = el("tbody");
    for (const t of estado.taf) {
      const set = (c) => (v) => { mudar((st) => {
        const a = st.taf.find((x) => x.id === t.id); if (a) a[c] = v;
      }); if (c === "corrida" || c === "natacao") pintar(); };

      const co = num(t.corrida), na = num(t.natacao);
      const okC = co !== null && co <= metaCorrida;
      const okN = na !== null && na <= metaNatacao;

      tbody.appendChild(el("tr", {}, [
        el("td", {}, [campoEditavel({ valor: t.data, tipo: "date", ao: set("data") })]),
        el("td", { class: "cen", estilo: co === null ? {} : (okC ? { background: "var(--ok-bg)" } : { background: "var(--bad-bg)" }) },
          [campoEditavel({ valor: t.corrida, tipo: "number", passo: "0.01", largura: "mini", ao: set("corrida"), placeholder: "13,75" })]),
        el("td", { class: "cen", estilo: na === null ? {} : (okN ? { background: "var(--ok-bg)" } : { background: "var(--bad-bg)" }) },
          [campoEditavel({ valor: t.natacao, tipo: "number", largura: "mini", ao: set("natacao"), placeholder: "88" })]),
        el("td", { class: "cen" }, [campoEditavel({ valor: t.barra, tipo: "number", largura: "mini", ao: set("barra") })]),
        el("td", { class: "cen" }, [campoEditavel({ valor: t.abdominais, tipo: "number", largura: "mini", ao: set("abdominais") })]),
        el("td", { class: "cen" }, [campoEditavel({ valor: t.flexoes, tipo: "number", largura: "mini", ao: set("flexoes") })]),
        el("td", { class: "cen" }, [campoEditavel({ valor: t.peso, tipo: "number", passo: "0.1", largura: "mini", ao: set("peso") })]),
        el("td", { class: "cen" }, [
          co === null && na === null ? el("span", { texto: "—" })
            : el("span", {}, [
                okC ? chip("corrida", "ok") : (co !== null ? chip("corrida", "bad") : null),
                " ",
                okN ? chip("natação", "ok") : (na !== null ? chip("natação", "bad") : null),
              ]),
        ]),
        el("td", {}, [campoEditavel({ valor: t.obs, ao: set("obs") })]),
        el("td", {}, [botaoApagar(() => { mudar((st) => { st.taf = st.taf.filter((x) => x.id !== t.id); }); pintar(); })]),
      ]));
    }
    tb.appendChild(tbody);
    corpo.appendChild(el("div", { class: "tabela-wrap" }, [tb]));

    const corridas = estado.taf.map((t) => num(t.corrida)).filter((x) => x !== null);
    const natacoes = estado.taf.map((t) => num(t.natacao)).filter((x) => x !== null);
    corpo.appendChild(el("div", { estilo: { padding: "12px 16px", borderTop: "1px solid var(--line)", display: "flex", gap: "20px", flexWrap: "wrap", fontSize: "13px" } }, [
      el("span", {}, ["Melhor corrida: ", el("b", { texto: corridas.length ? n2.format(Math.min(...corridas)) + " min" : "—" })]),
      el("span", {}, ["Melhor natação: ", el("b", { texto: natacoes.length ? Math.min(...natacoes) + " s" : "—" })]),
      corridas.length && natacoes.length && Math.min(...corridas) <= metaCorrida && Math.min(...natacoes) <= metaNatacao
        ? chip("Os dois índices já batidos — agora é manter", "ok")
        : chip("Ainda falta bater pelo menos um índice"),
    ]));
  }

  frag.appendChild(el("div", { class: "aviso" }, [
    el("div", {}, [
      el("b", { texto: "O TAF elimina tanto quanto a prova escrita" }),
      `Índices mínimos da EAM: correr 2.400 m em até ${n2.format(metaCorrida)} min (14 min 30 s) e nadar 50 m em até ${metaNatacao} s. ` +
      "Tempo de corrida em número decimal: 13,75 = 13 min 45 s.",
    ]),
  ]));
  frag.appendChild(cartao("Treinos", null, [corpo], [botaoNovo("Novo treino", novo)], true));
  pintar();
  return frag;
}
