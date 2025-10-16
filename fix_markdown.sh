#!/usr/bin/env python3
"""
Script pour corriger automatiquement les fichiers markdown
après conversion de Mintlify vers Jekyll

Usage: python3 fix_markdown.py [file.md ou dossier/]
"""

import re
import sys
import os
from pathlib import Path


def fix_accordion_tags(content):
    """Supprimer les balises <Accordion> et <AccordionGroup>"""
    # Supprimer <AccordionGroup>
    content = re.sub(r'<AccordionGroup>\s*', '', content)
    content = re.sub(r'\s*</AccordionGroup>', '', content)

    # Remplacer <Accordion title="..."> par rien (garder juste details)
    content = re.sub(r'<Accordion[^>]*>\s*', '', content)
    content = re.sub(r'\s*</Accordion>', '', content)

    return content


def fix_tabs_structure(content):
    """Corriger la structure des tabs"""
    # Trouver tous les blocs de tabs
    tabs_pattern = r'<div class="tabs-container">(.*?)</div>\s*</div>'

    def replace_tabs(match):
        tabs_content = match.group(1)

        # Extraire les tabs individuels
        tab_contents = re.findall(
            r'<div id="([^"]*)" class="tab-content">(.*?)</div>',
            tabs_content,
            re.DOTALL
        )

        if not tab_contents:
            return match.group(0)

        # Reconstruire proprement
        result = '<div class="tabs-container">\n  <div class="tab-buttons"></div>\n'

        for tab_id, tab_content in tab_contents:
            # Nettoyer le contenu
            tab_content = tab_content.strip()

            result += f'  <div id="{tab_id}" class="tab-content">\n'
            result += f'{tab_content}\n'
            result += '  </div>\n'

        result += '</div>'
        return result

    content = re.sub(tabs_pattern, replace_tabs, content, flags=re.DOTALL)

    return content


def fix_image_badges(content):
    """Convertir les balises <img> en syntaxe markdown pour les badges"""
    pattern = r'<img src="([^"]*)" alt="([^"]*)"[^>]*/?>'

    def replace_img(match):
        src = match.group(1)
        alt = match.group(2)
        return f'![{alt}]({src})'

    content = re.sub(pattern, replace_img, content)
    return content


def fix_code_blocks(content):
    """Corriger les blocs de code mal formatés"""
    # Corriger les blocs de code dans les listes
    content = re.sub(
        r'(\s+)<p>```(\w+)\s*(.*?)\s*```</p>',
        r'\1```\2\n\3\n```',
        content,
        flags=re.DOTALL
    )

    # Corriger les blocs de code isolés mal formatés
    content = re.sub(
        r'<p>```(\w+)\s*(.*?)\s*```</p>',
        r'```\1\n\2\n```',
        content,
        flags=re.DOTALL
    )

    return content


def clean_extra_whitespace(content):
    """Nettoyer les espaces en trop"""
    # Supprimer les lignes vides multiples
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Supprimer les espaces en fin de ligne
    content = re.sub(r' +\n', '\n', content)

    return content


def fix_details_summary(content):
    """S'assurer que les details/summary sont bien formatés"""
    # S'assurer qu'il y a une ligne vide après </summary>
    content = re.sub(
        r'</summary>\s*\n\s*(?![\n<])',
        '</summary>\n\n',
        content
    )

    return content


def add_nav_order_if_missing(content, filename):
    """Ajouter nav_order si manquant dans le frontmatter"""
    # Vérifier si c'est un fichier de projet
    if 'projects/' not in filename:
        return content

    # Ordre par défaut selon le nom du fichier
    nav_orders = {
        'libft': 1,
        'get-next-line': 2,
        'ft-printf': 3,
        'born2beroot': 4,
        'fdf': 5,
        'push-swap': 6,
        'minitalk': 7,
    }

    # Extraire le nom du fichier
    file_base = Path(filename).stem

    # Vérifier si nav_order existe déjà
    if 'nav_order:' in content:
        return content

    # Ajouter nav_order si connu
    if file_base in nav_orders:
        # Insérer après le frontmatter title
        content = re.sub(
            r'(title: "[^"]*"\n)',
            r'\1nav_order: ' + str(nav_orders[file_base]) + '\n',
            content,
            count=1
        )

    return content


def process_file(filepath):
    """Traiter un fichier markdown"""
    print(f"📄 Traitement de {filepath}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Appliquer toutes les corrections
        content = fix_accordion_tags(content)
        content = fix_tabs_structure(content)
        content = fix_image_badges(content)
        content = fix_code_blocks(content)
        content = fix_details_summary(content)
        content = add_nav_order_if_missing(content, filepath)
        content = clean_extra_whitespace(content)

        # Sauvegarder uniquement si modifié
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filepath} corrigé")
            return True
        else:
            print(f"ℹ️  {filepath} inchangé")
            return False

    except Exception as e:
        print(f"❌ Erreur avec {filepath}: {e}")
        return False


def process_directory(directory):
    """Traiter tous les fichiers .md d'un dossier"""
    path = Path(directory)
    markdown_files = list(path.glob('**/*.md'))

    if not markdown_files:
        print(f"Aucun fichier .md trouvé dans {directory}")
        return

    print(f"\n🔍 {len(markdown_files)} fichiers trouvés\n")

    modified_count = 0
    for md_file in markdown_files:
        if process_file(str(md_file)):
            modified_count += 1

    print(f"\n✨ Terminé ! {modified_count} fichier(s) modifié(s)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fix_markdown.py [file.md ou dossier/]")
        print("\nExemples:")
        print("  python3 fix_markdown.py projects/libft.md")
        print("  python3 fix_markdown.py projects/")
        print("  python3 fix_markdown.py .")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        process_file(target)
    elif os.path.isdir(target):
        process_directory(target)
    else:
        print(f"❌ {target} n'existe pas")
        sys.exit(1)


if __name__ == "__main__":
    main()