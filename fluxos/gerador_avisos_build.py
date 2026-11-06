import json, uuid, zipfile, copy, os
REF='/home/claude/fluxo/ref/x'
FID='a6c1e0d2-5b7f-4c1a-9e33-2f8d6b4c7a11'   # pasta do fluxo no pacote
DID='4e2b9c7a-81d3-4f6e-b0a5-9c3d2e1f7b88'   # nome interno do fluxo
SITE='https://ebserhnet.sharepoint.com/teams/RoundTransplante'
TZ='E. South America Standard Time'
NOME='Round Transplante - avisos de pendências'
SP={"apiId":"/providers/Microsoft.PowerApps/apis/shared_sharepointonline","connectionName":"shared_sharepointonline"}
O365={"apiId":"/providers/Microsoft.PowerApps/apis/shared_office365","connectionName":"shared_office365","operationId":"SendEmailV2"}
TEAMS={"apiId":"/providers/Microsoft.PowerApps/apis/shared_teams","connectionName":"shared_teams","operationId":"PostMessageToConversation"}
AUTH="@parameters('$authentication')"
def ra(*prev): return {p:["Succeeded"] for p in prev}
def getitems(table, flt=None, order=None, top=500, after=None):
    p={"dataset":SITE,"table":table,"$top":top}
    if flt: p["$filter"]=flt
    if order: p["$orderby"]=order
    a={"type":"OpenApiConnection","inputs":{"parameters":p,"host":dict(SP,operationId="GetItems"),"authentication":AUTH}}
    if after: a["runAfter"]=ra(after)
    return a
def patch_cfg(qname, title, value, after=None):
    a={"type":"OpenApiConnection","inputs":{"parameters":{"dataset":SITE,"table":"TxConfig",
        "id":"@{first(body('%s'))?['ID']}"%qname,"item/Title":title,"item/field_1":value},
        "host":dict(SP,operationId="PatchItem"),"authentication":AUTH}}
    if after: a["runAfter"]=ra(after)
    return a
def query(frm, where, after=None):
    a={"type":"Query","inputs":{"from":frm,"where":where}}
    if after: a["runAfter"]=ra(after)
    return a
def select(frm, sel, after=None):
    a={"type":"Select","inputs":{"from":frm,"select":sel}}
    if after: a["runAfter"]=ra(after)
    return a
def compose(x, after=None):
    a={"type":"Compose","inputs":x}
    if after: a["runAfter"]=ra(after)
    return a
def cfgval(q): return "trim(coalesce(first(body('%s'))?['field_1'], ''))"%q
TESTE="outputs('EmailTeste')"
def to(dest): return "@{if(empty(%s), %s, %s)}"%(TESTE,dest,TESTE)
def pref(dest): return "@{if(empty(%s), '', concat('[TESTE - destinatário real: ', %s, '] '))}"%(TESTE,dest)
def email(dest, subject, body, after=None):
    a={"type":"OpenApiConnection","inputs":{"parameters":{"emailMessage/To":to(dest),
        "emailMessage/Subject":"[Round UTX] "+pref(dest)+subject,
        "emailMessage/Body":"<div style=\"font-family:Segoe UI,Arial;font-size:14px\">"+"<p>"+pref(dest)+"</p>"+body+RODAPE+"</div>",
        "emailMessage/Importance":"Normal"},"host":O365,"authentication":AUTH}}
    if after: a["runAfter"]=ra(after)
    return a
def teams(dest, msg, after=None):
    a={"type":"OpenApiConnection","inputs":{"parameters":{"poster":"Flow bot","location":"Chat with Flow bot",
        "body/recipient":to(dest),"body/messageBody":"<p>"+pref(dest)+msg+"</p>"},"host":TEAMS,"authentication":AUTH}}
    if after: a["runAfter"]=ra(after)
    return a
RODAPE="<p style=\"color:#4A5B6D;font-size:12px\">Aviso automático do Round Multiprofissional da Unidade de Transplante (HUB-UnB/Ebserh). Este aviso não altera nada: a pendência é atualizada ou resolvida somente no app Round Transplante, na equipe Round Transplante do Teams.</p>"
TH="<tr style=\"background:#0F6D78;color:#FFFFFF\"><th>Leito</th><th>Paciente</th><th>Pendência</th><th>Prazo</th><th>Bloqueia alta</th><th>Rounds em aberto</th></tr>"
THC="<tr style=\"background:#0F6D78;color:#FFFFFF\"><th>Responsável</th><th>Leito</th><th>Paciente</th><th>Pendência</th><th>Prazo</th><th>Bloqueia alta</th><th>Rounds em aberto</th></tr>"
def tabela(sel, th=TH): return "<table border=\"1\" cellpadding=\"6\" style=\"border-collapse:collapse;font-size:13px\">"+th+"@{join(body('%s'), '')}</table>"%sel
def foreach(src, actions, after=None):
    a={"type":"Foreach","foreach":src,"actions":actions,"runtimeConfiguration":{"concurrency":{"repetitions":1}}}
    if after: a["runAfter"]=ra(after)
    return a
