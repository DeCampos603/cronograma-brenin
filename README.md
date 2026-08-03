# Cronograma do Brenin — ESA + EAM

Site do plano de estudos do Brenin para os concursos da **ESA** (Escola de Sargentos das
Armas, Exército) e da **EAM** (Escola de Aprendizes-Marinheiros, Marinha), ciclo 2026/2027.

É a planilha `Cronograma_Brenin_ESA_EAM.xlsx` transformada em site: mesma grade, mesmos
198 tópicos, mesmo plano mensal — mas com contagem regressiva viva, marcação de progresso
que fica salva e uma tela **Hoje** que diz o que fazer agora.

- **Site estático**, publicado no GitHub Pages. Sem servidor, sem build, sem framework.
- **Funciona offline** e dá para instalar na tela inicial do celular (PWA).
- **Zero rastreador**, zero CDN, fonte do sistema. Nada sai do aparelho por padrão.

---

## Como o progresso é salvo

GitHub Pages hospeda arquivos estáticos — não existe servidor para guardar dado. Então a
persistência tem três camadas, e as duas primeiras funcionam sem configuração nenhuma:

| Camada | O que faz | Precisa configurar? |
|---|---|---|
| **1. Neste aparelho** (`localStorage`) | Grava a cada clique. Funciona offline. É o padrão. | Não |
| **2. Backup manual** (JSON) | Baixar/restaurar tudo em Ajustes. A rede de proteção. | Não |
| **3. Nuvem** (Supabase) | Mesmo progresso no celular e no PC. | Sim — 15 min, uma vez |

> ⚠️ **Sem a camada 3, o progresso vive só no navegador daquele aparelho.** Limpar os dados
> do navegador ou trocar de celular apaga tudo. Ou o Brenin baixa um backup de vez em
> quando, ou vale ligar a sincronização.

---

## Publicar no GitHub Pages

O repositório **pode ser público**: ele guarda só código e o plano de estudos. Nenhum dado
pessoal do Brenin fica aqui — o progresso dele mora no aparelho ou no Supabase.

```bash
cd "G:/Meu Drive/REPO/Cronograma-Brenin"
git add .
git commit -m "Cronograma do Brenin — site"
git branch -M main
git remote add origin https://github.com/<seu-usuario>/cronograma-brenin.git
git push -u origin main
```

Depois, no GitHub: **Settings → Pages** → *Source* = `Deploy from a branch`,
branch `main`, pasta **`/docs`**.

Em um ou dois minutos o site sai em
`https://<seu-usuario>.github.io/cronograma-brenin/`.

> A pasta `/docs` é publicada de propósito: assim `ferramentas/` e `modelos/` ficam no
> repositório mas fora do ar.

### Atualizar depois

`git add . && git commit -m "..." && git push` — o Pages republica sozinho. O service
worker usa **rede primeiro**, então a versão nova chega sem ninguém precisar limpar cache.

---

## Ligar a sincronização entre celular e PC (opcional)

1. Crie um projeto gratuito em [supabase.com](https://supabase.com) (plano Free basta).
2. **SQL Editor → New query**: rode `modelos/supabase/01-schema.sql` e depois
   `modelos/supabase/02-rls.sql`.
3. **Authentication → Sign In / Providers → Email**: deixe ativo e
   **desligue "Enable email signups"** — você cria a conta na mão, ninguém se cadastra
   sozinho.
4. **Authentication → Users → Add user**: crie o e-mail e a senha do Brenin.
5. **Settings → API**: copie a *Project URL* e a chave **publishable** (`anon`).
6. Cole as duas em `docs/js/config.js`:

```js
export const SUPABASE = {
  url: "https://xxxxxxxx.supabase.co",
  chavePublishable: "eyJhbGciOi...",
};
```

7. `git commit && git push`. Pronto: em **Ajustes → Sincronizar**, o Brenin entra com
   e-mail e senha, e o progresso passa a acompanhar os dois aparelhos.

### Sobre as chaves

| Chave | Vai no código? | Se vazar |
|---|---|---|
| **publishable** (`anon`) | ✅ sim, por design | Nada — o RLS protege |
| **secret** (`service_role`) | 🔴 **nunca** | Acesso total, ignora RLS |

A chave publishable é feita para ficar exposta no navegador. Quem protege é o RLS de
`02-rls.sql`, que restringe cada usuário à própria linha. **Teste antes de confiar** — o
arquivo traz os comandos `curl` no rodapé.

⚠️ Projeto Supabase gratuito **é pausado após 1 semana sem acesso**. Como o Brenin usa o
site quase todo dia, isso não deve acontecer; se acontecer, despause pelo painel.

---

## Estrutura

```
Cronograma-Brenin/
├── docs/                      ← é isto que vai para o GitHub Pages
│   ├── index.html
│   ├── manifest.webmanifest · sw.js · robots.txt · .nojekyll
│   ├── dados/plano.json       ← o plano inteiro (gerado, não editar na mão)
│   ├── assets/css/app.css
│   ├── assets/icons/
│   └── js/
│       ├── config.js          ← Supabase (opcional)
│       ├── store.js           ← persistência: local + nuvem + backup
│       ├── ui.js · app.js
│       ├── vendor/supabase.js ← cliente mínimo, sem CDN
│       └── views/             ← uma tela por arquivo
├── ferramentas/               ← pipeline: planilha → JSON
│   ├── gerar_v2*.py           ← gera o .xlsx (fonte da verdade do plano)
│   ├── exportar_dados.py      ← .xlsx → docs/dados/plano.json
│   └── validate_palette.py    ← valida a paleta (daltonismo, contraste)
└── modelos/supabase/          ← 01-schema.sql · 02-rls.sql
```

## Mudar o plano de estudos

O conteúdo (grade, 198 tópicos, plano mensal) vive nos scripts Python, **não** no site —
assim a planilha e o site nunca divergem.

```bash
cd ferramentas
python gerar_v2c.py       # regera o .xlsx
python exportar_dados.py  # regera docs/dados/plano.json
```

Depois, `git commit && git push`. O progresso do Brenin **não se perde**: ele é gravado
por identificador de tópico, separado do plano.

> Cuidado ao **remover ou reordenar** tópicos: o progresso é ligado ao `id` numérico. Só
> acrescente ao fim da lista da matéria; não intercale no meio.

## Rodar localmente

```bash
python -m http.server 8131 --directory docs
```

Abra `http://localhost:8131`. Precisa ser por servidor — abrir o `index.html` direto no
navegador quebra os módulos ES e o `fetch` do plano.

## Decisões de projeto

| Tema | Decisão | Por quê |
|---|---|---|
| Hospedagem | GitHub Pages, pasta `/docs` | Já é o fluxo do usuário; sem dado pessoal, o plano Free basta |
| Stack | HTML + CSS + JS vanilla (ES modules) | Zero build, zero dependência que quebra |
| Persistência | localStorage → Supabase opcional | Funciona no primeiro acesso; sincroniza quando quiser |
| Modelagem | Um documento jsonb por usuário | É o progresso de uma pessoa; dez tabelas seriam manutenção sem ganho |
| Conflito entre aparelhos | Último a gravar vence, por `atualizado_em` | Um usuário, dois aparelhos — não compensa CRDT |
| Service worker | Rede primeiro, cache de reserva | Cache-first prenderia correções no aparelho |
| Cor | Codifica **para qual prova** a matéria serve | Validada por cálculo, não escolhida no olho |
| Fonte | Do sistema (Segoe UI) | Google Fonts enviaria o IP do usuário ao Google |
