"""
Serviço de Integração com Google Gemini Multimodal
Responsável pela comunicação com a Google GenAI SDK.
"""

from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types
# Carrega o prompt de avaliação a partir do ficheiro de texto
_PROMPT_PATH = Path(__file__).resolve().parent / "prompt_avaliacao.txt"
PROMPT_AVALIACAO = _PROMPT_PATH.read_text(encoding="utf-8")


def redimensionar_imagem(imagem: Image.Image, max_dim: int = 1080) -> Image.Image:
    """
    Redimensiona a imagem para caber numa resolução máxima (ex: 1080p),
    mantendo o rácio de aspeto (aspect ratio) e máxima nitidez (LANCZOS).
    Reduz drasticamente o tempo de upload e o consumo de tokens sem perder detalhes.
    """
    if max(imagem.size) > max_dim:
        img_copia = imagem.copy()
        img_copia.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        return img_copia
    return imagem


def avaliar_imagem(api_key: str, modelo: str, imagem: Image.Image) -> str:
    """
    Envia a imagem otimizada com as regras do prompt para o Gemini.

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

    # Redimensiona para 1080p para acelerar upload e inferência
    imagem_otimizada = redimensionar_imagem(imagem, max_dim=1080)

    # Lê sempre a versão mais recente do ficheiro de prompt
    prompt_atual = _PROMPT_PATH.read_text(encoding="utf-8")

    resposta = client.models.generate_content(
        model=modelo,
        contents=[imagem_otimizada, prompt_atual],
        config=types.GenerateContentConfig(
            temperature=0.0,
        ),
    )

    return resposta.text

