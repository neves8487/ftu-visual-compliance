# FTU Visual Compliance 🔍

Solução de Inteligência Artificial Multimodal desenvolvida para o **Case Study de Prompt Engineering da Altice Labs**, com foco na inspeção e auditoria visual automatizada de instalações de **Fibre Termination Unit (FTU)** em ambientes operacionais de telecomunicações.

🌐 **Demo Online em Produção (Caso esteja em baixo, aguardar uns segundos. Também disponível em dispositivos móveis):** [ftu-visual-compliance.streamlit.app](https://ftu-visual-compliance.streamlit.app/)

---

## 📊 Resumo de Desempenho

| Indicador | Resultado | Impacto |
| :--- | :---: | :--- |
| **Accuracy Global (OK vs NOK)** | **100% (25/25)** | Viável sem aprovação de defeitos |
| **Accuracy por Critério (NOKs)** | **92% (23/25)** | Por vezes nas NOK com bastante "ruído visual" adiciona critérios a mais, mas não chumba nenhuma OK |
| **Taxa de Falsos Negativos** | **0% (0/15)** | Nenhuma instalação com anomalia é aprovada |
| **Taxa de Falsos Positivos** | **0% (0/10)** | Nenhuma instalação conforme foi rejeitada |
| **Tempo Médio de Resposta** | **8s** | Mínimo: 3.16s \| Máximo: 28.70s dependendo da quantidade de ruído da imagem (outros dispositivos, tubos, etc.)|
| **Custo por Imagem** | **~0,0052 €** | Meio cêntimo de euro |
| **Modelo Multimodal** | `gemini-3.8-flash` | Equilíbrio ótimo entre capacidades de raciocínio espacial e latência |

---

## 🎯 Entregáveis Pedidos no Case Study (1 a 7)

### 1. Final Prompt (Prompt Final de Inspeção)
O prompt final encontra-se versionado e documentado em [`prompt_avaliacao.txt`](prompt_avaliacao.txt).

Principais características técnicas da engenharia do prompt:
- **Âncora de Escala Relativa (100 × 100 mm):** Usa as dimensões físicas conhecidas do corpo do FTU como régua proporcional de referência geométrica para o modelo inferir profundidade e distâncias no espaço 3D da foto.
- **Hierarquia de Autoridade (Template vs. Parede Nua):** Quando existe o autocolante impresso, as suas linhas de demarcação têm autoridade máxima. Em paredes nuas, é ativado o teste visual onde é usada a FTU como escala para medições e limites.
- **Explicação Eficiente:** Explicações técnicas estritas de no máximo 12 palavras, reduzindo o consumo de tokens de saída e a latência de inferência.

---

### 2. Models and Configurations Used (Modelos e Configurações)
Sobre o modelo usado
- **Modelo:** `Google Gemini 3.8 Flash` (`gemini-3.8-flash`).
- **SDK / API:** `google-genai` SDK oficial para Python.
- **Temperatura:** `temperature=0.0` no `GenerateContentConfig`, garantindo respostas consistentes e eliminação de alucinações.
- **Otimização e Pré-processamento de Imagem:** Redimensionamento preservando o rácio de aspeto para resolução máxima de 1080p (`max_dim=1080`) com interpolação `Image.Resampling.LANCZOS` (em [`gemini_service.py`](gemini_service.py)), reduzindo os tempos de transferência de rede e limitando os tokens visuais consumidos.

---

### 3. Results for Each Image (Resultados Detalhados das 25 Imagens)

Avaliação completa do dataset oficial de 25 imagens:

| Imagem | Resultado Global | Critérios Falhados Identificados pelo Modelo | Explicação Técnica Fornecida | Tempo (s) |
| :---: | :---: | :--- | :--- | :---: |
| **1.JPG** | ❌ **NOK** | Multiple FTUs visible | Two FTUs are visible side by side in the image. | 5.63s |
| **2.JPG** | ❌ **NOK** | Free space around the FTU | Black router mounted directly above FTU encroaches on required clearance space. | 18.65s |
| **3.JPG** | ❌ **NOK** | Free space around the FTU<br>Screw inside safe area | Horizontal cable duct crosses within 250 mm clearance below FTU.<br>Cable clip is mounted within 125 mm directly below FTU base. | 10.98s |
| **4.JPG** | ❌ **NOK** | Screw inside safe area<br>*(Free space around the FTU-ERRADO)* | Cable clip installed less than 125 mm below FTU base.<br>*(Pipe encroaches within 20 mm lateral margin on right)* | 28.70s |
| **5.JPG** | ❌ **NOK** | Screw inside safe area | Cable clip screw installed in prohibited zone directly below FTU. | 6.36s |
| **6.jpeg**| ❌ **NOK** | Correct FTU orientation | FTU is mounted sideways with text oriented vertically. | 7.46s |
| **7.jpeg**| ❌ **NOK** | FTU closed | Front protective cover is missing, exposing internal fiber tray. | 3.78s |
| **8.JPG** | ❌ **NOK** | Free space around the FTU<br>*(Screw inside safe area-ERRADO)* | Pipes encroach within 20 mm lateral clearance zone of FTU.<br>*(Cable clip mounted within prohibited zone directly below FTU)* | 8.87s |
| **9.JPG** | ❌ **NOK** | Free space around the FTU | Vertical conduit on left encroaches within 20 mm lateral margin. | 7.37s |
| **10.JPG**| ❌ **NOK** | Free space around the FTU | Pipes on both sides encroach within 20 mm lateral clearance margin. | 5.71s |
| **11.jpg**| ❌ **NOK** | Free space around the FTU | Grey conduit encroaches within 20 mm lateral clearance margin. | 6.21s |
| **12.jpeg**| ❌ **NOK** | FTU visible in the image | FTU is severely cropped with only bottom rim visible. | 3.16s |
| **13.jpeg**| ❌ **NOK** | FTU closed | Front protective cover is missing, exposing internal fiber tray. | 4.65s |
| **14.jpeg**| ❌ **NOK** | Correct FTU orientation | FTU is mounted sideways with vertical text and cable exiting horizontally. | 3.83s |
| **15.jpeg**| ❌ **NOK** | FTU closed | Front protective cover is missing and internal fibers are exposed. | 4.33s |
| **100.JPG**| ✅ **OK** | *Nenhum (Conforme)* | All 6 criteria verified and compliant. | 7.80s |
| **101.JPG**| ✅ **OK** | *Nenhum (Conforme)* | All 6 criteria verified and compliant. | 3.98s |
| **102.JPG**| ✅ **OK** | *Nenhum (Conforme)* | All 6 criteria verified and compliant. | 17.10s |
| **103.JPG**| ✅ **OK** | *Nenhum (Conforme)* | All 6 criteria verified and compliant. | 12.85s |
| **104.JPG**| ✅ **OK** | *Nenhum (Conforme)* | All 6 criteria verified and compliant. | 13.77s |
| **105.JPG**| ✅ **OK** | *Nenhum (Conforme)* | All 6 criteria verified and compliant. | 4.42s |
| **106.JPG**| ✅ **OK** | *Nenhum (Conforme)* | All 6 criteria verified and compliant. | 5.11s |
| **107.jpg**| ✅ **OK** | *Nenhum (Conforme)* | All 6 criteria verified and compliant. | 4.97s |
| **108.JPG**| ✅ **OK** | *Nenhum (Conforme)* | All 6 criteria verified and compliant. | 4.90s |
| **109.JPG**| ✅ **OK** | *Nenhum (Conforme)* | All 6 criteria verified and compliant. | 9.79s |

---

### 4. Evaluation Summary & Error Analysis (Resumo e Discussão Técnica)

- **Classificação Global (OK vs NOK): 25/25 (100%)** — Sucesso.
- **Concordância Exata nos Critérios NOK: 13/15 (86.7%)** (ou **23/25 = 92%** considerando todo o dataset).
- **Análise dos Casos no Limite (`4.JPG` e `8.JPG`):**
  - O modelo identificou corretamente que ambas as instalações eram **NOK** e acertou o defeito principal de cada uma.
  - No entanto, devido à ausência do autocolante e à presença de elevado "ruído visual" (cablagens desorganizadas, tubos de eletricidade e água no mesmo painel), o modelo adotou uma postura **hiper-conservadora**: na `4.JPG` sinalizou o cano lateral adjacente como violação de espaço livre, e na `8.JPG` calculou no limite a distância do parafuso como inferior a 125 mm.
  - **Conclusão Técnica:** Em contexto de auditoria técnica de qualidade, um modelo com viés conservador em instalações marginais e ruidosas é preferível a um modelo permissivo que deixe passar defeitos físicos.

---

### 5. Response-Time Measurements (Medições de Latência)

- **Tempo Total para Avaliar o Dataset (25 imagens):** ~3.5 minutos.
- **Tempo Médio por Imagem:** **8 segundos**.
- **Imagem Mais Rápida:** `12.jpeg` (**3.16s**).
- **Imagem Mais Lenta:** `4.JPG` (**28.70s**).

---

### 6. Approach and Iterations (Abordagem e Engenharia de Prompt)

O desenvolvimento seguiu a ordem:

- **Iteração 1 (Estrutura e Parsing):** Saída com análise explícita de todos os 6 critérios. Identificou-se que gerar explicações extensas para critérios conformes causava latência desnecessária.
- **Iteração 2 (Otimização de Latência por Filtragem Negativa):** Reformulação do formato de saída para emitir explicações **exclusivamente para critérios NOK**. Se tudo estiver OK, o modelo retorna apenas uma linha padrão. Isso reduziu os tokens de geração e acelerou a resposta.
- **Iteração 3 (Autoridade de autocolante - *Template vs Bare Wall*):** Introdução da distinção entre instalações com autocolante de papel e paredes nuas. A folha adesiva passou a ser tratada como autoridade geométrica máxima, eliminando tentativas de estimar milímetros em adesivos impressos.
- **Iteração 4 (Correção da Distribuição Espacial e Zonas do NT):** Com base no diagrama técnico dimensional de 350 × 140 × 100 mm, esclareceu-se que a zona proibida para parafusos é estritamente os primeiros 125 mm abaixo da base do FTU (zona do NT), sendo a metade inferior do adesivo permitida.
- **Iteração 5 (General Improvements):** Para paredes nuas, instruiu-se o modelo a empilhar mentalmente a altura de uma caixa FTU (100 mm) como régua visual comparativa.
- **Iteração 6 (Resizing):** Integração de redimensionamento da imagem para 1080p

---

### 7. Minimal Script & Execution Instructions (Como Reproduzir)

#### Opção A: Aceder à Aplicação na Nuvem (Sem Instalação)
Aceda diretamente a [ftu-visual-compliance.streamlit.app](https://ftu-visual-compliance.streamlit.app/) e carregue as imagens para inspecionar.

#### Opção B: Executar Localmente em 3 Passos

1. **Clonar o Repositório e Instalar Dependências:**
   ```bash
   git clone https://github.com/neves8487/ftu-visual-compliance.git
   cd ftu-visual-compliance
   pip install -r requirements.txt
   ```

2. **Configurar a Chave de API:**
   Crie um ficheiro `.env` na raiz do projeto (ou copie de `.env.example`):
   ```env
   GEMINI_API_KEY="sua_chave_do_google_ai_studio"
   ```

3. **Executar a Aplicação:**
   ```bash
   python -m streamlit run app.py
   ```
   Aceda a `http://localhost:8501` no navegador.
