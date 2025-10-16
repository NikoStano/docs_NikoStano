---
layout: default
title: "Get Next Line"
description: "Fonction de lecture ligne par ligne d'un fichier"
icon: "file-lines"
---

# 📄 Get Next Line

<img src="https://img.shields.io/badge/Score-125%2F100-success" alt="Score" />
<img src="https://img.shields.io/badge/Language-C-blue" alt="Language" />
<img src="https://img.shields.io/badge/Difficulty-Medium-orange" alt="Difficulty" />

## Introduction

**Get Next Line** (GNL) est un projet qui consiste à créer une fonction capable de lire un fichier ligne par ligne, quelle que soit la taille du buffer. Ce projet introduit les concepts de variables statiques et de gestion optimisée de la mémoire.

{: .note }
> 
Ce projet est essentiel pour comprendre la lecture de fichiers en C et sera réutilisé dans de nombreux projets futurs, notamment dans les parseurs.


## Prototype de la fonction

```c
char *get_next_line(int fd);
```

### Paramètres

- **fd** : File descriptor du fichier à lire

### Retour

- La ligne lue (incluant le `\n` si présent)
- `NULL` si fin de fichier ou erreur

## Fonctionnement

<div class="steps-container">
  <div class="step">
  <h4>Lecture par buffer</h4>
  <p>Lit le fichier par morceaux de taille BUFFER_SIZE</p>
</div>
  
  <div class="step">
  <h4>Stockage en variable statique</h4>
  <p>Conserve les données lues entre les appels de fonction</p>
