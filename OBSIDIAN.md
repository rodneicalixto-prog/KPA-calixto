# Usando este repositório como vault do Obsidian

Este repositório já pode ser aberto como um vault do Obsidian — toda a
estrutura do kit (`00_OS/`, `04_DIRETRIZES/`, `05_WORKSPACE/`, `06_OUTPUTS/`
etc.) é feita de arquivos Markdown com links relativos, que é exatamente
o que o Obsidian espera de um vault.

## Como abrir

1. Baixe e instale o Obsidian (https://obsidian.md) na sua máquina — isso
   não pode ser feito remotamente, precisa ser na sua própria máquina.
2. No Obsidian, escolha **Open folder as vault**.
3. Selecione a pasta raiz deste repositório (`KPA-calixto`).
4. Comece por `00_INDEX.md` — é o ponto de entrada do kit.

## O que já está preparado

- `.obsidian/app.json` — config mínima padrão, só pra o Obsidian reconhecer
  a pasta como vault sem overrides forçados. Ajuste as preferências do
  Obsidian (tema, plugins, etc.) normalmente pela interface do app depois
  de abrir.

## O que não foi feito aqui

- Nenhum plugin do Obsidian foi instalado ou configurado.
- Nenhum conteúdo `.md` existente foi alterado por causa disso.
- A instalação do próprio aplicativo Obsidian é responsabilidade sua, feita
  localmente — esta sessão roda num container remoto sem interface gráfica.
