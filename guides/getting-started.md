---
layout: default
title: "Getting Started"
description: "Guide de démarrage pour utiliser les projets"
icon: "rocket"
---

# 🚀 Getting Started

Ce guide vous aidera à cloner, compiler et exécuter tous mes projets 42.

## Prérequis généraux

<div class="steps-container">
  <div class="step">
  <h4>Système d'exploitation</h4>
  <p>- **macOS** (recommandé pour les projets graphiques)
    - **Linux** (Ubuntu, Debian, Rocky Linux)
    - **WSL2** pour Windows (limité pour les projets graphiques)</p>
</div>
  
  <div class="step">
  <h4>Outils de développement</h4>
  <p>```bash
    # macOS
    xcode-select --install
    
    # Linux (Debian/Ubuntu)
    sudo apt update
    sudo apt install build-essential git make
    
    # Linux (Rocky/Fedora)
    sudo dnf groupinstall "Development Tools"
    sudo dnf install git make
    ```</p>
</div>
  
  <div class="step">
  <h4>Vérification</h4>
  <p>```bash
    # Vérifier GCC
    gcc --version
    
    # Vérifier Make
    make --version
    
    # Vérifier Git
    git --version
    ```</p>
</div>
</div>

## Structure générale d'un projet

Tous mes projets suivent une structure similaire :

```
project/
├── src/              # Code source
├── includes/         # Headers (.h)
├── libft/           # Ma bibliothèque libft
├── Makefile         # Compilation automatique
└── README.md        # Instructions spécifiques
```

## Cloner un projet

<div class="tabs-container">
<div class="tab-buttons">
  <div id="méthode-simple" class="tab-content">
```bash
    # Cloner via HTTPS
    git clone https://github.com/NikoStano/libft.git
    cd libft
    ```
</div>
  
  <div id="méthode-ssh" class="tab-content">
```bash
    # Cloner via SSH (si configuré)
    git clone git@github.com:NikoStano/libft.git
    cd libft
    ```
</div>
  
  <div id="avec-submodules" class="tab-content">
```bash
    # Si le projet a des submodules
    git clone --recurse-submodules https://github.com/NikoStano/FdF.git
    cd FdF
    ```
</div>
</div>
</div>

## Compilation d'un projet

### Commandes Make standards

Tous mes projets utilisent un Makefile avec ces commandes :

```bash
# Compiler le projet
make

# Nettoyer les fichiers objets
make clean

# Nettoyer tout (objets + exécutable)
make fclean

# Recompiler depuis zéro
make re

# Compiler avec les bonus (si disponibles)
make bonus
```

### Exemple complet : Libft

<div class="steps-container">
  <div class="step">
  <h4>Cloner</h4>
  <p>```bash
    git clone https://github.com/NikoStano/libft.git
    cd libft
    ```</p>
</div>
  
  <div class="step">
  <h4>Compiler</h4>
  <p>```bash
    make
    # Crée libft.a
    ```</p>
</div>
  
  <div class="step">
  <h4>Tester</h4>
  <p>```bash
    # Créer un fichier de test
    cat > test.c << 'EOF'
    #include "libft.h"
    #include <stdio.h>

    int main(void)
    {
        char *str = ft_strdup("Hello 42!");
        printf("%s\n", str);
        free(str);
        return (0);
    }
    EOF
    
    # Compiler avec libft
    gcc test.c -L. -lft -I. -o test
    
    # Exécuter
    ./test
    ```</p>
</div>
</div>

### Exemple : FdF (projet graphique)

<div class="steps-container">
  <div class="step">
  <h4>Cloner</h4>
  <p>```bash
    git clone https://github.com/NikoStano/FdF.git
    cd FdF
    ```</p>
</div>
  
  <div class="step">
  <h4>Installer MiniLibX (si nécessaire)</h4>
  <p>```bash
    # macOS - déjà inclus
    
    # Linux
    sudo apt install libx11-dev libxext-dev libbsd-dev
    git clone https://github.com/42Paris/minilibx-linux.git
    cd minilibx-linux
    make
    cd ..
    ```</p>
</div>
  
  <div class="step">
  <h4>Compiler</h4>
  <p>```bash
    make
    ```</p>
</div>
  
  <div class="step">
  <h4>Exécuter</h4>
  <p>```bash
    # Avec une carte de test
    ./fdf maps/42.fdf
    ```</p>
</div>
</div>

### Exemple : Push Swap

<div class="steps-container">
  <div class="step">
  <h4>Cloner</h4>
  <p>```bash
    git clone https://github.com/NikoStano/push_swap.git
    cd push_swap
    ```</p>
</div>
  
  <div class="step">
  <h4>Compiler</h4>
  <p>```bash
    make
    # Crée l'exécutable push_swap
    
    # Pour le bonus (checker)
    make bonus
    ```</p>
</div>
  
  <div class="step">
  <h4>Tester</h4>
  <p>```bash
    # Trier 3 nombres
    ./push_swap 2 1 3
    
    # Trier 5 nombres
    ./push_swap 5 3 1 4 2
    
    # Trier 100 nombres aléatoires
    ARG=$(seq 1 100 | shuf | tr '\n' ' ')
    ./push_swap $ARG | wc -l
    
    # Vérifier avec checker
    ./push_swap $ARG | ./checker $ARG
    ```</p>
</div>
</div>

