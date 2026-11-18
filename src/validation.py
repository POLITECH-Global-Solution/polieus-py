"""
Garante que os dados sejam do tipo que as regras de negócio podem ser e de acordo com o que tem no banco
"""
from persistence import find_categories

STATUS = ("PENDENTE", "EM_ANALISE", "EM_ANDAMENTO", "CONCLUIDA", "NAO_APROVADA")

def load_categories() -> tuple[str, ...]:
    # pega apenas os nomes do banc e guarda como tupla (imutável)
    return tuple(find_categories().values())

def valid_occurrence(st_ocorrencia:str,ds_protocolo:str,ds_ocorrencia,nm_bairro:str,nm_categoria:str,ds_endereco:str) -> tuple[bool, str]:
    """Valida tipos, formatos e regras dos dados de uma ocorrência."""
    # tamanho da descrição
    if len(ds_ocorrencia.strip()) < 5:
       raise ValueError("A descrição deve ser um texto com pelo menos 5 caracteres.")

    # ve se bairro ta vazio
    if len(nm_bairro.strip()) == 0:
        raise ValueError("O bairro deve ser informado corretamente.")

    # ve se tem aquela categoria no banco
    categories = load_categories()
    if nm_categoria not in categories:
        raise ValueError(f"Categoria inválida. Escolha entre: {', '.join(categories)}")

    # ve se a ocorrencia é valida
    if st_ocorrencia not in STATUS:
        raise ValueError("A gravidade deve ser um número inteiro entre 1 e 5.")

    return True, "Dados válidos"

