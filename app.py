import os
import sys
from pathlib import Path
from PIL import Image
import streamlit as st
from dotenv import load_dotenv

# Garante que imports locais funcionem sem erro
sys.path.append(str(Path(__file__).resolve().parent))

# Importação do serviço de IA (as regras estão fixas dentro do gemini_service.py)
from gemini_service import avaliar_imagem

# Carrega variáveis do arquivo .env, se existir
load_dotenv()

# ==============================================================================
# Configuração da Página
# ==============================================================================
st.set_page_config(
    page_title="Avaliação de Imagens - Gemini",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Avaliador de Imagens com Google Gemini")
st.markdown("Carregue uma imagem para avaliação visual automática.")

# ==============================================================================
# Barra Lateral: Configurações
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Se a chave já existir no servidor (Streamlit Secrets ou .env), usa-a diretamente
    chave_servidor = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    
    if chave_servidor:
        api_key = chave_servidor
        st.success("🟢 API Conectada")
    else:
        # Só exibe o campo se o servidor não tiver a chave configurada
        api_key = st.text_input(
            "GEMINI_API_KEY",
            type="password",
            help="Insira a sua chave de API do Google Gemini."
        )
    
    modelo = st.selectbox(
        "Modelo Multimodal",
        options=["gemini-2.5-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.6-flash", "gemini-3.7-flash"],
        index=0
    )

# ==============================================================================
# Upload da Imagem
# ==============================================================================
ficheiro_imagem = st.file_uploader(
    "Selecione uma imagem (.jpg, .jpeg, .png)",
    type=["jpg", "jpeg", "png"]
)

imagem_carregada = None
if ficheiro_imagem is not None:
    try:
        imagem_carregada = Image.open(ficheiro_imagem)
        st.image(imagem_carregada, caption=f"Imagem: {ficheiro_imagem.name}", use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao abrir a imagem: {e}")

botao_avaliar = st.button(
    "🚀 Avaliar Imagem",
    type="primary",
    use_container_width=True,
    disabled=(imagem_carregada is None)
)

# ==============================================================================
# Chamada à IA e Apresentação do Resultado
# ==============================================================================
if botao_avaliar:
    if not api_key.strip():
        st.error("Por favor, introduza a sua GEMINI_API_KEY na barra lateral.")
    elif imagem_carregada is None:
        st.warning("Carregue uma imagem antes de avaliar.")
    else:
        with st.spinner(f"A avaliar a imagem com o modelo {modelo}..."):
            try:
                # Chama a IA diretamente (as regras estão fixas no gemini_service)
                resultado = avaliar_imagem(
                    api_key=api_key.strip(),
                    modelo=modelo,
                    imagem=imagem_carregada
                )
                st.session_state["resultado_gemini"] = resultado
            except Exception as e:
                st.error(f"Erro na avaliação da imagem: {e}")

# Exibe o resultado se já existir na sessão
if "resultado_gemini" in st.session_state:
    st.markdown("---")
    st.subheader("📋 Relatório de Avaliação")
    st.markdown(st.session_state["resultado_gemini"])
