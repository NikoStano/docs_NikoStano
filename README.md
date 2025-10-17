# 🎨 Guide des Composants Personnalisés

Ce guide explique comment utiliser tous les composants stylisés de votre site.

## 📝 Notes et Alertes

### Note (Bleu)
```markdown
{: .note }
>
> Ceci est une note importante avec des informations utiles.
```

### Tip (Vert)
```markdown
{: .tip }
>
> Voici une astuce pour vous aider !
```

### Warning (Orange)
```markdown
{: .warning }
>
> Attention ! Ceci est un avertissement.
```

### Info (Cyan)
```markdown
{: .info }
>
> Information supplémentaire à connaître.
```

### Check (Vert succès)
```markdown
{: .check }
>
> Validé ! Tout est correct.
```

## 📦 Cards

### Card simple
```html
<div class="card">
  <h3>Titre de la card</h3>
  <p>Description de la card</p>
  <a href="#" class="btn">Voir plus</a>
</div>
```

### Card avec badge
```html
<div class="project-card">
  <span class="badge badge-success">125/100</span>
  <h3>Titre du projet</h3>
  <p>Description du projet</p>
  <a href="#" class="btn btn-primary">Voir plus</a>
</div>
```

### Grille de cards
```html
<div class="card-container">
  <div class="card">
    <h3>Card 1</h3>
    <p>Contenu</p>
  </div>
  <div class="card">
    <h3>Card 2</h3>
    <p>Contenu</p>
  </div>
</div>
```

## 🔢 Steps (Étapes numérotées)

```html
<div class="steps-container">
  <div class="step">
    <h4>Étape 1</h4>
    <p>Description de l'étape</p>
  </div>
  <div class="step">
    <h4>Étape 2</h4>
    <p>Description de l'étape</p>
  </div>
</div>
```

## 📑 Tabs (Onglets)

```html
<div class="tabs-container">
  <div class="tab-buttons"></div>
  <div id="tab1" class="tab-content">
    Contenu de l'onglet 1
  </div>
  <div id="tab2" class="tab-content">
    Contenu de l'onglet 2
  </div>
</div>
```

Le JavaScript va automatiquement créer les boutons basés sur les IDs.

## 🔽 Accordéon (Details/Summary)

```html
<details>
  <summary>Titre cliquable</summary>

  Contenu caché qui s'affiche au clic.
</details>
```

## 🎨 Badges

```html
<!-- Badges de statut -->
<span class="badge badge-success">Success</span>
<span class="badge badge-info">Info</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-primary">Primary</span>
```

## 🔘 Boutons

```html
<!-- Bouton standard -->
<a href="#" class="btn">Bouton</a>

<!-- Bouton primaire -->
<a href="#" class="btn btn-primary">Bouton primaire</a>

<!-- Bouton externe (avec flèche) -->
<a href="#" class="btn btn-external">Lien externe</a>
```

## 📊 Tableaux

Les tableaux sont automatiquement stylisés :

```markdown
| Colonne 1 | Colonne 2 | Colonne 3 |
|-----------|-----------|-----------|
| Data 1    | Data 2    | Data 3    |
| Data 4    | Data 5    | Data 6    |
```

## 💻 Blocs de code

Les blocs de code ont automatiquement un bouton de copie :

````markdown
```javascript
function hello() {
  console.log("Hello World!");
}
```
````

## 🖼️ Images

### Image centrée
```markdown
![Description](image.png){: .centered-image}
```

### Badge image
```markdown
![Score](https://img.shields.io/badge/Score-125%2F100-success)
```

## 🎯 Classes utilitaires

```html
<!-- Centrer du texte -->
<div class="text-center">
  Texte centré
</div>
```

## 🎨 Personnalisation des couleurs

Pour changer les couleurs, modifiez les variables CSS dans `custom.css` :

```css
:root {
  --note-bg: #1e293b;
  --note-border: #3b82f6;
  --card-bg: #1e293b;
  --card-border: #334155;
  /* etc. */
}
```

## 📱 Responsive

Tous les composants sont automatiquement responsives et s'adaptent aux petits écrans.

## 💡 Exemples complets

### Page avec tous les composants

```markdown
---
layout: default
title: "Ma Page"
---

# Titre Principal

{: .note }
> Note importante en début de page

## Section 1

<div class="card-container">
  <div class="card">
    <h3>Feature 1</h3>
    <p>Description</p>
    <a href="#" class="btn">En savoir plus</a>
  </div>
  <div class="card">
    <h3>Feature 2</h3>
    <p>Description</p>
    <a href="#" class="btn">En savoir plus</a>
  </div>
</div>

## Section 2

<div class="steps-container">
  <div class="step">
    <h4>Première étape</h4>
    <p>Faire ceci</p>
  </div>
  <div class="step">
    <h4>Deuxième étape</h4>
    <p>Puis cela</p>
  </div>
</div>

{: .tip }
> Astuce finale pour conclure
```

## 🔧 Debugging

Si un composant ne s'affiche pas correctement :

1. Vérifiez que `custom.css` est bien chargé
2. Vérifiez que `custom.js` est bien chargé
3. Ouvrez la console du navigateur (F12) pour voir les erreurs
4. Vérifiez que la structure HTML est correcte

## 📖 Ressources

- [Just the Docs Documentation](https://just-the-docs.github.io/just-the-docs/)
- [Kramdown Syntax](https://kramdown.gettalong.org/syntax.html)
- [Jekyll Documentation](https://jekyllrb.com/docs/)