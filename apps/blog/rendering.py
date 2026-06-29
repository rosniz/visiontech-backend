"""Rendu Markdown -> HTML sécurisé + extraction de la table des matières."""
import bleach
import markdown as md

ALLOWED_TAGS = [
    'p', 'br', 'hr', 'strong', 'em', 'u', 's', 'del',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li',
    'blockquote', 'pre', 'code',
    'a', 'img',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'div', 'span', 'figure', 'figcaption',
]

ALLOWED_ATTRS = {
    'a':    ['href', 'title', 'target', 'rel'],
    'img':  ['src', 'alt', 'title', 'loading', 'width', 'height'],
    'div':  ['class'],
    'span': ['class'],
    'code': ['class'],
    'pre':  ['class'],
    'h1': ['id'], 'h2': ['id'], 'h3': ['id'], 'h4': ['id'], 'h5': ['id'], 'h6': ['id'],
}

ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


def render_markdown(texte: str):
    """Retourne (html_securise, table_des_matieres)."""
    if not texte:
        return '', []

    parser = md.Markdown(extensions=[
        'extra', 'fenced_code', 'codehilite', 'tables', 'toc', 'sane_lists', 'nl2br',
    ], extension_configs={
        'toc': {'permalink': False, 'baselevel': 2},
        'codehilite': {'guess_lang': False, 'noclasses': False},
    })

    html_brut = parser.convert(texte)

    html_propre = bleach.clean(
        html_brut,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )

    toc = [
        {'niveau': tok['level'], 'id': tok['id'], 'texte': tok['name']}
        for tok in getattr(parser, 'toc_tokens', [])
    ]

    return html_propre, toc
