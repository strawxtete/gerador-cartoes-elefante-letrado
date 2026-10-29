import base64
import io
import os
import re
from typing import Optional

import pandas as pd
import streamlit as st
from PIL import Image

from src.card_generator import carregar_modelo_bytes, gerar_cartao
from src.config import (
    CARD_TEMPLATE_PATH,
    COL_NOME,
    COL_SENHA,
    GRID_COLS,
    GRID_ROWS,
    ICON_PATH,
    LOGO_PATH,
    LOGO_WIDTH,
)
from src.extractor import extrair_alunos
from src.pdf_builder import gerar_pdf_dos_alunos, montar_pdf


def carregar_logo() -> Optional[Image.Image]:
    if not os.path.exists(LOGO_PATH):
        return None
    img = Image.open(LOGO_PATH).convert("RGBA")
    caixa = img.getchannel("A").getbbox()
    if caixa:
        img = img.crop(caixa)
    return img


@st.cache_resource(show_spinner=False)
def logo_cache() -> Optional[Image.Image]:
    return carregar_logo()


@st.cache_resource(show_spinner=False)
def icone_cache() -> Optional[Image.Image]:
    if not os.path.exists(ICON_PATH):
        return None
    return Image.open(ICON_PATH).convert("RGBA")


def html_imagem(png_bytes: bytes, largura: int, classe: str = "img-central") -> str:
    b64 = base64.b64encode(png_bytes).decode()
    return (
        f'<div class="{classe}"><img src="data:image/png;base64,{b64}" '
        f'style="width:{largura}px;max-width:100%;height:auto;" alt=""></div>'
    )


@st.cache_resource(show_spinner=False)
def logo_html() -> str:
    logo = logo_cache()
    if logo is None:
        return ""
    buf = io.BytesIO()
    logo.save(buf, format="PNG")
    return html_imagem(buf.getvalue(), LOGO_WIDTH, classe="logo-wrap")


