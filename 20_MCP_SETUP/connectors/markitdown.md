# MarkItDown MCP — Conversor de documentos para Markdown

Fork usado: https://github.com/rodneicalixto-prog/markitdown (upstream: microsoft/markitdown).

## Por que usar

Converte PDF, PowerPoint, Word, Excel, imagens (OCR), audio (transcricao), HTML, CSV/JSON/XML, ZIP, EPub e URLs do YouTube pra Markdown limpo. Usar quando o mentorado cola um PDF de briefing, planilha, deck ou print de concorrente e precisa virar texto que o Claude consegue ler direto.

## Pre-requisitos

Python 3.10+.

## Setup

Instalar o pacote MCP (via pip, do fork):

```bash
pip install "markitdown-mcp @ git+https://github.com/rodneicalixto-prog/markitdown.git#subdirectory=packages/markitdown-mcp"
```

Ou clonar e instalar em modo dev (se for ajustar algo no fork):

```bash
git clone https://github.com/rodneicalixto-prog/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
pip install -e 'packages/markitdown-mcp'
```

Registrar o MCP no Claude Code (STDIO, modo padrao):

```bash
claude mcp add markitdown -- markitdown-mcp
```

## Tools

| Tool | Funcao |
|---|---|
| `convert_to_markdown` | Converte um `uri` (`http:`, `https:`, `file:` ou `data:`) pra Markdown |

## Casos de uso

### Ler briefing em PDF do mentorado

```text
Converte file:///caminho/para/briefing-cliente.pdf pra Markdown.
Extrai: oferta, publico, objecoes, prazos.
Preenche o context pack do cliente com o que achar.
```

### Ler planilha de metricas

```text
Converte file:///caminho/para/relatorio-meta-ads.xlsx pra Markdown.
Resume as metricas principais por campanha.
```

### Ler pagina/print de concorrente salvo localmente

```text
Converte file:///caminho/para/pagina-concorrente.html pra Markdown.
Documenta oferta, preco e prova social.
```

## Seguranca

- **So aceita `file:` de caminho que o mentorado autorizou explicitamente.** Nunca apontar pra pasta fora do escopo combinado.
- **`markitdown-mcp` roda com os privilegios do processo atual** (mesmo aviso do `open()`/`requests.get()`) — nao apontar pra arquivo/URL nao confiavel.
- Por padrao roda em STDIO local. Se usar modo `--http`, mantem em `127.0.0.1` — nunca expor em interface publica.
- Nao commitar os arquivos convertidos se tiverem dado sensivel do cliente; salvar em `05_WORKSPACE/clientes/<cliente>/`.
