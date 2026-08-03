/* ==========================================================================
   Configuração do site.
   Enquanto SUPABASE.url estiver vazio, o site funciona 100% no aparelho
   (localStorage). Preencher url + chave liga a sincronização entre celular e PC.
   A chave publishable é pública por design — quem protege é o RLS no banco.
   Passo a passo em README.md.
   ========================================================================== */

export const SUPABASE = {
  url: "",              // ex.: "https://xxxxxxxx.supabase.co"
  chavePublishable: "", // ex.: "eyJhbGciOi..."  (anon / publishable — NUNCA a service_role)
};

export const APP = {
  nome: "Cronograma do Brenin",
  versao: "1.0.0",
  chaveLocal: "brenin.plano.v1",
  arquivoDados: "./dados/plano.json",
};

export const supabaseLigado = () =>
  Boolean(SUPABASE.url && SUPABASE.chavePublishable);
