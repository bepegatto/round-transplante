MÉTODO DE CONSTRUÇÃO DE APPS POWER APPS NA UTX - VERSÃO 2
Guia reutilizável para qualquer app · base: Round Transplante (ago-out/2026), Rastreio BMR (set/2026),
Pendências do Paciente (out/2026) · HUB-UnB · Ebserh
Versão 1 em 28/09/2026 · versão 2 em 09/10/2026 (incorpora os erros, os moldes e os padrões de todo o percurso)
Regras de celular e rito de publicação (06/11/2026): ver docs/84_padrao_celular.md.

Como usar este guia: ele é o primeiro anexo de qualquer conversa que abra um app novo ou retome um existente.
As seções 3 e 4 dizem como trabalhar; as seções 5 a 7 dizem como fazer cada camada (SharePoint, Power Apps,
Power Automate); a seção 10 lista os erros já pagos; os anexos trazem os moldes prontos.

======================================================================
0. O QUE JÁ EXISTE
======================================================================
Site SharePoint: https://ebserhnet.sharepoint.com/teams/RoundTransplante (estrutura pessoal do Giuseppe,
dados no tenant Ebserh). Site do Pendências: https://ebserhnet.sharepoint.com/teams/PendnciasdoWhatsapp

1. Round Transplante (ago-out/2026, em produção desde 28/09)
   - Round multiprofissional semanal: registro por categoria (8 categorias), herança de dados entre
     rounds, coordenação por leito, síntese, pendências por profissional, matriz, check-in, saída/alta
   - 11 listas Tx* (TxPaciente, TxRound, TxAnotacao, TxPendencia, TxMembro, TxMapaCargo, TxConfig,
     TxPlano, TxPlanoVersao, TxCriterioAlta, TxPresenca, TxDispositivo), cerca de 120 colunas
   - Fluxos: sincronizar equipe (hora em hora), cópia de segurança semanal, avisos de pendências
     (Teams e e-mail, a cada 30 min)
2. Rastreio BMR - UTX (set/2026, piloto): vigilância de BMR (PRT.UTX.005), 4 listas, 5 telas, matriz de
   coerência, alertas; decisão de separar em equipe e site próprios ("Vigilância BMR - HUB")
3. Pendências do Paciente - UTX (out/2026): demandas de pacientes por WhatsApp; listas Ci*; fluxo de
   avisos por e-mail e Teams (molde dos avisos do Round)

======================================================================
1. PRINCÍPIOS
======================================================================
1. Plataforma: Power Apps (canvas) + listas SharePoint + Power Automate, só com conectores padrão do
   Microsoft 365. Sem licença premium, sem servidor, sem registro de aplicativo no Entra ID. Git
   Integration e Code Apps foram verificados e descartados (exigem premium, Dataverse ou reescrita).
2. Sigilo: dados no tenant da Ebserh, coberto pelo contrato com a Microsoft. Site da equipe com acesso
   restrito ao grupo; biblioteca de cópia de segurança com permissão exclusiva; nunca baixar dados de
   paciente para o computador.
3. Estrutura pessoal com continuidade: site, apps e fluxos são do Giuseppe. Continuidade por
   coproprietário no site, no app e em cada fluxo, e por esta documentação.
4. Regra clínica ou de negócio escrita antes do código. O app aplica o protocolo; não o inventa.
5. Um lugar para cada regra: tabelas de regra em App.Formulas; parâmetros em lista de configuração
   (TxConfig); nada de número mágico em fórmula de tela.
6. Rastreabilidade: toda ação sensível grava quem, quando e por quê; histórico de versões ligado.
7. Uma verdade só: o app é o registro. Aviso, e-mail, tarefa e planilha são lembrete ou cópia, nunca
   um segundo lugar para alterar o dado.
8. Acessibilidade desde a primeira tela (seção 6.8). Não se deixa para depois.
9. Rede de segurança no OnStart: o app corrige sozinho o estado esperado (round vencido, data vencida)
   em vez de depender de alguém lembrar.

======================================================================
2. PAPÉIS
======================================================================
- Dono do produto, regras clínicas e de negócio, governança, decisões: Giuseppe
- Arquitetura, dados, fórmulas, YAML, fluxos, scripts, auditoria: Claude
- Execução no Studio e no navegador (colar, arrastar, exportar, rodar script), testes, homologação: Giuseppe
- Validação externa (CCIH, chefia, TI): reuniões com pauta de decisão numerada

