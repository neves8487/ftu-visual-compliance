"""
Serviço de Integração com Google Gemini Multimodal
Responsável pela comunicação com a Google GenAI SDK.
"""

from PIL import Image
from google import genai

# Regras e critérios de avaliação definidos diretamente no prompt
PROMPT_AVALIACAO = """
Age como um treinador.
Analisa a imagem fornecida de acordo com as seguintes regras e parâmetros:

1. Qualidade Técnica: Foco, nitidez, iluminação e ausência de borrões ou ruído.
2. Composição e Enquadramento: Centralização e destaque dos elementos principais.
3. Conformidade Visual: Identifica anomalias, defeitos ou elementos impróprios.

Para cada parâmetro:
- Atribui uma pontuação de 0 a 10.
- Fornece uma breve justificativa objetiva.
- Conclui com um Veredito Final: [APROVADO], [REPROVADO] ou [REQUER REVISÃO].
"""


def avaliar_imagem(api_key: str, modelo: str, imagem: Image.Image) -> str:
    """
    Envia a imagem com as regras pré-definidas diretamente no prompt para o Gemini.

    Args:
        api_key (str): Chave de API do Google Gemini.
        modelo (str): Nome do modelo (ex: 'gemini-2.5-flash').
        imagem (Image.Image): Objeto de imagem PIL.

    Returns:
        str: Resposta textual da avaliação.
    """
    if not api_key:
        raise ValueError("A chave de API do Gemini não foi fornecida.")

    client = genai.Client(api_key=api_key.strip())

    resposta = client.models.generate_content(
        model=modelo,
        contents=[imagem, PROMPT_AVALIACAO]
    )

    return resposta.text
