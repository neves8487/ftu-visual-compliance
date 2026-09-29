#APP STREAMLIT PARA AVALIAÇÃO DE FTU INSTALLATIONS

import os
import sys
import time
from pathlib import Path
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
# Importação do serviço de IA desenvolvido
from gemini_service import avaliar_imagem
# Garante que imports locais funcionem sem erro no streamlit
sys.path.append(str(Path(__file__).resolve().parent))

# Carrega variáveis do arquivo .env, se existir
load_dotenv()

# ==============================================================================
# Configuração da Página
# ==============================================================================
st.set_page_config(
    page_title="FTU Install Evaluation",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Avaliação de Instalação de FTU")
st.markdown("Carregue uma ou mais imagens para avaliação da instalação.")

# ==============================================================================
# Barra Lateral: Configurações
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Configurações")

    # Verifica se a chave existe no ambiente (.env) ou no Streamlit Secrets (na cloud)
    chave_servidor = os.getenv("GEMINI_API_KEY", "")
    if not chave_servidor:
        try:
            if "GEMINI_API_KEY" in st.secrets:
                chave_servidor = st.secrets["GEMINI_API_KEY"]
        except Exception:
            chave_servidor = ""

    if chave_servidor:
        api_key = chave_servidor
        st.success("🟢 API Conectada")
    else:
        api_key = st.text_input(
            "GEMINI_API_KEY",
            type="password",
            help="Insira a sua chave de API do Google Gemini."
        )

    MODELO = "gemini-3.8-flash"
    st.info("🤖 **Modelo:** Google Gemini 3.8 Flash")


# ==============================================================================
# Upload de Imagens (múltiplas)
# ==============================================================================
ficheiros_imagem = st.file_uploader(
    "Selecione uma ou mais imagens (.jpg, .jpeg, .png)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Carrega e mostra as imagens em grelha (thumbnails)
imagens: list[tuple[str, Image.Image]] = []
if ficheiros_imagem:
    colunas = st.columns(min(len(ficheiros_imagem), 4) if len(ficheiros_imagem) >= 4 else 4)
    for i, ficheiro in enumerate(ficheiros_imagem):
        try:
            img = Image.open(ficheiro)
            imagens.append((ficheiro.name, img))
            with colunas[i % len(colunas)]:
                st.image(img, caption=ficheiro.name, width=150)
        except Exception as e:
            st.error(f"Erro ao abrir '{ficheiro.name}': {e}")

botao_avaliar = st.button(
    f"🚀 Avaliar {'Imagens' if len(imagens) != 1 else 'Imagem'} ({len(imagens)})",
    type="primary",
    use_container_width=True,
    disabled=(len(imagens) == 0)
)

# ==============================================================================
# Chamada à IA e Apresentação dos Resultados
# ==============================================================================
if "resultados" not in st.session_state:
    st.session_state["resultados"] = {}

if botao_avaliar:
    if not api_key.strip():
        st.error("Por favor, introduza a sua GEMINI_API_KEY na barra lateral.")
    elif not imagens:
        st.warning("Carregue pelo menos uma imagem antes de avaliar.")
    else:
        barra_progresso = st.progress(0, text="A iniciar avaliação...")
        total = len(imagens)

        for idx, (nome, img) in enumerate(imagens):
            barra_progresso.progress(
                (idx) / total,
                text=f"A avaliar {nome} ({idx + 1}/{total})..."
            )
            inicio = time.perf_counter()
            try:
                resultado = avaliar_imagem(
                    api_key=api_key.strip(),
                    modelo=MODELO,
                    imagem=img
                )
                duracao = time.perf_counter() - inicio
                st.session_state["resultados"][nome] = {
                    "texto": resultado,
                    "tempo": duracao
                }
            except Exception as e:
                duracao = time.perf_counter() - inicio
                st.session_state["resultados"][nome] = {
                    "texto": f"❌ Erro: {e}",
                    "tempo": duracao
                }

        barra_progresso.progress(1.0, text="Avaliação concluída!")

# Exibe os resultados se existirem
if st.session_state.get("resultados"):
    st.markdown("---")
    st.subheader("📋 Relatórios de Avaliação")

    for nome, dados in st.session_state["resultados"].items():
        if isinstance(dados, dict):
            texto = dados.get("texto", "")
            tempo = dados.get("tempo", 0.0)
            titulo = f"📄 {nome} — ⏱️ {tempo:.2f}s"
        else:
            texto = str(dados)
            titulo = f"📄 {nome}"

        with st.expander(titulo, expanded=True):
            st.markdown(texto)

