from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings

FRONTEND_URL = getattr(settings, 'FRONTEND_URL', 'https://visiontech.vision')
LOGO_URL     = 'https://visiontech.vision/logo.png'

STATUT_LABELS = {
    'en_attente': "En attente d'examen",
    'en_etude':   "En cours d'étude",
    'accepte':    'Acceptée ✅',
    'refuse':     'Refusée',
}

STATUT_COLORS = {
    'en_attente': '#f59e0b',
    'en_etude':   '#3b82f6',
    'accepte':    '#22c55e',
    'refuse':     '#ef4444',
}


def _base_html(header_content, body_content):
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f0f4ff;font-family:Arial,sans-serif">
  <div style="max-width:600px;margin:32px auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08)">
    <div style="background:linear-gradient(135deg,#0f2b6e 0%,#1d4ed8 55%,#0ea5e9 100%);padding:24px;text-align:center">
      <img src="{LOGO_URL}" alt="VisionTech SARL" style="height:52px;width:auto;margin-bottom:6px;display:block;margin-left:auto;margin-right:auto" />
      {header_content}
    </div>
    <div style="padding:32px 28px">{body_content}</div>
    <div style="background:#f8fafc;padding:18px 28px;text-align:center;border-top:1px solid #e2e8f0">
      <p style="color:#94a3b8;font-size:12px;margin:0">
        &copy; 2026 VisionTech SARL &middot; Djemoun, Bafoussam, Cameroun<br>
        contact@visiontechsarl.com &middot; +237 674 55 49 47
      </p>
    </div>
  </div>
