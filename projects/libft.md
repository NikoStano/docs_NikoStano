---
layout: default
title: "Libft"
nav_order: 1
description: "Ma bibliothèque C personnelle - Premier projet 42"
icon: "book"
---

# 🔷 Libft - Bibliothèque C personnelle

![Score](https://img.shields.io/badge/Score-120%2F100-success)
![Language](https://img.shields.io/badge/Language-C-blue)

## Introduction

**Libft** est le premier projet du cursus 42 Paris. Il consiste à recréer une bibliothèque de fonctions C essentielles qui seront utilisées dans tous les projets futurs. Ce projet permet de comprendre en profondeur le fonctionnement des fonctions standard de la libc.

<div class="project-card">
  <h3>Voir sur GitHub</h3>
  <p>Accéder au repository GitHub</p>
  <a href="https://github.com/NikoStano/libft" class="btn btn-primary">Voir plus</a>
</div>

## Objectifs pédagogiques

<div class="steps-container">
  <div class="step">
  <h4>Maîtriser le C</h4>
  <p>Comprendre les bases du langage C : pointeurs, allocation mémoire, types de données</p>
</div>

  <div class="step">
  <h4>Reproduire la libc</h4>
  <p>Recréer les fonctions standard pour comprendre leur implémentation interne</p>
</div>

  <div class="step">
  <h4>Créer une bibliothèque</h4>
  <p>Organiser son code de manière modulaire et créer une bibliothèque statique</p>
</div>

  <div class="step">
  <h4>Bases solides</h4>
  <p>Constituer une base réutilisable pour tous les projets futurs</p>
</div>
</div>

## Fonctions implémentées

### Partie 1 : Fonctions de la libc

<details>
<summary>Manipulation de chaînes</summary>

- `ft_strlen` - Calcule la longueur d'une chaîne
  - `ft_strchr` - Recherche un caractère dans une chaîne
  - `ft_strrchr` - Recherche la dernière occurrence d'un caractère
  - `ft_strncmp` - Compare deux chaînes sur n caractères
  - `ft_strnstr` - Recherche une sous-chaîne dans une chaîne
  - `ft_strlcpy` - Copie une chaîne de manière sécurisée
  - `ft_strlcat` - Concatène deux chaînes de manière sécurisée
</details>

<details>
<summary>Manipulation de mémoire</summary>

- `ft_memset` - Remplit une zone mémoire avec un octet
  - `ft_bzero` - Met à zéro une zone mémoire
  - `ft_memcpy` - Copie une zone mémoire
  - `ft_memmove` - Copie une zone mémoire (gère le chevauchement)
  - `ft_memchr` - Recherche un octet dans une zone mémoire
  - `ft_memcmp` - Compare deux zones mémoire
  - `ft_calloc` - Alloue et initialise une zone mémoire
</details>

<details>
<summary>Tests et conversions</summary>

- `ft_isalpha` - Teste si un caractère est alphabétique
  - `ft_isdigit` - Teste si un caractère est un chiffre
  - `ft_isalnum` - Teste si un caractère est alphanumérique
  - `ft_isascii` - Teste si un caractère est ASCII
  - `ft_isprint` - Teste si un caractère est imprimable
  - `ft_toupper` - Convertit en majuscule
  - `ft_tolower` - Convertit en minuscule
  - `ft_atoi` - Convertit une chaîne en entier
</details>

### Partie 2 : Fonctions supplémentaires

<details>
<summary>Manipulation de chaînes avancée</summary>

- `ft_substr` - Extrait une sous-chaîne
  - `ft_strjoin` - Concatène deux chaînes (allocation)
  - `ft_strtrim` - Supprime des caractères aux extrémités
  - `ft_split` - Découpe une chaîne selon un délimiteur
  - `ft_itoa` - Convertit un entier en chaîne
  - `ft_strmapi` - Applique une fonction à chaque caractère
  - `ft_striteri` - Itère sur une chaîne avec une fonction
</details>

<details>
<summary>Fonctions d'écriture</summary>

- `ft_putchar_fd` - Écrit un caractère sur un fd
  - `ft_putstr_fd` - Écrit une chaîne sur un fd
  - `ft_putendl_fd` - Écrit une chaîne + retour ligne sur un fd
  - `ft_putnbr_fd` - Écrit un nombre sur un fd
</details>

### Bonus : Listes chaînées

{: .warning }
>
Les fonctions bonus permettent de manipuler des listes chaînées, une structure de données fondamentale en programmation.

- `ft_lstnew` - Crée un nouvel élément
- `ft_lstadd_front` - Ajoute un élément au début
- `ft_lstsize` - Compte le nombre d'éléments
- `ft_lstlast` - Retourne le dernier élément
- `ft_lstadd_back` - Ajoute un élément à la fin
- `ft_lstdelone` - Supprime un élément
- `ft_lstclear` - Supprime et libère toute la liste
- `ft_lstiter` - Applique une fonction à chaque élément
- `ft_lstmap` - Crée une nouvelle liste en appliquant une fonction

## Installation et compilation

<div class="tabs-container">
  <div class="tab-buttons"></div>
  <div id="clone" class="tab-content">

  ```bash
  git clone https://github.com/NikoStano/libft.git
  cd libft
  ```
  </div>
  <div id="compilation" class="tab-content">

  ```bash
  # Compilation standard
  make

  # Avec les bonus
  make bonus

  # Nettoyage
  make clean  # Supprime les .o
  make fclean # Supprime tout
  make re     # Recompile tout
  ```
  </div>
</div>
</div>

## Exemples d'utilisation

### Manipulation de chaînes

```c
#include "libft.h"

int main(void)
{
    char *str1 = "Hello";
    char *str2 = " World!";
    char *result;

    // Concaténation
    result = ft_strjoin(str1, str2);
    ft_putendl_fd(result, 1); // Affiche: Hello World!
    free(result);

    // Split
    char **words = ft_split("Bonjour les amis", ' ');
    int i = 0;
    while (words[i])
    {
        ft_putendl_fd(words[i], 1);
        free(words[i]);
        i++;
    }
    free(words);

    return (0);
}
```

### Listes chaînées

```c
#include "libft.h"

int main(void)
{
    t_list *list = NULL;

    // Ajout d'éléments
    ft_lstadd_back(&list, ft_lstnew("Premier"));
    ft_lstadd_back(&list, ft_lstnew("Deuxième"));
    ft_lstadd_back(&list, ft_lstnew("Troisième"));

    // Parcours
    t_list *current = list;
    while (current)
    {
        ft_putendl_fd((char *)current->content, 1);
        current = current->next;
    }

    // Libération
    ft_lstclear(&list, free);

    return (0);
}
```

## Points techniques importants

<details>
<summary>**Gestion de la mémoire**</summary>

  - Toujours vérifier les retours de `malloc`
  - Libérer toute mémoire allouée
  - Utiliser Valgrind pour détecter les fuites
  ```bash
    valgrind --leak-check=full ./program
  ```
</details>

  <details>
<summary>Protection contre les NULL</summary>

Toutes les fonctions doivent gérer les pointeurs NULL

  ```c
    char *ft_strdup(const char *s)
    {
        if (!s)
            return (NULL);
        // ... reste du code
    }
  ```
</details>

  <details>
<summary>Norme 42</summary>

  - Maximum 25 lignes par fonction
  - Maximum 5 fonctions par fichier
  - Respect strict de la Norminette

  ```bash
    norminette *.c *.h
  ```
</details>

## Conseils et astuces

{: .tip }
>
**Testez chaque fonction individuellement** avant de passer à la suivante. Créez vos propres tests ou utilisez des testeurs communautaires.

{: .tip }
>
**Documentez votre code** avec des commentaires clairs. Cela vous aidera pour vos projets futurs.

{: .warning }
>
**Attention aux fuites mémoire** : utilisez systématiquement Valgrind pour vérifier votre code.

## Ressources utiles

<div class="card-container">
  <div class="project-card">
  <h3>man pages</h3>
  <p>Consultez les pages man des fonctions originales
  ```bash
    man strlen
    man malloc
  ```</p>
</div>

  <div class="project-card">
  <h3>cplusplus.com</h3>
  <p>Documentation complète des fonctions C</p>
  <a href="https://cplusplus.com/reference/cstring/" class="btn btn-primary">Voir plus</a>
</div>

  <div class="project-card">
  <h3>Valgrind</h3>
  <p>Outil indispensable pour détecter les fuites mémoire</p>
</div>

  <div class="project-card">
  <h3>GDB</h3>
  <p>Debugger pour tracer l'exécution du programme</p>
</div>
</div>

## Conclusion

Libft est bien plus qu'un simple projet : c'est votre **boîte à outils personnelle** que vous utiliserez tout au long de votre parcours à 42. Prenez le temps de bien le construire !

{: .check }
>
Une fois validé, ce projet vous servira de base pour tous vos futurs projets C à 42.