======================================================================
3. REGRAS PERMANENTES DE EXECUÇÃO (preferências do Giuseppe)
======================================================================
PRINCÍPIO: MENOS CLIQUES = MENOS ERROS = MAIS TEMPO. Claude faz todo o trabalho e entrega um artefato
que se cola, importa ou roda de uma vez. O Giuseppe não monta nada à mão.

1. Um passo por mensagem, com a sequência completa visível no início, e só avançar depois da
   confirmação. Ao fim de cada passo, dizer o que deve aparecer e que resposta se espera.
2. Código completo, pronto para colar. Nunca "troque uma linha" nem "edite o valor X".
3. Power Apps: YAML do maior bloco que resolva a tarefa (tela ou contêiner inteiro), colado uma vez.
   Edição pela barra de fórmulas só para uma ou duas propriedades. Blocos acima de cerca de 600 linhas
   vão em partes (um contêiner por mensagem); o arquivo único grande falhou na colagem (PA1001).
4. Dois dialetos: YAML colado em en-US (vírgula entre argumentos, ";" entre comandos); barra de
   fórmulas em pt-BR (";" entre argumentos, ";;" entre comandos, decimal com vírgula). Nunca colar o
   nome da propriedade junto com a fórmula.
5. SharePoint: script de console em dois tempos, LISTAR (só lê) e APLICAR (grava e relê o estado
   final), sempre como dois scripts completos. F5 na aba antes de cada script (403 por sessão
   expirada). Nunca configurar pela interface.
6. Power Automate: pacote .zip completo, importado em Meus fluxos → Importar Pacote (Herdado), com
   "Criar como novo" na primeira vez e "Atualizar" nas seguintes. Nunca montar ou editar no designer.
7. Primeiro ato de toda sessão que mexe no app: Ctrl+S, exportar o .msapp e anexar à conversa.
8. Texto: português formal e direto, acentuação completa em tudo (código, rótulos, exemplos), sem
   travessão, decimal com vírgula.
9. Documentos numerados no projeto (NN_assunto.md). Todo doc de retomada começa pelas regras
   permanentes e pelo texto para colar ao abrir o novo chat.
10. Erros de preenchimento em pop-up central ou faixa na tela; Notify só para sucesso e falha de
    gravação. Avisos importantes em faixa grande e colorida (o pequeno passou despercebido).

======================================================================
4. CICLO DE VIDA DE UM APP
======================================================================
Fase 1 · Desenho (1 a 2 sessões)
  1. Briefing: problema, quem usa, quando, em que aparelho, o que precisa sair (indicadores, avisos)
  2. Regras de negócio escritas e decisões numeradas, fechadas pelo dono (template da seção 11)
  3. Desenho das listas (nome, colunas, tipos, índices, ligações) e esboço das telas em texto
  4. Pauta de decisão para a chefia ou o serviço parceiro, quando houver regra deles

Fase 2 · Dados (1 sessão)
  5. Auditoria do site (script de colunas, anexo A) e criação das listas por script LISTAR/CRIAR
  6. Lista de configuração (TxConfig: Title, Valor em field_1, Descricao em field_2) desde o início
  7. Limite de linhas de dados do app em 2000 no primeiro dia

Fase 3 · App (várias sessões, uma tela por vez)
  8. App.OnStart (variáveis de contexto, usuário e categoria, configuração, rede de segurança)
  9. Telas por YAML, da mais usada para a menos usada; teste de cada uma antes da próxima
  10. Pacote exportado e auditado a cada etapa (seção 6.7)

Fase 4 · Fluxos (1 sessão por fluxo)
  11. Sincronização de equipe, cópia de segurança, avisos: pacote .zip a partir do molde (anexo B)
  12. Modo de teste (linha AvisosSomentePara) até liberar

Fase 5 · Testes e publicação
  13. Roteiro numerado; paciente ZZ TESTE; conferência do banco por script; limpeza; checklist (seção 9)
  14. Mensagem à equipe com o que mudou, em linguagem de uso, não de sistema

Fase 6 · Operação
  15. Observar a primeira sessão real; apontamentos viram doc de retomada e nova rodada (fase 3)
  16. Pequenos ajustes acumulados entram numa publicação só, nunca na véspera do uso

