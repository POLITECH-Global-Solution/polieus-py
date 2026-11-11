"""
Garante que os dados sejam do tipo que as regras de negócio podem
"""

CATEGORIAS = ("Pavimentação", "Iluminação", "Acessibilidade", "Saneamento")
STATUS = ("Registrada", "Em análise", "Aprovada", "Em execução", "Concluída", "Não aprovada")

# PROVISÓRIO
def valid_data(categoria: str, descricao: str, bairro: str, gravidade: int) -> tuple[bool, str]:
    """Valida tipos, formatos e regras dos dados de uma ocorrência."""
    # 1. Validação de tipo e conteúdo da Descrição
    if not isinstance(descricao, str) or len(descricao.strip()) < 5:
        return False, "A descrição deve ser um texto com pelo menos 5 caracteres."

    # 2. Validação de tipo e conteúdo do Bairro
    if not isinstance(bairro, str) or len(bairro.strip()) == 0:
        return False, "O bairro deve ser informado corretamente."

    # 3. Validação de pertencimento à Tupla de Categorias
    if categoria not in CATEGORIAS_PERMITIDAS:
        return False, f"Categoria inválida. Escolha entre: {', '.join(CATEGORIAS_PERMITIDAS)}"

    # 4. Validação de tipo e faixa de valores da Gravidade (Int de 1 a 5)
    if not isinstance(gravidade, int) or not (1 <= gravidade <= 5):
        return False, "A gravidade deve ser um número inteiro entre 1 e 5."

    # Se passou por todas as checagens:
    return True, "Dados válidos"