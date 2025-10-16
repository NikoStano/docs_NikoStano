---
layout: default
title: "ft_printf"
description: "Reproduction de la fonction printf"
icon: "print"
---

# 🖨️ ft_printf

<img src="https://img.shields.io/badge/Score-100%2F100-success" alt="Score" />
<img src="https://img.shields.io/badge/Language-C-blue" alt="Language" />
<img src="https://img.shields.io/badge/Difficulty-Medium-orange" alt="Difficulty" />

## Introduction

**ft_printf** est un projet qui consiste à recréer la célèbre fonction `printf` de la bibliothèque standard C. Ce projet permet de comprendre le fonctionnement des fonctions variadiques et du parsing de format.

{: .note }
> 
Ce projet améliore considérablement votre compréhension du formatage de sortie et sera très utile pour vos futurs projets de debugging.


## Prototype

```c
int ft_printf(const char *format, ...);
```

### Paramètres

- **format** : Chaîne de format contenant du texte et des spécificateurs de conversion
- **...** : Nombre variable d'arguments à formater

### Retour

Le nombre de caractères affichés (comme printf original)

## Conversions à implémenter

<details>
<summary>%c - Caractère</summary>

<Accordion title="%c - Caractère">
    Affiche un seul caractère
    
    ```c
    ft_printf("Lettre: %c\n", 'A');
    // Output: Lettre: A
    ```
</details>
  
  <details>
<summary>%s - Chaîne de caractères</summary>

Affiche une chaîne de caractères
    
    ```c
    ft_printf("Message: %s\n", "Hello 42!");
    // Output: Message: Hello 42!
    
    ft_printf("NULL: %s\n", NULL);
    // Output: NULL: (null)
    ```
</details>
  
  <details>
<summary>%p - Pointeur</summary>

Affiche une adresse mémoire en hexadécimal
    
    ```c
    int x = 42;
    ft_printf("Adresse: %p\n", &x);
    // Output: Adresse: 0x7ffd5e8a2b4c
    ```
</details>
  
  <details>
<summary>%d et %i - Entier décimal</summary>

Affiche un nombre entier en base 10
    
    ```c
    ft_printf("Nombre: %d\n", 42);
    // Output: Nombre: 42
    
    ft_printf("Négatif: %i\n", -42);
    // Output: Négatif: -42
    ```
</details>
  
  <details>
<summary>%u - Entier non signé</summary>

Affiche un nombre entier non signé
    
    ```c
    ft_printf("Unsigned: %u\n", 4294967295);
    // Output: Unsigned: 4294967295
    ```
</details>
  
  <details>
<summary>%x et %X - Hexadécimal</summary>

Affiche un nombre en hexadécimal (minuscule ou majuscule)
    
    ```c
    ft_printf("Hex min: %x\n", 255);
    // Output: Hex min: ff
    
    ft_printf("Hex maj: %X\n", 255);
    // Output: Hex maj: FF
    ```
</details>
  
  <details>
<summary>%% - Pourcentage</summary>

Affiche le caractère %
    
    ```c
    ft_printf("Pourcentage: %%\n");
    // Output: Pourcentage: %
    ```
</details>


## Exemples d'utilisation

### Exemples basiques

```c
#include "ft_printf.h"

int main(void)
{
    int count;
    
    // Caractère
    count = ft_printf("Char: %c\n", 'A');
    ft_printf("Printed: %d chars\n\n", count);
    
    // String
    count = ft_printf("String: %s\n", "Hello 42");
    ft_printf("Printed: %d chars\n\n", count);
    
    // Numbers
    ft_printf("Decimal: %d\n", 42);
    ft_printf("Integer: %i\n", -42);
    ft_printf("Unsigned: %u\n", 4294967295);
    
    // Hexadecimal
    ft_printf("Hex lower: %x\n", 255);
    ft_printf("Hex upper: %X\n", 255);
    
    // Pointer
    int x = 42;
    ft_printf("Pointer: %p\n", &x);
    
    // Percent
    ft_printf("Percent: %%\n");
    
    return (0);
}
```

### Cas complexes

```c
#include "ft_printf.h"

int main(void)
{
    // Multiple conversions
    ft_printf("Name: %s, Age: %d, Grade: %c\n", 
              "Alice", 25, 'A');
    
    // NULL string
    ft_printf("NULL: %s\n", NULL);
    // Output: NULL: (null)
    
    // Negative numbers
    ft_printf("Negative: %d\n", -2147483648);
    
    // Zero
    ft_printf("Zero: %d, %x, %p\n", 0, 0, NULL);
    
    // Mix everything
    int num = 42;
    ft_printf("Mix: char=%c, str=%s, dec=%d, hex=%x, ptr=%p\n",
              'X', "test", num, num, &num);
    
    return (0);
}
```