======================================================================
5. CAMADA SHAREPOINT (scripts de console)
======================================================================
5.1 Padrão de todo script (anexo A)
- Função assíncrona autoexecutável; `site` e `L(nome)` no topo; `get` com Accept
  `application/json;odata=nometadata`; digest por POST em `/_api/contextinfo`; gravação com
  `X-RequestDigest`; MERGE com `IF-MATCH: *` e `X-HTTP-Method: MERGE`; exclusão com DELETE ou
  `/recycle()` (lixeira, preferível).
- LISTAR só lê e termina com "Nada foi alterado". APLICAR confere pré-condições, para com "PARADO:"
  se algo divergir, executa, relê e imprime o estado final. Trava de execução única por aba
  (`window.__tx...`).
- Quebra de linha com `String.fromCharCode(10)`; sem barra invertida (a área de transferência corrompe).
- Toda exclusão confere antes: Id, lista, paciente, autor e round esperados. Só então apaga.
- Resultado sempre colado de volta no chat; Claude lê antes de propor o próximo passo.

5.2 Nomes de coluna
- Nome interno congela na criação e nunca muda (VinculoS). Em fluxo e em REST vale o interno; no
  Power Apps vale o de exibição entre aspas simples.
- Listas criadas por script: nome de exibição = nome interno, sem acento e sem espaço. Evita o problema.
- Rodar o script de auditoria de colunas no início de toda sessão com fluxo ou script de gravação.
- Em TxConfig antiga, o valor fica em `field_1` e a descrição em `field_2`.
- Ids de usuário do site (siteusers) não são Ids da TxMembro. Dizer sempre qual é qual.

5.3 Lista de configuração
Uma linha por parâmetro: faixas de cor, categorias ativas e obrigatórias, dia e horário do round,
ProximoRound, marcadores de envio dos fluxos. O app lê no OnStart com faixa válida e padrão
(`If(v >= 1 && v <= 7; v; 2)`), porque `Value("")` não dá erro e uma linha ausente passa em silêncio.

5.4 Dados de teste
- Paciente de teste sempre "ZZ TESTE - NÃO USAR", prontuário 000000, leito TESTE. Criar, testar e dar
  saída no mesmo dia. Nunca na véspera do uso real.
- Anotação de teste gravada por engano em paciente real: localizar por autor, data e Id, e apagar por
  script que confere cada item antes.
- Script de limpeza segue as ligações (lookup e Ids numéricos) e apaga na ordem filho → pai.

5.5 Cópia de segurança
Fluxo semanal (CSV de todas as listas numa biblioteca restrita aos proprietários) e script COPIAR como
plano B (doc 60). Antes de qualquer limpeza ou migração: rodar a cópia.

5.6 Conferir o banco, não a tela
Quando o Studio mostrar dado inconsistente, o banco é consultado por script (o Studio guarda registro
antigo em memória). Diagnóstico de problema de uso começa por script de leitura (rounds, anotações,
autores, horários), antes de abrir o app.

======================================================================
6. CAMADA POWER APPS
======================================================================
6.1 Fonte
- Exportar o .msapp (make.powerapps.com → Aplicativos → ⋯ → Exportar pacote, ou baixar o .msapp).
  Dentro: `Src/*.pa.yaml` (uma tela por arquivo, mais App.pa.yaml) e `AppCheckerResult.sarif`.
- O .msapp usa barra invertida; abrir com `zipfile` do Python (o `unzip` reclama, mas extrai).
- Regenerar tela ou contêiner inteiro custa menos que editar propriedades avulsas (16 controles numa
  colagem: 2 minutos; 8 edições de propriedade: mais de uma hora).

6.2 Colagem
1. Apagar o controle antigo antes de colar o novo (colar por cima cria `_1` silencioso).
2. Selecionar a tela na Árvore (o seletor de propriedades mostra Fill e OnVisible) e Ctrl+V.
3. Depois de colar: procurar `_1` na Árvore; reordenar camadas (Ctrl+clique → Reordenar → Enviar para
   trás) porque o colado fica na frente de tudo; Ctrl+S.
4. Erros esperados logo após apagar contêineres (variáveis que só existem dentro deles) somem ao recolar.
5. Cópia longa pode sair truncada: conferir a última linha antes de colar; erro "Unknown variant" ou
   YamlInvalidSyntax quase sempre é cópia cortada, e a solução é colar de novo ou em partes.
