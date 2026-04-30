"""Génère un rapport PDF pro à partir d'une analyse."""
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib import colors
import datetime

EMERALD = HexColor('#10B981')
EMERALD_DARK = HexColor('#059669')
INK = HexColor('#0F172A')
SLATE = HexColor('#475569')


def generer_pdf(analyse, nom_terrain, localisation, user_name, donnees):
    """Retourne les bytes d'un PDF prêt à télécharger."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('T', parent=styles['Title'],
                                  textColor=EMERALD_DARK, fontSize=24, spaceAfter=6)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'],
                         textColor=INK, fontSize=14, spaceBefore=14, spaceAfter=8)
    body = ParagraphStyle('B', parent=styles['BodyText'], fontSize=10, textColor=INK, leading=14)
    muted = ParagraphStyle('M', parent=styles['BodyText'], fontSize=9, textColor=SLATE)

    elements = []

    # En-tête
    elements.append(Paragraph("TerraSafe — Rapport d'analyse", title_style))
    elements.append(Paragraph(
        f"Généré le {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')} pour <b>{user_name}</b>",
        muted))
    elements.append(Spacer(1, 12))

    # Bloc terrain
    elements.append(Paragraph("Identification du terrain", h2))
    info = [['Nom', nom_terrain], ['Localisation', localisation or '—']]
    t = Table(info, colWidths=[5*cm, 11*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0,0), (-1,-1), INK),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#E5E7EB')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t)

    # Verdict
    elements.append(Paragraph("Verdict global", h2))
    score = analyse['risque_score']
    classe = analyse['classe']
    color = EMERALD if classe == 'Faible' else (HexColor('#F59E0B') if classe == 'Moyen' else HexColor('#DC2626'))

    verdict_table = Table(
        [[f"Score de risque", f"{score:.1f} / 100"],
         [f"Classification", classe]],
        colWidths=[5*cm, 11*cm])
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), HexColor('#F1F5F9')),
        ('BACKGROUND', (1,1), (1,1), color),
        ('TEXTCOLOR', (1,1), (1,1), colors.white),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#E5E7EB')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(verdict_table)
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"<b>Recommandation :</b> {analyse['verdict']}", body))

    # Variables collectées
    elements.append(Paragraph("Variables analysées", h2))
    var_data = [['Variable', 'Valeur']] + [[k.replace('_', ' ').capitalize(), f"{v:.2f}"]
                                             for k, v in donnees.items()]
    vt = Table(var_data, colWidths=[10*cm, 6*cm])
    vt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), EMERALD),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, HexColor('#E5E7EB')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HexColor('#FAFAF9')]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(vt)

    # Projection future
    elements.append(PageBreak())
    elements.append(Paragraph("Projection future", h2))
    elements.append(Paragraph(
        "Estimation de l'évolution du risque selon un scénario tendanciel "
        "(intensification climatique + pression urbaine).", body))
    proj = analyse['projection']
    pt = Table([
        ['Horizon', 'Risque estimé'],
        ['Aujourd’hui', f"{proj['actuel']:.1f}"],
        ['Dans 5 ans', f"{proj['risque_5ans']:.1f}"],
        ['Dans 10 ans', f"{proj['risque_10ans']:.1f}"],
    ], colWidths=[8*cm, 8*cm])
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), EMERALD_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.3, HexColor('#E5E7EB')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(pt)

    # Méthodes
    elements.append(Paragraph("Méthodologie", h2))
    m = analyse['metrics_modeles']
    elements.append(Paragraph(
        f"L'analyse combine 5 techniques d'apprentissage statistique : "
        f"régression linéaire simple (R²={m['r2_simple']:.3f}), "
        f"régression linéaire multiple (R²={m['r2_multiple']:.3f}), "
        f"ACP (variance expliquée 2 axes : {sum(m['pca_variance'])*100:.1f}%), "
        f"Random Forest (précision {m['accuracy_rf']*100:.1f}%) et "
        f"K-Means (3 clusters de profils de terrains).", body))

    elements.append(Spacer(1, 24))
    elements.append(Paragraph(
        "<i>Document généré par TerraSafe — Outil d'aide à la décision. "
        "Ne se substitue pas à une étude géotechnique réglementaire.</i>", muted))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
