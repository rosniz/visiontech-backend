#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# Script d'installation VPS Ubuntu 24.04
# À exécuter UNE SEULE FOIS en tant que root sur le VPS
# Usage : bash setup-vps.sh
# ═══════════════════════════════════════════════════════════════════════════════

set -e
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# ─── Variables à adapter ──────────────────────────────────────────────────────
DEPLOY_USER="deploy"                           # Utilisateur dédié au déploiement
PROJECT_DIR="/var/www/visiontech-backend"      # Dossier du projet
REPO_URL="git@github.com:TON_USER/TON_REPO.git"  # ← Remplacer par ton repo
DOMAIN="visiontech.vision"

# ─── 1. Mise à jour système ───────────────────────────────────────────────────
log "Mise à jour du système..."
apt-get update && apt-get upgrade -y

# ─── 2. Installation des dépendances ─────────────────────────────────────────
log "Installation des dépendances..."
apt-get install -y \
    curl git nginx certbot python3-certbot-nginx \
    ufw fail2ban

# ─── 3. Installation Docker ───────────────────────────────────────────────────
log "Installation de Docker..."
if ! command -v docker &>/dev/null; then
    curl -fsSL https://get.docker.com | bash
    log "Docker installé"
else
    warn "Docker déjà installé"
fi

# ─── 4. Création de l'utilisateur deploy ─────────────────────────────────────
log "Création de l'utilisateur $DEPLOY_USER..."
if ! id "$DEPLOY_USER" &>/dev/null; then
    useradd -m -s /bin/bash "$DEPLOY_USER"
    usermod -aG docker "$DEPLOY_USER"
    usermod -aG sudo "$DEPLOY_USER"
    log "Utilisateur $DEPLOY_USER créé"
else
    warn "Utilisateur $DEPLOY_USER existe déjà"
fi

# ─── 5. Configurer SSH pour le déploiement ───────────────────────────────────
log "Configuration SSH pour $DEPLOY_USER..."
mkdir -p /home/$DEPLOY_USER/.ssh
chmod 700 /home/$DEPLOY_USER/.ssh
touch /home/$DEPLOY_USER/.ssh/authorized_keys
chmod 600 /home/$DEPLOY_USER/.ssh/authorized_keys
chown -R $DEPLOY_USER:$DEPLOY_USER /home/$DEPLOY_USER/.ssh

warn "⚠️  Ajoute ta clé SSH publique dans /home/$DEPLOY_USER/.ssh/authorized_keys"
warn "    Commande : ssh-keygen -t ed25519 -C 'github-actions-deploy'"

# ─── 6. Réseau Docker partagé pour Nginx ─────────────────────────────────────
log "Création du réseau Docker partagé nginx_proxy..."
docker network create nginx_proxy 2>/dev/null || warn "Réseau nginx_proxy existe déjà"

# ─── 7. Dossier du projet ─────────────────────────────────────────────────────
log "Création du dossier projet..."
mkdir -p "$PROJECT_DIR"
mkdir -p /var/www/visiontech/staticfiles
mkdir -p /var/www/visiontech/media
chown -R $DEPLOY_USER:$DEPLOY_USER "$PROJECT_DIR"
chown -R $DEPLOY_USER:www-data /var/www/visiontech

# ─── 8. Clone du repository ──────────────────────────────────────────────────
warn "Clone du repo (assure-toi d'avoir ajouté la deploy key sur GitHub)..."
if [ ! -d "$PROJECT_DIR/.git" ]; then
    sudo -u $DEPLOY_USER git clone "$REPO_URL" "$PROJECT_DIR"
    log "Repo cloné dans $PROJECT_DIR"
else
    warn "Repo déjà présent"
fi

# ─── 9. Configuration Nginx ───────────────────────────────────────────────────
log "Configuration Nginx..."
cp "$PROJECT_DIR/nginx/$DOMAIN.conf" "/etc/nginx/sites-available/$DOMAIN"
ln -sf "/etc/nginx/sites-available/$DOMAIN" "/etc/nginx/sites-enabled/$DOMAIN"
rm -f /etc/nginx/sites-enabled/default  # Supprimer le site par défaut
nginx -t && systemctl reload nginx
log "Nginx configuré"

# ─── 10. Certificat SSL avec Certbot ─────────────────────────────────────────
warn "Génération du certificat SSL pour $DOMAIN..."
warn "Lance manuellement : certbot --nginx -d $DOMAIN -d www.$DOMAIN"

# ─── 11. Firewall UFW ────────────────────────────────────────────────────────
log "Configuration du firewall..."
ufw --force enable
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw status

# ─── 12. Fail2ban ────────────────────────────────────────────────────────────
log "Activation de Fail2ban..."
systemctl enable fail2ban
systemctl start fail2ban

# ─── 13. Fichier .env.prod ───────────────────────────────────────────────────
if [ ! -f "$PROJECT_DIR/.env.prod" ]; then
    cp "$PROJECT_DIR/.env.prod.example" "$PROJECT_DIR/.env.prod"
    warn "⚠️  IMPORTANT : Édite $PROJECT_DIR/.env.prod avec tes vraies valeurs"
    warn "    nano $PROJECT_DIR/.env.prod"
fi

# ─── Fin ─────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   VPS configuré ! Étapes manuelles restantes :${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo "  1. Ajouter la clé SSH publique GitHub Actions dans :"
echo "     /home/$DEPLOY_USER/.ssh/authorized_keys"
echo ""
echo "  2. Éditer le fichier .env.prod :"
echo "     nano $PROJECT_DIR/.env.prod"
echo ""
echo "  3. Générer le certificat SSL :"
echo "     certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo ""
echo "  4. Lancer le projet pour la première fois :"
echo "     cd $PROJECT_DIR"
echo "     docker compose -f docker-compose.prod.yml up -d --build"
echo ""
echo "  5. Ajouter les secrets GitHub Actions (Settings → Secrets) :"
echo "     VPS_HOST     = IP de ton VPS"
echo "     VPS_USER     = $DEPLOY_USER"
echo "     VPS_SSH_KEY  = Clé privée SSH"
echo "     VPS_PORT     = 22"
echo ""