6. O Studio não executa OnVisible nem OnStart na edição: testar com F5 (pré-visualização) ou, para o
   OnStart, ⋯ no App → Executar OnStart.

6.3 Propriedades que o tipo de controle exige (sem elas o comportamento é errado em silêncio)
| Controle | Propriedade |
| Classic/DropDown | AllowEmptySelection: =true (senão grava a primeira opção sem ninguém tocar) |
| Classic/ComboBox | DisplayFields e SearchFields: =["Value"]; IsSearchable: =false em lista curta; DefaultSelectedItems, não Default |
| Classic/DatePicker | DefaultDate, não Default; StartYear e EndYear por campo (padrão 1970 a 2050) |
| Todo controle de entrada | Reset: =gResetForm, com a variável piscando (true, false) na troca de contexto |
| Filho de AutoLayout | LayoutMinHeight igual à altura |
| Qualquer valor com ": " | `|-` no YAML |
Enumerações sempre qualificadas (DateTimeFormat.ShortTime, NotificationType.Success, LayoutOverflow.Scroll).

6.4 Ligação com os dados
| Tipo | Controle | Default | Patch |
| Texto | TextInput | g.'Coluna' | ctrl.Text |
| Número | TextInput Format Number | idem | Value(ctrl.Text) |
| Escolha | DropDown, Items Choices(Lista.'Coluna') | g.'Coluna'.Value | ctrl.Selected |
| Escolha múltipla | ComboBox SelectMultiple | DefaultSelectedItems g.'Coluna' | Filter(ctrl.SelectedItems, !IsBlank(Value)) |
| Data | DatePicker | DefaultDate g.'Coluna' | ctrl.SelectedDate |
| Sim/Não | Toggle | g.'Coluna' | ctrl.Value |
| Pessoa | Patch com Claims "i:0#.f|membership|email", DisplayName, Email |
Todo Patch de criação preenche Title. Escolha grava {Value: "texto"} ou ctrl.Selected inteiro.

6.5 Padrões de tela já validados
1. Tela inicial com botões por papel (quem registra, quem coordena), visíveis pela categoria do
   usuário (gMinhaCategoria vem da TxMembro pelo login, não pelo e-mail inteiro).
2. Formulário por categoria: um GroupContainer AutoLayout vertical por categoria, mesma posição,
   `Visible: =gCategoria = "X"`, rolagem própria, legenda + controle por campo, campos condicionais
   com Visible, botão de gravar ao fim com validação em tabela (Filter(Table({c, t}), c)), Patch único
   embrulhado em Set(gAtual, Patch(...)), estado visual do botão ("Bloco gravado às hh:mm · atualizar").
3. Herança de dados: `gBase` = registro do contexto atual com conteúdo ou, na falta, o último registro
   da categoria com conteúdo; todos os Default leem gBase; faixa colorida diz a data de origem.
   Recalcular gBase em todo ponto que muda contexto (OnVisible, troca de aba, avanço).
4. Avanço automático: botão invisível (btnAvancar) acionado por `Select(btnAvancar)` ao fim de cada
   gravação; só avança se a gravação for recente (menos de 30 s), fora do modo de coordenação e com o
   item batendo com `Index(colOrdem, gPos)`. No último item, aviso e volta ao painel.
5. Coordenação: lista ordenada por leito, toque abre direto a tela de decisão, "Gravar e próximo", no
   último "Gravar e encerrar", encerramento com data da próxima sessão e criação imediata do próximo.
6. Janela sobreposta (encerramento, saída/alta, censo): fundo escuro + cartão + botões, controlada por
   variável gMostrarX; tudo o que pode sobrepor leva `&& !gMostrarX` no Visible.
7. Pop-up central de erro, bloqueio e confirmação; dois toques em ação irreversível.
8. Rede de segurança no OnStart (encerra o vencido, recalcula a próxima data) e aviso na tela inicial.
9. Rodapé de autoria e versão; caixa de sugestões por tela gravada em lista.
10. Layout responsivo: contêineres de layout automático; PaddingLeft/Right = Max(16; (Parent.Width - N) / 2);
    altura dinâmica de rodapé por modo.

