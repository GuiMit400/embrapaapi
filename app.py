from flask import Flask, jsonify, request
from flasgger import Swagger
import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask_httpauth import HTTPBasicAuth
import os

auth = HTTPBasicAuth()
USERS = {
    "admin":"secret",
    "user": "password"
}

@auth.verify_password
def verify_password(username,password):
    if username in USERS and USERS[username] == password:
        return username
    return None

app = Flask(__name__)

swagger = Swagger(app)



def extrair_dados(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {"class": "tb_base tb_dados"})

    if table:
        rows = table.find_all('tr')
        data = [[cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])] for row in rows]
        return pd.DataFrame(data)
    return None


@app.route('/producao/<int:ano>', methods=['GET'])
@auth.login_required
def producao(ano):
    """
    Retorna dados de produção para o ano especificado
    ---
    parameters:
      - name: ano
        in: path
        type: integer
        required: true
        description: Ano dos dados de produção
    responses:
      200:
        description: Dados de produção para o ano especificado
        schema:
          type: array
          items:
            type: object
      404:
        description: Dados não encontrados
    """
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02'
    df = extrair_dados(url)
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({"error": "Dados não encontrados"}), 404


@app.route('/processamento/<int:subopt>/<int:ano>', methods=['GET'])
@auth.login_required
def processamento(subopt, ano):
    """
    Retorna dados de processamento para o subtipo e ano especificado
    ---
    parameters:
      - name: subopt
        in: path
        type: integer
        required: true
        description: Subtipo de processamento
      - name: ano
        in: path
        type: integer
        required: true
        description: Ano dos dados de processamento
    responses:
      200:
        description: Dados de processamento para o subtipo e ano especificado
        schema:
          type: array
          items:
            type: object
      404:
        description: Dados não encontrados
    """
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao=subopt_0{subopt}'
    df = extrair_dados(url)
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({"error": "Dados não encontrados"}), 404


@app.route('/comercializacao/<int:ano>', methods=['GET'])
@auth.login_required
def get_comercializacao(ano):
    """
    Retorna dados de processamento para o subtipo e ano especificado
    ---
    parameters:
      - name: subopt
        in: path
        type: integer
        required: true
        description: Subtipo de processamento
      - name: ano
        in: path
        type: integer
        required: true
        description: Ano dos dados de processamento
    responses:
      200:
        description: Dados de processamento para o subtipo e ano especificado
        schema:
          type: array
          items:
            type: object
      404:
        description: Dados não encontrados
    """
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_04'
    df = extrair_dados(url)
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({"error": "Dados não encontrados"}), 404


@app.route('/importacao/<int:subopt>/<int:ano>', methods=['GET'])
@auth.login_required
def get_importacao(subopt, ano):
    """
    Retorna dados de processamento para o subtipo e ano especificado
    ---
    parameters:
      - name: subopt
        in: path
        type: integer
        required: true
        description: Subtipo de processamento
      - name: ano
        in: path
        type: integer
        required: true
        description: Ano dos dados de processamento
    responses:
      200:
        description: Dados de processamento para o subtipo e ano especificado
        schema:
          type: array
          items:
            type: object
      404:
        description: Dados não encontrados
    """
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_0{subopt}'
    df = extrair_dados(url)
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({"error": "Dados não encontrados"}), 404


@app.route('/exportacao/<int:subopt>/<int:ano>', methods=['GET'])
@auth.login_required
def get_exportacao(subopt, ano):
    """
    Retorna dados de processamento para o subtipo e ano especificado
    ---
    parameters:
      - name: subopt
        in: path
        type: integer
        required: true
        description: Subtipo de processamento
      - name: ano
        in: path
        type: integer
        required: true
        description: Ano dos dados de processamento
    responses:
      200:
        description: Dados de processamento para o subtipo e ano especificado
        schema:
          type: array
          items:
            type: object
      404:
        description: Dados não encontrados
    """
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao=subopt_0{subopt}'
    df = extrair_dados(url)
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({"error": "Dados não encontrados"}), 404


if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="http://127.0.0.1:5000", port=port)