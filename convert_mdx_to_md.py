#!/usr/bin/env python3
"""
Script pour convertir les fichiers MDX de Mintlify en Markdown Jekyll
Usage: python3 convert_mdx_to_md.py input.mdx output.md
"""

import re
import sys
import os

def convert_frontmatter(content):
    """Convertir le frontmatter Mintlify en Jekyll"""
    # Extraire le frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)

    if not frontmatter_match:
        return content

    frontmatter = frontmatter_match.group(1)
    rest_content = content[frontmatter_match.end():]

    # Ajouter les champs Jekyll nécessaires
    lines = frontmatter.split('\n')
    new_frontmatter = ['---', 'layout: default']

    for line in lines:
        if line.strip():
            new_frontmatter.append(line)

    new_frontmatter.append('---\n')

    return '\n'.join(new_frontmatter) + rest_content

def convert_note_components(content):
    """Convertir <Note> en bloc Jekyll"""
    # <Note>text</Note> -> {: .note } > text
    content = re.sub(
        r'<Note>(.*?)</Note>',
        r'{: .note }\n> \1',
        content,
        flags=re.DOTALL
    )
    return content

def convert_tip_components(content):
    """Convertir <Tip> en bloc Jekyll"""
    content = re.sub(
        r'<Tip>(.*?)</Tip>',
        r'{: .tip }\n> \1',
        content,
        flags=re.DOTALL
    )
    return content

def convert_warning_components(content):
    """Convertir <Warning> en bloc Jekyll"""
    content = re.sub(
        r'<Warning>(.*?)</Warning>',
        r'{: .warning }\n> \1',
        content,
        flags=re.DOTALL
    )
    return content

def convert_check_components(content):
    """Convertir <Check> en bloc Jekyll"""
    content = re.sub(
        r'<Check>(.*?)</Check>',
        r'{: .check }\n> \1',
        content,
        flags=re.DOTALL
    )
    return content

def convert_info_components(content):
    """Convertir <Info> en bloc Jekyll"""
    content = re.sub(
        r'<Info>(.*?)</Info>',
        r'{: .info }\n> \1',
        content,
        flags=re.DOTALL
    )
    return content

def convert_card_components(content):
    """Convertir <Card> en HTML Jekyll"""
    def replace_card(match):
        title = re.search(r'title="([^"]*)"', match.group(0))
        icon = re.search(r'icon="([^"]*)"', match.group(0))
        href = re.search(r'href="([^"]*)"', match.group(0))

        card_html = '<div class="project-card">\n'

        if title:
            card_html += f'  <h3>{title.group(1)}</h3>\n'

        # Contenu du card
        card_content = match.group(1).strip()
        if card_content:
            card_html += f'  <p>{card_content}</p>\n'

        if href:
            card_html += f'  <a href="{href.group(1)}" class="btn btn-primary">Voir plus</a>\n'

        card_html += '</div>'
        return card_html

    content = re.sub(
        r'<Card[^>]*>(.*?)</Card>',
        replace_card,
        content,
        flags=re.DOTALL
    )
    return content

def convert_cardgroup_components(content):
    """Convertir <CardGroup> en grille"""
    content = re.sub(
        r'<CardGroup[^>]*>',
        '<div class="card-container">',
        content
    )
    content = re.sub(
        r'</CardGroup>',
        '</div>',
        content
    )
    return content

def convert_steps_components(content):
    """Convertir <Steps> en liste numérotée"""
    # Remplacer <Steps>
    content = re.sub(
        r'<Steps>',
        '<div class="steps-container">',
        content
    )
    content = re.sub(
        r'</Steps>',
        '</div>',
        content
    )

    # Remplacer <Step title="...">
    def replace_step(match):
        title = re.search(r'title="([^"]*)"', match.group(0))
        step_content = match.group(1).strip()

        step_html = '<div class="step">\n'
        if title:
            step_html += f'  <h4>{title.group(1)}</h4>\n'
        step_html += f'  <p>{step_content}</p>\n'
        step_html += '</div>'
        return step_html

    content = re.sub(
        r'<Step[^>]*>(.*?)</Step>',
        replace_step,
        content,
        flags=re.DOTALL
    )

    return content

