# Round Transplante

App de round multiprofissional da Unidade de Transplante (UTX) do HUB-UnB · Ebserh.
Canvas app do Power Apps sobre listas SharePoint e fluxos do Power Automate, no ambiente Microsoft 365 da Ebserh.

**Repositório privado de trabalho.** O app em produção vive no Power Apps; aqui fica o código-fonte exportado a cada sessão, os scripts, as ferramentas e os documentos de método, para histórico e rastreabilidade.

## Regra que não se negocia
**Nenhum dado de paciente entra neste repositório.** Só código-fonte das telas (`.pa.yaml`), scripts, geradores e documentos de método. Resultados de script com nomes, prontuários ou datas de pacientes nunca são versionados.

## Estrutura
| Pasta | Conteúdo |
|---|---|
| `app/Src/` | Código-fonte das telas, extraído do `.msapp` exportado (uma tela por arquivo) |
| `scripts/console/` | Scripts REST para o console do navegador (sempre em dois tempos: LISTAR e APLICAR) |
| `fluxos/` | Geradores de pacote do Power Automate |
| `ferramentas/` | Verificadores e utilitários (ex.: verificador de layout no celular) |
| `docs/` | Método, fechamentos de sessão, análise de risco |

## Como atualizar a cada sessão
1. Exportar o `.msapp` no início da sessão.
2. Extrair `Src/*.pa.yaml` para `app/Src/` e fazer o commit com a data e o assunto da sessão.
3. Registrar a sessão em `REGISTRO_SESSOES.md` (data, início, fim, app, tipo de trabalho).

Responsável: Giuseppe Cesare Gatto. Desenvolvimento com apoio de assistente de IA.