6.6 Sinais de que a troca de contexto não recarregou
Dados de outra aba ou outro paciente nos campos. Causa: o OnSelect que muda o contexto está em outro
controle (ex.: lblAba dentro da galeria, e não a galeria) ou não recalcula gBase. Procurar no fonte onde
o Set da variável de contexto acontece e colocar lá o recálculo completo (atual, semAlt, base, reset).

6.7 Auditoria do pacote (a cada export)
1. Verificador: 0 erros; avisos contados por regra e por tela (sarif)
2. Nenhum controle `_1`; nenhuma tela órfã; variáveis e coleções sem uso
3. Nomes de coluna e opções citados existem na lista (contra a auditoria de colunas)
4. Todo controle de entrada com Reset; enumerações qualificadas
5. Delegação: filtros simples em colunas indexadas; o resto em coleções; limite 2000; dívida registrada
6. Acessibilidade por tela (6.8): zero nas telas novas ou recoladas
7. Comparação com o pacote anterior: o que mudou e o que já tinha sido colado (evita repetir)

6.8 Padrão de acessibilidade (obrigatório em toda tela nova ou recolada)
Decidido em 09/10/2026 (pacote 30 do Round com 874 avisos: 355 TabIndex, 309 borda de foco,
210 rótulo acessível). Toda tela nasce assim:
1. AccessibleLabel em todo controle interativo = texto visível do rótulo ou do botão; "" nos decorativos
2. TabIndex 0 nos interativos, na ordem visual; -1 nos decorativos
3. FocusedBorderThickness 2 e FocusedBorderColor RGBA(15, 109, 120, 1)
4. Área de toque: Height mínima 44 em botão, aba, alternância e ação em galeria
5. Fonte mínima 12 no que se lê durante o uso; 11 só em rodapé e legenda secundária
6. Contraste mínimo 4,5:1: secundário RGBA(74, 91, 109, 1) (6,98:1); apagado no máximo
   RGBA(107, 114, 128, 1) (4,83:1); proibidos para texto RGBA(140, 150, 160, 1) (3,01:1) e mais claros
7. Cor nunca sozinha: estado também em texto ou ícone com rótulo
8. Rótulo visível acima de todo campo; HintText não substitui
Dívida do Round registrada (botões de 22 a 32 na Síntese e no topo da scrPaciente, cinzas de 3:1,
268 rótulos em fonte 11): corrigir de carona quando cada tela for recolada, começando pela Síntese.

======================================================================
7. CAMADA POWER AUTOMATE
======================================================================
7.1 Entrega
Pacote .zip gerado por script Python a partir de um molde exportado do próprio ambiente (anexo B).
Importação: Meus fluxos → Importar → Importar Pacote (Herdado) → chave inglesa → "Criar como novo"
(primeira vez) ou "Atualizar" (seguintes, mantém histórico) → selecionar as conexões existentes →
Importar → conferir Ativado.

7.2 Estrutura do pacote (cinco arquivos, sem entrada de diretório)
manifest.json · Microsoft.Flow/flows/manifest.json · Microsoft.Flow/flows/<GUID>/apisMap.json ·
connectionsMap.json · definition.json. Detalhes que só aparecem num pacote real: segundo manifesto
`{"packageSchemaVersion":"1.0","flowAssets":{"assetPaths":["<GUID>"]}}`; recursos de fluxo e de
conexão sem `id` e `name`; toda ação de conector com `"authentication": "@parameters('$authentication')"`;
em `host` o campo é `connectionName`; GUID da pasta diferente do GUID do definition; `contentVersion`
"undefined"; intervalo de recorrência como string. Sempre partir de um export real e trocar só o miolo.

7.3 Ações já aprovadas no ambiente (copiar do molde, não inventar)
- SharePoint GetItems (dataset, table, $filter, $top, $orderby), PatchItem (id, item/Coluna)
- Office 365 Outlook SendEmailV2 (emailMessage/To, Subject, Body em HTML, Importance)
- Microsoft Teams PostMessageToConversation (poster "Flow bot", location "Chat with Flow bot",
  body/recipient = e-mail, body/messageBody em HTML)
- Office 365 Groups listar membros do grupo (sincronização de equipe)
- Query (filtrar matriz), Select, Compose, InitializeVariable, AppendToArrayVariable, Foreach com
  concurrency 1, If, union(sel, sel) para destinatários únicos