def convert_accordion_components(content):
    """Convertir <Accordion> en <details>"""
    def replace_accordion(match):
        title = re.search(r'title="([^"]*)"', match.group(0))
        accordion_content = match.group(1).strip()

        details_html = '<details>\n'
        if title:
            details_html += f'<summary>{title.group(1)}</summary>\n\n'
        details_html += accordion_content + '\n'
        details_html += '</details>'
        return details_html

    content = re.sub(
        r'<Accordion[^>]*>(.*?)</Accordion>',
        replace_accordion,
        content,
        flags=re.DOTALL
    )

    # AccordionGroup
    content = re.sub(r'<AccordionGroup>', '', content)
    content = re.sub(r'</AccordionGroup>', '', content)

    return content

def convert_tabs_components(content):
    """Convertir <Tabs> en tabs HTML/JS"""
    # Détection basique - à améliorer selon les besoins
    content = re.sub(
        r'<Tabs>',
        '<div class="tabs-container">\n<div class="tab-buttons">',
        content
    )
    content = re.sub(
        r'</Tabs>',
        '</div>\n</div>',
        content
    )

    # Tab individual
    def replace_tab(match):
        title = re.search(r'title="([^"]*)"', match.group(0))
        tab_content = match.group(1).strip()

        if title:
            tab_id = title.group(1).lower().replace(' ', '-')
            return f'<div id="{tab_id}" class="tab-content">\n{tab_content}\n</div>'
        return f'<div class="tab-content">\n{tab_content}\n</div>'

    content = re.sub(
        r'<Tab[^>]*>(.*?)</Tab>',
        replace_tab,
        content,
        flags=re.DOTALL
    )

    return content

def convert_codegroup_components(content):
    """Convertir <CodeGroup> en tabs pour code"""
    content = re.sub(r'<CodeGroup>', '<div class="code-tabs">', content)
    content = re.sub(r'</CodeGroup>', '</div>', content)
    return content

def convert_images(content):
    """Ajouter des classes aux images"""
    # Ajouter {: .centered-image } après les images si nécessaire
    content = re.sub(
        r'!\[(.*?)\]\((.*?)\)',
        r'![\1](\2){: .responsive-image }',
        content
    )
    return content

def clean_remaining_tags(content):
    """Nettoyer les balises restantes"""
    # Supprimer les imports MDX
    content = re.sub(r"import .* from .*;\n", "", content)

    # Frame -> figure
    content = re.sub(r'<Frame[^>]*>', '<figure>', content)
    content = re.sub(r'</Frame>', '</figure>', content)

    return content

def convert_file(input_file, output_file):
    """Convertir un fichier MDX en MD Jekyll"""
    print(f"Conversion de {input_file} vers {output_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Appliquer toutes les conversions
    content = convert_frontmatter(content)
    content = convert_note_components(content)
    content = convert_tip_components(content)
    content = convert_warning_components(content)
    content = convert_check_components(content)
    content = convert_info_components(content)
    content = convert_cardgroup_components(content)
    content = convert_card_components(content)
    content = convert_steps_components(content)
    content = convert_accordion_components(content)
    content = convert_tabs_components(content)
    content = convert_codegroup_components(content)
    content = convert_images(content)
    content = clean_remaining_tags(content)

    # Écrire le fichier de sortie
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Conversion terminée : {output_file}")

def convert_directory(input_dir, output_dir):
    """Convertir tous les fichiers .mdx d'un dossier"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.mdx'):
                input_path = os.path.join(root, file)

                # Créer le chemin de sortie
                rel_path = os.path.relpath(root, input_dir)
                output_path = os.path.join(output_dir, rel_path)

                if not os.path.exists(output_path):
                    os.makedirs(output_path)

                output_file = os.path.join(output_path, file.replace('.mdx', '.md'))
                convert_file(input_path, output_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 convert_mdx_to_md.py input.mdx output.md")
        print("  python3 convert_mdx_to_md.py input_dir/ output_dir/")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    if os.path.isdir(input_path):
        output_path = output_path or input_path + "_converted"
        convert_directory(input_path, output_path)
    else:
        output_path = output_path or input_path.replace('.mdx', '.md')
        convert_file(input_path, output_path)

    print("\n✨ Toutes les conversions sont terminées !")