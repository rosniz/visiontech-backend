from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings

LOGO_URL     = 'https://visiontech.vision/logo.png'
FRONTEND_URL = getattr(settings, 'FRONTEND_URL', 'https://visiontech.vision')


def _html(header, body):
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f0f4ff;font-family:Arial,sans-serif">
  <div style="max-width:600px;margin:32px auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08)">
    <div style="background:linear-gradient(135deg,#0f2b6e 0%,#1d4ed8 55%,#0ea5e9 100%);padding:24px;text-align:center">
      <img src="{LOGO_URL}" alt="VisionTech SARL" style="height:50px;width:auto;display:block;margin:0 auto 6px"/>
      {header}
    </div>
    <div style="padding:32px 28px">{body}</div>
    <div style="background:#f8fafc;padding:16px 28px;text-align:center;border-top:1px solid #e2e8f0">
      <p style="color:#94a3b8;font-size:12px;margin:0">
        &copy; 2026 VisionTech SARL &middot; Djemoun, Bafoussam, Cameroun<br>
        contact@visiontechsarl.com &middot; +237 674 55 49 47
      </p>
    </div>
  </div>
</body></html>"""


def send_contact_emails(contact):
    """Envoie 2 emails : accusé de réception au visiteur + notification à l'admin."""

    # ── 1. Accusé de réception au visiteur ───────────────────────────────────
    header_ar = '<p style="color:rgba(255,255,255,0.85);margin:4px 0 0;font-size:13px">Message bien reçu</p>'

    body_ar = f"""
      <h2 style="color:#0f172a;font-size:19px;margin:0 0 12px">Bonjour {contact.nom} &#128075;</h2>
      <p style="color:#475569;line-height:1.7;margin:0 0 20px">
        Nous avons bien reçu votre message et nous vous en remercions.
        Notre équipe vous répondra dans les meilleurs délais, généralement sous <strong>24 à 48 heures</strong>.
      </p>

      <div style="background:#f8fafc;border-radius:12px;padding:18px 20px;margin-bottom:24px;border:1px solid #e2e8f0">
        <h3 style="color:#0f172a;margin:0 0 12px;font-size:14px;font-weight:700">&#128203; Récapitulatif de votre message</h3>
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          {'<tr><td style="padding:5px 0;color:#64748b;width:110px">Sujet</td><td style="padding:5px 0;color:#0f172a;font-weight:600">' + contact.sujet + '</td></tr>' if contact.sujet else ''}
          <tr><td style="padding:5px 0;color:#64748b">Message</td><td style="padding:5px 0;color:#0f172a">{contact.message[:200]}{'...' if len(contact.message) > 200 else ''}</td></tr>
        </table>
      </div>

      <div style="text-align:center;margin-bottom:20px">
        <a href="{FRONTEND_URL}/contact"
           style="display:inline-block;padding:13px 28px;background:linear-gradient(135deg,#1d4ed8,#0ea5e9);
                  color:#fff;text-decoration:none;border-radius:12px;font-weight:700;font-size:14px">
          &#128222; Nous contacter à nouveau
        </a>
      </div>

      <p style="color:#94a3b8;font-size:12px;text-align:center;margin:0">
        WhatsApp : <a href="https://wa.me/237674554947" style="color:#0ea5e9">+237 674 55 49 47</a>
      </p>
    """

    msg_ar = EmailMultiAlternatives(
        subject="✅ Votre message a bien été reçu — VisionTech SARL",
        body=f"Bonjour {contact.nom}, nous avons bien reçu votre message. Nous vous répondrons sous 24-48h.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[contact.email],
    )
    msg_ar.attach_alternative(_html(header_ar, body_ar), "text/html")
    msg_ar.send()

    # ── 2. Notification admin ─────────────────────────────────────────────────
    sujet_txt = f" | Sujet : {contact.sujet}" if contact.sujet else ""
    tel_txt   = f"\nTél     : {contact.telephone}" if contact.telephone else ""

    send_mail(
        subject=f"[Contact] {contact.nom}{sujet_txt}",
        message=(
            f"Nouveau message de contact :\n\n"
            f"Nom     : {contact.nom}\n"
            f"Email   : {contact.email}"
            f"{tel_txt}\n"
            f"{'Sujet   : ' + contact.sujet + chr(10) if contact.sujet else ''}"
            f"\nMessage :\n{contact.message}\n\n"
            f"Admin   : https://api.visiontech.vision/admin/contact/contact/"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        fail_silently=True,
    )
