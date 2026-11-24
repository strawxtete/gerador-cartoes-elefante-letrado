import re
from pathlib import Path
from typing import List
from urllib.parse import quote

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.config import GRID_COLS, GRID_ROWS
from src.extractor import extrair_alunos
from src.pdf_builder import gerar_pdf_dos_alunos

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = BASE_DIR / "public"


class AlunoItem(BaseModel):
    nome: str
    senha: str


class GerarPdfRequest(BaseModel):
    alunos: List[AlunoItem]
    nome_arquivo: str = "cartoes"


def limpar_nome_arquivo(texto: str, padrao: str = "cartoes") -> str:
    limpo = re.sub(r'[\\/*?:"<>|]+', "", texto.strip())
    limpo = " ".join(limpo.split())
    return limpo or padrao


@app.post("/api/extrair")
async def api_extrair(arquivo: UploadFile = File(...)):
    if not arquivo.filename or not arquivo.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Envie um arquivo PDF válido.")
    try:
        conteudo = await arquivo.read()
        alunos, esperado, turma = extrair_alunos(conteudo, arquivo.filename)
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"Não foi possível ler o PDF: {exc}"
        ) from exc

    return {
        "alunos": [{"nome": n, "senha": s} for n, s in alunos],
        "esperado": esperado,
        "turma": turma,
    }


@app.post("/api/gerar-pdf")
async def api_gerar_pdf(dados: GerarPdfRequest):
    pares = [
        (item.nome.strip(), item.senha.strip())
        for item in dados.alunos
        if item.nome.strip() and item.senha.strip()
    ]
    if not pares:
        raise HTTPException(
            status_code=400,
            detail="A lista está vazia. Preencha ao menos um aluno.",
        )
    try:
        pdf_bytes = gerar_pdf_dos_alunos(pares)
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Erro ao gerar os cartões: {exc}"
        ) from exc

    nome_limpo = limpar_nome_arquivo(dados.nome_arquivo, "cartoes")
    por_pagina = GRID_COLS * GRID_ROWS
    paginas = (len(pares) + por_pagina - 1) // por_pagina
    nome_codificado = quote(f"{nome_limpo}.pdf")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{nome_codificado}",
            "X-Total-Cartoes": str(len(pares)),
            "X-Total-Paginas": str(paginas),
            "X-Nome-Arquivo": quote(f"{nome_limpo}.pdf"),
        },
    )


if PUBLIC_DIR.exists():
    @app.get("/")
    async def servir_index():
        return FileResponse(PUBLIC_DIR / "index.html")

    app.mount("/", StaticFiles(directory=str(PUBLIC_DIR), html=True), name="public")
