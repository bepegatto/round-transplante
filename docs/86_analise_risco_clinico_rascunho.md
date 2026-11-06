# Análise de risco clínico do Round Transplante (FMEA) - RASCUNHO para o Núcleo de Segurança do Paciente
**Round Multiprofissional do Transplante · Unidade de Transplante (UTX) · HUB-UnB · Ebserh**
Versão 0.1 · 06/11/2026 · rascunho elaborado com apoio de assistente de IA a partir do código-fonte do app (pacote 1_0_1) e do histórico de defeitos; **pontuações são estimativas a validar pelo Núcleo de Segurança do Paciente e pela equipe da UTX.**

## 1. Escopo e natureza do sistema
1. O Round Transplante é ferramenta de **organização do round multiprofissional semanal**: registro por categoria, plano de alta com data-alvo, pendências, critérios de alta, painel de duplo J, precaução e alerta de vigilância (swab).
2. **Não é prontuário** e **não prescreve**. O registro oficial continua no AGHU; o app gera um texto que o profissional revisa e copia para o prontuário.
3. Plataforma: Power Apps sobre listas SharePoint no ambiente Microsoft 365 da Ebserh; avisos de pendências por e-mail e Teams (Power Automate).
4. Funções analisadas (influenciam conduta): A. plano de alta e desvio; B. pendências que bloqueiam a alta; C. duplo J; D. precaução e vigilância; E. registro multiprofissional; F. cadastro e infraestrutura.

## 2. Método
FMEA simplificada. Para cada modo de falha: efeito no paciente, causa, controles existentes e três notas de 1 a 5:
- **G - gravidade** do efeito no paciente (1 nenhum dano; 3 atraso ou dano leve evitável; 5 dano grave);
- **O - ocorrência** provável (1 remota; 3 ocasional; 5 frequente);
- **D - detecção** antes do dano (1 quase certa; 3 possível; 5 improvável).

**NPR = G × O × D** (1 a 125). Prioridade: NPR a partir de 30, ou G 5 com qualquer NPR.

## 3. Análise

### A. Plano de alta, data-alvo e desvio
| # | Modo de falha | Efeito no paciente | Causa | Controles existentes | G | O | D | NPR |
|---|---|---|---|---|---|---|---|---|
| A1 | Data-alvo exibida vazia ou errada | Desvio de alta não discutido; internação prolongada | Fórmula lendo coluna errada (**caso real**, corrigido em 06/11) | Síntese mostra os dois alvos; correção publicada | 3 | 1 | 3 | 9 |
| A2 | Alvo original sobrescrito | Perda da linha de base do desvio (afeta indicador, não o paciente) | Edição indevida | O app nunca regrava o alvo original; versões do plano guardadas | 2 | 1 | 4 | 8 |
| A3 | Síntese gravada sem revisão no modo de coordenação ("Gravar e próximo") | Previsão e meta desatualizadas registradas como decididas | Pressa no round | Campos visíveis antes de gravar | 3 | 2 | 3 | 18 |

### B. Pendências que bloqueiam a alta
| # | Modo de falha | Efeito no paciente | Causa | Controles existentes | G | O | D | NPR |
|---|---|---|---|---|---|---|---|---|
| B1 | **Pendência resolvida por engano** (toque acidental em "resolver" na Carteira) | Pendência real (ex.: término de antibioticoterapia) deixa de bloquear a alta; alta antes da hora | Botão de um toque, sem confirmação | "Reabrir" disponível; histórico de versões do SharePoint mostra quem alterou | 4 | 3 | 3 | **36** |
| B2 | Pendência bloqueante não aparece na Síntese | Alta sem resolver a pendência | Erro de carga; filtro | Síntese consulta a lista diretamente; Carteira recarrega ao abrir; aviso semanal por e-mail e Teams | 4 | 1 | 3 | 12 |
| B3 | Pendência sem responsável | Ninguém age | Cadastro incompleto | Fluxo envia à chefia da UTX | 3 | 2 | 2 | 12 |
| B4 | Fluxo de avisos para de rodar | Lembretes não chegam | Falha de conector ou de conta | O app continua sendo o registro; pendências visíveis no round | 2 | 2 | 4 | 16 |

### C. Cateter duplo J
| # | Modo de falha | Efeito no paciente | Causa | Controles existentes | G | O | D | NPR |
|---|---|---|---|---|---|---|---|---|
| C1 | **Duplo J implantado e não registrado no app** | Cateter esquecido: incrustação, obstrução, infecção, novo procedimento | Registro depende de lembrança da Medicina; campo não obrigatório | Seção "Cateter duplo J" no bloco da Medicina | **5** | 3 | 4 | **60** |
| C2 | Inserção sem data | Prazo de retirada não calculado | Data não preenchida | Selo "SEM DATA" no painel | 4 | 2 | 2 | 16 |
| C3 | Retirada registrada por engano ou com data errada | Cateter some do painel estando implantado | Toque na linha errada | Data não pode ser futura nem anterior à inserção; janela de confirmação | 4 | 1 | 3 | 12 |
| C4 | Paciente de alta com duplo J esquecido fora da internação | Retenção prolongada após a alta | Painel só consultado durante a internação | Painel inclui internados e de alta | **5** | 2 | 4 | **40** |

