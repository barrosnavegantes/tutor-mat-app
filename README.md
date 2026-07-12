<p align="center">
  <img src="https://img.shields.io/badge/model-LFM%202.5-6366f1?style=flat-square" alt="LFM 2.5">
  <img src="https://img.shields.io/badge/ollama-local%20AI-000000?style=flat-square&logo=ollama" alt="Ollama">
  <img src="https://img.shields.io/badge/react-19-61DAFB?style=flat-square&logo=react" alt="React 19">
  <img src="https://img.shields.io/badge/vite-8-646CFF?style=flat-square&logo=vite" alt="Vite 8">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT">
</p>

<h1 align="center">📐 Tutor de Matemática<br><sub>Math Tutor — Local AI for Public Exam Preparation</sub></h1>

<p align="center">
  <strong>🇺🇸 English</strong> &nbsp;|&nbsp; <a href="#portugues">🇧🇷 Português</a>
</p>

<hr>

<h2 id="english">🇺🇸 English</h2>

### 📖 About

**Math Tutor** is a web application that uses **100% local artificial intelligence** (via [Ollama](https://ollama.com)) to teach math in a didactic way to public exam candidates.

The core idea: adapt small-parameter AI models — such as **LFM 2.5 (8B)** — for real educational contexts, proving that a high-quality private tutor can run entirely on your own computer, without paid APIs or internet dependency.

The tutor was originally configured with the exam syllabus for the **São Domingos do Capim City Council Public Exam (Notice 001/2026)**, but can be easily adapted to any syllabus — just replace the `public/pdf_content.txt` file with your desired program content.

### ✨ Features

- ⚡ **100% local AI** — no internet, no costs, no request limits
- 📚 **Syllabus-aware** — the tutor knows the exam's program content
- 💬 **Real-time streaming** — responses appear token by token, with the model's reasoning visible
- 🧮 **LaTeX support** — math formulas rendered with KaTeX (e.g. $$A = \pi r^2$$)
- 🎨 **Modern UI** — dark theme, responsive, markdown support (tables, lists, code)
- 🧠 **Visible thinking** — the model's reasoning appears before the final answer

### 🛠️ Stack

| Layer | Technology |
|---|---|
| Frontend | React 19 + Vite 8 + CSS Modules |
| Backend | Express 5 (API proxy) |
| AI | Ollama + LFM 2.5 (8B, Q4_K_M) |
| Rendering | KaTeX (LaTeX) + React-Markdown |
| Tunnel (optional) | Cloudflare Tunnel (`cloudflared`) |

### 📦 Installation (1 command)

```bash
git clone https://github.com/josenavegantes/tutor-matematica.git
cd tutor-matematica
python3 setup.py

# (Optional) Also start a Cloudflare tunnel
python3 setup.py --cloudflared
```

**Prerequisites:** Python 3.8+, ~8 GB free RAM, ~15 GB free disk.

The `setup.py` script handles:
1. Install/update Node.js (v22+)
2. Install npm dependencies
3. Build frontend (Vite)
4. Install Ollama (if needed)
5. Download the LFM 2.5 model (~5.2 GB)
6. Create the custom `tutor-matematica` model
7. Start the server at `http://localhost:5173`

### 🚀 Usage

1. Open `http://localhost:5173`
2. The tutor greets you with a welcome message
3. Ask anything about the exam's math topics
4. The tutor responds step by step, with practical examples and exercises at the end

### 👥 Authors

<p>
  <strong>José Navegantes Junior</strong> and <strong>Dayane Barros</strong><br>
  <em>Belém — Pará — Brazil 🇧🇷</em>
</p>

**José Navegantes Junior** is a former state employee, approved in 3 public exams. Although his academic background is in law, he has had a strong interest in computing since childhood. He realized that programming was an excellent way to study and enhance learning — and that is how the idea of combining local AI with exam preparation was born.

**Dayane Barros** is a Systems Analysis student who shares José's enthusiasm for programming and artificial intelligence. Together, they publish this code with the goal of helping teachers, exam candidates, and anyone who wants to study math more efficiently with the support of local, free AI.

### 📄 License

MIT — feel free to use, modify, and share.

---

<hr>

<h1 align="center">📐 Tutor de Matemática — Concurso Público CMSDC 2026</h1>

Chatbot educacional de matemática focado no **Concurso Público da Câmara Municipal de São Domingos do Capim (Edital 001/2026)**. O tutor usa IA local via [Ollama](https://ollama.com) para ensinar matemática de forma didática, paciente e prática, com exemplos do dia a dia administrativo.

## ✨ Funcionalidades

- 🎓 Chat com IA especializada em matemática para concursos públicos
- 📊 Renderização de fórmulas matemáticas com **KaTeX**
- 📝 Suporte a Markdown (tabelas, listas, código)
- 🌐 Interface em português brasileiro
- 🖥️ Roda 100% local com Ollama (privacidade total)
- 📚 Contexto completo do edital carregado no prompt

## 📋 Conteúdos abordados

- Operações básicas (adição, subtração, multiplicação, divisão)
- Sistema Monetário Nacional
- Porcentagem, juros simples e compostos
- Regra de três e proporcionalidade
- Raciocínio lógico
- E muito mais!

## 🚀 Pré-requisitos

- [Node.js](https://nodejs.org/) v18+
- [Ollama](https://ollama.com) instalado e rodando
- Modelo `LFM2.5-8B-A1B:ctx131k` baixado no Ollama (ou `tutor-matematica` criado a partir dele)

### Configurando o modelo

```bash
# Baixar o modelo base (8B parâmetros, otimizado para raciocínio)
ollama pull LFM2.5-8B-A1B:ctx131k

# Criar o modelo tutor-matematica com parâmetros otimizados
ollama create tutor-matematica -f Modelfile
```

Exemplo de `Modelfile`:

```
FROM LFM2.5-8B-A1B:ctx131k
PARAMETER temperature 0.5
PARAMETER top_p 0.9
```

## 🔧 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/tutor-mat-app.git
cd tutor-mat-app

# Instale as dependências
npm install

# Faça o build de produção
npm run build

# Inicie o servidor
npm start
```

O servidor estará disponível em `http://localhost:5173`.

## 📜 Scripts disponíveis

| Comando         | Descrição                            |
| --------------- | ------------------------------------ |
| `npm run dev`   | Inicia o servidor de desenvolvimento |
| `npm run build` | Gera build de produção               |
| `npm start`     | Inicia o servidor de produção        |
| `npm run lint`  | Roda o linter (Oxlint)               |

## 🛠️ Stack

- **Frontend:** React 19 + Vite
- **Backend:** Express (proxy para Ollama)
- **UI:** CSS puro com tema escuro
- **Renderização:** react-markdown + remark-gfm + rehype-katex + KaTeX
- **IA:** Ollama (modelo local)

## 📁 Estrutura do projeto

```
tutor-mat-app/
├── public/
│   ├── favicon.svg
│   ├── icons.svg
│   └── pdf_content.txt      # Conteúdo do edital
├── src/
│   ├── assets/
│   ├── App.jsx               # Componente principal
│   ├── App.css               # Estilos do chat
│   ├── main.jsx              # Entry point React
│   └── index.css             # Estilos globais
├── server.js                 # Servidor Express (produção)
├── index.html
├── vite.config.js
└── package.json
```

---

<hr>

<h2 id="portugues">🇧🇷 Português</h2>

### 📖 Sobre o Projeto

O **Tutor de Matemática** é uma aplicação web que utiliza **inteligência artificial 100% local** (via [Ollama](https://ollama.com)) para ensinar matemática de forma didática a candidatos de concursos públicos.

A proposta é simples: adaptar modelos de IA de poucos parâmetros — como o **LFM 2.5 (8B)** — para um contexto educacional real, mostrando que é possível ter um tutor particular de qualidade rodando inteiramente no seu computador, sem depender de APIs pagas ou internet.

O tutor foi originalmente configurado com o edital do **Concurso Público da Câmara Municipal de São Domingos do Capim (Edital 001/2026)**, mas pode ser adaptado para qualquer edital com facilidade — basta substituir o arquivo `public/pdf_content.txt` pelo conteúdo programático desejado.

### ✨ Funcionalidades

- ⚡ **IA 100% local** — sem internet, sem custos, sem limites de requisição
- 📚 **Contextualizado no edital** — o tutor conhece o conteúdo programático do concurso
- 💬 **Streaming em tempo real** — respostas aparecem letra por letra, com o raciocínio do modelo visível
- 🧮 **Suporte a LaTeX** — fórmulas matemáticas renderizadas com KaTeX (ex: $$A = \pi r^2$$)
- 🎨 **Interface moderna** — dark theme, responsivo, com suporte a markdown (tabelas, listas, código)
- 🧠 **Thinking visível** — o raciocínio do modelo aparece antes da resposta final

### 🛠️ Stack

| Camada | Tecnologia |
|---|---|
| Frontend | React 19 + Vite 8 + CSS Modules |
| Backend | Express 5 (proxy API) |
| IA | Ollama + LFM 2.5 (8B, Q4_K_M) |
| Renderização | KaTeX (LaTeX) + React-Markdown |
| Tunnel (opcional) | Cloudflare Tunnel (`cloudflared`) |

### 📦 Instalação (1 comando)

```bash
git clone https://github.com/josenavegantes/tutor-matematica.git
cd tutor-matematica
python3 setup.py

# (Opcional) Iniciar também o túnel Cloudflare
python3 setup.py --cloudflared
```

**Pré-requisitos:** Python 3.8+, ~8 GB RAM livre, ~15 GB de disco.

O script `setup.py` cuida de:
1. Instalar/atualizar Node.js (v22+)
2. Instalar dependências npm
3. Buildar o frontend (Vite)
4. Instalar Ollama (se necessário)
5. Baixar o modelo LFM 2.5 (~5.2 GB)
6. Criar o modelo customizado `tutor-matematica`
7. Iniciar o servidor em `http://localhost:5173`

### 🚀 Uso

1. Abra `http://localhost:5173`
2. O tutor te recebe com uma mensagem de boas-vindas
3. Pergunte qualquer coisa sobre os tópicos de matemática do edital
4. O tutor responde passo a passo, com exemplos práticos e exercícios ao final

### 👥 Autores

<p>
  <strong>José Navegantes Junior</strong> e <strong>Dayane Barros</strong><br>
  <em>Belém — Pará — Brasil 🇧🇷</em>
</p>

**José Navegantes Junior** é ex-servidor estadual, aprovado em 3 concursos públicos. Apesar de sua formação ser na área jurídica, desde pequeno sempre teve forte interesse pela computação. Percebeu que programação era um excelente meio de estudar e potencializar o aprendizado — e foi assim que nasceu a ideia de unir IA local com preparação para concursos.

**Dayane Barros** é estudante de Análise de Sistemas e compartilha com José o entusiasmo por programação e inteligência artificial. Juntos, publicam este código com o objetivo de auxiliar professores, concurseiros e qualquer pessoa que deseje estudar matemática de forma mais eficiente com o apoio de IA local e gratuita.

### 📄 Licença

MIT — sinta-se livre para usar, modificar e compartilhar.
