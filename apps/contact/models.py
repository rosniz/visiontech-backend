from django.db import models


class Contact(models.Model):
    """Modèle pour les messages de contact"""
    
    nom = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Message")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    lu = models.BooleanField(default=False, verbose_name="Lu")
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
    
    def __str__(self):
        return f"{self.nom} - {self.email} ({self.date.strftime('%d/%m/%Y')})"