def cond(expr, actions, after=None):
    a={"type":"If","expression":expr,"actions":actions,"else":{"actions":{}}}
    if after: a["runAfter"]=ra(after)
    return a

CFG="@body('Config')?['value']"
A={}
A["Config"]=getitems("TxConfig",top=200)
prev="Config"
for q,t in [("CfgTeste","AvisosSomentePara"),("CfgSemResp","AvisoSemResponsavel"),("CfgUltimo","AvisoUltimoRound"),
            ("CfgRoundData","AvisoRoundData"),("CfgQuintaData","AvisoQuintaData"),("CfgProximo","ProximoRound"),("CfgExtra","AvisoExtraData")]:
    A[q]=query(CFG,"@equals(item()?['Title'], '%s')"%t,prev); prev=q
A["EmailTeste"]=compose("@"+cfgval("CfgTeste"),prev)
A["SemResp"]=compose("@"+cfgval("CfgSemResp"),"EmailTeste")
A["Proximo"]=compose("@"+cfgval("CfgProximo"),"SemResp")
A["Hoje"]=compose("@convertFromUtc(utcNow(), '%s', 'yyyy-MM-dd')"%TZ,"Proximo")
A["Hora"]=compose("@int(convertFromUtc(utcNow(), '%s', 'HH'))"%TZ,"Hoje")
A["DueRound"]=compose("@and(equals(outputs('Hoje'), outputs('Proximo')), greaterOrEquals(outputs('Hora'), 7), not(equals(%s, outputs('Hoje'))))"%cfgval("CfgRoundData"),"Hora")
A["DueQuinta"]=compose("@and(or(equals(dayOfWeek(convertFromUtc(utcNow(), '%s')), 4), equals(%s, outputs('Hoje'))), greaterOrEquals(outputs('Hora'), 8), not(equals(%s, outputs('Hoje'))))"%(TZ,cfgval("CfgExtra"),cfgval("CfgQuintaData")),"DueRound")
ULT="int(if(empty(%s), '0', %s))"%(cfgval("CfgUltimo"),cfgval("CfgUltimo"))
A["Rounds"]=getitems("TxRound","StatusRound eq 'Encerrado' and ID gt @{%s}"%ULT,"ID asc",50,"DueQuinta")
A["IniciarLinhas"]={"type":"InitializeVariable","inputs":{"variables":[{"name":"vLinhas","type":"array"}]},"runAfter":ra("Rounds")}

# ---- dentro de "TemTrabalho"
W={}
W["Pendencias"]=getitems("TxPendencia","StatusPendencia eq 'Aberta'","Prazo asc",500)
W["Pacientes"]=getitems("TxPaciente",None,None,500,"Pendencias")
P="items('PorPend')"
PRAZO="convertFromUtc(outputs('PrazoTs'), '%s', '%%s')"%TZ
L={}
L["QPac"]=query("@body('Pacientes')?['value']","@equals(item()?['ID'], %s?['PacienteRef']?['Id'])"%P)
L["PrazoBruto"]=compose("@{coalesce(%s?['Prazo'], '1900-01-01')}"%P,"QPac")
L["PrazoTs"]=compose("@{concat(substring(outputs('PrazoBruto'), 0, 10), 'T12:00:00Z')}","PrazoBruto")
L["PrazoISO"]=compose("@{if(empty(%s?['Prazo']), '', %s)}"%(P,PRAZO%'yyyy-MM-dd'),"PrazoTs")
L["Vencida"]=compose("@and(not(empty(outputs('PrazoISO'))), less(outputs('PrazoISO'), outputs('Hoje')))","PrazoISO")
L["Celulas"]=compose("<td>@{coalesce(first(body('QPac'))?['Leito'], '-')}</td><td>@{coalesce(%s?['PacienteRef']?['Value'], '-')}</td><td>@{coalesce(%s?['DescricaoCompleta'], %s?['Title'], '')}</td><td>@{if(empty(outputs('PrazoISO')), '-', %s)}@{if(outputs('Vencida'), ' (vencida)', '')}</td><td>@{if(equals(%s?['BloqueiaAlta'], true), 'Sim', 'Não')}</td><td>@{coalesce(%s?['RoundsEmAberto'], 0)}</td>"%(P,P,P,PRAZO%'dd/MM/yyyy',P,P),"Vencida")
L["AbreLinha"]=compose("<tr@{if(outputs('Vencida'), ' style=\"color:#B91C1C;font-weight:600\"', '')}>","Celulas")
L["Guardar"]={"type":"AppendToArrayVariable","inputs":{"name":"vLinhas","value":{
    "dest":"@{if(empty(%s?['Responsavel']?['Email']), outputs('SemResp'), %s?['Responsavel']?['Email'])}"%(P,P),
    "resp":"@{if(empty(%s?['Responsavel']?['DisplayName']), 'Sem responsável', %s?['Responsavel']?['DisplayName'])}"%(P,P),
    "round":"@%s?['RoundOrigemRef']?['Id']"%P,
    "prazo":"@{outputs('PrazoISO')}",
    "vencida":"@outputs('Vencida')",
    "html":"@{outputs('AbreLinha')}@{outputs('Celulas')}</tr>",
    "htmlC":"@{outputs('AbreLinha')}<td>@{if(empty(%s?['Responsavel']?['DisplayName']), 'Sem responsável', %s?['Responsavel']?['DisplayName'])}</td>@{outputs('Celulas')}</tr>"%(P,P)}},
    "runAfter":ra("AbreLinha")}
