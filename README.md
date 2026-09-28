# FTU Visual Compliance 🔍

Aplicação interativa desenvolvida em **Streamlit** e integrada com o **Google Gemini Multimodal** para auditoria visual e verificação de conformidade técnica em imagens.

---

## 🛠️ Tecnologias Utilizadas

- **Interface**: [Streamlit](https://streamlit.io/)
- **Modelo de IA Multimodal**: [Google GenAI SDK](https://github.com/google/google-genai) (`gemini-2.5-flash`)
- **Processamento de Imagem**: Pillow (PIL)
- **Configuração de Ambiente**: Python Dotenv

---

## 🚀 Como Executar Localmente

### 1. Clonar o Repositório e Instalar Dependências

```bash
git clone https://github.com/<SEU_UTILIZADOR>/ftu-visual-compliance.git
cd ftu-visual-compliance
pip install -r requirements.txt
```

### 2. Configurar a Chave de API

Pode obter uma chave gratuita no [Google AI Studio](https://aistudio.google.com/).

- **Opção A (Recomendada)**: Copie o ficheiro `.env.example` para `.env` e insira a sua chave:
  ```env
  GEMINI_API_KEY="sua_chave_aqui"
  ```
- **Opção B**: Insira a chave diretamente no campo seguro disponível na barra lateral da aplicação.

### 3. Iniciar a Aplicação

```bash
streamlit run app.py
```

Aceda a `http://localhost:8501` no seu navegador.

---

## ☁️ Deploy no Streamlit Community Cloud

1. Conecte o repositório `ftu-visual-compliance` à sua conta [Streamlit Community Cloud](https://share.streamlit.io/).
2. Defina o **Main file path** como `app.py`.
3. Em **Advanced Settings** > **Secrets**, configure:
   ```toml
   GEMINI_API_KEY = "sua_chave_aqui"
   ```
4. Clique em **Deploy**!