### Retour de fonction

```c
#include "ft_printf.h"

int main(void)
{
    int len;
    
    len = ft_printf("Hello");
    ft_printf("\nLength: %d\n", len);  // 5
    
    len = ft_printf("%d + %d = %d", 2, 3, 5);
    ft_printf("\nLength: %d\n", len);  // 9
    
    len = ft_printf("");
    ft_printf("Empty length: %d\n", len);  // 0
    
    return (0);
}
```

## Fonctions variadiques

<details>
<summary>Comment fonctionnent les fonctions variadiques ?</summary>

Les fonctions variadiques utilisent les macros `va_start`, `va_arg` et `va_end` du header `<stdarg.h>`.
  
  ```c
  #include <stdarg.h>
  
  int ft_printf(const char *format, ...)
  {
      va_list args;
      int count;
      
      // Initialiser la liste d'arguments
      va_start(args, format);
      
      // Traiter la chaîne de format
      count = parse_format(format, args);
      
      // Nettoyer
      va_end(args);
      
      return (count);
  }
  ```
  
  ### Récupérer les arguments
  
  ```c
  // Récupérer un int
  int num = va_arg(args, int);
  
  // Récupérer un char (promu en int)
  char c = (char)va_arg(args, int);
  
  // Récupérer une string
  char *str = va_arg(args, char *);
  
  // Récupérer un pointeur
  void *ptr = va_arg(args, void *);
  
  // Récupérer un unsigned int
  unsigned int u = va_arg(args, unsigned int);
  ```
</details>

## Architecture recommandée

```
ft_printf/
├── ft_printf.c           # Fonction principale
├── ft_printf.h           # Header
├── ft_printf_utils.c     # Fonctions utilitaires
├── ft_print_char.c       # Gestion %c
├── ft_print_string.c     # Gestion %s
├── ft_print_ptr.c        # Gestion %p
├── ft_print_nbr.c        # Gestion %d et %i
├── ft_print_unsigned.c   # Gestion %u
├── ft_print_hex.c        # Gestion %x et %X
└── Makefile
```

## Algorithme général

```c
int ft_printf(const char *format, ...)
{
    1. Initialiser va_list
    
    2. Parcourir la chaîne format caractère par caractère:
       
       Si caractère normal:
         • Afficher le caractère
         • Incrémenter le compteur
       
       Si '%':
         • Lire le caractère suivant (spécificateur)
         • Selon le spécificateur:
           - 'c': Récupérer char et afficher
           - 's': Récupérer string et afficher
           - 'p': Récupérer pointeur et afficher en hex
           - 'd'/'i': Récupérer int et afficher
           - 'u': Récupérer unsigned et afficher
           - 'x'/'X': Récupérer int et afficher en hex
           - '%': Afficher '%'
         • Incrémenter le compteur du nombre de chars affichés
    
    3. Nettoyer va_list
    
    4. Retourner le compteur
}
```

## Implémentations clés

### Fonction principale

```c
#include "ft_printf.h"

int ft_printf(const char *format, ...)
{
    va_list args;
    int     count;
    int     i;
    
    va_start(args, format);
    count = 0;
    i = 0;
    while (format[i])
    {
        if (format[i] == '%')
        {
            i++;
            count += handle_conversion(format[i], args);
        }
        else
            count += ft_putchar(format[i]);
        i++;
    }
    va_end(args);
    return (count);
}
```

### Gestion des conversions

```c
int handle_conversion(char specifier, va_list args)
{
    int count;
    
    count = 0;
    if (specifier == 'c')
        count = ft_print_char(va_arg(args, int));
    else if (specifier == 's')
        count = ft_print_string(va_arg(args, char *));
    else if (specifier == 'p')
        count = ft_print_ptr(va_arg(args, void *));
    else if (specifier == 'd' || specifier == 'i')
        count = ft_print_nbr(va_arg(args, int));
    else if (specifier == 'u')
        count = ft_print_unsigned(va_arg(args, unsigned int));
    else if (specifier == 'x')
        count = ft_print_hex(va_arg(args, unsigned int), 0);
    else if (specifier == 'X')
        count = ft_print_hex(va_arg(args, unsigned int), 1);
    else if (specifier == '%')
        count = ft_putchar('%');
    return (count);
}
```

### Affichage d'un nombre

```c
int ft_print_nbr(int n)
{
    int     count;
    long    nb;
    
    count = 0;
    nb = n;
    if (nb < 0)
    {
        count += ft_putchar('-');
        nb = -nb;
    }
    if (nb >= 10)
        count += ft_print_nbr(nb / 10);
    count += ft_putchar((nb % 10) + '0');
    return (count);
}
```

