import io
import os
import re
from typing import List, Optional, Tuple

import pdfplumber

ALUNO_PATTERN = re.compile(
    r"(?P<matricula>\d{9})\s+"
    r"(?P<nome>[^\d]+?)\s+"
    r"(?P<carteirinha>[A-Za-z]{2}\d{7})"
)

TOTAL_PATTERN = re.compile(r"Nome\s*\((\d+)\)")
TURMA_PATTERN = re.compile(r"Turma:\s*([^\r\n]+)", re.IGNORECASE)
TURMA_CURTA_PATTERN = re.compile(
    r"\b(\d+\s*[º°]?\s*(?:ANO|SÉRIE|SERIE)\s*[A-Z0-9]+)\b", re.IGNORECASE
)


def extrair_nome_turma(texto: str, nome_arquivo: str = "") -> str:
    m = TURMA_PATTERN.search(texto)
    if m:
        bruto = " ".join(m.group(1).split())
        curto = TURMA_CURTA_PATTERN.search(bruto)
        if curto:
            return " ".join(curto.group(1).split())
        limpo = re.sub(
            r"\b(ANUAL|SEMESTRAL|TARDE|MANHÃ|MANHA|INTEGRAL|MATUTINO|VESPERTINO)\b",
            "",
            bruto,
            flags=re.IGNORECASE,
        )
        limpo = " ".join(limpo.split()).strip(" -_/")
        if limpo:
            return limpo

    if nome_arquivo:
        base = os.path.splitext(nome_arquivo)[0].strip()
        if base:
            return base
    return "Turma"


def extrair_alunos(
    pdf_bytes: bytes, nome_arquivo: str = ""
) -> Tuple[List[Tuple[str, str]], Optional[int], str]:
    textos = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            textos.append(page.extract_text() or "")
    texto = "\n".join(textos)

    totais = TOTAL_PATTERN.findall(texto)
    esperado = sum(int(t) for t in totais) if totais else None
    turma = extrair_nome_turma(texto, nome_arquivo)

    alunos: List[Tuple[str, str]] = []
    for m in ALUNO_PATTERN.finditer(texto):
        nome = " ".join(m.group("nome").split())
        alunos.append((nome, m.group("carteirinha").upper()))

    return alunos, esperado, turma
