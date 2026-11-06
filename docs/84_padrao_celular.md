# Padrão de celular (responsividade) - Round Transplante e apps da UTX (06/11/2026)
**Complemento obrigatório do doc 66 (seção 6.9 até a versão 3 do guia). Ler junto com ele ao abrir ou retomar qualquer app.**

## 1. O erro que se repetia
O app foi desenhado no Studio em 1366 de largura, com "Ajustar à tela" desligado (app responsivo, MinScreenWidth 320). No celular a tela tem cerca de 360 a 390 de largura útil. Três defeitos apareceram em quase todas as telas:
1. **Largura que encolhe demais**: `Parent.Width - 450` (ou `TemplateWidth - 240`) fica negativa ou mínima no celular. O nome do paciente sumiu do painel por isso.
2. **Texto variável em altura fixa**: rótulo com nome, título ou linha de dados em `Height` fixa quebra em duas linhas no celular e a segunda é cortada.
3. **Botão ao lado do título**: no celular o botão ocupa a largura do título e fica por cima dele.

Agravante: a fonte do sistema do celular pode estar ampliada; o mesmo `Size` ocupa mais espaço no aparelho do que no Studio. Por isso a altura nunca pode depender de o texto caber em uma linha.

## 2. Regra permanente (toda tela nova ou recolada)
1. **Um ponto de corte**: `App.Width < 600` = celular. No computador, o desenho atual fica intacto (todo valor novo vai em `If(App.Width < 600, <celular>, <computador>)`).
2. **Nada de largura `Parent.Width - N` com N grande**: no celular, largura = `Parent.Width - 48` (margens de 24) ou divisão da linha (`(Parent.Width - 64) / 3` para três botões).
3. **Todo rótulo de texto variável** (nome, título, item de galeria, resumo) com `AutoHeight: =App.Width < 600`.
4. **Empilhar em cascata**: no celular, o Y de cada controle vem do de cima (`Y: =lblA.Y + lblA.Height + 8`). Nunca Y fixo abaixo de um texto variável.
5. **Botões ao lado do título descem** para uma linha própria no celular, lado a lado e com altura 40 a 44.
6. **Galerias**: `TemplateSize` maior no celular (itens em três ou quatro linhas) e itens empilhados; selos e ações em linha própria.
7. **Cabeçalho de controles soltos** vai para um contêiner manual (`GroupContainer@1.5.0`, Variant `ManualLayout`) com `Height` igual ao fundo do último controle; o conteúdo abaixo usa `Y: =ctnCabecalho.Height + 8` e `Height: =Parent.Height - Self.Y - 8`.
8. **Fonte mínima 12 e toque mínimo 40 a 44** no celular (seção 6.8 do doc 66).
9. **Teste no celular antes de dar a tela por pronta**: publicar, fechar e reabrir o app no aparelho, print de cada tela alterada.

## 3. Rito de execução que funcionou (06/11)
1. Recolar o **maior bloco** que resolve (galeria inteira ou cabeçalho inteiro), apagando o antigo antes.
2. Controle colado direto na tela fica na frente de tudo: **Reordenar → Enviar para trás** (senão cobre as janelas sobrepostas de Saída, Dispositivo e Sugestão).
3. Ajuste da mesma propriedade em vários controles: **seleção múltipla na Árvore** (clique + Shift) e uma fórmula só na barra (funcionou com os 8 contêineres de categoria).
4. Fórmulas sem separador (`ctnCabecalho.Height + 8`) servem nos dois dialetos. Fórmula com separador na barra em pt-BR exige `;` (erro de 06/11: `If(gPDEdit, 80, 0)` foi entregue com vírgula e falhou; certo é `If(gPDEdit; 80; 0)`).
5. Publicar só depois que a tela inteira estiver coerente (cabeçalho e conteúdo juntos).

## 4. Auditoria automática a cada pacote
O script abaixo roda sobre o `.msapp` extraído e aponta os três defeitos por tela. Entra na auditoria do pacote (doc 66, seção 6.7, item novo): **zero apontamentos nas telas novas ou recoladas**.

