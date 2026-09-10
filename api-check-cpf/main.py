from flask import Flask, request, jsonify

app = Flask(__name__)


def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF tem 11 dígitos e não é uma sequência repetida (ex: 111.111.111-11)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_digito = (soma * 10) % 11
    if primeiro_digito == 10:
        primeiro_digito = 0

    if primeiro_digito != int(cpf[9]):
        return False

    # Calcula o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_digito = (soma * 10) % 11
    if segundo_digito == 10:
        segundo_digito = 0

    if segundo_digito != int(cpf[10]):
        return False

    return True


def formatar_cpf(cpf_limpo):
    # Formata para 111.222.333-44
    return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"


@app.route('/validarcpf', methods=['GET'])
def main():
    cpf_input = request.args.get('cpf')

    # Valida se o parâmetro foi enviado
    if not cpf_input:
        return jsonify({"error": "Parâmetro 'cpf' não informado"}), 400

    cpf_limpo = ''.join(filter(str.isdigit, cpf_input))

    # Valida se tem 11 dígitos antes de qualquer coisa
    if len(cpf_limpo) != 11:
        return jsonify({"error": "CPF deve conter 11 dígitos"}), 400

    valido = validar_cpf(cpf_limpo)

    # Pega o formato desejado via query param: ?formato=limpo | formatado | ambos (padrão: ambos)
    formato = request.args.get('formato', 'ambos').lower()

    resposta = {
        "return": valido
    }

    if formato == 'limpo':
        resposta["cpfClean"] = cpf_limpo

    elif formato == 'formatado':
        resposta["cpfDefault"] = formatar_cpf(cpf_limpo)

    else:  # ambos (padrão)
        resposta["cpfClean"] = cpf_limpo
        resposta["cpfDefault"] = formatar_cpf(cpf_limpo)

    return jsonify(resposta), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5022)