def gerar_css(tema_escuro: bool) -> str:
    if tema_escuro:
        bg_main = "#0e1117"
        bg_sec = "#262730"
        bg_drag = "rgba(30, 35, 45, 0.96)"
        txt_main = "#ffffff"
        txt_sec = "#d1d5db"
        borda_suave = "rgba(203, 213, 225, 0.32)"
        borda_hover = "rgba(203, 213, 225, 0.65)"
        btn_dis_bg = "rgba(128, 128, 128, 0.2)"
        btn_dis_txt = "rgba(180, 180, 180, 0.7)"
    else:
        bg_main = "#ffffff"
        bg_sec = "#f1f5f9"
        bg_drag = "rgba(241, 245, 249, 0.96)"
        txt_main = "#1e293b"
        txt_sec = "#64748b"
        borda_suave = "rgba(100, 116, 139, 0.35)"
        borda_hover = "rgba(100, 116, 139, 0.65)"
        btn_dis_bg = "#e2e8f0"
        btn_dis_txt = "#94a3b8"

    return f"""
<style>
:root {{
    --rosa: #e42993;
    --rosa-escuro: #c41f7d;
    --teal: #1ac0ad;
    --teal-escuro: #0d7f72;
    --teal-claro: #e6f8f5;
    --primary-color: #e42993 !important;
    --background-color: {bg_main} !important;
    --secondary-background-color: {bg_sec} !important;
    --text-color: {txt_main} !important;
}}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
    background-color: {bg_main} !important;
    color: {txt_main} !important;
}}

header[data-testid="stHeader"],
[data-testid="stHeader"],
[data-testid="stStatusWidget"],
[data-testid="stToolbar"],
[data-testid="stToolbarActions"],
[data-testid="stDecoration"],
[data-testid="stAppDeployButton"],
.stDeployButton,
#MainMenu {{
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    pointer-events: none !important;
}}

.block-container {{
    max-width: 720px;
    padding-top: 1.5rem;
    padding-bottom: 6rem;
    text-align: center;
}}
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stHeading"],
[data-testid="stHeading"] h1, [data-testid="stHeading"] h2, [data-testid="stHeading"] h3,
[data-testid="stCaptionContainer"] {{
    text-align: center;
    width: 100%;
    color: {txt_main};
}}
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {{
    color: {txt_sec} !important;
}}

[data-testid="stHeading"] h1,
[data-testid="stHeading"] h2,
[data-testid="stHeading"] h3 {{
    color: {txt_main} !important;
    font-weight: 700 !important;
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
}}
[data-testid="stHeaderActionElements"],
[data-testid="stHeading"] a,
.stHeading a,
h1 a, h2 a, h3 a {{
    display: none !important;
    visibility: hidden !important;
}}

[data-testid="stWidgetLabel"] {{ justify-content: center; width: 100%; }}
[data-testid="stWidgetLabel"] p {{ text-align: center; font-weight: 500; color: {txt_main} !important; }}
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {{
    text-align: center;
    color: {txt_main} !important;
}}
[data-baseweb="input"],
[data-baseweb="base-input"] {{
    background-color: {bg_sec} !important;
}}
[data-baseweb="tab-list"] {{ justify-content: center; gap: 1.5rem; }}
[data-testid="stAlertContainer"] {{ justify-content: center; text-align: center; }}
[data-testid="stAlertContainer"] p {{ text-align: center; }}

[data-testid="stFileUploaderDropzone"] {{
    justify-content: center;
    background-color: {bg_sec} !important;
    border-radius: 0.75rem !important;
    border: 1.5px dashed {borda_suave} !important;
    box-shadow: none !important;
    transition: border-color 0.15s ease, background-color 0.15s ease;
}}
[data-testid="stFileUploaderDropzone"]:hover,
[data-testid="stFileUploaderDropzone"]:focus-within {{
    border-color: {borda_hover} !important;
    box-shadow: none !important;
}}
[data-testid="stFileUploaderDropzone"] > input + div {{
    background-color: {bg_drag} !important;
    border-radius: 0.65rem !important;
}}
[data-testid="stFileUploaderDropzone"] > input + div > span {{
    font-size: 0 !important;
    color: transparent !important;
}}
[data-testid="stFileUploaderDropzone"] > input + div > span::after {{
    content: "Solte o arquivo PDF aqui";
    font-size: 0.92rem !important;
    color: {txt_sec} !important;
    font-weight: 600 !important;
}}
[data-testid="stFileUploaderDropzoneInstructions"] span {{
    font-size: 0 !important;
    color: transparent !important;
}}
[data-testid="stFileUploaderDropzoneInstructions"] span::after {{
    content: "Arraste e solte o arquivo PDF aqui (máx. 20MB)";
    font-size: 0.88rem !important;
    color: {txt_sec} !important;
}}
[data-testid="stFileUploaderDropzone"] span.e12r9z2m6 button {{
    font-size: 0 !important;
    line-height: 0 !important;
    color: transparent !important;
    background-color: {bg_main} !important;
    border: 1px solid {borda_suave} !important;
}}
[data-testid="stFileUploaderDropzone"] span.e12r9z2m6 button * {{
    display: none !important;
    font-size: 0 !important;
}}
[data-testid="stFileUploaderDropzone"] span.e12r9z2m6 button::after {{
    content: "Procurar PDF";
    font-size: 0.88rem !important;
    line-height: 1.2 !important;
    color: {txt_main} !important;
    font-weight: 500 !important;
}}
[data-testid="stFileUploaderFile"] {{
    background-color: {bg_main} !important;
    color: {txt_main} !important;
    border: 1px solid {borda_suave} !important;
    border-radius: 0.5rem !important;
    padding: 0.25rem 0.6rem !important;
}}
[data-testid="stFileUploaderFile"] span,
[data-testid="stFileUploaderFile"] small {{
    color: {txt_main} !important;
}}

.logo-wrap, .img-central {{ display: flex; justify-content: center; margin: 0 0 0.4rem 0; }}

button[data-baseweb="tab"] p {{ font-size: 0.95rem; font-weight: 600; color: {txt_sec}; }}
button[data-baseweb="tab"]:hover p,
button[data-baseweb="tab"]:focus p {{ color: var(--rosa) !important; }}
button[data-baseweb="tab"][aria-selected="true"],
button[data-baseweb="tab"][aria-selected="true"] p {{ color: var(--rosa) !important; }}
[data-baseweb="tab-highlight"] {{ background-color: var(--rosa) !important; }}

[data-baseweb="input"]:focus-within,
[data-baseweb="base-input"]:focus-within {{
    border-color: var(--rosa) !important;
    box-shadow: 0 0 0 1px var(--rosa) !important;
}}

[data-testid="stProgress"] [role="progressbar"] > div,
[data-testid="stProgress"] > div > div > div > div {{
    background-color: var(--teal) !important;
}}

div[data-testid="stButton"] > button[kind="primary"] {{
    background: var(--rosa) !important;
    border: 1px solid var(--rosa) !important;
    color: #ffffff !important;
    min-height: 2.5rem !important;
    height: 2.5rem !important;
    padding: 0.45rem 1.25rem !important;
    border-radius: 0.5rem !important;
    box-shadow: 0 2px 6px rgba(228, 41, 147, 0.22);
    transition: all 0.15s ease;
}}
div[data-testid="stButton"] > button[kind="primary"]:hover:not(:disabled) {{
    background: var(--rosa-escuro) !important;
    border-color: var(--rosa-escuro) !important;
    box-shadow: 0 4px 10px rgba(228, 41, 147, 0.32);
    transform: translateY(-1px);
}}
div[data-testid="stButton"] > button[kind="primary"]:disabled {{
    background: {btn_dis_bg} !important;
    border-color: {borda_suave} !important;
    color: {btn_dis_txt} !important;
    box-shadow: none !important;
    cursor: not-allowed;
}}

div[data-testid="stButton"] > button[kind="secondary"] {{
    background: {bg_sec} !important;
    border: 1px solid {borda_suave} !important;
    color: {txt_main} !important;
    min-height: 2.1rem !important;
    height: 2.1rem !important;
    padding: 0.25rem 0.85rem !important;
    border-radius: 0.45rem !important;
    transition: all 0.15s ease;
}}
div[data-testid="stButton"] > button[kind="secondary"]:hover {{
    border-color: var(--rosa) !important;
    color: var(--rosa) !important;
}}
div[data-testid="stButton"] > button[kind="secondary"] p {{
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}}

div[data-testid="stDownloadButton"] > button {{
    background: transparent !important;
    border: 1.5px solid var(--teal) !important;
    color: var(--teal) !important;
    min-height: 2.5rem !important;
    height: 2.5rem !important;
    padding: 0.45rem 1.25rem !important;
    border-radius: 0.5rem !important;
    transition: all 0.15s ease;
}}
div[data-testid="stDownloadButton"] > button:hover {{
    background: var(--teal) !important;
    border-color: var(--teal) !important;
    color: #ffffff !important;
    box-shadow: 0 3px 10px rgba(26, 192, 173, 0.25);
    transform: translateY(-1px);
}}

div[data-testid="stButton"] > button[kind="primary"] p,
div[data-testid="stDownloadButton"] button p {{
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    line-height: 1.2 !important;
    color: inherit !important;
}}

.resumo-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.9rem;
    margin: 0.25rem 0 0.75rem 0;
    border-radius: 999px;
    background: rgba(26, 192, 173, 0.12);
    border: 1px solid rgba(26, 192, 173, 0.35);
    color: var(--teal);
    font-size: 0.85rem;
    font-weight: 600;
}}

.aviso-lgpd {{
    position: fixed;
    bottom: 0.85rem;
    left: 50%;
    transform: translateX(-50%);
    width: min(640px, 92vw);
    padding: 0.55rem 1rem;
    border-radius: 0.6rem;
    background: var(--teal-claro);
    border: 1px solid rgba(26, 192, 173, 0.45);
    color: var(--teal-escuro);
    text-align: center;
    font-size: 0.82rem;
    z-index: 999;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}}
</style>
"""