7.4 Padrão de fluxo de avisos (Round, doc 82)
- Um fluxo, recorrência (30 min no Round, 10 min no Pendências), que decide sozinho o que enviar e só
  lê as listas pesadas quando há trabalho
- Marcadores de envio na lista de configuração (AvisoUltimoRound, AvisoRoundData, AvisoQuintaData):
  nunca envia duas vezes; rebaixar um marcador reenvia (só em modo de teste)
- Linha AvisosSomentePara: preenchida, tudo vai para um e-mail com "[TESTE - destinatário real: ...]";
  vazia, vai para a equipe. Liberação é apagar o valor por script, que antes confere os marcadores
- Linha AvisoExtraData: envio extra numa data escolhida, uma vez
- Destinatário vazio vai para um responsável padrão (chefia), nunca se perde
- Teams curto com o número e "a lista está no seu e-mail"; e-mail com tabela (vencidas em vermelho),
  rodapé dizendo que o aviso não altera nada e que se resolve no app
- Teste: rebaixar o marcador, executar à mão, conferir Teams, e-mail e execução verde; liberar; o
  primeiro envio real pode ser forçado pelo AvisoExtraData com a equipe já avisada

7.5 Armadilhas do Power Automate
- Data sem hora do SharePoint chega como "2026-10-05T00:00:00.0000000" (sem Z) e convertFromUtc
  recusa: usar os 10 primeiros caracteres + "T12:00:00Z"
- Nome interno da coluna (VinculoS) e nome de lista exatos; WorkflowOperationParametersExtraParameter
  é erro de conteúdo, não de empacotamento; MissingPackageManifest é o segundo manifesto
- Gatilho de evento é melhor esforço: estado que precisa estar certo usa recorrência
- E-mail dentro do app (OnSelect) trava a tela e sai da caixa de quem clica: avisos sempre por fluxo
- Fluxo fica na conta do dono: remetente é a caixa dele até existir caixa institucional
- Quando o fluxo falha dentro de um bloco, o aviso "ActionFailed" é genérico: abrir a etapa vermelha
  (dentro do laço, na repetição que falhou) e copiar a mensagem completa

======================================================================
8. TESTES
======================================================================
1. Roteiro numerado: o que fazer, o que deve acontecer, o que mandar de volta (print ou resultado de
   script). Nunca "teste aí".
2. Testar o caso real, não só o artificial (a regra de data falhou com data vencida de verdade).
3. Antes de gravar em teste: confirmar o paciente (ZZ TESTE) e o modo (registrar ou coordenar). Voltar
   ao painel pela tela do paciente mantém o modo anterior.
4. Depois do teste: script de leitura do banco (o que foi gravado, por quem, em que round) e limpeza
   por script que confere Id, paciente e autor antes de apagar.
5. Cada teste com dado real exige F5 e, quando o OnStart muda, Executar OnStart.
6. Quando um print mostra dado inesperado, o primeiro passo é comparar com o banco por script, não
   mexer no app.

======================================================================
9. CHECKLIST ANTES DE PUBLICAR
======================================================================
1. Pacote auditado: 0 erros, sem `_1`, telas novas sem avisos de acessibilidade
2. Limite de linhas de dados em 2000
3. Cópia de segurança rodada; dados de teste limpos (anotações, sínteses, rounds, ZZ TESTE com saída)
4. Teste com usuário que não é proprietário (gravar, campos de pessoa)
5. Permissões de edição nas listas para o grupo; app compartilhado com o grupo; aba no Teams
6. Coproprietário no site, no app e nos fluxos
7. Rodapé com versão; doc de fechamento escrito (estado do banco, o que foi publicado, pendências)
8. Mensagem à equipe em linguagem de uso ("Registrar minha avaliação", não "gModoCoord")
9. Nunca publicar na véspera do uso real algo que não foi testado no fluxo completo

======================================================================
10. ARMADILHAS JÁ PAGAS (NÃO REPETIR)
======================================================================
Dados
- Nome interno diferente do exibido (VinculoS) → auditoria de colunas em toda sessão com fluxo
- Linha de configuração ausente passa em silêncio (Value("") não erra) → faixa válida + padrão
- Lista com Title obrigatório → todo Patch de criação preenche Title
- Excel remove zero à esquerda e reformata data → prontuário texto; restaurar só do CSV original
- Limite de 500 linhas ignora dados sem avisar → 2000 no primeiro dia
- Conta duplicada de usuário (dois logins) → unificar: transferir itens, desativar na TxMembro e
  remover do Teams (senão a sincronização reativa)
