# -*- coding: utf-8 -*-
"""Parte 2 do gerador: continua gerar_v2.py (compartilha o mesmo workbook)."""
import os, io
_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gerar_v2.py")
exec(compile(io.open(_base, encoding="utf-8").read(), _base, "exec"), globals())

# ═══════════════════════════════════════════════════ 4 · PLANO MENSAL
wm = wb.create_sheet("PLANO MENSAL")
wm.sheet_properties.tabColor = "9F6E00"
NC = 8
for j, w in enumerate([2.5, 10, 18, 60, 32, 12, 11, 2.5], 1):
    wm.column_dimensions[get_column_letter(j)].width = w
r = band(wm, 1, NC, "  PLANO MENSAL  ·  AGO/2026 → JUL/2027",
         "  Leia no primeiro dia de cada mês. É isto que preenche os blocos da tarde e da noite na GRADE SEMANAL.")
back(wm, NC)
r += 1
mg(wm, r, 2, r, 7)
st(wm.cell(r, 2, "Se o curso estiver em outro assunto naquele mês, o curso manda: a revisão das 12h sempre acompanha a aula do dia. "
                 "Este plano rege os blocos da tarde e da noite, que são seus."),
   sz=8.5, i=True, fg=INK2, bg=NEU_BG, wrap=True)
wm.row_dimensions[r].height = 26
r += 2

