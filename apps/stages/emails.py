from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings

FRONTEND_URL = getattr(settings, 'FRONTEND_URL', 'https://visiontech.vision')

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
    <div style="background:linear-gradient(135deg,#0f2b6e 0%,#1d4ed8 55%,#0ea5e9 100%);padding:28px 24px;text-align:center">
      {header_content}
    </div>
    <div style="padding:32px 28px">{body_content}</div>
    <div style="background:#f8fafc;padding:18px 28px;text-align:center;border-top:1px solid #e2e8f0">
      <p style="color:#94a3b8;font-size:12px;margin:0">
        © 2025 VisionTech SARL · Djemoun, Bafoussam, Cameroun<br>
        📧 contact@visiontech.vision · 📞 +237 674 55 49 47
      </p>
    </div>
  </div>
</body></html>"""


def send_confirmation_email(demande):
    """Email envoyé au candidat après soumission."""
    suivi_url = f"{FRONTEND_URL}/stages/suivi?token={demande.token}"

    header = """
      <h1 style="color:#fff;margin:0;font-size:22px;font-weight:800">VisionTech SARL</h1>
      <p style="color:rgba(255,255,255,0.75);margin:6px 0 0;font-size:13px">Demande de stage reçue</p>
    """

    body = f"""
      <h2 style="color:#0f172a;font-size:19px;margin:0 0 12px">Bonjour {demande.prenom} 👋</h2>
      <p style="color:#475569;line-height:1.7;margin:0 0 20px">
        Nous avons bien reçu votre demande de stage en
        <strong style="color:#1d4ed8">{demande.get_domaine_display()}</strong>.
        Notre équipe va étudier votre dossier et vous notifiera dans les plus brefs délais.
      </p>

      <div style="background:#f8fafc;border-radius:12px;padding:18px 20px;margin-bottom:24px;border:1px solid #e2e8f0">
        <h3 style="color:#0f172a;margin:0 0 12px;font-size:14px;font-weight:700">📋 Récapitulatif</h3>
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          <tr>
            <td style="padding:5px 0;color:#64748b">Domaine</td>
            <td style="padding:5px 0;color:#0f172a;font-weight:600">{demande.get_domaine_display()}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#64748b">Niveau</td>
            <td style="padding:5px 0;color:#0f172a;font-weight:600">{demande.get_niveau_etude_display()}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#64748b">Période souhaitée</td>
            <td style="padding:5px 0;color:#0f172a;font-weight:600">
              {demande.date_debut.strftime('%d/%m/%Y')} → {demande.date_fin.strftime('%d/%m/%Y')}
            </td>
          </tr>
        </table>
      </div>

      <div style="text-align:center;margin-bottom:24px">
        <a href="{suivi_url}"
           style="display:inline-block;padding:14px 32px;background:linear-gradient(135deg,#1d4ed8,#0ea5e9);
                  color:#fff;text-decoration:none;border-radius:12px;font-weight:700;font-size:15px;
                  box-shadow:0 4px 18px rgba(29,78,216,0.35)">
          🔍 Suivre ma demande
        </a>
      </div>

      <p style="color:#94a3b8;font-size:12px;text-align:center;margin:0">
        Conservez ce lien pour suivre l'état de votre dossier.<br>
        Token : <code style="background:#f1f5f9;padding:2px 8px;border-radius:6px;color:#475569;font-size:11px">{demande.token}</code>
      </p>
    """

    subject = "✅ Demande de stage reçue — VisionTech SARL"
    html    = _base_html(header, body)
    text    = f"Bonjour {demande.prenom}, votre demande de stage a été reçue. Suivez-la ici : {suivi_url}"

    msg = EmailMultiAlternatives(
        subject=subject, body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[demande.email],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()

    # Notifier l'admin
    send_mail(
        subject=f"[Stage] Nouvelle demande — {demande.prenom} {demande.nom}",
        message=(
            f"Nouvelle demande de stage :\n\n"
            f"Nom     : {demande.prenom} {demande.nom}\n"
            f"Email   : {demande.email}\n"
            f"Domaine : {demande.get_domaine_display()}\n"
            f"Période : {demande.date_debut} → {demande.date_fin}\n\n"
            f"Admin   : https://api.visiontech.vision/admin/stages/demandestage/{demande.pk}/change/"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        fail_silently=True,
    )


def send_status_update_email(demande):
    """Email envoyé quand le statut change."""
    suivi_url = f"{FRONTEND_URL}/stages/suivi?token={demande.token}"
    color     = STATUT_COLORS.get(demande.statut, '#3b82f6')
    label     = STATUT_LABELS.get(demande.statut, demande.get_statut_display())

    if demande.statut == 'accepte':
        icon    = '🎉'
        headline = f"Félicitations {demande.prenom} ! Votre demande est acceptée"
        intro    = (
            "Nous avons le plaisir de vous informer que votre demande de stage a été "
            "<strong style='color:#22c55e'>acceptée</strong>. "
            "Notre équipe prendra contact avec vous très prochainement pour les détails pratiques."
        )
    elif demande.statut == 'refuse':
        icon    = '😔'
        headline = "Résultat de votre demande de stage"
        intro    = (
            "Nous avons étudié votre dossier avec la plus grande attention. "
            "Malheureusement, nous ne sommes pas en mesure de donner suite à votre demande pour le moment. "
            "Nous vous encourageons à repostuler lors de la prochaine session."
        )
    elif demande.statut == 'en_etude':
        icon    = '🔍'
        headline = "Votre dossier est en cours d'examen"
        intro    = (
            "Bonne nouvelle ! Votre dossier est actuellement examiné par notre équipe. "
            "Nous reviendrons vers vous très prochainement."
        )
    else:
        icon    = '📋'
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

    header = f"""
      <div style="font-size:36px;margin-bottom:8px">{icon}</div>
      <h1 style="color:#fff;margin:0;font-size:20px;font-weight:800">VisionTech SARL</h1>
    """

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
          📊 Voir le détail de ma demande
        </a>
      </div>
    """

    subject = f"{icon} {headline} — VisionTech SARL"
    html    = _base_html(header, body)
    text    = f"{headline}. Statut : {label}. Voir : {suivi_url}"

    msg = EmailMultiAlternatives(
        subject=subject, body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[demande.email],
    )
    msg.attach_alternative(html, "text/html")
    msg.send()
