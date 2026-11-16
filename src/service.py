"""
As requisições de API são feitas aqui
"""

import requests

def get_address(cep:str) -> dict | None:
    url = f"https://viacep.com.br/ws/{cep}/json/"
    # coloquei timeout para não ficar travado
    try:
        response = requests.get(url, timeout=5, verify=False)
        match response.status_code:
            case 200:
                data = resposta.json()
                # O ViaCEP retorna HTTP 200 com {"erro": true} quando o CEP não existe na base, isso vai servir para validar ele
                if dados.get("erro"):
                    raise Exception("CEP inválido")
                return {
                    #coloca o endreco se nao tiver nada coloca vazio
                    "ds_endereco": data.get("ogradouro", "").strip(),
                    "nm_bairro": data.get("bairro", "").strip()
                }
            case 400:
                raise requests.exceptions.HTTPError("Requisição inválida (HTTP 400). Verifique o formato do CEP.")
            case 404:
                raise requests.exceptions.HTTPError("Serviço ou rota do CEP não encontrada (HTTP 404).")
            case 500 | 502 | 503 | 504:
                raise requests.exceptions.HTTPError(f"Servidor do ViaCEP temporariamente indisponível (HTTP {resposta.status_code}).")
            case _:
                raise requests.exceptions.HTTPError(f"Retorno inesperado da API (HTTP {resposta.status_code}).")
    except requests.Timeout as e:
        #vou mandar as mensagens todas pra onde chama
        raise requests.Timeout("Tempo limite esgotado: ", e)
    except requests.ConnectionError as e:
        raise requests.ConnectionError("Sem conexão com a internet: ",e)
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(e)
    except requests.RequestException as e:
        raise requests.RequestException("Falha na requisição: ", e)