### Affichage en hexadécimal

```c
int ft_print_hex(unsigned int n, int uppercase)
{
    int     count;
    char    *base;
    
    if (uppercase)
        base = "0123456789ABCDEF";
    else
        base = "0123456789abcdef";
    
    count = 0;
    if (n >= 16)
        count += ft_print_hex(n / 16, uppercase);
    count += ft_putchar(base[n % 16]);
    return (count);
}
```

### Affichage d'un pointeur

```c
int ft_print_ptr(void *ptr)
{
    int             count;
    unsigned long   addr;
    
    if (!ptr)
        return (ft_print_string("(nil)"));
    
    addr = (unsigned long)ptr;
    count = ft_print_string("0x");
    count += ft_print_hex_long(addr, 0);
    return (count);
}
```

### Affichage d'une string

```c
int ft_print_string(char *s)
{
    int count;
    
    if (!s)
        return (ft_print_string("(null)"));
    
    count = 0;
    while (s[count])
    {
        ft_putchar(s[count]);
        count++;
    }
    return (count);
}
```

## Cas limites

<details>
<summary>INT_MIN et INT_MAX</summary>

<Accordion title="INT_MIN et INT_MAX">
    ```c
    ft_printf("INT_MIN: %d\n", -2147483648);
    ft_printf("INT_MAX: %d\n", 2147483647);
    ```
</details>
  
  <details>
<summary>NULL pointeurs</summary>

```c
    ft_printf("String NULL: %s\n", NULL);
    // Output: String NULL: (null)
    
    ft_printf("Pointer NULL: %p\n", NULL);
    // Output: Pointer NULL: (nil) ou 0x0
    ```
</details>
  
  <details>
<summary>Chaîne vide</summary>

```c
    ft_printf("");  // Retourne 0
    ft_printf("%s", "");  // Retourne 0
    ```
</details>
  
  <details>
<summary>Zéro</summary>

```c
    ft_printf("%d\n", 0);   // 0
    ft_printf("%x\n", 0);   // 0
    ft_printf("%p\n", 0);   // (nil) ou 0x0
    ```
</details>
  
  <details>
<summary>Multiples %</summary>

```c
    ft_printf("%%");    // %
    ft_printf("%%%%");  // %%
    ```
</details>


## Compilation

<div class="tabs-container">
<div class="tab-buttons">
  <div id="makefile" class="tab-content">
```makefile
    NAME = libftprintf.a
    
    CC = gcc
    CFLAGS = -Wall -Wextra -Werror
    
    SRCS = ft_printf.c \
           ft_print_char.c \
           ft_print_string.c \
           ft_print_ptr.c \
           ft_print_nbr.c \
           ft_print_unsigned.c \
           ft_print_hex.c \
           ft_printf_utils.c
    
    OBJS = $(SRCS:.c=.o)
    
    all: $(NAME)
    
    $(NAME): $(OBJS)
    	ar rcs $(NAME) $(OBJS)
    
    clean:
    	rm -f $(OBJS)
    
    fclean: clean
    	rm -f $(NAME)
    
    re: fclean all
    
    .PHONY: all clean fclean re
    ```
</div>
  
  <div id="compilation-simple" class="tab-content">
```bash
    # Compiler la bibliothèque
    make
    
    # Compiler avec un main
    gcc main.c libftprintf.a
    ./a.out
    ```
</div>
  
  <div id="tests" class="tab-content">
```bash
    # Compiler avec flags de debug
    gcc -Wall -Wextra -Werror -g ft_printf.c \
        ft_print_*.c main.c
    
    # Tester avec valgrind
    valgrind --leak-check=full ./a.out
    ```
</div>
</div>
</div>

## Tests recommandés

### Comparaison avec printf

```c
#include "ft_printf.h"
#include 

int main(void)
{
    int ret1, ret2;
    
    printf("=== TEST CHAR ===\n");
    ret1 = printf("Original: %c\n", 'A');
    ret2 = ft_printf("Mine:     %c\n", 'A');
    printf("Return: %d vs %d\n\n", ret1, ret2);
    
    printf("=== TEST STRING ===\n");
    ret1 = printf("Original: %s\n", "Hello");
    ret2 = ft_printf("Mine:     %s\n", "Hello");
    printf("Return: %d vs %d\n\n", ret1, ret2);
    
    printf("=== TEST INT ===\n");
    ret1 = printf("Original: %d\n", -42);
    ret2 = ft_printf("Mine:     %d\n", -42);
    printf("Return: %d vs %d\n\n", ret1, ret2);
    
    printf("=== TEST HEX ===\n");
    ret1 = printf("Original: %x %X\n", 255, 255);
    ret2 = ft_printf("Mine:     %x %X\n", 255, 255);
    printf("Return: %d vs %d\n\n", ret1, ret2);
    
    return (0);
}
```

