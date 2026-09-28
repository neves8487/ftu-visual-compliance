"""
Serviço de Integração com Google Gemini Multimodal
Responsável pela comunicação com a Google GenAI SDK.
"""

from pathlib import Path

from PIL import Image
from google import genai

# Carrega o prompt de avaliação a partir do ficheiro de texto
_PROMPT_PATH = Path(__file__).resolve().parent / "prompt_avaliacao.txt"
PROMPT_AVALIACAO = _PROMPT_PATH.read_text(encoding="utf-8")


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