W["PorPend"]=foreach("@body('Pendencias')?['value']",L,"Pacientes")
W["Linhas"]=query("@variables('vLinhas')","@not(empty(item()?['dest']))","PorPend")

def bloco_pessoal(tag, fonte, assunto, intro, teamsmsg):
    # envia a cada destinatário as linhas de 'fonte'
    D={}
    D["Q"+tag]=query(fonte,"@equals(item()?['dest'], items('PorDest%s'))"%tag)
    D["QV"+tag]=query("@body('Q%s')"%tag,"@equals(item()?['vencida'], true)","Q"+tag)
    D["Sel"+tag]=select("@body('Q%s')"%tag,"@item()?['html']","QV"+tag)
    dest="items('PorDest%s')"%tag
    n="@{length(body('Q%s'))}"%tag; v="@{length(body('QV%s'))}"%tag
    D["Email"+tag]=email(dest,assunto.replace('{n}',n),"<p>"+intro.replace('{n}',n).replace('{v}',v)+"</p>"+tabela("Sel"+tag),"Sel"+tag)
    D["Teams"+tag]=teams(dest,teamsmsg.replace('{n}',n).replace('{v}',v),"Email"+tag)
    return D

# A - antes do round
RA={}
RA["SelDestR"]=select("@body('Linhas')","@item()?['dest']")
RA["PorDestR"]=foreach("@union(body('SelDestR'), body('SelDestR'))",bloco_pessoal("R","@body('Linhas')",
    "Suas pendências abertas para o round de hoje ({n})",
    "Bom dia. Hoje há Round Multiprofissional da Unidade de Transplante. Você tem <b>{n}</b> pendência(s) aberta(s), das quais <b>{v}</b> vencida(s). Lembrete: registre sua avaliação no app até as 9h.",
    "Round Multiprofissional hoje: você tem <b>{n}</b> pendência(s) aberta(s) ({v} vencida(s)). A lista está no seu e-mail. Registre sua avaliação no app Round Transplante até as 9h."),"SelDestR")
RA["MarcarRound"]=patch_cfg("CfgRoundData","AvisoRoundData","@{outputs('Hoje')}","PorDestR")
W["SeRound"]=cond({"equals":["@outputs('DueRound')",True]},RA,"Linhas")

# C - quinta
RC={}
RC["LinhasQ"]=query("@body('Linhas')","@and(not(empty(item()?['prazo'])), lessOrEquals(item()?['prazo'], outputs('Proximo')))")
RC["SelDestQ"]=select("@body('LinhasQ')","@item()?['dest']","LinhasQ")
RC["PorDestQ"]=foreach("@union(body('SelDestQ'), body('SelDestQ'))",bloco_pessoal("Q","@body('LinhasQ')",
    "Pendências que vencem até o próximo round ({n})",
    "Você tem <b>{n}</b> pendência(s) vencida(s) ou com prazo até o próximo round, das quais <b>{v}</b> já vencida(s).",
    "Lembrete do Round Multiprofissional: <b>{n}</b> pendência(s) vencem até o próximo round ({v} já vencida(s)). A lista está no seu e-mail; atualize no app Round Transplante."),"SelDestQ")
RC["MarcarQuinta"]=patch_cfg("CfgQuintaData","AvisoQuintaData","@{outputs('Hoje')}","PorDestQ")
W["SeQuinta"]=cond({"equals":["@outputs('DueQuinta')",True]},RC,"SeRound")

