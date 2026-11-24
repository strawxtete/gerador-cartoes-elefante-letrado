# Elefante Letrado - Gerador de Cartões de Acesso

Aplicação web desenvolvida com **FastAPI (Python)** e interface **Web Responsiva (HTML/CSS/JS)** para automatizar a criação de cartões de acesso (Login e Senha) dos alunos na plataforma **Elefante Letrado**, prontos para impressão em folhas A4 (grade 2x3) e preparada para hospedagem gratuita na **Vercel**.

---

## Funcionalidades

- **Geração em lote via PDF**: Lê automaticamente o arquivo PDF *Relação de Usuários da Escola*, extrai o nome da turma, os nomes dos alunos e os códigos das carteirinhas, permite revisar/editar a tabela na tela e gera um único PDF para impressão nomeado com a turma (ex.: `1 ANO A.pdf`).
- **Geração individual (Manual)**: Permite preencher o nome e a carteirinha de um único aluno e exportar o cartão em PDF com o nome do estudante.
- **Carregamento Instantâneo e Zero Marca d'Água**: Interface estática servida diretamente via CDN com API Serverless em Python.
- **Modo Escuro e Modo Claro**: Alternância direta de tema no canto superior direito da tela (iniciando por padrão no Modo Escuro).
- **Design 100% Responsivo**: Interface adaptada para uso tanto no computador quanto no celular (smartphones e tablets).
- **Privacidade e LGPD**: Todo o processamento dos arquivos e imagens ocorre 100% em memória (`io.BytesIO`), sem salvar dados de alunos no disco ou servidor.

---

## Como Hospedar Gratuitamente na Vercel

1. Acesse [vercel.com](https://vercel.com/) e faça login com sua conta do **GitHub**.
2. Clique em **Add New...** -> **Project**.
3. Selecione o repositório **`gerador-cartoes-elefante-letrado`** e clique em **Import**.
4. Não é necessário alterar nenhuma configuração (o arquivo `vercel.json` já configura tudo automaticamente). Basta clicar em **Deploy**.

---

## Como Executar Localmente

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
python app.py
```

Acesse no navegador:
```text
http://127.0.0.1:8000
```
