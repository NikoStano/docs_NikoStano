# Guide de Migration : Mintlify → Jekyll (GitHub Pages)

Ce guide explique comment migrer votre documentation de Mintlify vers Jekyll pour l'héberger sur GitHub Pages.

## 📋 Prérequis

- Ruby 3.0+ installé
- Git configuré
- Compte GitHub
- Accès au dossier Mintlify existant

### Installation de Ruby (si nécessaire)

```bash
# macOS
brew install ruby

# Linux (Ubuntu/Debian)
sudo apt-get install ruby-full build-essential

# Vérifier l'installation
ruby --version
gem --version
```

---

## 🚀 Étapes de Migration

### 1. Créer le nouveau projet Jekyll

```bash
# Créer le dossier du projet
mkdir nikostano-docs-jekyll
cd nikostano-docs-jekyll

# Créer le Gemfile
cat > Gemfile << 'EOF'
source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "just-the-docs", "0.7.0"
gem "jekyll-seo-tag"
gem "jekyll-sitemap"

group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-relative-links"
end
EOF

# Installer les dépendances
bundle install
```

### 2. Créer la structure du projet

```bash
# Créer les dossiers
mkdir -p assets/css assets/images projects guides _includes/components

# Créer les fichiers de configuration
touch _config.yml index.md about.md
```

### 3. Copier les fichiers de configuration

Copiez le contenu de `_config.yml` fourni dans l'artifact précédent.

### 4. Copier et adapter les assets

```bash
# Copier les logos et favicon
cp ../mintlify-docs/logo/light.svg assets/images/logo.png
cp ../mintlify-docs/favicon.svg assets/images/favicon.png

# Créer le CSS personnalisé
cp custom.css assets/css/custom.css
```

### 5. Convertir les fichiers MDX en Markdown

#### Option A : Conversion manuelle

Pour chaque fichier `.mdx`, créer un `.md` équivalent en:
1. Modifiant le frontmatter
2. Remplaçant les composants Mintlify par des équivalents Jekyll
3. Ajustant la syntaxe

#### Option B : Utiliser le script de conversion

```bash
# Rendre le script exécutable
chmod +x convert_mdx_to_md.py

# Convertir un fichier unique
python3 convert_mdx_to_md.py ../mintlify-docs/projects/libft.mdx projects/libft.md

# Convertir tout un dossier
python3 convert_mdx_to_md.py ../mintlify-docs/projects/ projects/
```

### 6. Adapter les composants

#### Composants Mintlify → Équivalents Jekyll

| Mintlify | Jekyll |
|----------|--------|
| `<Note>` | `{: .note }` + blockquote |
| `<Tip>` | `{: .tip }` + blockquote |
| `<Warning>` | `{: .warning }` + blockquote |
| `<Card>` | `<div class="project-card">` |
| `<Steps>` | `<div class="steps-container">` |
| `<Accordion>` | `<details>` |
| `<Tabs>` | Custom HTML + JS |

#### Exemples de conversion

**Note:**
```markdown
<!-- Avant (Mintlify) -->
<Note>
Ceci est une note importante
</Note>

<!-- Après (Jekyll) -->
{: .note }
> Ceci est une note importante
```

**Card:**
```markdown
<!-- Avant (Mintlify) -->
<Card title="GitHub" icon="github" href="https://github.com/NikoStano">
  Voir mes projets
</Card>

<!-- Après (Jekyll) -->
<div class="project-card">
  <h3>🔗 GitHub</h3>
  <p>Voir mes projets</p>
  <a href="https://github.com/NikoStano" class="btn">Accéder</a>
</div>
```

**Steps:**
```markdown
<!-- Avant (Mintlify) -->
<Steps>
  <Step title="Installation">
    Installer les dépendances
  </Step>
  <Step title="Configuration">
    Configurer le projet
  </Step>
</Steps>

<!-- Après (Jekyll) -->
<div class="steps-container">
  <div class="step">
    <h4>Installation</h4>
    <p>Installer les dépendances</p>
  </div>
  <div class="step">
    <h4>Configuration</h4>
    <p>Configurer le projet</p>
  </div>
</div>
```

### 7. Configurer la navigation

Dans `_config.yml`, la navigation est automatique avec Just the Docs.

Pour personnaliser l'ordre, ajouter dans le frontmatter:

```yaml
---
title: "Libft"
nav_order: 1
parent: "Projets"
---
```

### 8. Tester localement

```bash
# Démarrer le serveur Jekyll
bundle exec jekyll serve

# Ou avec live reload
bundle exec jekyll serve --livereload

# Accéder au site
# Ouvrir http://localhost:4000
```

