# Génère les rapports PDF avec ReportLab

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm

# Dossier où stocker les PDFs
PDF_DIR = "uploads/reports"
os.makedirs(PDF_DIR, exist_ok=True)


def generate_pdf(result, child, parent) -> str:
    """
    Génère un rapport PDF pour une évaluation.
    Retourne le chemin vers le fichier PDF créé.
    """

    # Chemin du fichier PDF
    pdf_path = f"{PDF_DIR}/rapport_{result.id}.pdf"

    # Créer le document
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    # Couleurs selon niveau de risque
    risk_colors = {
        "VERT": HexColor("#1a7a4a"),
        "ORANGE": HexColor("#c96a1a"),
        "ROUGE": HexColor("#c62828"),
    }
    risk_color = risk_colors.get(result.risk_level, HexColor("#333333"))

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        fontSize=22,
        textColor=HexColor("#111218"),
        spaceAfter=6,
        fontName="Helvetica-Bold",
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        fontSize=13,
        textColor=HexColor("#3d3e4a"),
        spaceAfter=4,
        fontName="Helvetica",
    )

    risk_style = ParagraphStyle(
        "Risk",
        fontSize=18,
        textColor=risk_color,
        spaceAfter=6,
        fontName="Helvetica-Bold",
    )

    body_style = ParagraphStyle(
        "Body",
        fontSize=11,
        textColor=HexColor("#3d3e4a"),
        spaceAfter=6,
        fontName="Helvetica",
        leading=16,
    )

    warning_style = ParagraphStyle(
        "Warning",
        fontSize=9,
        textColor=HexColor("#7a7b8a"),
        fontName="Helvetica-Oblique",
        leading=14,
    )

    # ─── CONTENU ──────────────────────────────────────────────
    elements = []

    # Titre
    elements.append(Paragraph("NeuroKid AI", title_style))
    elements.append(Paragraph("Rapport d'évaluation du développement", subtitle_style))
    elements.append(Spacer(1, 0.5 * cm))

    # Ligne de séparation
    elements.append(
        Table(
            [[""]],
            colWidths=[17 * cm],
            style=TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1, HexColor("#e0e0e0"))]),
        )
    )
    elements.append(Spacer(1, 0.5 * cm))

    # Infos enfant
    elements.append(Paragraph("Informations", subtitle_style))

    date_str = result.created_at.strftime("%d/%m/%Y à %H:%M")

    info_data = [
        ["Enfant :", child.first_name],
        ["Âge :", f"{child.age_months} mois"],
        ["Genre :", "Garçon" if child.gender == "M" else "Fille"],
        ["Parent :", parent.full_name],
        ["Date :", date_str],
    ]

    info_table = Table(info_data, colWidths=[4 * cm, 13 * cm])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("TEXTCOLOR", (0, 0), (0, -1), HexColor("#111218")),
                ("TEXTCOLOR", (1, 0), (1, -1), HexColor("#3d3e4a")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(info_table)
    elements.append(Spacer(1, 0.8 * cm))

    # Résultat
    elements.append(Paragraph("Résultat de l'évaluation", subtitle_style))
    elements.append(Spacer(1, 0.2 * cm))
    elements.append(Paragraph(f"Niveau de risque : {result.risk_level}", risk_style))
    elements.append(
        Paragraph(f"Score final : {int(result.score_final * 100)}%", subtitle_style)
    )
    elements.append(Spacer(1, 0.8 * cm))

    # Recommandations
    elements.append(Paragraph("Recommandations", subtitle_style))
    elements.append(Spacer(1, 0.2 * cm))

    recommendations = {
        "VERT": [
            "Le développement de votre enfant semble se dérouler normalement.",
            "Continuez les activités d'éveil quotidiennes.",
            "Lisez des histoires ensemble chaque soir.",
            "Encouragez les jeux d'imitation et la communication.",
        ],
        "ORANGE": [
            "Quelques points méritent une attention particulière.",
            "Une consultation avec votre pédiatre est conseillée dans les 3 prochains mois.",
            "Encouragez les jeux d'imitation et le contact visuel.",
            "Consultez un orthophoniste si le langage ne progresse pas.",
        ],
        "ROUGE": [
            "Une consultation rapide avec un pédopsychiatre est fortement recommandée.",
            "Ne tardez pas — un dépistage précoce améliore significativement les résultats.",
            "Vous faites déjà quelque chose d'important en cherchant à comprendre.",
            "Contactez votre pédiatre dès cette semaine pour une orientation.",
        ],
    }

    for rec in recommendations.get(result.risk_level, []):
        elements.append(Paragraph(f"• {rec}", body_style))

    elements.append(Spacer(1, 1 * cm))

    # Avertissement éthique
    elements.append(
        Table(
            [[""]],
            colWidths=[17 * cm],
            style=TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1, HexColor("#e0e0e0"))]),
        )
    )
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(
        Paragraph(
            "⚠️ Cet outil aide au dépistage précoce — il ne pose pas de diagnostic médical. "
            "En cas de doute, consultez toujours un professionnel de santé qualifié.",
            warning_style,
        )
    )

    # Générer le PDF
    doc.build(elements)
    return pdf_path