MESES = [
 ("Ago/26", "FASE 1 · BASE", "Montar a rotina e não quebrar. Meta: 4 semanas cheias sem furo.", [
  ("Matemática", "Conjuntos numéricos, operações, MMC e MDC, razão e proporção, regra de três, porcentagem e juros", "300 questões de aritmética"),
  ("Português", "Interpretação de texto, tipologia e gêneros textuais, coesão e coerência", "2 textos comentados por semana"),
  ("Física", "Grandezas e unidades (SI), notação científica, cinemática escalar (MU e MUV), gráficos do movimento", "Dominar os gráficos s×t e v×t"),
  ("Química", "Matéria e energia, estados físicos, propriedades, misturas e separação de misturas", "Tabela dos métodos de separação"),
  ("História", "Povos indígenas, período pré-colonial, expansão marítima, administração colonial", "Linha do tempo 1500–1600"),
  ("Geografia", "Posição geográfica, limites e fronteiras, fusos horários, cartografia", "30 questões de fuso horário"),
  ("Literatura", "Introdução à literatura, gêneros literários, figuras de linguagem, versificação", "Fichar as 15 figuras principais"),
  ("Redação", "Estrutura do dissertativo-argumentativo; tese e delimitação do tema", "4 redações — uma por semana"),
  ("Inglês", "Nouns, articles, simple present, vocabulário de rotina", "Diagnóstico: uma prova antiga")]),
 ("Set/26", "FASE 1 · BASE", "Primeiro simulado completo no último sábado do mês.", [
  ("Matemática", "Equações e inequações de 1º e 2º grau; funções: domínio, imagem e gráfico; função afim", "Zerar equações do 2º grau"),
  ("Português", "Fonética e fonologia, ortografia oficial, Acordo de 1990, acentuação gráfica", "Lista de 100 palavras-armadilha"),
  ("Física", "Queda livre, lançamento vertical, cinemática vetorial, lançamentos e MCU", "150 questões de cinemática"),
  ("Química", "Ar atmosférico e água — os dois tópicos citados literalmente no edital da EAM", "Resumo de uma página de cada"),
  ("História", "Economia açucareira e escravidão, invasões holandesas, entradas e bandeiras", "Mapa da expansão territorial"),
  ("Geografia", "Estrutura geológica, relevo brasileiro, clima e massas de ar", "Desenhar o relevo de memória"),
  ("Literatura", "Trovadorismo, Humanismo, Classicismo e Quinhentismo", "Quadro-resumo por escola"),
  ("Redação", "Parágrafo de introdução; construção do argumento", "4 redações"),
  ("Inglês", "Pronouns, adjectives and adverbs, comparative and superlative", "30 questões")]),
 ("Out/26", "FASE 1 · BASE", "Começa a revisão espaçada dos tópicos de agosto (30 dias).", [
  ("Matemática", "Função quadrática, função modular e função exponencial", "Gráficos sem calculadora"),
  ("Português", "Estrutura e formação de palavras; substantivo, adjetivo, artigo, numeral e pronome", "Classificação em 200 questões"),
  ("Física", "Leis de Newton e aplicações: atrito, plano inclinado, tração e sistemas de blocos", "Diagrama de corpo livre automático"),
  ("Química", "Modelos atômicos, estrutura do átomo, semelhanças atômicas, distribuição eletrônica", "Pauling de cor"),
  ("História", "Mineração, tratados de limites e rebeliões nativistas", "Quadro das revoltas: causa e efeito"),
  ("Geografia", "Vegetação, domínios morfoclimáticos, hidrografia e questões ambientais", "Mapa dos 6 domínios"),
  ("Literatura", "Barroco e Arcadismo", "Gregório de Matos e Tomás A. Gonzaga"),
  ("Redação", "Repertório sociocultural: montar um banco de 20 repertórios", "Banco pronto + 4 redações"),
  ("Inglês", "Simple past, past continuous, present perfect", "30 questões")]),
 ("Nov/26", "FASE 1 · BASE", "Fechar a primeira passada das exatas.", [
  ("Matemática", "Logaritmos e função logarítmica; sequências, PA e PG", "200 questões de PA e PG"),
  ("Português", "Verbo: conjugação, tempos, modos e vozes; advérbio, preposição, conjunção", "Verbo é campeão de questões"),
  ("Física", "Trabalho, potência, energia e conservação; impulso, quantidade de movimento e colisões", "150 questões de energia"),
  ("Química", "Tabela periódica: organização e propriedades periódicas", "Prever propriedades sem consultar"),
  ("História", "Movimentos pró-independência, período joanino e Independência de 1822", "Ligar 1808 → 1822 → 1824"),
  ("Geografia", "Formação do território, regionalização (IBGE e geoeconômica), industrialização", "Comparar as duas regionalizações"),
  ("Literatura", "Romantismo: poesia (3 gerações) e prosa", "Alencar, Álvares de Azevedo, Castro Alves"),
  ("Redação", "Conclusão e proposta de intervenção; coesão e conectivos", "4 redações"),
  ("Inglês", "Past perfect e formas de futuro (will / going to)", "30 questões")]),
 ("Dez/26", "FASE 2 · APROFUNDAR", "Todo exercício passa a vir de prova anterior. Recesso do curso: use o PLANO SEM CURSO.", [
  ("Matemática", "Trigonometria: triângulo retângulo, ciclo, funções, leis dos senos e cossenos", "Ciclo trigonométrico decorado"),
  ("Português", "Sintaxe I: termos essenciais, integrantes e acessórios; período simples", "Analisar 100 períodos"),
  ("Física", "Estática e hidrostática (pressão, Pascal, Arquimedes)", "Cai muito na EAM, por contexto naval"),
  ("Química", "Ligações iônica, covalente e metálica; geometria molecular e polaridade", "Prever geometria e polaridade"),
  ("História", "Primeiro Reinado, Confederação do Equador, Período Regencial e revoltas", "Quadro das 4 revoltas regenciais"),
  ("Geografia", "Agricultura, pecuária, agronegócio, extrativismo e recursos minerais", "Mapa da produção por região"),
  ("Literatura", "Realismo e Naturalismo: Machado de Assis e Aluísio Azevedo", "Fichar Dom Casmurro e O Cortiço"),
  ("Redação", "Norma culta aplicada e gestão de tempo: rascunho em 15 min", "4 redações cronometradas"),
  ("Inglês", "Modal verbs; prepositions of time, place and movement", "30 questões")]),
 ("Jan/27", "FASE 2 · APROFUNDAR", "EDITAL DA EAM PREVISTO. Conferir o conteúdo oficial e ajustar esta planilha.", [
  ("Matemática", "Análise combinatória e probabilidade", "200 questões"),
  ("Português", "Sintaxe II: período composto por coordenação e por subordinação", "Classificar 150 orações"),
  ("Física", "Termologia: escalas, dilatação, calorimetria, mudanças de estado e gases", "150 questões"),
  ("Química", "Funções inorgânicas: ácidos, bases, sais e óxidos", "Nomear 100 compostos"),
  ("História", "Segundo Reinado: café, Guerra do Paraguai, abolição e crise do Império", "Guerra do Paraguai cai muito"),
  ("Geografia", "Energia e matriz energética; transportes; comércio exterior", "Matriz energética atualizada"),
  ("Literatura", "Parnasianismo e Simbolismo", "Olavo Bilac e Cruz e Sousa"),
  ("Redação", "Temas militares e de atualidades, cronometrado em 60 min", "4 redações"),
  ("Inglês", "Conjunctions, linking words e reading comprehension", "30 questões")]),
 ("Fev/27", "FASE 3 · RETA EAM", "APLICAR O AJUSTE DA FASE 3 NA GRADE. Simulado no formato EAM toda semana.", [
  ("Matemática", "Matrizes, determinantes e sistemas lineares", "150 questões"),
  ("Português", "Concordância nominal e verbal; regência; crase", "Os três assuntos mais cobrados"),
  ("Física", "Óptica geométrica (espelhos e lentes) e ondulatória", "150 questões"),
  ("Química", "Reações químicas: tipos e balanceamento", "Balancear 100 reações"),
  ("História", "Manutenção — só flashcards", "3 revisões por semana"),
  ("Geografia", "Manutenção — só flashcards", "3 revisões por semana"),
  ("Literatura", "Manutenção — só flashcards", "2 revisões por semana"),
  ("Redação", "Uma redação por semana para não perder a mão", "4 redações"),
  ("Inglês", "Reading comprehension com textos de prova da EAM", "Uma prova antiga por semana")]),
 ("Mar/27", "FASE 3 · RETA EAM", "EDITAL DA ESA PREVISTO. Confirmar a inscrição na EAM.", [
  ("Matemática", "Geometria plana completa: Tales, semelhança, relações métricas, polígonos, círculo e áreas", "O bloco mais cobrado na EAM"),
  ("Português", "Colocação pronominal, pontuação e semântica", "150 questões"),
  ("Física", "Acústica, eletrostática e eletrodinâmica (Ohm, resistores, circuitos, potência)", "200 questões"),
  ("Química", "Mol, estequiometria, soluções e concentrações", "150 questões"),
  ("História", "Manutenção — flashcards", "2 revisões por semana"),
  ("Geografia", "Manutenção — flashcards", "2 revisões por semana"),
  ("Literatura", "Manutenção — flashcards", "2 revisões por semana"),
  ("Redação", "Uma redação por semana", "4 redações"),
  ("Inglês", "Vocabulário náutico e militar; revisão de grammar", "Uma prova antiga por semana")]),
 ("Abr/27", "FASE 3 · PICO EAM", "PROVA DA EAM NO FIM DO MÊS. Nada de assunto novo depois do dia 10.", [
  ("Matemática", "Geometria espacial (prismas, pirâmides, cilindros, cones, esferas) + REVISÃO GERAL", "10 provas anteriores completas"),
  ("Português", "REVISÃO GERAL: refazer o caderno de erros inteiro + 5 provas da EAM", "Zerar o caderno de erros"),
  ("Física", "Magnetismo e eletromagnetismo + REVISÃO GERAL de toda a Física", "10 provas anteriores"),
  ("Química", "REVISÃO GERAL de toda a Química + provas anteriores", "10 provas anteriores"),
  ("História", "Congelado até a prova da EAM", "—"),
  ("Geografia", "Congelado até a prova da EAM", "—"),
  ("Literatura", "Congelado até a prova da EAM", "—"),
  ("Redação", "Congelado (não cai na EAM). Retomar no dia seguinte à prova", "—"),
  ("Inglês", "Revisão de grammar + 10 provas anteriores da EAM", "10 provas")]),
 ("Mai/27", "FASE 4 · VIRADA ESA", "APLICAR O AJUSTE DA FASE 4. Física e Química saem da grade. Inscrição na ESA.", [
  ("Matemática", "Exclusivos da ESA: polinômios, equações polinomiais, números complexos, binômio de Newton, geometria analítica", "200 questões"),
  ("Português", "Figuras de linguagem, versificação, funções da linguagem e variedades linguísticas", "Exclusivos da ESA"),
  ("Física", "FORA DA GRADE — não cai na ESA", "—"),
  ("Química", "FORA DA GRADE — não cai na ESA", "—"),
  ("História", "Era Vargas, Brasil na 2ª Guerra e a FEB, República Populista", "A FEB cai muito na ESA"),
  ("Geografia", "Demografia, migrações, urbanização, mercado de trabalho e IDH", "150 questões"),
  ("Literatura", "Modernismo: 1ª fase (Semana de 22) e 2ª fase", "Quadro por fase e autor"),
  ("Redação", "Duas redações por semana, com correção rigorosa", "8 redações"),
  ("Inglês", "INTENSIVO — vale 10 questões: reading, conditionals e passive voice", "Uma prova antiga por semana")]),
 ("Jun/27", "FASE 4 · VIRADA ESA", "Simulado no formato ESA toda semana.", [
  ("Matemática", "REVISÃO GERAL + 10 provas anteriores da ESA", "Acerto acima de 75%"),
  ("Português", "REVISÃO GERAL da gramática + 10 provas da ESA", "Acerto acima de 75%"),
  ("Física", "FORA DA GRADE", "—"),
  ("Química", "FORA DA GRADE", "—"),
  ("História", "Regime Militar, Nova República e Brasil contemporâneo + revisão cronológica", "Linha do tempo 1500 até hoje"),
  ("Geografia", "Geopolítica, Amazônia e fronteiras + revisão geral", "Acerto acima de 75%"),
  ("Literatura", "Modernismo 3ª fase e contemporânea + revisão", "Quadro-resumo completo"),
  ("Redação", "Duas redações por semana; foco na proposta de intervenção", "8 redações"),
  ("Inglês", "10 provas anteriores da ESA", "Acerto acima de 70%")]),
 ("Jul/27", "FASE 5 · PICO ESA", "PROVA DA ESA NO FIM DO MÊS. Zero assunto novo — só revisão, questões e ritmo.", [
  ("Matemática", "Refazer o caderno de erros + 2 simulados por semana", "Acerto acima de 80%"),
  ("Português", "Refazer o caderno de erros + 2 simulados por semana", "Acerto acima de 80%"),
  ("Física", "FORA DA GRADE", "—"),
  ("Química", "FORA DA GRADE", "—"),
  ("História", "Revisão relâmpago por flashcards, todo dia", "Ciclo completo a cada 3 dias"),
  ("Geografia", "Revisão relâmpago por flashcards, todo dia", "Ciclo completo a cada 3 dias"),
  ("Literatura", "Revisão relâmpago por flashcards, todo dia", "Ciclo completo a cada 3 dias"),
  ("Redação", "Duas por semana até a semana da prova", "Nota estável acima de 7,0"),
  ("Inglês", "Revisão de grammar + um texto por dia", "Manter o ritmo de leitura")]),
]

