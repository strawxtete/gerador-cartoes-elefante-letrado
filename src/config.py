from pathlib import Path
from reportlab.lib.units import mm

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
FONTS_DIR = ASSETS_DIR / "fonts"

COR_ROSA = (228, 41, 147)

CARD_TEMPLATE_PATH = IMAGES_DIR / "cartao_modelo.png"
LOGO_PATH = IMAGES_DIR / "logo_elefante_letrado.png"
LOGO_WIDTH = 300
ICON_PATH = IMAGES_DIR / "icone_elefante_letrado.png"

FONT_PATH = FONTS_DIR / "Oswald-Regular.ttf"
FONT_FALLBACKS = [
    "arial.ttf",
    "DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]

REF_WIDTH = 840
TEXT_X = 120
LOGIN_Y = 200
SENHA_Y = 275
FONT_SIZE = 44
NAME_LABEL = "LOGIN: "
NUMBER_LABEL = "SENHA: "
TEXT_COLOR = COR_ROSA

MAX_TEXT_WIDTH = 565

COVER_OLD_TEXT = True
COVER_BOX = (100, 160, 555, 330)

FIX_BORDER = True

GRID_COLS = 2
GRID_ROWS = 3
PAGE_MARGIN = 10 * mm
CELL_PADDING = 3 * mm
DRAW_CUT_GUIDES = False

COL_NOME = "Nome"
COL_SENHA = "Senha (carteirinha)"