- Linha criada à mão na TxMembro sem Login vira duplicata na sincronização → Login sempre preenchido
- Escrever teste em paciente real → ZZ TESTE e conferir antes de gravar
Power Apps
- Colar duas vezes cria `_1` → apagar antes; procurar `_1`
- Colado fica na frente → Enviar para trás; esconder faixas quando uma janela abre (`&& !gMostrarX`)
- Fórmula no controle errado (galeria em vez do rótulo dentro dela) → procurar no fonte onde o
  contexto muda
- Enumeração sem prefixo (ShortTime) → sempre qualificada
- DropDown sem AllowEmptySelection grava a primeira opção → sempre com a propriedade
- DatePicker: DefaultDate, StartYear e EndYear; data vazia aparece como 31/12/2001 → tratar o vazio
- Controle sem Reset mostra o paciente anterior → Reset: =gResetForm em todos
- Studio mostra dado antigo → conferir no banco por script
- Studio não roda OnStart nem OnVisible na edição → F5 ou Executar OnStart
- Round (ou período) não encerrado faz tudo cair no período errado → encerramento obrigatório +
  rede de segurança no OnStart
- Aviso pequeno passa despercebido → faixa grande e colorida
- Acessibilidade deixada para depois vira centenas de avisos → padrão 6.8 desde a primeira tela
- Dois modos (registrar e coordenar) sem indicação clara → o modo define botões, ordem e rodapé
Power Automate
- Formato do pacote não documentado → exportar um fluxo real do ambiente como molde
- Data sem Z → 10 caracteres + "T12:00:00Z"
- Reenvio por marcador rebaixado em produção → só em modo de teste (AvisosSomentePara preenchido)
Trabalho
- Prescrição em documento não é execução → conferir no fonte se a variável ou a fórmula já existe
- Cópia longa cortada → conferir a última linha; dividir em contêineres
- Sessão do SharePoint expira (403) → F5 antes de cada script
- Publicar e testar na véspera do uso → ajustes pequenos esperam a próxima publicação

======================================================================
11. COMO ABRIR UM APP NOVO (template da primeira mensagem)
======================================================================
"Vamos começar um projeto: <nome do app>, pelo método do guia anexo (doc 66, versão 2)."
Anexar: este guia; o .msapp mais recente de um app parecido (molde de controles e padrões); um .zip de
fluxo exportado do ambiente (molde do Power Automate); exemplos reais anonimizados do problema.

Preencher:
PROJETO / OBJETIVO / ESTÁGIO (novo, continuação, refinamento) / ENTREGA ESPERADA / RESTRIÇÕES /
CONTEXTO ADICIONAL

Primeira sessão: briefing e decisões numeradas (fase 1). Claude responde com o desenho das listas, o
esboço das telas em texto, a pauta de decisões pendentes e a ordem das sessões seguintes.

======================================================================
ANEXO A · CABEÇALHO PADRÃO DE SCRIPT DE CONSOLE
======================================================================
(async () => {
  const MODO = "LISTAR";   // ou "APLICAR"
  const site = "https://ebserhnet.sharepoint.com/teams/<Site>";
  const h = { Accept: "application/json;odata=nometadata" };
  const L = (n) => "/_api/web/lists/getbytitle('" + n + "')";
  const NL = String.fromCharCode(10);
  const get = async (u) => { const r = await fetch(site + u, { headers: h, cache: "no-store" }); if (!r.ok) throw new Error(r.status + " em " + u); return r.json(); };
  const digest = async () => (await (await fetch(site + "/_api/contextinfo", { method: "POST", headers: h })).json()).FormDigestValue;
  const merge = async (lista, id, corpo, dig) => fetch(site + L(lista) + "/items(" + id + ")", { method: "POST", headers: { ...h, "Content-Type": "application/json;odata=nometadata", "X-RequestDigest": dig, "IF-MATCH": "*", "X-HTTP-Method": "MERGE" }, body: JSON.stringify(corpo) });
  const criar = async (lista, corpo, dig) => fetch(site + L(lista) + "/items", { method: "POST", headers: { ...h, "Content-Type": "application/json;odata=nometadata", "X-RequestDigest": dig }, body: JSON.stringify(corpo) });
  const lixeira = async (lista, id, dig) => fetch(site + L(lista) + "/items(" + id + ")/recycle()", { method: "POST", headers: { ...h, "X-RequestDigest": dig } });
  try {
    // 1. ler o estado; 2. conferir pré-condições (console.log("PARADO: ...") e return);
    // 3. se MODO = APLICAR: executar; 4. reler e imprimir o estado final
  } catch (e) { console.log("ERRO: " + e.message); }
})();
Auditoria de colunas (todas as listas Tx*): doc 32, seção 3.3. Criação de listas: doc 52. Limpeza de
teste: doc 55. Cópia de segurança: doc 60.