# B - round encerrado
R="items('PorRound')"
RB={}
RB["LinhasE"]=query("@body('Linhas')","@equals(item()?['round'], %s?['ID'])"%R)
RB["SelDestE"]=select("@body('LinhasE')","@item()?['dest']","LinhasE")
RB["PorDestE"]=foreach("@union(body('SelDestE'), body('SelDestE'))",bloco_pessoal("E","@body('LinhasE')",
    "Pendências registradas no @{%s?['Title']} ({n})"%R,
    "O @{%s?['Title']} foi encerrado. Ficaram sob sua responsabilidade <b>{n}</b> pendência(s) registrada(s) na sessão."%R,
    "@{%s?['Title']} encerrado: <b>{n}</b> pendência(s) nova(s) com você. A lista está no seu e-mail; acompanhe no app Round Transplante."%R),"SelDestE")
RB["SelConsol"]=select("@body('Linhas')","@item()?['htmlC']","PorDestE")
ED="%s?['Editor']?['Email']"%R
RB["EmailConsol"]=email(ED,"Consolidado de pendências abertas após o @{%s?['Title']} (@{length(body('Linhas'))})"%R,
    "<p>O @{%s?['Title']} foi encerrado. Pendências abertas na unidade: <b>@{length(body('Linhas'))}</b>. Cada responsável recebeu as suas.</p>@{if(empty(body('Linhas')), '<p>Nenhuma pendência aberta.</p>', '')}"%R+tabela("SelConsol",THC),"SelConsol")
RB["TeamsConsol"]=teams(ED,"@{%s?['Title']} encerrado. Consolidado com <b>@{length(body('Linhas'))}</b> pendência(s) aberta(s) enviado ao seu e-mail."%R,"EmailConsol")
RB["MarcarUltimo"]=patch_cfg("CfgUltimo","AvisoUltimoRound","@{%s?['ID']}"%R,"TeamsConsol")
W["PorRound"]=foreach("@body('Rounds')?['value']",RB,"SeQuinta")

A["TemTrabalho"]=cond({"or":[{"equals":["@outputs('DueRound')",True]},{"equals":["@outputs('DueQuinta')",True]},
    {"greater":["@length(body('Rounds')?['value'])",0]}]},W,"IniciarLinhas")

ref=json.load(open(REF+'/Microsoft.Flow/flows/739c278a-19e9-4c4f-b46a-311d37eda9a4/definition.json'))
d=copy.deepcopy(ref)
d["name"]=DID; d["id"]="/providers/Microsoft.Flow/flows/"+DID
d["properties"]["displayName"]=NOME
df=d["properties"]["definition"]
df["triggers"]={"Recurrence":{"recurrence":{"frequency":"Minute","interval":"30","startTime":"2026-10-09T22:00:00.000Z"},
    "evaluatedRecurrence":{"frequency":"Minute","interval":"30","startTime":"2026-10-09T22:00:00.000Z"},"type":"Recurrence"}}
df["actions"]=A
out='/home/claude/fluxo/gen/pkg'; os.makedirs(out+'/Microsoft.Flow/flows/'+FID,exist_ok=True)
man=json.load(open(REF+'/manifest.json'))
res=man["resources"]; fl=res.pop("739c278a-19e9-4c4f-b46a-311d37eda9a4")
fl["details"]["displayName"]=NOME; fl["suggestedCreationType"]="New"
res[FID]=fl
man["details"]["displayName"]=NOME
man["resources"]={FID:fl, **{k:v for k,v in res.items() if k!=FID}}
json.dump(man,open(out+'/manifest.json','w'),ensure_ascii=False)
json.dump({"packageSchemaVersion":"1.0","flowAssets":{"assetPaths":[FID]}},open(out+'/Microsoft.Flow/flows/manifest.json','w'))
for f in ['apisMap.json','connectionsMap.json']:
    open(out+'/Microsoft.Flow/flows/'+FID+'/'+f,'w').write(open(REF+'/Microsoft.Flow/flows/739c278a-19e9-4c4f-b46a-311d37eda9a4/'+f).read())
json.dump(d,open(out+'/Microsoft.Flow/flows/'+FID+'/definition.json','w'),ensure_ascii=False)
z='/mnt/user-data/outputs/Round_avisos_pendencias.zip'; os.makedirs('/mnt/user-data/outputs',exist_ok=True)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as zf:
    for root,_,files in os.walk(out):
        for f in files:
            p=os.path.join(root,f); zf.write(p,os.path.relpath(p,out))
print(z)
