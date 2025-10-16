---
layout: default
title: "Born2beroot"
nav_order: 4
description: "Administration système et virtualisation"
icon: "server"
---

# 🖥️ Born2beroot

![Score](https://img.shields.io/badge/Score-125%2F100-success)
![OS](https://img.shields.io/badge/OS-Rocky%20Linux-blue)
![Type](https://img.shields.io/badge/Type-SysAdmin-orange)

## Introduction

**Born2beroot** est votre premier projet d'administration système. Vous devez créer et configurer une machine virtuelle sous Rocky Linux (ou Debian) avec des politiques de sécurité strictes.

{: .note }
>
Ce projet vous initie aux concepts fondamentaux de l'administration système Linux : virtualisation, partitionnement, services, sécurité et monitoring.

## Objectifs du projet

<div class="steps-container">
  <div class="step">
  <h4>Créer une VM</h4>
  <p>Installer Rocky Linux sur VirtualBox ou UTM</p>
</div>

  <div class="step">
  <h4>Configurer LVM</h4>
  <p>Mettre en place le Logical Volume Manager avec partitions chiffrées</p>
</div>

  <div class="step">
  <h4>Sécuriser le système</h4>
  <p>Configurer SSH, pare-feu, politique de mots de passe</p>
</div>

  <div class="step">
  <h4>Créer un script monitoring</h4>
  <p>Script bash affichant des informations système toutes les 10 minutes</p>
</div>
</div>

## Configuration requise

### Partitionnement obligatoire

```
sda
├── sda1       512M    /boot
└── sda5       XXXG    Chiffré (LVM)
    └── LVMGroup
        ├── root    10G     /
        ├── swap    2.3G    swap
        ├── home    5G      /home
        ├── var     3G      /var
        ├── srv     3G      /srv
        ├── tmp     3G      /tmp
        └── var-log 4G      /var/log
```

{: .warning }
>
La partition principale doit être chiffrée avec LUKS. Vous devrez entrer le mot de passe au démarrage.

### Services à configurer

<details>
<summary>SSH (Secure Shell)</summary>

- Port personnalisé (pas 22)
  - Interdire connexion root
  - Utiliser clés SSH

  ```bash
  # /etc/ssh/sshd_config
  Port 4242
  PermitRootLogin no
  PasswordAuthentication no
  ```
</details>

<details>
<summary>UFW (Uncomplicated Firewall)</summary>

- Autoriser uniquement le port SSH
  - Bloquer tout le reste par défaut

  ```bash
  ufw enable
  ufw allow 4242
  ufw status
  ```
</details>

<details>
<summary>Sudo</summary>

- Configuration stricte
  - Limitation des tentatives
  - Logs des commandes

  ```bash
  # /etc/sudoers.d/sudo_config
  Defaults  passwd_tries=3
  Defaults  badpass_message="Wrong password. Try again!"
  Defaults  logfile="/var/log/sudo/sudo.log"
  Defaults  log_input,log_output
  Defaults  requiretty
  ```
</details>

<details>
<summary>Politique de mots de passe</summary>

- Expiration tous les 30 jours
  - Minimum 2 jours avant changement
  - Avertissement 7 jours avant expiration
  - Longueur minimum 10 caractères
  - Complexité requise

  ```bash
  # /etc/login.defs
  PASS_MAX_DAYS 30
  PASS_MIN_DAYS 2
  PASS_WARN_AGE 7
  ```

  ```bash
  # /etc/security/pwquality.conf
  minlen = 10
  ucredit = -1
  dcredit = -1
  lcredit = -1
  maxrepeat = 3
  usercheck = 1
  difok = 7
  enforce_for_root
  ```
</details>

## Installation pas à pas

### 1. Création de la VM

<div class="tabs-container">
  <div class="tab-buttons"></div>
  <div id="virtualbox" class="tab-content">
```bash
    # Configuration recommandée
    Type: Linux
    Version: Red Hat (64-bit)
    RAM: 2048 MB
    Disque: 30 GB (VDI, dynamiquement alloué)

    # Réseau
    Adaptateur 1: NAT ou Pont
    ```
  </div>
</div>
</div>

### 2. Installation Rocky Linux

<div class="steps-container">
  <div class="step">
  <h4>Démarrage</h4>
  <p>Monter l'ISO Rocky Linux et démarrer la VM</p>
</div>

  <div class="step">
  <h4>Langue et clavier</h4>
  <p>Sélectionner Anglais et disposition clavier</p>
</div>

  <div class="step">
  <h4>Partitionnement manuel</h4>
  <p>Choisir "Custom" pour créer les partitions manuellement

    ```
    1. Créer /boot (512M, ext4)
    2. Créer partition chiffrée (reste du disque)
    3. Créer volume group LVMGroup
    4. Créer les logical volumes
    ```</p>
</div>

  <div class="step">
  <h4>Chiffrement</h4>
  <p>Activer le chiffrement LUKS sur la partition principale

    **Mot de passe fort requis !**</p>
</div>

  <div class="step">
  <h4>Utilisateur</h4>
  <p>- Créer utilisateur (votre login 42)
    - Définir mot de passe root
    - NE PAS créer d'utilisateur supplémentaire pendant l'installation</p>
</div>

  <div class="step">
  <h4>Installation minimale</h4>
  <p>Choisir "Minimal Install" - pas d'interface graphique</p>
</div>
</div>

### 3. Configuration post-installation

#### Mise à jour du système

```bash
# Se connecter en root
su -

# Mettre à jour
dnf update -y

# Installer les outils nécessaires
dnf install -y vim sudo ufw
```

#### Configuration sudo

```bash
# Ajouter l'utilisateur au groupe sudo
usermod -aG sudo votre_login

# Créer le fichier de config sudo
visudo -f /etc/sudoers.d/sudo_config
```

Contenu du fichier :
```
Defaults  passwd_tries=3
Defaults  badpass_message="Wrong password!"
Defaults  logfile="/var/log/sudo/sudo.log"
Defaults  log_input,log_output
Defaults  iolog_dir="/var/log/sudo"
Defaults  requiretty
Defaults  secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```

#### Configuration SSH

```bash
# Modifier le fichier sshd_config
vim /etc/ssh/sshd_config
```

Modifications :
```bash
Port 4242
PermitRootLogin no
PasswordAuthentication yes  # pour l'évaluation
```

```bash
# Redémarrer SSH
systemctl restart sshd

# Activer au démarrage
systemctl enable sshd
```

#### Configuration UFW

```bash
# Activer UFW
ufw enable

# Autoriser le port SSH
ufw allow 4242

# Vérifier
ufw status numbered
```

#### Politique de mots de passe

```bash
# Installer libpwquality
dnf install -y libpwquality

# Modifier login.defs
vim /etc/login.defs
```

```bash
PASS_MAX_DAYS 30
PASS_MIN_DAYS 2
PASS_WARN_AGE 7
```

```bash
# Modifier pwquality.conf
vim /etc/security/pwquality.conf
```

```bash
minlen = 10
ucredit = -1
dcredit = -1
lcredit = -1
maxrepeat = 3
usercheck = 1
difok = 7
enforce_for_root
```

```bash
# Appliquer aux utilisateurs existants
chage -M 30 -m 2 -W 7 votre_login
chage -M 30 -m 2 -W 7 root
```

## Script de monitoring

Le script `monitoring.sh` doit afficher ces informations toutes les 10 minutes via wall :

```bash
#!/bin/bash

# Architecture
arch=$(uname -a)

# CPU physiques
pcpu=$(grep "physical id" /proc/cpuinfo | wc -l)

# CPU virtuels
vcpu=$(grep "processor" /proc/cpuinfo | wc -l)

# Mémoire RAM
ram_total=$(free --mega | awk '$1 == "Mem:" {print $2}')
ram_used=$(free --mega | awk '$1 == "Mem:" {print $3}')
ram_percent=$(free --mega | awk '$1 == "Mem:" {printf("%.2f"), $3/$2*100}')

# Disque
disk_total=$(df -m | grep "/dev/" | grep -v "/boot" | awk '{disk_t += $2} END {printf ("%.1fGb\n"), disk_t/1024}')
disk_used=$(df -m | grep "/dev/" | grep -v "/boot" | awk '{disk_u += $3} END {print disk_u}')
disk_percent=$(df -m | grep "/dev/" | grep -v "/boot" | awk '{disk_u += $3} {disk_t+= $2} END {printf("%d"), disk_u/disk_t*100}')

# CPU load
cpu_load=$(vmstat 1 2 | tail -1 | awk '{printf $15}')
cpu_op=$(expr 100 - $cpu_load)
cpu_fin=$(printf "%.1f" $cpu_op)

# Dernier boot
lb=$(who -b | awk '$1 == "system" {print $3 " " $4}')

# LVM actif
lvmu=$(if [ $(lsblk | grep "lvm" | wc -l) -gt 0 ]; then echo yes; else echo no; fi)

# Connexions TCP
tcpc=$(ss -ta | grep ESTAB | wc -l)

# Nombre d'utilisateurs
ulog=$(users | wc -w)

# Adresse IP et MAC
ip=$(hostname -I)
mac=$(ip link | grep "link/ether" | awk '{print $2}')

# Nombre de commandes sudo
cmds=$(journalctl _COMM=sudo | grep COMMAND | wc -l)

wall "	Architecture: $arch
	CPU physical: $pcpu
	vCPU: $vcpu
	Memory Usage: $ram_used/${ram_total}MB ($ram_percent%)
	Disk Usage: $disk_used/${disk_total} ($disk_percent%)
	CPU load: $cpu_fin%
	Last boot: $lb
	LVM use: $lvmu
	Connections TCP: $tcpc ESTABLISHED
	User log: $ulog
	Network: IP $ip ($mac)
	Sudo: $cmds cmd"
```

### Configuration cron

```bash
# Éditer crontab en root
sudo crontab -e

# Ajouter la ligne
*/10 * * * * /usr/local/bin/monitoring.sh
```

{: .tip }
>
Pour tester sans attendre 10 minutes : `sudo /usr/local/bin/monitoring.sh`

## Commandes essentielles

### Gestion des utilisateurs

```bash
# Créer un utilisateur
sudo adduser username

# Ajouter au groupe
sudo usermod -aG groupname username

# Changer le mot de passe
sudo passwd username

# Voir les groupes d'un utilisateur
groups username

# Lister tous les utilisateurs
cat /etc/passwd

# Politique de mot de passe d'un utilisateur
sudo chage -l username
```

### Gestion des groupes

```bash
# Créer un groupe
sudo groupadd groupname

# Supprimer un groupe
sudo groupdel groupname

# Lister tous les groupes
cat /etc/group

# Voir les membres d'un groupe
getent group groupname
```

### SSH

```bash
# Status du service
sudo systemctl status sshd

# Redémarrer
sudo systemctl restart sshd

# Se connecter depuis l'hôte
ssh votre_login@localhost -p 4242
```

### UFW

```bash
# Status
sudo ufw status numbered

# Ajouter une règle
sudo ufw allow 8080

# Supprimer une règle
sudo ufw delete 2

# Désactiver
sudo ufw disable
```

### Hostname

```bash
# Voir le hostname
hostnamectl

# Changer le hostname
sudo hostnamectl set-hostname nouveau_nom

# Modifier aussi /etc/hosts
sudo vim /etc/hosts
```

### LVM

```bash
# Afficher les volumes
sudo lvdisplay

# Afficher les groupes
sudo vgdisplay

# Afficher les partitions physiques
sudo pvdisplay

# Résumé
lsblk
```

## Questions fréquentes de défense

<details>
<summary>Quelle est la différence entre apt et aptitude ?</summary>

- **apt** : Interface en ligne de commande simple
    - **aptitude** : Interface plus avancée avec résolution de dépendances

    Sur Rocky Linux, on utilise **dnf** (ou yum)
</details>

  <details>
<summary>Qu'est-ce que SELinux / AppArmor ?</summary>

Systèmes de contrôle d'accès obligatoire (MAC) qui renforcent la sécurité

    - **SELinux** : utilisé par Rocky Linux/RedHat
    - **AppArmor** : utilisé par Debian/Ubuntu
</details>

  <details>
<summary>Comment fonctionne LVM ?</summary>

**LVM** (Logical Volume Manager) permet :
    - Redimensionner les partitions à chaud
    - Créer des snapshots
    - Gérer plusieurs disques comme un seul volume

    Hiérarchie : Physical Volume → Volume Group → Logical Volume
</details>

  <details>
<summary>Pourquoi sudo ?</summary>

- Meilleur audit des commandes
    - Pas besoin du mot de passe root
    - Permissions granulaires
    - Logs des actions
</details>

  <details>
<summary>Qu'est-ce qu'UFW ?</summary>

**Uncomplicated Firewall** : interface simplifiée pour iptables

    Permet de gérer facilement les règles de pare-feu
</details>

## Checklist de défense

<div class="steps-container">
  <div class="step">
  <h4>Vérifications initiales</h4>
  <p>- [ ] Pas d'interface graphique
    - [ ] SSH fonctionne sur port 4242
    - [ ] UFW actif avec bonnes règles
    - [ ] Partitionnement correct (lsblk)</p>
</div>

  <div class="step">
  <h4>Utilisateurs et groupes</h4>
  <p>- [ ] Créer nouvel utilisateur
    - [ ] Créer groupe "evaluating"
    - [ ] Ajouter utilisateur au groupe
    - [ ] Expliquer politique de mots de passe</p>
</div>

  <div class="step">
  <h4>Hostname et partitions</h4>
  <p>- [ ] Afficher hostname
    - [ ] Modifier hostname
    - [ ] Afficher partitions (lsblk)
    - [ ] Expliquer LVM</p>
</div>

  <div class="step">
  <h4>Sudo</h4>
  <p>- [ ] Vérifier config sudo
    - [ ] Montrer les logs
    - [ ] Expliquer TTY requirement</p>
</div>

  <div class="step">
  <h4>UFW</h4>
  <p>- [ ] Vérifier règles
    - [ ] Ajouter/supprimer règle</p>
</div>

  <div class="step">
  <h4>SSH</h4>
  <p>- [ ] Vérifier config
    - [ ] Expliquer pourquoi pas root
    - [ ] Tester connexion</p>
</div>

  <div class="step">
  <h4>Script monitoring</h4>
  <p>- [ ] Expliquer chaque ligne
    - [ ] Montrer cron
    - [ ] Arrêter/démarrer cron</p>
</div>
</div>

## Bonus

<details>
<summary>WordPress + Lighttpd + MariaDB + PHP</summary>

Configuration d'un serveur web complet avec :
  - Lighttpd comme serveur web
  - MariaDB pour la base de données
  - PHP pour WordPress
  - Configuration sur un port différent
</details>

<details>
<summary>Service supplémentaire</summary>

Installer et configurer un service utile de votre choix :
  - Fail2ban (protection contre bruteforce)
  - Netdata (monitoring en temps réel)
  - Cockpit (interface web d'administration)
</details>

## Ressources

<div class="card-container">
  <div class="project-card">
  <h3>man sudoers</h3>
  <p>```bash
    man sudoers
    ```
    Configuration complète de sudo</p>
</div>

  <div class="project-card">
  <h3>Rocky Linux Docs</h3>
  <p>Documentation officielle</p>
  <a href="https://docs.rockylinux.org/" class="btn btn-primary">Voir plus</a>
</div>

  <div class="project-card">
  <h3>LVM Guide</h3>
  <p>Comprendre LVM</p>
  <a href="https://www.redhat.com/sysadmin/lvm-vs-partitioning" class="btn btn-primary">Voir plus</a>
</div>

  <div class="project-card">
  <h3>SSH Hardening</h3>
  <p>Sécuriser SSH</p>
  <a href="https://www.ssh.com/academy/ssh/sshd_config" class="btn btn-primary">Voir plus</a>
</div>
</div>

## Conclusion

Born2beroot est votre porte d'entrée dans le monde de l'administration système. Les compétences acquises sont essentielles pour comprendre comment fonctionnent les serveurs Linux.

{: .check }
>
Ce projet vous servira de base pour tous les projets futurs nécessitant un serveur ou une VM.

{: .note }
>
Prenez le temps de comprendre chaque commande plutôt que de simplement copier-coller. L'évaluation testera votre compréhension réelle !