======================================================================
ANEXO B · GERADOR DE PACOTE DO POWER AUTOMATE (Python)
======================================================================
Fonte completo do gerador dos avisos do Round: fluxos/gerador_avisos_build.py (doc 83). Esqueleto:
1. Extrair um pacote real exportado (REF). Carregar manifest.json e definition.json.
2. Funções que devolvem ações no formato OpenApiConnection: getitems(table, filtro, ordem, top),
   patch(table, id, campos), email(to, subject, body), teams(to, msg), query(from, where),
   select(from, expr), compose(expr), foreach(src, actions), cond(expr, actions). Cada uma com
   `runAfter` opcional e `authentication` fixa.
3. Montar `actions` como dicionário ordenado; trocar `triggers` pela recorrência desejada.
4. Copiar o manifest de referência trocando o GUID do fluxo e o displayName
   (suggestedCreationType "New"); copiar apisMap e connectionsMap; gravar os cinco arquivos e zipar
   sem diretórios.
5. Conferir: `unzip -l` com cinco entradas; abrir o definition e ler `actions` e `runAfter`.
Expressões úteis: convertFromUtc(utcNow(), 'E. South America Standard Time', 'yyyy-MM-dd');
dayOfWeek(...) (4 = quinta); int(...); coalesce(first(body('X'))?['campo'], ''); union(a, a) para
valores únicos; join(body('Select'), '') para montar HTML; if(empty(x), a, b).

======================================================================
ANEXO C · ESQUELETO DE BLOCO YAML DE FORMULÁRIO
======================================================================
- ctnCategoria:
    Control: GroupContainer@1.5.0
    Variant: AutoLayout
    Properties:
      LayoutDirection: =LayoutDirection.Vertical
      LayoutAlignItems: =LayoutAlignItems.Stretch
      LayoutOverflowY: =LayoutOverflow.Scroll
      LayoutGap: =6
      Visible: =gCategoria = "Categoria"
    Children:
      - lblCampoCap:
          Control: Label@2.5.1
          Properties:
            Text: ="Rótulo do campo"
            Size: =12
            Color: =RGBA(74, 91, 109, 1)
            Height: =22
            LayoutMinHeight: =22
            TabIndex: =-1
      - ddCampo:
          Control: Classic/DropDown@2.3.1
          Properties:
            Items: =Choices(Lista.'Coluna')
            Default: =gBase.'Coluna'.Value
            AllowEmptySelection: =true
            Reset: =gResetForm
            Height: =44
            LayoutMinHeight: =44
            Size: =12
            AccessibleLabel: ="Rótulo do campo"
            TabIndex: =0
            FocusedBorderThickness: =2
            FocusedBorderColor: =RGBA(15, 109, 120, 1)
      - btnGravar:
          Control: Classic/Button@2.2.0
          Properties:
            Height: =48
            LayoutMinHeight: =48
            AccessibleLabel: ="Gravar bloco de Categoria"
            TabIndex: =0
            OnSelect: |-
              =With({f: Concat(Filter(Table({c: IsBlank(ddCampo.Selected.Value), t: "campo"}), c), t, "; ")},
                If(!IsBlank(f), Set(gFaltas, {p: gItem.ID, m: "Não gravado. Falta preencher: " & f & "."}),
                  Set(gFaltas, {p: gItem.ID, m: ""});
                  Set(gAtual, Patch(Lista, Coalesce(LookUp(Lista, <chave do contexto>), Defaults(Lista)), {Title: ..., 'Coluna': ddCampo.Selected}));
                  Notify("Gravado.", NotificationType.Success)
                )
              ); Select(btnAvancar)

HUB - Hospital Universitário de Brasília · Ebserh · UnB · SUS
