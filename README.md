# CPF API Git Tags

Laboratório em Flask para testar operações com CPF e praticar versionamento usando Git, tags do GitHub e Docker.

## Objetivo

O projeto recebe um CPF, remove caracteres de formatação para trabalhar apenas com os 11 dígitos e valida os dígitos verificadores. A mesma API também consegue devolver o CPF em seus dois formatos:

- **Limpo:** `11122233344`
- **Formatado:** `111.222.333-44`

Assim, o laboratório representa as duas operações comuns de tratamento do CPF: adicionar a pontuação e removê-la.

> No código atual, essas operações estão concentradas na rota `/validarcpf` e são selecionadas pelo parâmetro `formato`. Ainda não existem duas rotas HTTP independentes.

## Tecnologias

- Python 3.11
- Flask
- Docker e Docker Compose
- `python-dotenv`

## Como funciona

1. A aplicação recebe o CPF pelo parâmetro de consulta `cpf`.
2. Todos os caracteres que não são números são removidos.
3. A aplicação verifica se restaram exatamente 11 dígitos.
4. Os dois dígitos verificadores são calculados e comparados com o CPF informado.
5. A resposta informa se o CPF é válido e pode trazer o valor limpo, formatado ou ambos.

## Executando localmente

Entre no diretório da aplicação, crie um ambiente virtual e instale as dependências:

```bash
cd api-check-cpf
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

A API ficará disponível em `http://localhost:5022`.

## Executando com Docker

Para executar a imagem localmente:

```bash
cd api-check-cpf
docker build -t api-check-cpf .
docker run --rm -p 5022:5022 api-check-cpf
```

O arquivo `compose.yaml` é usado no ambiente de publicação. Ele utiliza variáveis definidas no arquivo `.env`, conecta o serviço à rede externa `api-cpf-net` e configura o acesso HTTPS pelo Traefik.

## Endpoint

### `GET /validarcpf`

Valida o CPF e retorna o formato solicitado.

| Parâmetro | Obrigatório | Valores | Padrão |
| --- | --- | --- | --- |
| `cpf` | Sim | CPF com ou sem pontuação | - |
| `formato` | Não | `limpo`, `formatado` ou `ambos` | `ambos` |

### Exemplos

Retornar os dois formatos:

```bash
curl "http://localhost:5022/validarcpf?cpf=11144477735"
```

Resposta:

```json
{
	"return": true,
	"cpfClean": "11144477735",
	"cpfDefault": "111.444.777-35"
}
```

Retornar apenas o CPF formatado:

```bash
curl "http://localhost:5022/validarcpf?cpf=11144477735&formato=formatado"
```

Retornar apenas o CPF sem pontuação:

```bash
curl "http://localhost:5022/validarcpf?cpf=111.444.777-35&formato=limpo"
```

## Erros de entrada

Quando o parâmetro `cpf` não é enviado, a API retorna HTTP `400`. O mesmo status é usado quando o valor não contém exatamente 11 dígitos após a limpeza.

Exemplo:

```json
{
	"error": "CPF deve conter 11 dígitos"
}
```

## Estrutura

```text
api-check-cpf/
├── compose.yaml       # Configuração de publicação com Docker Compose e Traefik
├── Dockerfile         # Imagem da aplicação
├── env_example        # Variáveis esperadas no ambiente de publicação
├── main.py            # Aplicação Flask e regra de validação do CPF
└── requirements.txt   # Dependências Python
```

## Tags e versões

As tags registram versões do laboratório. Para consultar as versões disponíveis:

```bash
git tag
```

Para executar uma versão específica:

```bash
git checkout v1.0.1
```