r = thead(wm, r, ["", "MÊS", "MATÉRIA", "O QUE ESTUDAR NESTE MÊS", "META DO MÊS", "STATUS", "% FEITO", ""], h=24)
pm0 = r
for mes, fase, marco, itens in MESES:
    pico = "PICO" in fase
    mg(wm, r, 1, r, 8)
    st(wm.cell(r, 1, f"    {mes}   ·   {fase}   ·   {marco}"), b=True, sz=10,
       fg="FFFFFF", bg=BAD_FG if pico else NAVY)
    wm.row_dimensions[r].height = 23
    r += 1
    for mat, cont, meta in itens:
        fam, bar, t1, t2, ink = SUB[mat]
        fora = cont.startswith(("FORA DA GRADE", "Congelado", "Manutenção"))
        st(wm.cell(r, 1, None), bg=bar)
        st(wm.cell(r, 2, mes), sz=8, ha="center", bg=CARD, fg=INK3)
        st(wm.cell(r, 3, mat), b=True, sz=9, fg=ink, bg=t1)
        st(wm.cell(r, 4, cont), sz=8.5, wrap=True, bg=CARD, fg=INK3 if fora else INK, i=fora)
        st(wm.cell(r, 5, meta), sz=8.5, i=True, wrap=True, bg=CARD, fg=INK3)
        st(wm.cell(r, 6, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG)
        st(wm.cell(r, 7, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="0%")
        wm.row_dimensions[r].height = 26
        r += 1
pm1 = r - 1
dv = DataValidation(type="list", formula1='"Não iniciado,Em andamento,Concluído,Atrasado"', allow_blank=True)
wm.add_data_validation(dv); dv.add(f"F{pm0}:F{pm1}")
wm.conditional_formatting.add(f"F{pm0}:F{pm1}", CellIsRule(operator="equal", formula=['"Concluído"'],
    fill=PatternFill("solid", fgColor=OK_BG), font=Font(name=FT, bold=True, color=OK_FG)))
wm.conditional_formatting.add(f"F{pm0}:F{pm1}", CellIsRule(operator="equal", formula=['"Atrasado"'],
    fill=PatternFill("solid", fgColor=BAD_BG), font=Font(name=FT, bold=True, color=BAD_FG)))
wm.conditional_formatting.add(f"G{pm0}:G{pm1}",
    DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="1A51BD", showValue=True))
wm.freeze_panes = "D5"
wm.auto_filter.ref = f"B{pm0-1}:G{pm1}"
finish(wm, NC, 90)

# ═══════════════════════════════════════════ 5 · CONTEÚDO E REVISÃO
wc = wb.create_sheet("CONTEÚDO E REVISÃO")
wc.sheet_properties.tabColor = "0C7E65"
NC = 16
for j, w in enumerate([2.5, 12, 22, 50, 9, 7, 10, 13, 11, 11, 11, 11, 10, 9, 28, 2.5], 1):
    wc.column_dimensions[get_column_letter(j)].width = w
r = band(wc, 1, NC, "  CONTEÚDO PROGRAMÁTICO  +  REVISÃO ESPAÇADA",
         "  Só as colunas claras são suas. Preencha a data em que estudou e as três revisões aparecem sozinhas.")
back(wc, NC)
r += 1
r = thead(wc, r, ["", "Matéria", "Unidade", "Tópico", "Prova", "Prior.", "Mês previsto", "Status",
                  "Data em que\nestudei", "Revisão 1\n(+1 dia)", "Revisão 2\n(+7 dias)", "Revisão 3\n(+30 dias)",
                  "Confiança\n1 a 5", "% acerto", "Observações e erros que se repetem", ""], h=34)

TOP = []
def add(mat, uni, lst, prova, prior, mes):
    for t in lst:
        TOP.append((mat, uni, t, prova, prior, mes))

add("Matemática", "Aritmética e conjuntos", [
 "Noções de conjuntos, operações e diagramas; raciocínio lógico",
 "Conjuntos numéricos (N, Z, Q, I, R) e propriedades",
 "Operações, potenciação, radiciação; MMC e MDC",
 "Razão, proporção e regra de três simples e composta",
 "Porcentagem, juros simples e juros compostos"], "AMBAS", 1, "Ago/26")
add("Matemática", "Álgebra", [
 "Equações e inequações do 1º grau", "Equações e inequações do 2º grau",
 "Funções: definição, domínio, imagem e gráfico", "Função afim (linear)",
 "Função quadrática"], "AMBAS", 1, "Set/26")
add("Matemática", "Álgebra", ["Função modular"], "ESA", 2, "Out/26")
add("Matemática", "Álgebra", ["Função exponencial e equações exponenciais",
 "Logaritmos: definição, propriedades e função logarítmica"], "AMBAS", 1, "Out/26")
add("Matemática", "Sequências", ["Sequências numéricas e progressão aritmética (PA)",
 "Progressão geométrica (PG) e soma dos termos"], "AMBAS", 1, "Nov/26")
add("Matemática", "Trigonometria", ["Trigonometria no triângulo retângulo",
 "Ciclo trigonométrico, arcos e redução ao 1º quadrante",
 "Funções e equações trigonométricas", "Leis dos senos e dos cossenos"], "AMBAS", 1, "Dez/26")
add("Matemática", "Contagem", ["Análise combinatória: princípio fundamental, arranjo, permutação e combinação",
 "Probabilidade: eventos, união, intersecção e condicional"], "AMBAS", 1, "Jan/27")
add("Matemática", "Contagem", ["Binômio de Newton"], "ESA", 3, "Mai/27")
add("Matemática", "Álgebra linear", ["Matrizes: tipos e operações", "Determinantes e propriedades",
 "Sistemas lineares e escalonamento"], "AMBAS", 2, "Fev/27")
add("Matemática", "Geometria plana", ["Ângulos, retas paralelas e Teorema de Tales",
 "Triângulos: congruência, semelhança e relações métricas",
 "Quadriláteros e polígonos regulares", "Circunferência e círculo",
 "Áreas de figuras planas"], "AMBAS", 1, "Mar/27")
add("Matemática", "Geometria espacial", ["Geometria espacial de posição (retas e planos)"], "ESA", 2, "Mai/27")
add("Matemática", "Geometria espacial", ["Prismas e cubos: área e volume", "Pirâmides: área e volume",
 "Cilindros, cones e esferas: área e volume"], "AMBAS", 1, "Abr/27")
add("Matemática", "Geometria analítica", ["Ponto e reta no plano cartesiano",
 "Circunferência e seções cônicas"], "AMBAS", 2, "Mai/27")
add("Matemática", "Polinômios", ["Polinômios: operações e teorema do resto",
 "Equações polinomiais e relações de Girard", "Números complexos"], "ESA", 3, "Mai/27")
add("Matemática", "Estatística", ["Estatística básica: média, moda, mediana e gráficos"], "AMBAS", 2, "Jan/27")

add("Português", "Texto", ["Leitura, interpretação e análise de textos",
 "Tipologia e gêneros textuais; tipos de discurso", "Coesão e coerência textual",
 "Variedades linguísticas e funções da linguagem"], "AMBAS", 1, "Ago/26")
add("Português", "Fonologia e ortografia", ["Fonética e fonologia: encontros vocálicos, consonantais e dígrafos",
 "Ortografia oficial e Acordo Ortográfico de 1990", "Acentuação gráfica"], "AMBAS", 1, "Set/26")
add("Português", "Morfologia", ["Estrutura e formação de palavras", "Substantivo e adjetivo",
 "Artigo, numeral e pronome", "Verbo: conjugação, tempos, modos e vozes",
 "Advérbio, preposição, conjunção e interjeição"], "AMBAS", 1, "Out/26")
add("Português", "Sintaxe", ["Termos essenciais da oração: sujeito e predicado",
 "Termos integrantes e acessórios: complementos, adjuntos, aposto e vocativo",
 "Período composto por coordenação",
 "Período composto por subordinação: substantivas, adjetivas e adverbiais"], "AMBAS", 1, "Dez/26")
add("Português", "Morfossintaxe", ["Concordância nominal", "Concordância verbal",
 "Regência nominal e verbal", "Crase", "Colocação pronominal", "Pontuação"], "AMBAS", 1, "Fev/27")
add("Português", "Semântica e estilística", ["Semântica: sinonímia, antonímia, polissemia e ambiguidade",
 "Figuras de linguagem"], "AMBAS", 2, "Mar/27")
add("Português", "Estilística", ["Noções de versificação: metrificação, rima e estrofe"], "ESA", 3, "Mai/27")

add("Literatura", "Origens", ["Introdução à literatura e gêneros literários",
 "Trovadorismo e Humanismo", "Classicismo e Quinhentismo (literatura de informação)"], "ESA", 3, "Ago/26")
add("Literatura", "Séculos XVII–XVIII", ["Barroco: Gregório de Matos e Padre Antônio Vieira",
 "Arcadismo: Cláudio Manuel da Costa e Tomás Antônio Gonzaga"], "ESA", 3, "Out/26")
add("Literatura", "Século XIX", ["Romantismo — poesia: as três gerações",
 "Romantismo — prosa: José de Alencar e Manuel Antônio de Almeida",
 "Realismo e Naturalismo: Machado de Assis e Aluísio Azevedo",
 "Parnasianismo: Olavo Bilac", "Simbolismo: Cruz e Sousa"], "ESA", 2, "Nov/26")
add("Literatura", "Século XX", ["Pré-Modernismo: Euclides da Cunha, Lima Barreto e Monteiro Lobato",
 "Modernismo 1ª fase: Semana de 22, Mário e Oswald de Andrade",
 "Modernismo 2ª fase — poesia: Drummond, Cecília Meireles, Vinicius de Moraes",
 "Modernismo 2ª fase — prosa regionalista: Graciliano Ramos, Jorge Amado, Rachel de Queiroz",
 "Modernismo 3ª fase: Guimarães Rosa, Clarice Lispector e João Cabral",
 "Literatura contemporânea"], "ESA", 2, "Mai/27")

add("Redação", "Técnica", ["Estrutura do texto dissertativo-argumentativo",
 "Delimitação do tema e construção da tese", "Parágrafo de introdução",
 "Parágrafos de desenvolvimento e tipos de argumento",
 "Repertório sociocultural e dados de apoio", "Conclusão e proposta de intervenção",
 "Coesão: conectivos e referenciação", "Norma culta aplicada: erros que derrubam a nota",
 "Gestão de tempo: rascunho e revisão em 60 minutos",
 "Temas recorrentes: cidadania, Forças Armadas, tecnologia e meio ambiente"], "ESA", 1, "Ago/26")

add("História", "Brasil Colônia", ["Povos indígenas e período pré-colonial",
 "Expansão marítima e a chegada dos portugueses",
 "Administração colonial: capitanias hereditárias e governo-geral",
 "Economia açucareira e escravidão", "Invasões estrangeiras: holandeses e franceses",
 "Entradas, bandeiras e expansão territorial", "Mineração e sociedade mineradora",
 "Tratados de limites e consolidação do território",
 "Rebeliões nativistas: Beckman, Emboabas, Mascates e Vila Rica",
 "Movimentos pró-independência: Inconfidência Mineira e Conjuração Baiana"], "ESA", 2, "Ago/26")
add("História", "Brasil Império", ["Período joanino e a vinda da Corte (1808)",
 "Independência do Brasil (1822) e a Constituição de 1824",
 "Primeiro Reinado e a Confederação do Equador",
 "Período Regencial: Cabanagem, Sabinada, Balaiada e Farroupilha",
 "Segundo Reinado: política e economia cafeeira", "Guerra do Paraguai",
 "Abolição da escravidão e crise do Império"], "ESA", 2, "Dez/26")
add("História", "Brasil República", ["Proclamação da República e República da Espada",
 "República Oligárquica: coronelismo, política dos governadores e revoltas",
 "Revolução de 1930 e Era Vargas (1930–1945)",
 "Brasil na Segunda Guerra Mundial e a Força Expedicionária Brasileira",
 "República Populista (1945–1964)", "Regime Militar (1964–1985)",
 "Nova República e Brasil contemporâneo"], "ESA", 2, "Mai/27")

add("Geografia", "Espaço natural", ["Posição geográfica, limites e fronteiras do Brasil", "Fusos horários",
 "Cartografia: escalas, projeções e coordenadas", "Estrutura geológica e relevo brasileiro",
 "Clima do Brasil e massas de ar", "Vegetação e domínios morfoclimáticos",
 "Hidrografia e bacias hidrográficas", "Questões ambientais e unidades de conservação"], "ESA", 2, "Ago/26")
add("Geografia", "Espaço econômico", ["Formação do território e regionalização (IBGE e geoeconômica)",
 "Industrialização brasileira e polos industriais", "Agricultura, pecuária e agronegócio",
 "Extrativismo e recursos minerais", "Fontes de energia e matriz energética",
 "Transportes e infraestrutura", "Comércio exterior e blocos econômicos"], "ESA", 2, "Nov/26")
add("Geografia", "Espaço político", ["Estrutura administrativa e organização política do Brasil",
 "Geopolítica brasileira, Amazônia e faixa de fronteira"], "ESA", 2, "Fev/27")
add("Geografia", "Espaço humano", ["Demografia: crescimento, estrutura etária e IDH",
 "Migrações internas e externas", "Urbanização e rede urbana",
 "Mercado de trabalho e desigualdade social"], "ESA", 2, "Mai/27")

add("Física", "Introdução e cinemática", ["Grandezas físicas, unidades do SI e notação científica",
 "Cinemática escalar: movimento uniforme e uniformemente variado",
 "Gráficos do movimento (s×t, v×t, a×t)", "Queda livre e lançamento vertical",
 "Cinemática vetorial; lançamento horizontal e oblíquo", "Movimento circular uniforme"], "EAM", 1, "Ago/26")
add("Física", "Dinâmica", ["Leis de Newton",
 "Aplicações: força de atrito, plano inclinado, tração e sistemas de blocos",
 "Trabalho e potência", "Energia cinética, potencial e conservação de energia",
 "Impulso, quantidade de movimento e colisões"], "EAM", 1, "Out/26")
add("Física", "Estática e hidrostática", ["Estática do ponto material e do corpo extenso",
 "Hidrostática: pressão, princípio de Pascal e princípio de Arquimedes"], "EAM", 1, "Dez/26")
add("Física", "Termologia", ["Escalas termométricas e dilatação", "Calorimetria e mudanças de estado",
 "Estudo dos gases e noções de termodinâmica"], "EAM", 1, "Jan/27")
add("Física", "Óptica e ondas", ["Óptica geométrica: reflexão e espelhos planos e esféricos",
 "Refração e lentes", "Ondulatória: características e fenômenos ondulatórios",
 "Acústica: qualidades do som e efeito Doppler"], "EAM", 1, "Fev/27")
add("Física", "Eletricidade e magnetismo", ["Eletrostática: eletrização, Lei de Coulomb e campo elétrico",
 "Eletrodinâmica: corrente, Leis de Ohm e resistores",
 "Circuitos elétricos, potência e consumo de energia",
 "Magnetismo: ímãs, campo magnético e eletromagnetismo"], "EAM", 1, "Mar/27")

add("Química", "Fundamentos", ["Matéria e energia; estados físicos e mudanças de estado",
 "Propriedades da matéria e transformações físicas e químicas",
 "Substâncias puras e misturas", "Processos de separação de misturas"], "EAM", 1, "Ago/26")
add("Química", "Ar e água", ["Ar atmosférico: composição, camadas e poluição",
 "Água: propriedades, tratamento e poluição"], "EAM", 1, "Set/26")
add("Química", "Atomística", ["Modelos atômicos: de Dalton a Rutherford-Bohr",
 "Estrutura do átomo; número atômico e número de massa",
 "Semelhanças atômicas: isótopos, isóbaros e isótonos",
 "Distribuição eletrônica (diagrama de Linus Pauling)"], "EAM", 1, "Out/26")
add("Química", "Tabela periódica", ["Tabela periódica: organização e classificação dos elementos",
 "Propriedades periódicas e aperiódicas"], "EAM", 1, "Nov/26")
add("Química", "Ligações", ["Ligação iônica", "Ligação covalente e geometria molecular",
 "Ligação metálica; polaridade e forças intermoleculares"], "EAM", 1, "Dez/26")
add("Química", "Funções inorgânicas", ["Ácidos: classificação, nomenclatura e propriedades",
 "Bases: classificação, nomenclatura e propriedades",
 "Sais e óxidos: classificação e nomenclatura"], "EAM", 1, "Jan/27")
add("Química", "Reações e cálculos", ["Reações químicas: tipos e balanceamento",
 "Massa atômica, massa molecular e conceito de mol", "Estequiometria",
 "Soluções e concentrações"], "EAM", 1, "Mar/27")

add("Inglês", "Reading", ["Reading comprehension: textos curtos e médios",
 "Vocabulário: rotina, esportes, roupas, alimentos, números e datas",
 "Vocabulário náutico e militar"], "AMBAS", 2, "Ago/26")
add("Inglês", "Grammar", ["Nouns: plural, countable and uncountable, genitive case",
 "Articles (a, an, the)", "Pronouns: personal, possessive, reflexive and relative",
 "Adjectives and adverbs; comparative and superlative"], "AMBAS", 2, "Set/26")
add("Inglês", "Verb tenses", ["Simple present and present continuous",
 "Simple past and past continuous", "Present perfect and past perfect",
 "Future forms: will and going to", "Modal verbs"], "AMBAS", 2, "Out/26")
add("Inglês", "Estruturas", ["Prepositions of time, place and movement",
 "Conjunctions and linking words"], "AMBAS", 2, "Dez/26")
add("Inglês", "Estruturas", ["Conditional sentences (if clauses)", "Passive voice"], "ESA", 3, "Mai/27")

PROVA_TAG = {"AMBAS": ("D1DCF2", "0244BE"), "EAM": ("CEE5E0", "01614D"), "ESA": ("E5DDCC", "6D4B04")}
ct0 = r
for i, (mat, uni, top, prova, prior, mes) in enumerate(TOP, 1):
    fam, bar, t1, t2, ink = SUB[mat]
    zeb = CARD if i % 2 else "FBFCFD"
    st(wc.cell(r, 1, None), bg=bar)
    st(wc.cell(r, 2, mat), b=True, sz=8.5, fg=ink, bg=t1)
    st(wc.cell(r, 3, uni), sz=8, fg=INK2, bg=zeb, wrap=True)
    st(wc.cell(r, 4, top), sz=8.5, bg=zeb, wrap=True)
    pbg, pfg = PROVA_TAG[prova]
    st(wc.cell(r, 5, prova), b=True, sz=7.5, ha="center", bg=pbg, fg=pfg)
    st(wc.cell(r, 6, prior), b=True, sz=8.5, ha="center", bg=zeb, fg=INK2)
    st(wc.cell(r, 7, mes), sz=8, ha="center", bg=zeb, fg=INK3)
    st(wc.cell(r, 8, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG)
    st(wc.cell(r, 9, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="DD/MM/YYYY")
    for k, dias in ((10, 1), (11, 7), (12, 30)):
        st(wc.cell(r, k, f'=IF($I{r}="","",$I{r}+{dias})'), sz=8.5, ha="center", bg=zeb, fmt="DD/MM/YYYY")
    st(wc.cell(r, 13, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG)
    st(wc.cell(r, 14, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="0%")
    st(wc.cell(r, 15, None), sz=8.5, bg=INPUT_BG, fg=INPUT_FG, wrap=True)
    wc.row_dimensions[r].height = 21
    r += 1
ct1 = r - 1

dv2 = DataValidation(type="list", formula1='"Não iniciado,Em andamento,Concluído,Revisado"', allow_blank=True)
wc.add_data_validation(dv2); dv2.add(f"H{ct0}:H{ct1}")
dv3 = DataValidation(type="whole", operator="between", formula1=1, formula2=5, allow_blank=True)
wc.add_data_validation(dv3); dv3.add(f"M{ct0}:M{ct1}")
for val, bg, fg in (("Concluído", OK_BG, OK_FG), ("Revisado", "CFE8D8", OK_FG),
                    ("Em andamento", "E9EEF6", NAVY2), ("Não iniciado", NEU_BG, NEU_FG)):
    wc.conditional_formatting.add(f"H{ct0}:H{ct1}", CellIsRule(operator="equal", formula=[f'"{val}"'],
        fill=PatternFill("solid", fgColor=bg), font=Font(name=FT, bold=True, size=8.5, color=fg)))
for col in ("J", "K", "L"):
    wc.conditional_formatting.add(f"{col}{ct0}:{col}{ct1}", FormulaRule(
        formula=[f'AND({col}{ct0}<>"",{col}{ct0}<TODAY(),$H{ct0}<>"Revisado")'],
        fill=PatternFill("solid", fgColor=BAD_BG), font=Font(name=FT, bold=True, size=8.5, color=BAD_FG)))
wc.conditional_formatting.add(f"M{ct0}:M{ct1}", IconSetRule("5Rating", "num", [1, 2, 3, 4, 5], showValue=True))
wc.conditional_formatting.add(f"N{ct0}:N{ct1}",
    DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="0C7E65", showValue=True))
wc.auto_filter.ref = f"B{ct0-1}:O{ct1}"
wc.freeze_panes = "E5"
finish(wc, NC, 90)
print("topicos:", len(TOP))
