(async () => {
  const SITE = "https://ebserhnet.sharepoint.com/teams/RoundTransplante";
  const NL = String.fromCharCode(10);
  const h = { headers: { Accept: "application/json;odata=nometadata" }, cache: "no-store" };
  const arr = (j) => j.value || (j.d && j.d.results) || [];
  const get = async (u) => { const r = await fetch(SITE + u, h); if (!r.ok) throw new Error("HTTP " + r.status + " em " + u); return r.json(); };
  const ALVOS = [
    { lista: "TxPlano", espelho: "PacienteId", ligacao: "PacienteRef" },
    { lista: "TxPendencia", espelho: "PacienteId", ligacao: "PacienteRef" },
    { lista: "TxRoundPaciente", espelho: "PacienteId", ligacao: "PacienteRef" },
    { lista: "TxRoundPaciente", espelho: "RoundId", ligacao: "RoundRef" },
    { lista: "TxCriterioAlta", espelho: "PlanoId", ligacao: "PlanoRef" }
  ];
  try {
    let out = "DELEGAÇÃO - LEVANTAMENTO (somente leitura)" + NL;
    const listas = arr(await get("/_api/web/lists?$select=Title,ItemCount,Hidden&$top=500")).filter(l => !l.Hidden && l.Title.startsWith("Tx"));
    out += NL + "LINHAS POR LISTA E RITMO DE CRESCIMENTO" + NL;
    for (const l of listas.sort((a, b) => b.ItemCount - a.ItemCount)) {
      let ritmo = "";
      if (l.ItemCount > 0) {
        const p = arr(await get("/_api/web/lists/getbytitle('" + l.Title + "')/items?$select=Created&$orderby=ID asc&$top=1"))[0];
        const dias = Math.max(1, (Date.now() - new Date(p.Created).getTime()) / 86400000);
        const porMes = l.ItemCount / dias * 30;
        const meses = porMes > 0 ? (2000 - l.ItemCount) / porMes : 0;
        ritmo = " | " + porMes.toFixed(1).replace(".", ",") + " por mês | 2000 linhas em cerca de " + (meses > 0 ? Math.round(meses) + " meses" : "já passou");
      }
      out += "  " + l.Title.padEnd(18) + String(l.ItemCount).padStart(6) + ritmo + NL;
    }
    out += NL + "COLUNAS DE LIGAÇÃO" + NL;
    for (const a of ALVOS) {
      const campos = arr(await get("/_api/web/lists/getbytitle('" + a.lista + "')/fields?$top=500"));
      const lig = campos.find(f => (f.InternalName === a.ligacao || f.Title === a.ligacao) && f.TypeAsString === "Lookup");
      const esp = campos.find(f => f.InternalName === a.espelho);
      if (!lig) { out += "  " + a.lista + "." + a.espelho + ": PARADO - coluna de ligação " + a.ligacao + " não encontrada" + NL; continue; }
      const itens = arr(await get("/_api/web/lists/getbytitle('" + a.lista + "')/items?$select=Id," + lig.InternalName + "Id" + (esp ? "," + a.espelho : "") + "&$top=5000"));
      const semLig = itens.filter(i => !i[lig.InternalName + "Id"]).length;
      let estado = esp ? "existe (" + esp.TypeAsString + (esp.Indexed ? ", indexada" : ", SEM índice") + ")" : "NÃO EXISTE - será criada";
      let difer = "";
      if (esp) {
        const d = itens.filter(i => i[lig.InternalName + "Id"] && i[a.espelho] !== i[lig.InternalName + "Id"]).length;
        difer = " | a preencher ou corrigir: " + d;
      } else {
        difer = " | a preencher: " + (itens.length - semLig);
      }
      out += "  " + (a.lista + "." + a.espelho).padEnd(28) + estado + " | ligação interna " + lig.InternalName + " | itens " + itens.length + " | sem ligação: " + semLig + difer + NL;
    }
    out += NL + "Nada foi alterado.";
    console.log(out);
  } catch (e) { console.log("ERRO: " + e.message); }
})();