</div>
  
  <div class="step">
  <h4>Extraction de ligne</h4>
  <p>Extrait une ligne complète (jusqu'au `\n`) du buffer</p>
</div>
  
  <div class="step">
  <h4>Gestion du reste</h4>
  <p>Conserve les données restantes pour le prochain appel</p>
</div>
</div>

## Compilation avec BUFFER_SIZE

Le BUFFER_SIZE est défini à la compilation et détermine le nombre d'octets lus à chaque appel à `read()`.

<div class="tabs-container">
<div class="tab-buttons">
  <div id="petit-buffer" class="tab-content">
```bash
    # Buffer de 1 octet (test extrême)
    gcc -Wall -Wextra -Werror -D BUFFER_SIZE=1 \
        get_next_line.c get_next_line_utils.c
    ```
</div>
  
  <div id="buffer-standard" class="tab-content">
```bash
    # Buffer de 42 octets
    gcc -Wall -Wextra -Werror -D BUFFER_SIZE=42 \
        get_next_line.c get_next_line_utils.c
    ```
</div>
  
  <div id="grand-buffer" class="tab-content">
```bash
    # Buffer de 4096 octets (1 page)
    gcc -Wall -Wextra -Werror -D BUFFER_SIZE=4096 \
        get_next_line.c get_next_line_utils.c
    ```
</div>
</div>
</div>

## Exemple d'utilisation

### Lecture d'un fichier simple

```c
#include "get_next_line.h"
#include 
#include 

int main(void)
{
    int fd;
    char *line;
    
    fd = open("test.txt", O_RDONLY);
    if (fd < 0)
        return (1);
    
    // Lecture ligne par ligne
    while ((line = get_next_line(fd)) != NULL)
    {
        printf("%s", line);
        free(line);
    }
    
    close(fd);
    return (0);
}
```

### Lecture de plusieurs fichiers simultanément (Bonus)

```c
#include "get_next_line_bonus.h"
#include 
#include 

int main(void)
{
    int fd1, fd2, fd3;
    char *line;
    
    fd1 = open("file1.txt", O_RDONLY);
    fd2 = open("file2.txt", O_RDONLY);
    fd3 = open("file3.txt", O_RDONLY);
    
    // Lit alternativement dans les 3 fichiers
    line = get_next_line(fd1);
    printf("File1: %s", line);
    free(line);
    
    line = get_next_line(fd2);
    printf("File2: %s", line);
    free(line);
    
    line = get_next_line(fd3);
    printf("File3: %s", line);
    free(line);
    
    // Continue avec fd1...
    line = get_next_line(fd1);
    printf("File1: %s", line);
    free(line);
    
    close(fd1);
    close(fd2);
    close(fd3);
    return (0);
}
```

### Lecture depuis stdin

```c
#include "get_next_line.h"
#include 

int main(void)
{
    char *line;
    
    printf("Entrez du texte (Ctrl+D pour terminer):\n");
    
    // Lecture depuis l'entrée standard (fd = 0)
    while ((line = get_next_line(0)) != NULL)
    {
        printf("Vous avez écrit: %s", line);
        free(line);
    }
    
    return (0);
}
```

## Concepts clés

### Variables statiques

<details>
<summary>Qu'est-ce qu'une variable statique ?</summary>

Une variable statique conserve sa valeur entre les appels de fonction.
  
  ```c
  char *get_next_line(int fd)
  {
      static char *saved;  // Conservée entre les appels
      
      if (!saved)
          saved = malloc(BUFFER_SIZE + 1);
      // ...
  }
  ```
  
  {: .warning }
> 
  La variable statique doit être libérée avant de retourner NULL à la fin du fichier !
</details>

### Gestion de la mémoire

<details>
<summary>Allocation dynamique</summary>

<Accordion title="Allocation dynamique">
    ```c
    // Allouer un buffer de lecture
    char *buffer = malloc(sizeof(char) * (BUFFER_SIZE + 1));
    if (!buffer)
        return (NULL);
    
    // Toujours initialiser
    buffer[BUFFER_SIZE] = '\0';
    ```
</details>
  
  <details>
<summary>Libération mémoire</summary>

```c
    // Libérer et mettre à NULL
    free(buffer);
    buffer = NULL;
    
    // Pour la variable statique en fin de fichier
    if (saved)
    {
        free(saved);
        saved = NULL;
    }
    return (NULL);
    ```
</details>
  
  <details>
<summary>Réallocation</summary>

```c
    // Agrandir le buffer si nécessaire
    char *new_buffer = ft_strjoin(saved, buffer);
    free(saved);
    saved = new_buffer;
    ```
</details>


### File Descriptors

<details>
<summary>Comprendre les file descriptors</summary>

- **0** : stdin (entrée standard)
  - **1** : stdout (sortie standard)  
  - **2** : stderr (sortie d'erreur)
  - **3+** : fichiers ouverts par le programme
  
  ```c
  // Ouvrir un fichier
  int fd = open("file.txt", O_RDONLY);
  
  // Vérifier l'ouverture
  if (fd < 0)
      return (error);
  
  // Lire avec get_next_line
  char *line = get_next_line(fd);
  
  // Toujours fermer !
  close(fd);
  ```
</details>

## Partie Bonus

{: .warning }
> 
Le bonus consiste à gérer plusieurs file descriptors simultanément avec une seule variable statique de type tableau.


### Gestion multi-fd

```c
#define MAX_FD 1024

char *get_next_line(int fd)
{
    static char *saved[MAX_FD];  // Un slot par fd possible
    
    if (fd < 0 || fd >= MAX_FD)
        return (NULL);
    
    // Utilise saved[fd] pour ce fichier spécifique
    // ...
}
```

### Exemple bonus

```c
// Ouvrir 3 fichiers
int fd1 = open("file1.txt", O_RDONLY);
int fd2 = open("file2.txt", O_RDONLY);
int fd3 = open("file3.txt", O_RDONLY);

// Lire dans n'importe quel ordre
get_next_line(fd1);  // Ligne 1 de file1
get_next_line(fd3);  // Ligne 1 de file3
get_next_line(fd1);  // Ligne 2 de file1
get_next_line(fd2);  // Ligne 1 de file2
get_next_line(fd3);  // Ligne 2 de file3
```

## Cas limites à gérer

<details>
<summary>Fichier vide</summary>

<Accordion title="Fichier vide">
    ```c
    // Doit retourner NULL immédiatement
    int fd = open("empty.txt", O_RDONLY);
    char *line = get_next_line(fd);  // NULL
    ```
</details>
  
  <details>
<summary>Ligne sans \n à la fin</summary>

```c
    // Dernière ligne sans retour à la ligne
    // Doit quand même retourner la ligne
    "Dernière ligne sans \\n"  // Doit être retourné
    ```
</details>
  
  <details>
<summary>Fichier avec uniquement \n</summary>

```c
    // Fichier contenant : "\n\n\n"
    line1 = get_next_line(fd);  // "\n"
    line2 = get_next_line(fd);  // "\n"
    line3 = get_next_line(fd);  // "\n"
    line4 = get_next_line(fd);  // NULL
    ```
</details>
  
  <details>
<summary>Buffer size = 1</summary>

```c
    // Doit fonctionner même avec un buffer d'1 octet
    gcc -D BUFFER_SIZE=1 ...
    ```
</details>
  
  <details>
<summary>Très grande ligne</summary>

```c
    // Ligne de 10000 caractères
    // Doit être gérée correctement
    ```
</details>


## Algorithme général

```c
1. Si fd invalide ou erreur → retourner NULL

2. Lire BUFFER_SIZE octets du fichier
   - Si erreur de lecture → libérer et retourner NULL
   - Si fin de fichier (0 octets lus) → traiter le reste et retourner NULL

3. Ajouter les octets lus au buffer statique

4. Chercher '\n' dans le buffer statique
   - Si trouvé :
     • Extraire la ligne (jusqu'au '\n' inclus)
     • Garder le reste dans le buffer statique
     • Retourner la ligne
   
   - Si non trouvé :
     • Retourner à l'étape 2 (lire plus de données)

5. À la fin du fichier :
   - Si buffer statique non vide → retourner ce qu'il reste
   - Sinon → retourner NULL
```

## Structure recommandée

```
get_next_line/
├── get_next_line.c        # Fonction principale
├── get_next_line_utils.c  # Fonctions utilitaires
├── get_next_line.h        # Header
├── get_next_line_bonus.c  # Version bonus (multi-fd)
├── get_next_line_bonus.h  # Header bonus
└── test/
    ├── main.c             # Tests
    └── files/             # Fichiers de test
```

## Fonctions utilitaires

<div class="tabs-container">
<div class="tab-buttons">
  <div id="strlen" class="tab-content">
```c
    size_t  ft_strlen(const char *s)
    {
        size_t i = 0;
        while (s[i])
            i++;
        return (i);
    }
    ```
</div>
  
  <div id="strchr" class="tab-content">
```c
    char    *ft_strchr(const char *s, int c)
    {
        while (*s)
        {
            if (*s == (char)c)
                return ((char *)s);
            s++;
        }
        if (c == '\0')
            return ((char *)s);
        return (NULL);
    }
    ```
</div>
  
  <div id="strjoin" class="tab-content">
```c
    char    *ft_strjoin(char const *s1, char const *s2)
    {
        char    *result;
        size_t  i, j;
        
        if (!s1 || !s2)
            return (NULL);
        result = malloc(ft_strlen(s1) + ft_strlen(s2) + 1);
        if (!result)
            return (NULL);
        i = 0;
        while (s1[i])
        {
            result[i] = s1[i];
            i++;
        }
        j = 0;
        while (s2[j])
            result[i++] = s2[j++];
        result[i] = '\0';
        return (result);
    }
    ```
</div>
</div>
</div>

## Tests recommandés

<div class="code-tabs">
```bash Testeur Tripouille
git clone https://github.com/Tripouille/gnlTester.git
cd gnlTester
make m  # Tests mandatory
make b  # Tests bonus
```

```bash Tests manuels
# Créer des fichiers de test
echo -e "Line 1\nLine 2\nLine 3" > test.txt
echo -n "No newline at end" > test2.txt
echo -e "\n\n\n" > test3.txt

# Compiler et tester
gcc -Wall -Wextra -Werror -D BUFFER_SIZE=42 \
    get_next_line.c get_next_line_utils.c main.c
./a.out
```

```bash Valgrind
# Vérifier les fuites mémoire
valgrind --leak-check=full --show-leak-kinds=all ./a.out
```
</div>

## Pièges à éviter

{: .warning }
> 
**Fuite mémoire sur la variable statique** : Pensez à libérer saved avant de retourner NULL en fin de fichier.


{: .warning }
> 
**Oubli du \\0** : Toujours terminer vos chaînes avec un caractère nul.


{: .warning }
> 
**Mauvaise gestion du reste** : Le reste après un \\n doit être conservé pour le prochain appel.


{: .warning }
> 
**Buffer non initialisé** : Toujours initialiser vos buffers avant utilisation.


## Conseils

{: .tip }
> 
**Testez avec différents BUFFER_SIZE** : 1, 42, 1024, 10000000. Votre fonction doit fonctionner dans tous les cas.


{: .tip }
> 
**Dessinez le flux de données** : Faites des schémas pour visualiser comment les données circulent entre les appels.


{: .tip }
> 
**Utilisez des testeurs** : Les testeurs de la communauté couvrent de nombreux cas limites.


## Ressources

<div class="card-container">
  <div class="project-card">
  <h3>man read</h3>
  <p>```bash
    man 2 read
    ```
    Documentation de la fonction read()</p>
</div>
  
  <div class="project-card">
  <h3>man open</h3>
  <p>```bash
    man 2 open
    ```
    Documentation de la fonction open()</p>
</div>
  
  <div class="project-card">
  <h3>Static variables</h3>
  <p>Comprendre les variables statiques en C</p>
  <a href="https://www.geeksforgeeks.org/static-variables-in-c/" class="btn btn-primary">Voir plus</a>
</div>
  
  <div class="project-card">
  <h3>File I/O</h3>
  <p>Guide complet sur les I/O en C</p>
  <a href="https://www.gnu.org/software/libc/manual/html_node/Low_002dLevel-I_002fO.html" class="btn btn-primary">Voir plus</a>
</div>
</div>

## Conclusion

Get Next Line est un projet fondamental qui vous apprendra :
- La gestion de la mémoire dynamique
- Les variables statiques
- La manipulation de fichiers
- L'optimisation des lectures

{: .check }
> 
Cette fonction sera réutilisée dans presque tous vos projets futurs nécessitant la lecture de fichiers !
