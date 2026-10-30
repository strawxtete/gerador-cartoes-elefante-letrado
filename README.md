# Elefante Letrado - Gerador de Cartões de Acesso

Aplicação web desenvolvida em Python com **Streamlit** para automatizar a criação de cartões de acesso (Login e Senha) dos alunos na plataforma **Elefante Letrado**, prontos para impressão em folhas A4 (grade 2x3).

---

## Funcionalidades

- **Geração em lote via PDF**: Lê automaticamente o arquivo PDF *Relação de Usuários da Escola*, extrai o nome da turma, os nomes dos alunos e os códigos das carteirinhas, permite revisar/editar a tabela na tela e gera um único PDF para impressão nomeado com a turma.
- **Geração individual (Manual)**: Permite preencher o nome e a carteirinha de um único aluno e exportar o cartão em PDF com o nome do estudante.
- **Modo Escuro e Modo Claro**: Alternância direta de tema no canto superior direito da tela (iniciando por padrão no Modo Escuro).
- **Design 100% Responsivo**: Interface adaptada para uso tanto no computador quanto no celular (smartphones e tablets), com botões e campos otimizados para toque.
- **Privacidade e LGPD**: Todo o processamento dos arquivos e imagens ocorre 100% em memória (`io.BytesIO`), sem salvar dados de alunos no disco ou servidor.

---

## Pré-requisitos

- **Python 3.10** ou superior instalado.

---

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/strawxtete/gerador-cartoes-elefante-letrado.git
cd gerador-cartoes-elefante-letrado
```

### 2. Criar e ativar um ambiente virtual (opcional, mas recomendado)

**No Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**No Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Iniciar a aplicação

```bash
streamlit run app.py
```

O sistema abrirá automaticamente no navegador no endereço:
```text
http://localhost:8501
```
└── .gitignore                  # Arquivos ignorados pelo Git
```