### D. Precaução e vigilância de BMR
| # | Modo de falha | Efeito no paciente | Causa | Controles existentes | G | O | D | NPR |
|---|---|---|---|---|---|---|---|---|
| D1 | Precaução não registrada | Isolamento não instituído; transmissão cruzada | Esquecimento | Faixa "ISOLAMENTO NÃO AVALIADO" no painel e no paciente; Enfermagem não consegue confirmar "sem alteração" sem registrar precaução | 4 | 2 | 2 | 16 |
| D2 | **Precaução registrada errada** (ex.: padrão em paciente colonizado) | Transmissão cruzada de BMR | Informação de cultura não refletida no Round | Rastreio BMR em app separado; integração prevista | **5** | 2 | 3 | **30** |
| D3 | Alerta de swab calculado errado | Coleta de vigilância perdida ou duplicada | Regra de data (âncora semanal, data anterior à internação) | Aviso quando a data gravada é anterior à internação | 3 | 2 | 3 | 18 |

### E. Registro multiprofissional
| # | Modo de falha | Efeito no paciente | Causa | Controles existentes | G | O | D | NPR |
|---|---|---|---|---|---|---|---|---|
| E1 | **Dado herdado do round anterior confirmado sem revisão** ("Sem alteração desde o round anterior") | Informação desatualizada tratada como atual nas decisões | Um toque confirma tudo | Faixa laranja com a data de origem dos dados | 3 | 3 | 4 | **36** |
| E2 | Registro gravado no paciente errado | Decisão baseada em dado de outro paciente | Troca de contexto entre pacientes | Campos reiniciam na troca; nome do paciente no topo | 4 | 1 | 3 | 12 |
| E3 | Texto para o prontuário com erro ou omissão | Registro oficial incompleto | Geração automática | Texto revisável antes de copiar; cópia é ato do profissional | 3 | 2 | 3 | 18 |

### F. Cadastro e infraestrutura
| # | Modo de falha | Efeito no paciente | Causa | Controles existentes | G | O | D | NPR |
|---|---|---|---|---|---|---|---|---|
| F1 | Data de nascimento regravada errada | Idade errada no cadastro | Campo de data limitado a 1970 (**caso real**, corrigido em 06/11; nenhum dado corrompido) | Faixa 1920 a ano atual; conferência por script | 2 | 1 | 3 | 6 |
| F2 | App ou SharePoint indisponível no dia do round | Round sem a síntese estruturada | Falha da plataforma | Cópia de segurança semanal em CSV | 2 | 2 | 1 | 4 |
| F3 | Acesso indevido aos dados | Exposição de dados de saúde | Compartilhamento amplo | Acesso restrito à equipe do Teams; ambiente Ebserh | - | - | - | encaminhar ao encarregado de dados (LGPD) |

## 4. Prioridades e ações propostas
| Prioridade | Item | Ação proposta | Tipo |
|---|---|---|---|
| 1 | C1 (NPR 60, G 5) | Pergunta obrigatória no bloco da Medicina para paciente transplantado nos últimos 90 dias: "Duplo J: implantado / não implantado / retirado", sem permitir gravar em branco | App |
| 2 | C4 (NPR 40, G 5) | Duplo J em uso de pacientes já de alta incluído no aviso semanal (e-mail e Teams), com o prazo de retirada | Fluxo |
| 3 | B1 (NPR 36) | Confirmação em dois toques para "resolver" pendência que bloqueia a alta, com registro de quem resolveu | App |
| 4 | E1 (NPR 36) | Mostrar a idade do dado herdado ("dados de 14 dias atrás") e exigir revisão quando o dado tiver mais de 2 rounds | App |
| 5 | D2 (NPR 30, G 5) | Round passa a ler a precaução e a colonização diretamente do Rastreio BMR (decisão de 29/09 já prevista) | Integração |
| 6 | Todos | Roteiro de teste por publicação incluindo os casos de risco acima; revisão desta análise a cada 6 meses ou a cada função nova | Processo |

## 5. Pendências para validação
1. Validar as notas G, O e D com a equipe da UTX e o Núcleo de Segurança do Paciente.
2. Confirmar se o NSP adota escala própria (1 a 10, por exemplo) e converter.
3. Definir responsável e prazo para cada ação da seção 4.
4. Encaminhar F3 ao encarregado de dados da Ebserh.

Elaborado por: Giuseppe Cesare Gatto (dono do produto), com apoio de assistente de IA.
Revisado por (NSP): ____________________ Data: ___/___/______

**HUB - Hospital Universitário de Brasília · Ebserh · UnB · SUS**