def limpar_nome_arquivo(texto: str, padrao: str = "cartoes") -> str:
    limpo = re.sub(r'[\\/*?:"<>|]+', "", texto.strip())
    limpo = " ".join(limpo.split())
    return limpo or padrao


def mostrar_aviso_lgpd() -> None:
    st.markdown(
        '<div class="aviso-lgpd"><b>Privacidade (LGPD):</b> os arquivos são '
        "processados apenas na memória e <b>não são salvos</b> no servidor.</div>",
        unsafe_allow_html=True,
    )


def botao_centralizado(rotulo: str, **kwargs) -> bool:
    _, meio, _ = st.columns([1.4, 1.2, 1.4])
    with meio:
        return st.button(rotulo, width="stretch", **kwargs)


def download_centralizado(
    rotulo: str, dados: bytes, nome_arquivo: str, chave: str, mime: str = "application/pdf"
) -> None:
    _, meio, _ = st.columns([1.4, 1.2, 1.4])
    with meio:
        st.download_button(
            label=rotulo,
            data=dados,
            file_name=nome_arquivo,
            mime=mime,
            width="stretch",
            key=chave,
        )


def aba_lista_pdf() -> None:
    st.write("Envie o PDF **Relação de Usuários da Escola** com a lista de alunos da turma.")
    arquivo = st.file_uploader(
        "Lista de alunos (PDF)", type=["pdf"], label_visibility="collapsed"
    )

    if arquivo is None:
        for chave in ("assinatura", "alunos_df", "esperado", "turma_nome", "pdf_final", "qtd"):
            st.session_state.pop(chave, None)
        botao_centralizado("Gerar Cartões", type="primary", disabled=True, key="gerar_pdf_off")
        return

    assinatura = (arquivo.name, arquivo.size)
    if st.session_state.get("assinatura") != assinatura:
        try:
            alunos, esperado, turma_nome = extrair_alunos(arquivo.getvalue(), arquivo.name)
        except Exception as e:
            st.error(f"Não foi possível ler o PDF: {e}")
            return
        st.session_state["assinatura"] = assinatura
        st.session_state["alunos_df"] = pd.DataFrame(alunos, columns=[COL_NOME, COL_SENHA])
        st.session_state["esperado"] = esperado
        st.session_state["turma_nome"] = turma_nome
        st.session_state.pop("pdf_final", None)

    df_base: pd.DataFrame = st.session_state["alunos_df"]
    esperado = st.session_state.get("esperado")

    if df_base.empty:
        st.error("Nenhum aluno encontrado. Verifique se o PDF segue o padrão esperado.")
        botao_centralizado("Gerar Cartões", type="primary", disabled=True, key="gerar_pdf_vazio")
        return

    st.success(f"{len(df_base)} alunos encontrados.")
    if esperado is not None and esperado != len(df_base):
        st.warning(
            f"O cabeçalho do PDF indica {esperado} alunos, mas foram lidos {len(df_base)}. "
            "Confira a lista abaixo."
        )

    st.caption(
        "Confira os dados. Você pode corrigir nomes cortados pelo PDF, "
        "ou adicionar/remover linhas."
    )
    df_editado = st.data_editor(
        df_base,
        num_rows="dynamic",
        hide_index=True,
        key=f"editor_{assinatura}",
    )

    if botao_centralizado("Gerar Cartões", type="primary", key="gerar_pdf"):
        pares = [
            (str(n).strip(), str(s).strip())
            for n, s in zip(df_editado[COL_NOME], df_editado[COL_SENHA])
            if str(n).strip() not in ("", "None", "nan") and str(s).strip() not in ("", "None", "nan")
        ]
        if not pares:
            st.error("A lista está vazia. Preencha ao menos um aluno.")
        else:
            try:
                st.session_state["pdf_final"] = gerar_pdf_dos_alunos(pares)
                st.session_state["qtd"] = len(pares)
            except FileNotFoundError:
                st.error(f"Arquivo '{CARD_TEMPLATE_PATH}' não encontrado na pasta do app.")
            except Exception as e:
                st.error(f"Erro ao gerar os cartões: {e}")

    if "pdf_final" in st.session_state:
        qtd = st.session_state["qtd"]
        por_pagina = GRID_COLS * GRID_ROWS
        paginas = (qtd + por_pagina - 1) // por_pagina
        label_pag = "folha A4" if paginas == 1 else "folhas A4"
        st.markdown(
            f'<div><span class="resumo-badge">{qtd} cartões gerados • '
            f"{paginas} {label_pag} para impressão</span></div>",
            unsafe_allow_html=True,
        )
        nome_turma = limpar_nome_arquivo(st.session_state.get("turma_nome", ""), "turma")
        download_centralizado(
            "Baixar PDF dos Cartões",
            st.session_state["pdf_final"],
            f"{nome_turma}.pdf",
            "baixar_pdf_lista",
        )