### Exemple : Minitalk

<div class="steps-container">
  <div class="step">
  <h4>Cloner</h4>
  <p>```bash
    git clone https://github.com/NikoStano/minitalk.git
    cd minitalk
    ```</p>
</div>
  
  <div class="step">
  <h4>Compiler</h4>
  <p>```bash
    make
    # Crée server et client
    ```</p>
</div>
  
  <div class="step">
  <h4>Utiliser</h4>
  <p>```bash
    # Terminal 1 : Lancer le serveur
    ./server
    # Note le PID affiché, par exemple: 12345
    
    # Terminal 2 : Envoyer un message
    ./client 12345 "Hello 42!"
    ```</p>
</div>
</div>

## Résolution des problèmes courants

<details>
<summary>Erreur: command not found</summary>

<Accordion title="Erreur: command not found">
    **Problème** : `make: command not found`
    
    **Solution** :
    ```bash
    # macOS
    xcode-select --install
    
    # Linux
    sudo apt install make
    ```
</details>
  
  <details>
<summary>Erreur: No rule to make target</summary>

**Problème** : `make: *** No rule to make target`
    
    **Solution** :
    ```bash
    # Vérifier que vous êtes dans le bon dossier
    ls Makefile
    
    # Nettoyer et recompiler
    make fclean
    make
    ```
</details>
  
  <details>
<summary>Erreur de compilation avec libft</summary>

**Problème** : `libft.h: No such file or directory`
    
    **Solution** :
    ```bash
    # Compiler libft d'abord
    cd libft
    make
    cd ..
    
    # Puis recompiler le projet
    make
    ```
</details>
  
  <details>
<summary>Erreur MiniLibX (macOS)</summary>

**Problème** : `mlx.h: No such file or directory`
    
    **Solution** :
    ```bash
    # Installer depuis le repo officiel
    git clone https://github.com/42Paris/minilibx-opengl.git mlx
    cd mlx
    make
    cd ..
    
    # Ajuster le Makefile si nécessaire
    ```
</details>
  
  <details>
<summary>Erreur MiniLibX (Linux)</summary>

**Problème** : Linking errors avec MLX
    
    **Solution** :
    ```bash
    # Installer les dépendances
    sudo apt install libx11-dev libxext-dev libbsd-dev
    
    # Cloner et compiler minilibx
    git clone https://github.com/42Paris/minilibx-linux.git
    cd minilibx-linux
    make
    ```
</details>
  
  <details>
<summary>Permission denied</summary>

**Problème** : `./program: Permission denied`
    
    **Solution** :
    ```bash
    # Donner les droits d'exécution
    chmod +x program
    
    # Ou recompiler
    make re
    ```
</details>


## Tests et validation

### Norminette

Tous mes projets respectent la norme 42 :

```bash
# Installer norminette
pip3 install norminette

# Vérifier un fichier
norminette file.c

# Vérifier tout le projet
norminette src/*.c includes/*.h

# Vérifier avec libft
norminette src/*.c includes/*.h libft/*.c libft/*.h
```

### Valgrind (détection de fuites mémoire)

```bash
# Installer valgrind
# macOS (difficile, utiliser plutôt leaks)
brew install valgrind

# Linux
sudo apt install valgrind

# Utiliser valgrind
valgrind --leak-check=full ./program arguments

# macOS alternative : leaks
leaks -atExit -- ./program arguments
```

### Tests unitaires

Mes projets peuvent être testés avec des testeurs communautaires :

```bash
# Pour libft
git clone https://github.com/Tripouille/libftTester.git
cd libftTester
make

# Pour get_next_line
git clone https://github.com/Tripouille/gnlTester.git
cd gnlTester
make m

# Pour ft_printf
git clone https://github.com/Tripouille/printfTester.git
cd printfTester
make
```

## Workflow de développement recommandé

<div class="steps-container">
  <div class="step">
  <h4>Comprendre le sujet</h4>
  <p>- Lire le PDF du sujet attentivement
    - Identifier les fonctions autorisées
    - Comprendre les contraintes</p>
</div>
  
  <div class="step">
  <h4>Planifier</h4>
  <p>- Dessiner l'architecture du projet
    - Lister les fonctions à créer
    - Définir les structures de données</p>
</div>
  
  <div class="step">
  <h4>Coder</h4>
  <p>- Commencer par les fonctions simples
    - Tester chaque fonction individuellement
    - Commit régulièrement
    
    ```bash
    git add file.c
    git commit -m "Add: ft_strlen function"
    ```</p>
</div>
  
  <div class="step">
  <h4>Tester</h4>
  <p>- Compiler souvent
    - Utiliser les testeurs
    - Vérifier avec valgrind
    
    ```bash
    make re
    valgrind ./program test
    norminette
    ```</p>
</div>
  
  <div class="step">
  <h4>Optimiser</h4>
  <p>- Refactoriser le code
    - Améliorer la lisibilité
    - Optimiser les performances</p>
</div>
</div>

## Variables d'environnement utiles

```bash
# Ajouter à ~/.bashrc ou ~/.zshrc

# Flags de compilation stricte
export CFLAGS="-Wall -Wextra -Werror -g"

# Alias utiles
alias norm="norminette"
alias val="valgrind --leak-check=full --show-leak-kinds=all"
alias remake="make fclean && make"

# Couleurs