### Testeur automatique

```bash
# Cloner un testeur
git clone https://github.com/Tripouille/printfTester.git
cd printfTester
make

# Ou
git clone https://github.com/paulo-santana/ft_printf_tester.git
cd ft_printf_tester
make test
```

## Astuces et conseils

{: .tip }
> 
**Commencez simple** : Implémentez d'abord %c et %s avant de passer aux conversions numériques.


{: .tip }
> 
**Testez au fur et à mesure** : Comparez systématiquement avec le vrai printf pour chaque conversion.


{: .tip }
> 
**Gérez les retours** : N'oubliez pas que printf retourne le nombre de caractères affichés, pas le nombre d'arguments !


{: .warning }
> 
**Attention aux promotions** : Les types char et short sont promus en int dans les fonctions variadiques.


{: .warning }
> 
**Protection NULL** : Gérez les pointeurs NULL pour %s et %p comme le fait printf.


## Erreurs fréquentes

<details>
<summary>Oublier va_end()</summary>

<Accordion title="Oublier va_end()">
    ```c
    // ❌ Mauvais
    int ft_printf(const char *format, ...)
    {
        va_list args;
        va_start(args, format);
        // ... traitement
        return (count);  // Oubli de va_end !
    }
    
    // ✅ Bon
    int ft_printf(const char *format, ...)
    {
        va_list args;
        va_start(args, format);
        // ... traitement
        va_end(args);
        return (count);
    }
    ```
</details>
  
  <details>
<summary>Mauvais comptage</summary>

```c
    // ❌ Mauvais
    count = ft_putnbr(n);  // Ne retourne rien
    
    // ✅ Bon
    count += ft_putnbr(n);  // Retourne le nb de chars
    ```
</details>
  
  <details>
<summary>Type incorrect dans va_arg</summary>

```c
    // ❌ Mauvais
    char c = va_arg(args, char);  // char est promu en int
    
    // ✅ Bon
    char c = (char)va_arg(args, int);
    ```
</details>
  
  <details>
<summary>INT_MIN mal géré</summary>

```c
    // ❌ Mauvais
    if (n < 0)
        n = -n;  // Overflow avec INT_MIN !
    
    // ✅ Bon
    long nb = n;
    if (nb < 0)
        nb = -nb;
    ```
</details>


## Optimisations possibles

### Bufferisation

```c
// Au lieu d'écrire caractère par caractère
// Accumuler dans un buffer

#define BUFFER_SIZE 1024

typedef struct s_printf
{
    char    buffer[BUFFER_SIZE];
    int     index;
    int     total;
}   t_printf;

void    buffer_char(t_printf *data, char c)
{
    if (data->index >= BUFFER_SIZE - 1)
    {
        write(1, data->buffer, data->index);
        data->index = 0;
    }
    data->buffer[data->index++] = c;
    data->total++;
}

void    flush_buffer(t_printf *data)
{
    if (data->index > 0)
    {
        write(1, data->buffer, data->index);
        data->index = 0;
    }
}
```

## Ressources

<div class="card-container">
  <div class="project-card">
  <h3>man stdarg</h3>
  <p>```bash
    man 3 stdarg
    ```
    Documentation des fonctions variadiques</p>
</div>
  
  <div class="project-card">
  <h3>man printf</h3>
  <p>```bash
    man 3 printf
    ```
    Comportement de printf original</p>
</div>
  
  <div class="project-card">
  <h3>Variadic Functions</h3>
  <p>Tutoriel complet sur les fonctions variadiques</p>
  <a href="https://www.cprogramming.com/tutorial/c/lesson17.html" class="btn btn-primary">Voir plus</a>
</div>
  
  <div class="project-card">
  <h3>printf implementation</h3>
  <p>Code source de printf (GNU)</p>
  <a href="https://github.com/coreutils/coreutils/blob/master/src/printf.c" class="btn btn-primary">Voir plus</a>
</div>
</div>

## Conclusion

ft_printf est un excellent projet pour :
- Comprendre les fonctions variadiques
- Maîtriser le parsing de format
- Améliorer la gestion des conversions numériques
- Créer un outil de debugging personnel

{: .check }
> 
Une fois terminé, vous pourrez utiliser votre propre printf dans tous vos projets !


{: .note }
> 
Ce projet pose les bases pour les parseurs plus complexes que vous rencontrerez dans les projets futurs comme minishell ou cub3d.
