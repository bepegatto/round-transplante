# Fechamento da sessão de 06/11/2026 - Round Transplante no celular
**Round Multiprofissional do Transplante · HUB-UnB · Ebserh**

## Parte I - Regras permanentes de execução
1. Um passo por mensagem, com a sequência completa visível no início; avançar só depois da confirmação. Dizer ao fim de cada passo o que deve aparecer e que resposta se espera.
2. Código completo, pronto para colar. Power Apps: YAML do maior bloco que resolva (galeria, cabeçalho ou contêiner inteiro), colado com a tela selecionada (seletor mostra OnVisible), depois Reordenar → Enviar para trás.
3. Dois dialetos: YAML colado em en-US (vírgula entre argumentos); barra de fórmulas em pt-BR (";" entre argumentos, ";;" entre comandos). Fórmula sem separador serve nos dois. Erro desta sessão: `If(gPDEdit, 80, 0)` entregue com vírgula para a barra.
4. Mesma propriedade em vários controles: seleção múltipla na Árvore (Shift ou Ctrl) e uma fórmula só.
5. **Publicar em lote** (pedido do Giuseppe em 06/11): Ctrl+S a cada passo, teste no Studio (F5), uma publicação só no fim do lote.
6. Primeiro ato de sessão que mexe no app: exportar o .msapp e anexar.
7. Padrão de celular (doc 84) e os quatro requisitos de concepção (skill power-platform-sharepoint, seção 2.4) valem para toda tela nova ou recolada.
8. Atualização da skill só vale depois que o Giuseppe salva o cartão; conferir na sessão seguinte.
9. **Registro de horas** (decidido em 06/11, para o artigo metodológico): todo documento de fechamento traz a linha de sessão com data, início, fim, duração, app trabalhado e tipo de trabalho (construção, correção, desenho, teste, documentação). Tempo de relógio da conversa, com pausas longas descontadas.

## Registro da sessão
| Data | Início | Fim | Duração | App | Tipo de trabalho |
|---|---|---|---|---|---|
| 06/11/2026 | 10h16 | 12h33 | 2h17 | Round Transplante | correção (celular, dados), melhoria de leitura, método, levantamento de delegação, análise de risco clínico |

Esforço acumulado até 06/11 (reconstruído, não medido): 19 dias de trabalho entre 04/08 e 06/11; piso de 67 h pelos intervalos entre documentos de cada dia; estimativa de 90 a 130 h no projeto inteiro (Round Transplante + Rastreio BMR) e 60 a 90 h só no Round. Equivalente de mercado estimado: R$ 280 mil a R$ 350 mil pelos dois apps (R$ 170 mil a R$ 220 mil só o Round), contra 1.000 a 1.650 h estimadas de empresa.

## Parte II - O que foi feito
1. Copilot do Power Apps avaliado: a edição de app em linguagem natural foi retirada em 06/01/2026; sobra o Copilot da barra de fórmulas (uma propriedade por vez). Caminho promissor para o futuro: ferramentas de código ligadas à coautoria do Studio (a testar no tenant).
2. Celular, publicado e conferido: scrPainel (galPacientes), scrPaciente (ctnCabecalho + 8 contêineres), scrCarteira (galCarteira), scrSintese (ctnSinCab + 4 áreas), scrDuploJ (ctnDuploJ, janela de retirada cabendo na tela), scrPacienteDados (ctnPDCab + ctnPD), scrInicio (legendas dos indicadores).
3. Tempo pós-transplante (aprovado pela equipe): até 3 meses em dias (D45), de 3 a 12 meses em meses completos (7m), 1 ano ou mais em anos e meses (1a 6m); por extenso no Cadastro. Idade em anos completos.
4. Defeito de dado corrigido: dtpPDNasc sem StartYear (padrão 1970) mostrava 01/01/1970 para nascidos antes de 1970 e podia regravar o nascimento ao salvar. StartYear 1920, EndYear Year(Today()). Script de leitura: 12 pacientes, 3 nascidos antes de 1970, nenhum corrompido.
5. Defeito corrigido: quadros de alvo da scrPaciente liam colunas antigas vazias ('Data-alvo de alta ORIGINAL' e 'Data-alvo de alta atual'); passaram a ler DataAlvoAltaOriginal e DataAlvoAltaAtual, como Admissão, Cadastro e Síntese. As colunas antigas da TxPlano parecem sem uso; conferir por script antes de qualquer remoção.
6. Leitura: Carteira com prazo relativo ("vencida há 3 dias (03/11)", "vence hoje", "vence em N dias"); Duplo J com "retirar até dd/mm/aaaa" ou "retirada atrasada desde"; Síntese com "vencido há N dias". Itens descartados por pouco ganho: dias no selo do Painel (já aparecem na linha acima) e ano nas datas de alvo (não cabe no quadro do celular).
7. Botão Sugestão: mantido; Giuseppe avalia a retirada em cerca de 30 dias (nenhuma sugestão registrada até agora).
8. Análise de risco clínico (FMEA) em rascunho: doc 86, 20 modos de falha; prioridades: duplo J não registrado (NPR 60), duplo J de paciente de alta (40), pendência resolvida por engano com um toque na Carteira (36), dado herdado confirmado sem revisão (36), precaução errada sem leitura do BMR (30). Aguarda validação do NSP.
9. Método: doc 84 (padrão de celular, verificador automático); skill power-platform-sharepoint v2.1 (seções 2.4, 8.6, item 15 da auditoria, StartYear/EndYear, correções de 28/09 recuperadas).

