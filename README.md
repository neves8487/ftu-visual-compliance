# FTU Visual Compliance 🔍

Solução de Inteligência Artificial Multimodal desenvolvida para o **Case Study de Prompt Engineering da Altice Labs**, com foco na inspeção e auditoria visual automatizada de instalações de **Fibre Termination Unit (FTU)**.

A aplicação avalia fotografias de instalações reais, classificando cada verificação como **OK** ou **NOK**, com explicações técnicas concisas e medição de tempo de resposta fim-a-fim (*end-to-end*).

---

## 📋 Critérios de Inspeção Avaliados

A solução inspeciona rigorosamente os **6 critérios oficiais** definidos pela Altice Labs:

1. **FTU visible in the image:** O corpo do FTU deve estar claramente visível e enquadrado (sem cortes severos, oclusões totais ou desfoque impeditivo).
2. **Multiple FTUs visible:** Exatamente um FTU deve estar presente para evitar ambiguidades.
3. **FTU closed:** A tampa de proteção frontal deve estar devidamente instalada e fechada (sem expor a bandeja de fusão ou fibra interna).
4. **Correct FTU orientation:** Montagem na vertical com texto horizontal e entrada/saída de cabo diretamente por baixo.
5. **Free space around the FTU:** Volume de desobstrução de pelo menos **350 × 140 × 100 mm** (A × L × P), garantindo 20 mm de margem lateral e ~250 mm livres abaixo da base do FTU para futuros equipamentos ativos (NT/ONT).
6. **Screw inside safe area:** Avaliação de clips/parafusos de fixação do cabo de fibra. A zona imediatamente abaixo da base do FTU até ~125 mm (1.25× a altura do FTU) é reservada ao NT (**proibida**). Fixações na parte inferior do gabarito ou a mais de 125 mm da base são **permitidas**.

---

## 🧠 Arquitetura e Estratégia de Engenharia de Prompt

- **Modelo Multimodal:** `Google Gemini 3.8 Flash` — escolhido pelo equilíbrio perfeito entre acuidade espacial geométrica, velocidade de resposta e custo ultra-baixo.
- **Configuração de Inferência Determinística:** Execução com `temperature=0.0` no SDK para garantir repetibilidade, consistência e ausência de alucinações.
- **Otimização de Imagem (LANCZOS 1080p):** Pré-processamento automático das imagens preservando o rácio de aspeto. Reduz a latência de upload e o consumo de tokens sem perder detalhes finos.
- **Regras de Precedência (*Stop Rules*):** Prevenção de erros em cascata (ex.: se o FTU estiver cortado no enquadramento, não avalia espaço livre como falha secundária).
- **Calibração Espacial Relativa:** Uso de testes visuais baseados na proporção do próprio corpo do FTU (100 × 100 mm), permitindo aferir distâncias em paredes sem escala métrica explícita.
- **Medição de Desempenho Integrada:** Cada imagem avaliada apresenta o tempo exato de resposta (*end-to-end latency* em segundos).

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Interface Web:** [Streamlit](https://streamlit.io/)
- **SDK Multimodal:** [Google GenAI SDK](https://github.com/google/google-genai) (`google-genai`)
- **Processamento de Imagem:** Pillow (PIL)
- **Variáveis de Ambiente:** Python Dotenv

---

## 🚀 Como Executar Localmente

### 1. Clonar o Repositório e Instalar Dependências

```bash
git clone https://github.com/neves8487/ftu-visual-compliance.git
cd ftu-visual-compliance
pip install -r requirements.txt
```

### 2. Configurar a Chave de API

Obtenha uma chave gratuita no [Google AI Studio](https://aistudio.google.com/).

- **Opção A (Ficheiro `.env`):** Crie um ficheiro `.env` na raiz do projeto com:
  ```env
  GEMINI_API_KEY="sua_chave_de_api_aqui"
  ```
- **Opção B (Interface):** Insira a chave diretamente no campo seguro na barra lateral da aplicação.

### 3. Iniciar a Aplicação

```bash
python -m streamlit run app.py
```

Aceda a `http://localhost:8501` no seu navegador.

---

## ☁️ Deploy no Streamlit Community Cloud

1. Conecte o repositório `ftu-visual-compliance` à sua conta [Streamlit Community Cloud](https://share.streamlit.io/).
2. Defina o **Main file path** como `app.py`.
3. Em **Advanced Settings** > **Secrets**, configure:
   ```toml
   GEMINI_API_KEY = "sua_chave_de_api_aqui"
   ```
4. Clique em **Deploy**!