### 9. Préparer le repository GitHub

```bash
# Initialiser Git
git init
git add .
git commit -m "Initial Jekyll setup"

# Créer le repository sur GitHub
# Puis :
git remote add origin https://github.com/NikoStano/nikostano.github.io.git
git branch -M main
git push -u origin main
```

### 10. Configurer GitHub Pages

1. Aller dans **Settings** > **Pages**
2. Source: **GitHub Actions**
3. Créer `.github/workflows/jekyll.yml` (voir artifact précédent)
4. Push le workflow:

```bash
mkdir -p .github/workflows
# Copier le contenu de jekyll.yml dans .github/workflows/jekyll.yml
git add .github/workflows/jekyll.yml
git commit -m "Add GitHub Actions workflow"
git push
```

### 11. Vérifier le déploiement

1. Aller dans l'onglet **Actions** de votre repository
2. Vérifier que le workflow s'exécute correctement
3. Une fois terminé, votre site sera accessible à `https://nikostano.github.io`

---

## 📝 Checklist de Migration

- [ ] Ruby et Jekyll installés
- [ ] Projet Jekyll créé
- [ ] `_config.yml` configuré
- [ ] CSS personnalisé copié
- [ ] Page d'accueil (`index.md`) créée
- [ ] Page "À propos" (`about.md`) créée
- [ ] Tous les projets convertis
- [ ] Tous les guides convertis
- [ ] Navigation testée localement
- [ ] Images et assets copiés
- [ ] Repository GitHub créé
- [ ] GitHub Actions configuré
- [ ] Déploiement vérifié
- [ ] Site accessible en ligne

---

## 🎨 Personnalisation

### Changer les couleurs

Éditer `_config.yml`:

```yaml
color_scheme: dark  # ou 'light'
```

Ou créer un thème personnalisé dans `_sass/color_schemes/custom.scss`

### Modifier le logo

Remplacer `assets/images/logo.png` par votre logo.

### Ajouter des pages

1. Créer un fichier `.md` à la racine ou dans un dossier
2. Ajouter le frontmatter:

```yaml
---
layout: default
title: "Ma Page"
nav_order: 5
---
```

### Modifier le footer

Dans `_config.yml`:

```yaml
footer_content: "Mon texte de footer personnalisé"
```

---

## 🐛 Dépannage

### Erreur: "Could not find gem 'just-the-docs'"

```bash
bundle update
bundle install
```

### Le site ne se build pas sur GitHub

1. Vérifier les logs dans Actions
2. Vérifier que `Gemfile.lock` est commité
3. Vérifier la version de Ruby dans le workflow

### Les styles ne s'appliquent pas

1. Vérifier que `custom.css` est dans `assets/css/`
2. Ajouter dans `_config.yml`:

```yaml
sass:
  style: compressed
```

### Les liens internes ne fonctionnent pas

Utiliser des liens relatifs:

```markdown
[Lien]({{ site.baseurl }}/projects/libft)
```

---

## 📚 Ressources

- [Documentation Jekyll](https://jekyllrb.com/docs/)
- [Documentation Just the Docs](https://just-the-docs.com/)
- [GitHub Pages](https://pages.github.com/)
- [Kramdown Syntax](https://kramdown.gettalong.org/syntax.html)

---

## 🎯 Prochaines étapes

Après la migration:

1. **SEO**: Ajouter un `sitemap.xml` et `robots.txt`
2. **Analytics**: Intégrer Google Analytics ou Plausible
3. **Recherche**: Activer la recherche Just the Docs
4. **Performance**: Optimiser les images
5. **Commentaires**: Ajouter Giscus ou Utterances
6. **PWA**: Transformer en Progressive Web App

---

## ✅ Validation finale

Avant de considérer la migration comme terminée:

- [ ] Toutes les pages s'affichent correctement
- [ ] Tous les liens fonctionnent
- [ ] Les images sont chargées
- [ ] La navigation est fonctionnelle
- [ ] Le site est responsive (mobile/desktop)
- [ ] Les blocs de code ont la coloration syntaxique
- [ ] Les composants (notes, tips, etc.) s'affichent bien
- [ ] Le site est accessible (test avec Lighthouse)
- [ ] Le SEO est correct (test avec Lighthouse)

---

## 📞 Support

Si vous rencontrez des problèmes:

1. Consulter la [documentation Jekyll](https://jekyllrb.com/docs/)
2. Chercher dans [Stack Overflow](https://stackoverflow.com/questions/tagged/jekyll)
3. Poser une question dans [Jekyll Talk](https://talk.jekyllrb.com/)

Bon courage avec la migration ! 🚀