## Parte III - Verificador do pacote de 06/11 (antes das correções)
Acessibilidade 874 (igual a 09/10), fórmulas 72 (todas de delegação, cerca de 30 fórmulas filtrando por PacienteRef.Id, PlanoRef.Id ou RoundRef.Id; Síntese concentra 52), desempenho 9 (3 ForAll com Patch, 3 Collect de lista inteira, 1 CountRows de galeria, 1 tela com controles demais), celular cerca de 105.

## Parte III-A - Delegação: dívida aceita (decisão de 06/11, com dados medidos)
Levantamento por script de leitura (pacote 1_0_1, 06/11, 12h30): nenhuma das listas com aviso chega perto do limite de 2000 linhas. TxPendencia 24 linhas, 18 por mês, cerca de 9 anos; TxPlano 13, 9 por mês, cerca de 18 anos; TxRoundPaciente 5, 5 por mês, cerca de 35 anos; TxCriterioAlta 5, 4 por mês, cerca de 43 anos (ritmo inflado por dados de teste e cadastro inicial). A lista que mais cresce, TxAnotacao (78 linhas, 60 por mês, cerca de 32 meses), já usa colunas de número e não gera aviso.
Decisão: os 72 avisos de delegação ficam como dívida aceita. Não recolar a Síntese (tela crítica do round) só por isso: o risco de regressão supera o benefício.
Gatilho de reavaliação: rodar o mesmo script de levantamento a cada 6 meses (próximo em maio/2027), ou antes se o app for expandido para outras unidades ou se qualquer uma dessas listas passar de 1.000 linhas. Se a Síntese for recolada por outro motivo, fazer a troca de carona (colunas PacienteId, RoundId e PlanoId; gravação primeiro, leitura depois).
App novo: nasce com as colunas de número (skill, seção 2.4).

## Parte IV - Próxima sessão
0. **Resumo pré-round (decidido em 06/11, fazer na segunda 09/11):** novo envio no fluxo "Round Transplante - avisos de pendências", às **9h15 do dia do round** (huddle às 9h15 e round na sequência), por e-mail completo e Teams curto, para Giuseppe e Gustavo (destinatários numa linha da TxConfig, ResumoRoundPara). Conteúdo: preenchimento por categoria e paciente; pacientes por prioridade (faixa, dias, leito); desvio de alta com dias de atraso; pendências que bloqueiam a alta com responsável e prazo; alertas de isolamento não avaliado, swab vencido ou sem swab admissional, duplo J perto de D60 ou atrasado, inclusive de pacientes de alta (cobre o risco C4 do doc 86); pacientes sem plano. Primeiro em modo de teste só para o Giuseppe. Base: gerador do doc 83.
1. Exportar o .msapp atualizado e rodar o verificador (celular + resumo do sarif) para medir o efeito das recolagens.
2. scrMatriz no celular.
3. Delegação: dívida aceita (Parte III-A); nada a fazer até o gatilho.
3A. Ajustes de risco do doc 86 num lote: pergunta obrigatória de duplo J no bloco da Medicina (transplante há menos de 90 dias); confirmação em dois toques para resolver pendência que bloqueia a alta; idade do dado herdado. Depois: duplo J de alta no aviso semanal. Levar o doc 86 ao NSP (gerar versão Word se pedirem).
4. Desempenho: trocar os 3 ForAll com Patch por gravação em lote ao recolar as telas correspondentes.
5. Molde de app com os quatro requisitos, antes da Central de Informações.
6. Conferir se a última proposta da skill (StartYear/EndYear) foi salva.

**HUB - Hospital Universitário de Brasília · Ebserh · UnB · SUS**