Resultado no pacote de 06/11/2026 (antes das correções do dia): scrPaciente 48, scrSintese 15, scrDuploJ 12, scrMatriz 12, scrCarteira 8, scrPainel 5, scrPacienteDados 4, scrInicio 1, scrAdmissao 0, scrMetodo 0. Heurístico: aponta candidatos, a decisão é por tela.

```python
import yaml, glob, re, sys
from collections import Counter
src = sys.argv[1]  # pasta do .msapp extraído
for f in sorted(glob.glob(src + '/Src/scr*.pa.yaml')):
    d = yaml.safe_load(open(f)); scr = list(d['Screens'])[0]; out = []
    def walk(ch):
        for c in ch:
            n = list(c)[0]; v = c[n]; p = v.get('Properties', {}); ctl = v['Control']
            if n.startswith(('ctnSug', 'recSug', 'lblSug', 'txtSug', 'btnSug')): continue
            w = str(p.get('Width', '')); t = str(p.get('Text', ''))
            if 'App.Width < 600' not in w:
                m = re.search(r'(Parent\.(?:Template)?Width)\s*-\s*(\d+)', w)
                if m and int(m.group(2)) >= 150: out.append((n, 'largura encolhe demais'))
                m2 = re.fullmatch(r'=(\d+)', w)
                if m2 and int(m2.group(1)) >= 300: out.append((n, 'largura fixa grande'))
            if ctl.startswith('Label') and 'AutoHeight' not in p:
                h = re.fullmatch(r'=(\d+)', str(p.get('Height', '=40')))
                if re.search(r'ThisItem|\bg[A-Z]|&', t) and h and int(h.group(1)) <= 40:
                    out.append((n, 'texto variável em altura fixa'))
            walk(v.get('Children', []))
    walk(d['Screens'][scr]['Children'])
    print(scr, len(out), dict(Counter(x[1] for x in out)))
    for x in out: print('   ', x[0], '-', x[1])
```

## 5. Estado das correções (06/11/2026, fim da manhã)
1. Publicados e conferidos no celular: scrPainel (galPacientes); scrPaciente (ctnCabecalho + 8 contêineres de categoria); scrCarteira (galCarteira); scrSintese (ctnSinCab + 4 áreas de conteúdo, inclusive Anterior e Gravar e próximo no modo de coordenação); scrDuploJ (ctnDuploJ inteiro, janela de retirada cabendo na tela); scrPacienteDados (ctnPDCab + ctnPD); scrInicio (altura das legendas dos indicadores).
2. Botão Sugestão: não mexer; Giuseppe avalia a retirada em cerca de 30 dias.
3. Tempo pós-transplante (aprovado pela equipe em 06/11): até 3 meses em dias (D45); de 3 a 12 meses em meses completos (7m); 1 ano ou mais em anos e meses (1a 6m). Por extenso no Cadastro ("1 ano e 6 meses pós-transplante"). Meses completos = DateDiff em meses menos 1 se o dia de hoje for menor que o dia da data. Idade no Cadastro corrigida para anos completos.
4. Defeito de dado encontrado e corrigido: dtpPDNasc sem StartYear (padrão 1970) mostrava 01/01/1970 para nascidos antes de 1970, e "Salvar alterações" podia regravar o nascimento. Corrigido com StartYear 1920 e EndYear Year(Today()). Conferência por script: 12 pacientes, 3 nascidos antes de 1970, nenhum com nascimento em 01/01/1970, nenhum corrompido.
5. Pendentes: Matriz (11 rótulos); quadros de alvo vazios na scrPaciente (a Síntese do mesmo paciente mostra os alvos; correção provável: usar o mesmo plano carregado pela Síntese); melhorias de apresentação propostas em 06/11: prazo relativo na Carteira ("vencida há 3 dias"), "retirar até dd/mm" no Duplo J, tamanho do desvio na Síntese ("vencido há 8 dias"), dias no selo de faixa do Painel, ano nas datas fora do ano corrente.
6. Regra nova para apps: prazo sempre relativo a hoje; tempo longo em unidade legível; todo alerta diz o porquê; DatePicker sempre com StartYear e EndYear.

**HUB - Hospital Universitário de Brasília · Ebserh · UnB · SUS**