</body></html>"""


def send_confirmation_email(demande):
    suivi_url = f"{FRONTEND_URL}/stages/mes-demandes"

    header = '<p style="color:rgba(255,255,255,0.85);margin:4px 0 0;font-size:13px">Demande de stage reçue</p>'

    body = f"""
      <h2 style="color:#0f172a;font-size:19px;margin:0 0 12px">Bonjour {demande.prenom} &#128075;</h2>
      <p style="color:#475569;line-height:1.7;margin:0 0 20px">
        Nous avons bien reçu votre demande de stage.
        Notre équipe va étudier votre dossier et vous notifiera dans les plus brefs délais.
      </p>

      <div style="background:#f8fafc;border-radius:12px;padding:18px 20px;margin-bottom:24px;border:1px solid #e2e8f0">
        <h3 style="color:#0f172a;margin:0 0 12px;font-size:14px;font-weight:700">&#128203; Récapitulatif</h3>
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          <tr>
            <td style="padding:5px 0;color:#64748b">Profil</td>
            <td style="padding:5px 0;color:#0f172a;font-weight:600">{demande.get_profil_display()}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#64748b">Domaine</td>
            <td style="padding:5px 0;color:#0f172a;font-weight:600">{demande.get_domaine_display() if demande.domaine else 'Non précisé'}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#64748b">Période souhaitée</td>
            <td style="padding:5px 0;color:#0f172a;font-weight:600">
              {demande.date_debut.strftime('%d/%m/%Y') if demande.date_debut else 'Non précisée'}
              &rarr;
              {demande.date_fin.strftime('%d/%m/%Y') if demande.date_fin else 'Non précisée'}
            </td>
          </tr>
        </table>
      </div>

      <div style="text-align:center;margin-bottom:24px">
        <a href="{suivi_url}"
           style="display:inline-block;padding:14px 32px;background:linear-gradient(135deg,#1d4ed8,#0ea5e9);
                  color:#fff;text-decoration:none;border-radius:12px;font-weight:700;font-size:15px;
                  box-shadow:0 4px 18px rgba(29,78,216,0.35)">
          &#128269; Suivre ma demande
        </a>
      </div>

      <p style="color:#94a3b8;font-size:12px;text-align:center;margin:0">
        Connectez-vous à votre espace pour suivre l'état de votre dossier.
      </p>
    """

    subject = "&#9989; Demande de stage reçue — VisionTech SARL"
    html    = _base_html(header, body)
    text    = f"Bonjour {demande.prenom}, votre demande de stage a été reçue. Suivez-la ici : {suivi_url}"

    msg = EmailMultiAlternatives(
        subject="Demande de stage reçue — VisionTech SARL",
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[demande.email_contact],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()

    send_mail(
        subject=f"[Stage] Nouvelle demande — {demande.prenom} {demande.nom}",
        message=(
            f"Nouvelle demande :\n\n"
            f"Candidat : {demande.prenom} {demande.nom}\n"
            f"Profil   : {demande.get_profil_display()}\n"
            f"Email    : {demande.email_contact}\n"
            f"Domaine  : {demande.get_domaine_display() if demande.domaine else 'N/A'}\n\n"
            f"Admin    : https://api.visiontech.vision/admin/stages/demandestage/{demande.pk}/change/"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        fail_silently=True,
    )


def send_status_update_email(demande):
    suivi_url = f"{FRONTEND_URL}/stages/mes-demandes"
    color     = STATUT_COLORS.get(demande.statut, '#3b82f6')
    label     = STATUT_LABELS.get(demande.statut, demande.get_statut_display())

    if demande.statut == 'accepte':
        icon     = '&#127881;'
        headline = f"Félicitations {demande.prenom} ! Votre demande est acceptée"
        intro    = (
            "Nous avons le plaisir de vous informer que votre demande de stage a été "
            f"<strong style='color:{color}'>acceptée</strong>. "
            "Notre équipe prendra contact avec vous très prochainement."
        )
    elif demande.statut == 'refuse':
        icon     = '&#128532;'
        headline = "Résultat de votre demande de stage"
        intro    = (
            "Nous avons étudié votre dossier avec attention. "
            "Malheureusement, nous ne sommes pas en mesure de donner suite à votre demande pour le moment."
        )
    elif demande.statut == 'en_etude':
        icon     = '&#128269;'
        headline = "Votre dossier est en cours d'examen"
        intro    = "Bonne nouvelle ! Votre dossier est actuellement examiné par notre équipe."
    else:
        icon     = '&#128203;'
        headline = "Mise à jour de votre demande de stage"
        intro    = "Le statut de votre demande a été mis à jour."

    comment_block = ""
    if demande.commentaire_admin:
        comment_block = f"""
        <div style="background:#f0fdf4;border-left:4px solid {color};border-radius:0 12px 12px 0;
                    padding:14px 18px;margin:20px 0">
          <p style="color:#0f172a;margin:0 0 4px;font-weight:700;font-size:13px">Message de notre équipe :</p>
          <p style="color:#475569;margin:0;line-height:1.7;font-size:14px">{demande.commentaire_admin}</p>
        </div>
        """

    header = f'<p style="color:rgba(255,255,255,0.85);margin:4px 0 0;font-size:22px">{icon}</p>'

    body = f"""
      <h2 style="color:#0f172a;font-size:18px;margin:0 0 14px">{headline}</h2>
      <p style="color:#475569;line-height:1.7;margin:0 0 20px">{intro}</p>

      <div style="text-align:center;margin:20px 0">
        <span style="display:inline-block;padding:8px 24px;background:{color}20;
                     border:2px solid {color};border-radius:30px;
                     color:{color};font-weight:800;font-size:15px">{label}</span>
      </div>

      {comment_block}

      <div style="text-align:center;margin:24px 0">
        <a href="{suivi_url}"
           style="display:inline-block;padding:13px 28px;background:linear-gradient(135deg,#1d4ed8,#0ea5e9);
                  color:#fff;text-decoration:none;border-radius:12px;font-weight:700;font-size:14px">
          &#128202; Voir mes demandes
        </a>
      </div>
    """

    msg = EmailMultiAlternatives(
        subject=f"{headline} — VisionTech SARL",
        body=f"{headline}. Statut : {label}. Voir : {suivi_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[demande.email_contact],
    )
    msg.attach_alternative(_base_html(header, body), "text/html")
    msg.send()
