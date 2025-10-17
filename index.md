---
layout: default
title: Accueil
nav_order: 1
description: "Documentation des projets de nistanoj @ 42 Paris"
permalink: /
---

# 👋 Bienvenue sur ma Documentation

![42 Badge](https://badge.mediaplus.ma/darkblue/nistanoj?1337Badge=off&42Network=off&UM6P=off){: .centered-image}

## À propos

Je suis **Nikola** (nistanoj), étudiant à **42 Paris**. Cette documentation regroupe tous mes projets réalisés durant mon cursus, avec des explications techniques, des guides d'utilisation et des ressources pour comprendre chaque projet en profondeur.

---

## 🚀 Navigation rapide

<div class="card-grid">
  <div class="card">
    <h3>📁 Découvrir mes projets</h3>
    <p>Explorez mes réalisations à 42 Paris</p>
    <a href="{{ site.baseurl }}/projects/" class="btn">Voir les projets</a>
  </div>

  <div class="card">
    <h3>📖 Guides pratiques</h3>
    <p>Apprenez à compiler et utiliser mes projets</p>
    <a href="{{ site.baseurl }}/guides/getting-started" class="btn">Commencer</a>
  </div>

  <div class="card">
    <h3>🔗 GitHub</h3>
    <p>Consultez le code source sur GitHub</p>
    <a href="https://github.com/NikoStano" class="btn btn-external">GitHub</a>
  </div>

  <div class="card">
    <h3>👤 Mon Portfolio</h3>
    <p>Découvrez mon portfolio complet</p>
    <a href="https://nikostano.github.io/portfolio" class="btn btn-external">Portfolio</a>
  </div>
</div>

---

## 🎯 Projets phares

### 🔷 Libft - Ma bibliothèque C personnelle
Recréation des fonctions essentielles de la libc en C. Premier projet du cursus 42, il constitue la base de tous mes projets suivants.

[Voir la documentation →]({{ site.baseurl }}/projects/libft){: .btn .btn-primary}

---

### 🎨 FdF - Wireframe 3D
Affichage graphique d'une carte en 3D avec projection isométrique. Utilisation de transformations matricielles et de la MiniLibX.

[Voir la documentation →]({{ site.baseurl }}/projects/fdf){: .btn .btn-primary}

---

### 📊 Push Swap - Algorithme de tri
Programme de tri optimisé utilisant deux piles et un ensemble limité d'opérations. Challenge algorithmique complexe.

[Voir la documentation →]({{ site.baseurl }}/projects/push-swap){: .btn .btn-primary}

---

### 📡 Minitalk - Communication Unix
Système de communication client-serveur utilisant les signaux Unix (SIGUSR1 et SIGUSR2).

[Voir la documentation →]({{ site.baseurl }}/projects/minitalk){: .btn .btn-primary}

---

## 💻 Technologies maîtrisées

| Langages | Outils | Systèmes | Concepts |
|----------|--------|----------|----------|
| C | Git / GitHub | Linux / Unix | Algorithmie |
| Python | Make | Rocky Linux | Gestion mémoire |
| Shell Script | GDB / Valgrind | Debian | Structures de données |

---

## 💡 Philosophie

{: .note }
> Mon parcours à 42 est guidé par une soif insatiable de connaissances et une passion pour la résolution de problèmes complexes. J'aime comprendre comment les choses fonctionnent en profondeur.

{: .tip }
> **Rigoureux, sérieux et curieux**, je sais m'intégrer dans toutes situations et j'apprécie l'originalité et la pensée latérale dans la programmation.

---

## 📬 Contact

Pour toute question ou collaboration :

**Email:** [nistanoj@student.42.fr](mailto:nistanoj@student.42.fr)

**GitHub:** [NikoStano](https://github.com/NikoStano)

---

<style>
.centered-image {
  display: block;
  margin: 2rem auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.card {
  padding: 1.5rem;
  border: 1px solid var(--border-color, #e1e4e8);
  border-radius: 8px;
  background: var(--card-bg,rgb(59, 60, 62));
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.card h3 {
  margin-top: 0;
  color: var(--primary-color, #0366d6);
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  margin-top: 0.5rem;
  background: var(--primary-color, #0366d6);
  color: white !important;
  text-decoration: none;
  border-radius: 6px;
  transition: background 0.2s;
}

.btn:hover {
  background: var(--primary-hover, #0256c7);
}

.btn-external::after {
  content: " ↗";
}
</style>