def aba_manual() -> None:
    st.write("Preencha os dados para gerar o cartão de **um** aluno.")
    c1, c2 = st.columns(2)
    with c1:
        nome = st.text_input(
            "Nome do aluno",
            key="manual_nome",
            placeholder="Digite o nome completo do aluno",
        )
    with c2:
        senha = st.text_input(
            "Senha (carteirinha)",
            key="manual_senha",
            placeholder="Digite o código da carteirinha",
        )

    if botao_centralizado("Gerar Cartão", type="primary", key="gerar_manual"):
        if not nome.strip() or not senha.strip():
            st.error("Preencha o nome e a senha do aluno.")
        else:
            try:
                cartao = gerar_cartao(nome.strip(), senha.strip(), carregar_modelo_bytes())
                st.session_state["pdf_manual"] = montar_pdf([cartao])
                st.session_state["nome_manual_arq"] = limpar_nome_arquivo(nome, "aluno")
            except FileNotFoundError:
                st.error(f"Arquivo '{CARD_TEMPLATE_PATH}' não encontrado na pasta do app.")
            except Exception as e:
                st.error(f"Erro ao gerar o cartão: {e}")

    if "pdf_manual" in st.session_state:
        nome_arq = st.session_state.get("nome_manual_arq", "aluno")
        st.markdown(
            f'<div><span class="resumo-badge">Cartão gerado para {nome_arq}</span></div>',
            unsafe_allow_html=True,
        )
        download_centralizado(
            "Baixar PDF do Cartão",
            st.session_state["pdf_manual"],
            f"{nome_arq}.pdf",
            "baixar_pdf_manual",
        )


