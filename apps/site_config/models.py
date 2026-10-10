from django.conf import settings
from django.core.cache import cache
from django.db import models

CACHE_KEY = 'site_config:parametres'
CACHE_TTL = 30  # secondes


class ParametresSite(models.Model):
    """Paramètres globaux du site (une seule ligne, pk=1)."""

    maintenance_active  = models.BooleanField(default=False, verbose_name='Mode maintenance actif')
    maintenance_message = models.TextField(
        blank=True,
        default="Notre site fait peau neuve. Nous revenons très vite !",
        verbose_name='Message affiché aux visiteurs',
    )
    maintenance_fin = models.DateTimeField(null=True, blank=True, verbose_name='Retour prévu')

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='+', verbose_name='Modifié par',
    )

    class Meta:
        verbose_name = 'Paramètres du site'
        verbose_name_plural = 'Paramètres du site'

    def __str__(self):
        return 'Paramètres du site'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete(CACHE_KEY)

    def delete(self, *args, **kwargs):
        pass  # singleton : ne se supprime pas

    @classmethod
    def charger(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @classmethod
    def etat_maintenance(cls):
        """État de maintenance mis en cache (lu à chaque requête API par le middleware)."""
        etat = cache.get(CACHE_KEY)
        if etat is None:
            p = cls.charger()
            etat = {
                'maintenance': p.maintenance_active,
                'message': p.maintenance_message,
                'fin': p.maintenance_fin.isoformat() if p.maintenance_fin else None,
            }
            cache.set(CACHE_KEY, etat, CACHE_TTL)
        return etat
