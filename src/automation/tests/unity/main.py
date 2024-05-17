import requests
from pyscript import document
from requests.exceptions import RequestException
import urllib3

# Supress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def gerar_resposta(event):
    pergunta = document.getElementById('pergunta').value
    api_key = 'AIzaSyCLvfwuw4z2wQcixVttPHQHbC9qFUdNZ18'  # Substitua pela sua chave de API
    resposta = gerar_conteudo(pergunta, api_key)
    output_div = document.getElementById('resposta')
    output_div.innerText = resposta

def gerar_conteudo(text, api_key):
    """Gera conteúdo usando a API do Gemini Pro."""

    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
    headers = {'Content-Type': 'application/json'}
    data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': text
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, params={'key': api_key}, verify=False)
        response.raise_for_status()

        # Verifica a estrutura da resposta para obter o texto correto
        resposta_json = response.json()
        if 'candidates' in resposta_json and len(resposta_json['candidates']) > 0:
            return resposta_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return 'Erro: Estrutura de resposta inesperada.'
    except RequestException as e:
        return f'Erro na requisição: {e}'
    except KeyError as e:
        return f'Erro na estrutura da resposta: {e}'
