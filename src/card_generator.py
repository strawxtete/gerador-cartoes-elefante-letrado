import io
from typing import Dict, Optional

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

from src.config import (
    CARD_TEMPLATE_PATH,
    COVER_BOX,
    COVER_OLD_TEXT,
    FIX_BORDER,
    FONT_FALLBACKS,
    FONT_PATH,
    FONT_SIZE,
    LOGIN_Y,
    MAX_TEXT_WIDTH,
    NAME_LABEL,
    NUMBER_LABEL,
    REF_WIDTH,
    SENHA_Y,
    TEXT_COLOR,
    TEXT_X,
)


def carregar_fonte(tamanho: int) -> ImageFont.FreeTypeFont:
    for caminho in [str(FONT_PATH), *FONT_FALLBACKS]:
        try:
            return ImageFont.truetype(caminho, tamanho)
        except OSError:
            continue
    return ImageFont.load_default(size=tamanho)


def ajustar_fonte(
    draw: ImageDraw.ImageDraw, texto: str, tamanho: int, largura_max: float
) -> ImageFont.FreeTypeFont:
    while tamanho > 12:
        fonte = carregar_fonte(tamanho)
        if draw.textlength(texto, font=fonte) <= largura_max:
            return fonte
        tamanho -= max(1, tamanho // 25)
    return carregar_fonte(tamanho)


@st.cache_resource(show_spinner=False)
def carregar_modelo_bytes() -> bytes:
    with open(CARD_TEMPLATE_PATH, "rb") as f:
        return f.read()


def apagar_texto_antigo(img: Image.Image, k: float) -> None:
    x1, y1, x2, y2 = (int(v * k) for v in COVER_BOX)
    x2, y2 = min(x2, img.width), min(y2, img.height)
    regiao = np.array(img.crop((x1, y1, x2, y2)), dtype=np.int16)
    r, g, _ = regiao[..., 0], regiao[..., 1], regiao[..., 2]
    rosado = (r > 180) & (r - g > 5)
    regiao[rosado] = (255, 255, 255)
    img.paste(Image.fromarray(regiao.astype(np.uint8)), (x1, y1))


def layout_atual() -> Dict[str, int]:
    ss = st.session_state
    return {
        "x": ss.get("lay_x", TEXT_X),
        "y_login": ss.get("lay_y_login", LOGIN_Y),
        "y_senha": ss.get("lay_y_senha", SENHA_Y),
        "tamanho": ss.get("lay_tamanho", FONT_SIZE),
    }


def gerar_cartao(
    nome: str, senha: str, modelo_bytes: bytes, layout: Optional[Dict[str, int]] = None
) -> io.BytesIO:
    lay = layout or layout_atual()

    rgba = Image.open(io.BytesIO(modelo_bytes)).convert("RGBA")
    caixa_recorte = rgba.getchannel("A").getbbox() if FIX_BORDER else None
    fundo_branco = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    img = Image.alpha_composite(fundo_branco, rgba).convert("RGB")

    k = img.width / REF_WIDTH
    draw = ImageDraw.Draw(img)

    if COVER_OLD_TEXT:
        apagar_texto_antigo(img, k)

    texto_login = f"{NAME_LABEL}{nome}".upper()
    texto_senha = f"{NUMBER_LABEL}{senha}".upper()

    tamanho = max(12, int(lay["tamanho"] * k))
    largura_max = MAX_TEXT_WIDTH * k
    fonte_login = ajustar_fonte(draw, texto_login, tamanho, largura_max)
    fonte_senha = ajustar_fonte(draw, texto_senha, tamanho, largura_max)
    menor = min(fonte_login.size, fonte_senha.size)
    fonte_login = fonte_senha = carregar_fonte(int(menor))

    draw.text((lay["x"] * k, lay["y_login"] * k), texto_login, font=fonte_login, fill=TEXT_COLOR)
    draw.text((lay["x"] * k, lay["y_senha"] * k), texto_senha, font=fonte_senha, fill=TEXT_COLOR)

    if caixa_recorte:
        img = img.crop(caixa_recorte)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