def main() -> None:
    logo = logo_cache()
    icone = icone_cache()
    st.set_page_config(
        page_title="Elefante Letrado - Cartões",
        page_icon=icone if icone is not None else logo,
        layout="centered",
    )

    if "tema_escuro" not in st.session_state:
        st.session_state["tema_escuro"] = True

    _, col_tema = st.columns([5.2, 1.3])
    with col_tema:
        rotulo_tema = "Modo Claro" if st.session_state["tema_escuro"] else "Modo Escuro"
        if st.button(rotulo_tema, type="secondary", width="stretch", key="btn_alternar_tema"):
            st.session_state["tema_escuro"] = not st.session_state["tema_escuro"]
            st.rerun()

    st.markdown(gerar_css(st.session_state["tema_escuro"]), unsafe_allow_html=True)

    if logo is not None:
        st.markdown(logo_html(), unsafe_allow_html=True)
        st.subheader("Gerador de Cartões de Acesso", anchor=False)
    else:
        st.title("Elefante Letrado — Gerador de Cartões de Acesso", anchor=False)

    aba_pdf, aba_man = st.tabs(["Enviar lista (PDF)", "Preencher manualmente"])
    with aba_pdf:
        aba_lista_pdf()
    with aba_man:
        aba_manual()

    mostrar_aviso_lgpd()
