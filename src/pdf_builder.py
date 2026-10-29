import io
from typing import List, Tuple

import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from src.card_generator import carregar_modelo_bytes, gerar_cartao, layout_atual
from src.config import CELL_PADDING, DRAW_CUT_GUIDES, GRID_COLS, GRID_ROWS, PAGE_MARGIN


def montar_pdf(cartoes: List[io.BytesIO]) -> bytes:
    saida = io.BytesIO()
    c = canvas.Canvas(saida, pagesize=A4)
    page_w, page_h = A4

    cell_w = (page_w - 2 * PAGE_MARGIN) / GRID_COLS
    cell_h = (page_h - 2 * PAGE_MARGIN) / GRID_ROWS
    por_pagina = GRID_COLS * GRID_ROWS

    for i, cartao in enumerate(cartoes):
        posicao = i % por_pagina

        if i > 0 and posicao == 0:
            c.showPage()

        col = posicao % GRID_COLS
        linha = posicao // GRID_COLS

        x_cell = PAGE_MARGIN + col * cell_w
        y_cell = page_h - PAGE_MARGIN - (linha + 1) * cell_h

        cartao.seek(0)
        imagem = ImageReader(cartao)
        img_w, img_h = imagem.getSize()

        area_w = cell_w - 2 * CELL_PADDING
        area_h = cell_h - 2 * CELL_PADDING
        escala = min(area_w / img_w, area_h / img_h)
        draw_w, draw_h = img_w * escala, img_h * escala

        x = x_cell + (cell_w - draw_w) / 2
        y = y_cell + (cell_h - draw_h) / 2

        c.drawImage(imagem, x, y, width=draw_w, height=draw_h)

        if DRAW_CUT_GUIDES:
            c.setLineWidth(0.3)
            c.setStrokeColorRGB(0.7, 0.7, 0.7)
            c.rect(x, y, draw_w, draw_h)

    c.save()
    return saida.getvalue()


def gerar_pdf_dos_alunos(pares: List[Tuple[str, str]]) -> bytes:
    modelo = carregar_modelo_bytes()
    lay = layout_atual()
    barra = st.progress(0.0, text="Gerando cartões...")
    cartoes = []
    for idx, (nome, senha) in enumerate(pares, start=1):
        cartoes.append(gerar_cartao(nome, senha, modelo, lay))
        barra.progress(idx / len(pares), text=f"Gerando cartões... {idx}/{len(pares)}")
    pdf = montar_pdf(cartoes)
    barra.empty()
    return pdf
