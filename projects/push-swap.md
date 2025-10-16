---
layout: default
title: "Push Swap"
nav_order: 6
description: "Algorithme de tri optimisé avec deux piles"
icon: "arrows-up-down"
---

# 🔄 Push Swap

![Score](https://img.shields.io/badge/Score-125%2F100-success)
![Language](https://img.shields.io/badge/Language-C-blue)
![Difficulty](https://img.shields.io/badge/Difficulty-Hard-red)

## Introduction

**Push Swap** est un projet d'algorithmie où vous devez trier des nombres en utilisant deux piles et un ensemble limité d'opérations. L'objectif est de trier avec le minimum de mouvements possible.

<div class="project-card">
  <h3>Voir sur GitHub</h3>
  <p>Accéder au repository GitHub</p>
  <a href="https://github.com/NikoStano/push_swap" class="btn btn-primary">Voir plus</a>
</div>

{: .note }
>
Ce projet teste votre capacité à concevoir et optimiser des algorithmes de tri sous contraintes.

## Règles du jeu

### Les deux piles

- **Stack A** : Contient initialement tous les nombres (dans le désordre)
- **Stack B** : Vide au début

**Objectif** : Trier tous les nombres dans la stack A (ordre croissant), stack B doit être vide à la fin.

### Opérations autorisées

<details>
<summary>sa (swap a)</summary>

Intervertir les 2 premiers éléments de la stack A

    ```
    Avant:  A: [3, 1, 2]    B: []
    sa
    Après:  A: [1, 3, 2]    B: []
    ```
</details>

  <details>
<summary>sb (swap b)</summary>

Intervertir les 2 premiers éléments de la stack B

    ```
    Avant:  A: [1]       B: [5, 3]
    sb
    Après:  A: [1]       B: [3, 5]
    ```
</details>

  <details>
<summary>ss (swap both)</summary>

Faire `sa` et `sb` en même temps

    ```
    Avant:  A: [3, 1]    B: [5, 2]
    ss
    Après:  A: [1, 3]    B: [2, 5]
    ```
</details>

  <details>
<summary>pa (push a)</summary>

Prendre le premier élément de B et le mettre en haut de A

    ```
    Avant:  A: [1, 2]    B: [5, 3]
    pa
    Après:  A: [5, 1, 2] B: [3]
    ```
</details>

  <details>
<summary>pb (push b)</summary>

Prendre le premier élément de A et le mettre en haut de B

    ```
    Avant:  A: [3, 1, 2]    B: []
    pb
    Après:  A: [1, 2]       B: [3]
    ```
</details>

  <details>
<summary>ra (rotate a)</summary>

Décaler tous les éléments de A vers le haut (premier devient dernier)

    ```
    Avant:  A: [1, 2, 3]    B: []
    ra
    Après:  A: [2, 3, 1]    B: []
    ```
</details>

  <details>
<summary>rb (rotate b)</summary>

Décaler tous les éléments de B vers le haut

    ```
    Avant:  A: []        B: [1, 2, 3]
    rb
    Après:  A: []        B: [2, 3, 1]
    ```
</details>

  <details>
<summary>rr (rotate both)</summary>

Faire `ra` et `rb` en même temps
</details>

  <details>
<summary>rra (reverse rotate a)</summary>

Décaler tous les éléments de A vers le bas (dernier devient premier)

    ```
    Avant:  A: [1, 2, 3]    B: []
    rra
    Après:  A: [3, 1, 2]    B: []
    ```
</details>

  <details>
<summary>rrb (reverse rotate b)</summary>

Décaler tous les éléments de B vers le bas

    ```
    Avant:  A: []        B: [1, 2, 3]
    rrb
    Après:  A: []        B: [3, 1, 2]
    ```
</details>

  <details>
<summary>rrr (reverse rotate both)</summary>

Faire `rra` et `rrb` en même temps
</details>

## Objectifs de performance

<div class="tabs-container">
  <div class="tab-buttons"></div>
  <div id="3-nombres" class="tab-content">
- Maximum **3 opérations**
    - Facile avec conditions simples
  </div>
  <div id="5-nombres" class="tab-content">
- Maximum **12 opérations**
    - Utiliser un tri simple
  </div>
  <div id="100-nombres" class="tab-content">
- **Moins de 700** : 5 points ⭐⭐⭐⭐⭐
    - **Moins de 900** : 4 points ⭐⭐⭐⭐
    - **Moins de 1100** : 3 points ⭐⭐⭐
    - **Moins de 1300** : 2 points ⭐⭐
    - **Moins de 1500** : 1 point ⭐
  </div>
</div>
</div>

## Architecture du projet

```
push_swap/
├── src/
│   ├── main.c              # Point d'entrée
│   ├── parsing.c           # Validation et parsing des arguments
│   ├── stack_init.c        # Initialisation des stacks
│   ├── operations/
│   │   ├── swap.c          # sa, sb, ss
│   │   ├── push.c          # pa, pb
│   │   ├── rotate.c        # ra, rb, rr
│   │   └── reverse.c       # rra, rrb, rrr
│   ├── algorithm/
│   │   ├── sort_small.c    # Tri pour 3 et 5 nombres
│   │   ├── sort_large.c    # Tri pour 100+ nombres
│   │   └── utils.c         # Fonctions utilitaires
│   └── utils/
│       ├── stack_utils.c   # Manipulation de stacks
│       └── error.c         # Gestion d'erreurs
├── bonus/
│   └── checker.c           # Programme checker (bonus)
├── includes/
│   └── push_swap.h
├── libft/
└── Makefile
```

## Structures de données

### Structure de nœud (liste chaînée)

```c
typedef struct s_node
{
    int             value;      // Valeur du nombre
    int             index;      // Index après tri (0, 1, 2...)
    int             pos;        // Position actuelle dans la pile
    int             target_pos; // Position cible dans l'autre pile
    int             cost_a;     // Coût pour atteindre le top de A
    int             cost_b;     // Coût pour atteindre le top de B
    struct s_node   *next;      // Pointeur vers le suivant
}   t_node;

typedef struct s_stack
{
    t_node  *top;       // Sommet de la pile
    int     size;       // Nombre d'éléments
}   t_stack;
```

## Parsing et validation

```c
int main(int argc, char **argv)
{
    t_stack *stack_a;
    t_stack *stack_b;

    if (argc < 2)
        return (0);

    // Validation des arguments
    if (!validate_args(argc, argv))
    {
        ft_putendl_fd("Error", 2);
        return (1);
    }

    // Initialisation des stacks
    stack_a = init_stack(argc, argv);
    stack_b = create_empty_stack();

    // Si déjà trié, ne rien faire
    if (is_sorted(stack_a))
    {
        free_stack(stack_a);
        free_stack(stack_b);
        return (0);
    }

    // Choisir l'algorithme selon la taille
    if (stack_a->size <= 3)
        sort_three(stack_a);
    else if (stack_a->size <= 5)
        sort_five(stack_a, stack_b);
    else
        sort_large(stack_a, stack_b);

    // Libération
    free_stack(stack_a);
    free_stack(stack_b);

    return (0);
}
```

### Validation des arguments

```c
int validate_args(int argc, char **argv)
{
    int i;
    int j;
    long num;

    i = 1;
    while (i < argc)
    {
        // Vérifier que c'est un nombre valide
        if (!is_valid_number(argv[i]))
            return (0);

        // Vérifier les limites INT
        num = ft_atol(argv[i]);
        if (num < INT_MIN || num > INT_MAX)
            return (0);

        // Vérifier les doublons
        j = i + 1;
        while (j < argc)
        {
            if (ft_atoi(argv[i]) == ft_atoi(argv[j]))
                return (0);
            j++;
        }
        i++;
    }
    return (1);
}

int is_valid_number(char *str)
{
    int i;

    i = 0;
    if (str[i] == '+' || str[i] == '-')
        i++;

    if (!str[i])
        return (0);

    while (str[i])
    {
        if (!ft_isdigit(str[i]))
            return (0);
        i++;
    }
    return (1);
}
```

## Implémentation des opérations

### Swap

```c
void sa(t_stack *stack_a, int print)
{
    swap(stack_a);
    if (print)
        ft_putendl_fd("sa", 1);
}

void sb(t_stack *stack_b, int print)
{
    swap(stack_b);
    if (print)
        ft_putendl_fd("sb", 1);
}

void ss(t_stack *stack_a, t_stack *stack_b, int print)
{
    swap(stack_a);
    swap(stack_b);
    if (print)
        ft_putendl_fd("ss", 1);
}

static void swap(t_stack *stack)
{
    t_node *first;
    t_node *second;

    if (!stack || !stack->top || !stack->top->next)
        return;

    first = stack->top;
    second = first->next;

    first->next = second->next;
    second->next = first;
    stack->top = second;
}
```

### Push

```c
void pa(t_stack *stack_a, t_stack *stack_b, int print)
{
    push(stack_a, stack_b);
    if (print)
        ft_putendl_fd("pa", 1);
}

void pb(t_stack *stack_a, t_stack *stack_b, int print)
{
    push(stack_b, stack_a);
    if (print)
        ft_putendl_fd("pb", 1);
}

static void push(t_stack *dst, t_stack *src)
{
    t_node *tmp;

    if (!src || !src->top)
        return;

    tmp = src->top;
    src->top = src->top->next;
    src->size--;

    tmp->next = dst->top;
    dst->top = tmp;
    dst->size++;
}
```

### Rotate

```c
void ra(t_stack *stack_a, int print)
{
    rotate(stack_a);
    if (print)
        ft_putendl_fd("ra", 1);
}

void rb(t_stack *stack_b, int print)
{
    rotate(stack_b);
    if (print)
        ft_putendl_fd("rb", 1);
}

void rr(t_stack *stack_a, t_stack *stack_b, int print)
{
    rotate(stack_a);
    rotate(stack_b);
    if (print)
        ft_putendl_fd("rr", 1);
}

static void rotate(t_stack *stack)
{
    t_node *first;
    t_node *last;

    if (!stack || !stack->top || !stack->top->next)
        return;

    first = stack->top;
    stack->top = first->next;

    last = stack->top;
    while (last->next)
        last = last->next;

    last->next = first;
    first->next = NULL;
}
```

### Reverse Rotate

```c
void rra(t_stack *stack_a, int print)
{
    reverse_rotate(stack_a);
    if (print)
        ft_putendl_fd("rra", 1);
}

void rrb(t_stack *stack_b, int print)
{
    reverse_rotate(stack_b);
    if (print)
        ft_putendl_fd("rrb", 1);
}

void rrr(t_stack *stack_a, t_stack *stack_b, int print)
{
    reverse_rotate(stack_a);
    reverse_rotate(stack_b);
    if (print)
        ft_putendl_fd("rrr", 1);
}

static void reverse_rotate(t_stack *stack)
{
    t_node *last;
    t_node *second_last;

    if (!stack || !stack->top || !stack->top->next)
        return;

    second_last = NULL;
    last = stack->top;

    while (last->next)
    {
        second_last = last;
        last = last->next;
    }

    second_last->next = NULL;
    last->next = stack->top;
    stack->top = last;
}
```

## Algorithmes de tri

### Tri pour 3 nombres

```c
void sort_three(t_stack *stack_a)
{
    int first;
    int second;
    int third;

    first = stack_a->top->value;
    second = stack_a->top->next->value;
    third = stack_a->top->next->next->value;

    if (first > second && second < third && first < third)
        sa(stack_a, 1);  // 2 1 3
    else if (first > second && second > third)
    {
        sa(stack_a, 1);  // 3 2 1 -> 2 3 1
        rra(stack_a, 1); // 2 3 1 -> 1 2 3
    }
    else if (first > second && second < third && first > third)
        ra(stack_a, 1);  // 3 1 2
    else if (first < second && second > third && first < third)
    {
        sa(stack_a, 1);  // 1 3 2 -> 3 1 2
        ra(stack_a, 1);  // 3 1 2 -> 1 2 3
    }
    else if (first < second && second > third && first > third)
        rra(stack_a, 1); // 2 3 1
}
```

### Tri pour 5 nombres

```c
void sort_five(t_stack *stack_a, t_stack *stack_b)
{
    // Pousser les 2 plus petits dans B
    push_min_to_b(stack_a, stack_b);
    push_min_to_b(stack_a, stack_b);

    // Trier les 3 restants dans A
    sort_three(stack_a);

    // Ramener les 2 de B dans A
    pa(stack_a, stack_b, 1);
    pa(stack_a, stack_b, 1);
}

void push_min_to_b(t_stack *stack_a, t_stack *stack_b)
{
    int min_pos;
    int size;

    min_pos = find_min_position(stack_a);
    size = stack_a->size;

    // Amener le minimum en haut
    if (min_pos <= size / 2)
    {
        while (min_pos--)
            ra(stack_a, 1);
    }
    else
    {
        while (min_pos++ < size)
            rra(stack_a, 1);
    }

    // Pousser dans B
    pb(stack_a, stack_b, 1);
}
```

### Tri pour grandes quantités (Algorithme Turk/Chunk)

```c
void sort_large(t_stack *stack_a, t_stack *stack_b)
{
    // 1. Indexer les valeurs (0 à n-1)
    index_stack(stack_a);

    // 2. Pousser tout dans B par chunks, sauf 3
    push_to_b_by_chunks(stack_a, stack_b);

    // 3. Trier les 3 restants dans A
    sort_three(stack_a);

    // 4. Ramener de B vers A de manière optimisée
    while (stack_b->size > 0)
    {
        // Calculer les coûts pour chaque élément de B
        calculate_costs(stack_a, stack_b);

        // Exécuter le mouvement le moins coûteux
        execute_cheapest_move(stack_a, stack_b);
    }

    // 5. Rotation finale pour mettre le minimum en haut
    final_rotation(stack_a);
}
```

### Indexation

```c
void index_stack(t_stack *stack)
{
    t_node *current;
    t_node *compare;
    int index;

    current = stack->top;
    while (current)
    {
        index = 0;
        compare = stack->top;

        // Compter combien d'éléments sont plus petits
        while (compare)
        {
            if (compare->value < current->value)
                index++;
            compare = compare->next;
        }

        current->index = index;
        current = current->next;
    }
}
```

### Push par chunks

```c
void push_to_b_by_chunks(t_stack *stack_a, t_stack *stack_b)
{
    int chunk_size;
    int chunk_max;
    int pushed;

    // Définir la taille des chunks selon la taille totale
    if (stack_a->size <= 100)
        chunk_size = 20;
    else
        chunk_size = 35;

    chunk_max = chunk_size;
    pushed = 0;

    // Pousser tout sauf 3 éléments
    while (stack_a->size > 3)
    {
        if (stack_a->top->index < chunk_max)
        {
            pb(stack_a, stack_b, 1);
            pushed++;

            // Rotation de B pour optimiser
            if (stack_b->top->index < chunk_max - chunk_size / 2)
                rb(stack_b, 1);
        }
        else
            ra(stack_a, 1);

        // Passer au chunk suivant
        if (pushed == chunk_max)
            chunk_max += chunk_size;
    }
}
```

### Calcul des coûts

```c
void calculate_costs(t_stack *stack_a, t_stack *stack_b)
{
    t_node *current_b;
    int size_a;
    int size_b;

    size_a = stack_a->size;
    size_b = stack_b->size;

    assign_positions(stack_a);
    assign_positions(stack_b);

    current_b = stack_b->top;
    while (current_b)
    {
        // Trouver la position cible dans A
        current_b->target_pos = find_target_position(stack_a, current_b->index);

        // Calculer le coût pour B
        if (current_b->pos <= size_b / 2)
            current_b->cost_b = current_b->pos;
        else
            current_b->cost_b = -(size_b - current_b->pos);

        // Calculer le coût pour A
        if (current_b->target_pos <= size_a / 2)
            current_b->cost_a = current_b->target_pos;
        else
            current_b->cost_a = -(size_a - current_b->target_pos);

        current_b = current_b->next;
    }
}

int find_target_position(t_stack *stack_a, int index_b)
{
    t_node *current;
    int target_index;
    int target_pos;

    target_index = INT_MAX;
    target_pos = 0;

    current = stack_a->top;
    while (current)
    {
        // Trouver le plus petit index dans A qui est plus grand que index_b
        if (current->index > index_b && current->index < target_index)
        {
            target_index = current->index;
            target_pos = current->pos;
        }
        current = current->next;
    }

    // Si aucun trouvé, chercher le minimum dans A
    if (target_index == INT_MAX)
        target_pos = find_min_position(stack_a);

    return (target_pos);
}
```

### Exécution du mouvement le moins coûteux

```c
void execute_cheapest_move(t_stack *stack_a, t_stack *stack_b)
{
    t_node *cheapest;
    int cost_a;
    int cost_b;

    cheapest = find_cheapest(stack_b);
    cost_a = cheapest->cost_a;
    cost_b = cheapest->cost_b;

    // Optimiser avec les rotations doubles
    while (cost_a > 0 && cost_b > 0)
    {
        rr(stack_a, stack_b, 1);
        cost_a--;
        cost_b--;
    }

    while (cost_a < 0 && cost_b < 0)
    {
        rrr(stack_a, stack_b, 1);
        cost_a++;
        cost_b++;
    }

    // Rotations restantes pour A
    while (cost_a > 0)
    {
        ra(stack_a, 1);
        cost_a--;
    }
    while (cost_a < 0)
    {
        rra(stack_a, 1);
        cost_a++;
    }

    // Rotations restantes pour B
    while (cost_b > 0)
    {
        rb(stack_b, 1);
        cost_b--;
    }
    while (cost_b < 0)
    {
        rrb(stack_b, 1);
        cost_b++;
    }

    // Push vers A
    pa(stack_a, stack_b, 1);
}

t_node *find_cheapest(t_stack *stack_b)
{
    t_node *current;
    t_node *cheapest;
    int min_cost;
    int current_cost;

    current = stack_b->top;
    cheapest = current;
    min_cost = INT_MAX;

    while (current)
    {
        current_cost = abs(current->cost_a) + abs(current->cost_b);

        if (current_cost < min_cost)
        {
            min_cost = current_cost;
            cheapest = current;
        }
        current = current->next;
    }

    return (cheapest);
}
```

### Rotation finale

```c
void final_rotation(t_stack *stack_a)
{
    int min_pos;
    int size;

    min_pos = find_min_position(stack_a);
    size = stack_a->size;

    if (min_pos <= size / 2)
    {
        while (min_pos--)
            ra(stack_a, 1);
    }
    else
    {
        while (min_pos++ < size)
            rra(stack_a, 1);
    }
}
```

## Bonus : Checker

Le checker vérifie si une séquence d'opérations trie correctement la stack.

```c
int main(int argc, char **argv)
{
    t_stack *stack_a;
    t_stack *stack_b;
    char    *line;

    if (argc < 2)
        return (0);

    if (!validate_args(argc, argv))
    {
        ft_putendl_fd("Error", 2);
        return (1);
    }

    stack_a = init_stack(argc, argv);
    stack_b = create_empty_stack();

    // Lire les opérations depuis stdin
    while (get_next_line(0, &line) > 0)
    {
        if (!execute_operation(line, stack_a, stack_b))
        {
            ft_putendl_fd("Error", 2);
            free(line);
            return (1);
        }
        free(line);
    }

    // Vérifier si trié
    if (is_sorted(stack_a) && stack_b->size == 0)
        ft_putendl_fd("OK", 1);
    else
        ft_putendl_fd("KO", 1);

    free_stack(stack_a);
    free_stack(stack_b);
    return (0);
}

int execute_operation(char *line, t_stack *a, t_stack *b)
{
    if (ft_strcmp(line, "sa") == 0)
        sa(a, 0);
    else if (ft_strcmp(line, "sb") == 0)
        sb(b, 0);
    else if (ft_strcmp(line, "ss") == 0)
        ss(a, b, 0);
    else if (ft_strcmp(line, "pa") == 0)
        pa(a, b, 0);
    else if (ft_strcmp(line, "pb") == 0)
        pb(a, b, 0);
    else if (ft_strcmp(line, "ra") == 0)
        ra(a, 0);
    else if (ft_strcmp(line, "rb") == 0)
        rb(b, 0);
    else if (ft_strcmp(line, "rr") == 0)
        rr(a, b, 0);
    else if (ft_strcmp(line, "rra") == 0)
        rra(a, 0);
    else if (ft_strcmp(line, "rrb") == 0)
        rrb(b, 0);
    else if (ft_strcmp(line, "rrr") == 0)
        rrr(a, b, 0);
    else
        return (0);
    return (1);
}
```

## Tests

### Tester manuellement

```bash
# Trier 3 nombres
./push_swap 2 1 3

# Trier 5 nombres
./push_swap 5 3 1 4 2

# Trier 100 nombres aléatoires
ARG=$(seq 1 100 | shuf | tr '\n' ' ')
./push_swap $ARG | wc -l

# Vérifier avec checker
ARG="3 2 1"
./push_swap $ARG | ./checker $ARG
```

### Script de test automatique

```bash
#!/bin/bash

# test.sh

# Fonction pour générer des nombres aléatoires
generate_random() {
    seq 1 $1 | shuf | tr '\n' ' '
}

# Test 100 nombres (5 fois)
echo "Testing 100 numbers..."
for i in {1..5}; do
    ARG=$(generate_random 100)
    COUNT=$(./push_swap $ARG | wc -l)
    echo "Test $i: $COUNT operations"
done

# Test 500 nombres (5 fois)
echo -e "\nTesting 500 numbers..."
for i in {1..5}; do
    ARG=$(generate_random 500)
    COUNT=$(./push_swap $ARG | wc -l)
    echo "Test $i: $COUNT operations"
done
```

### Visualiseur

Utilisez un visualiseur pour voir les mouvements :

```bash
# Cloner un visualiseur
git clone https://github.com/o-reo/push_swap_visualizer.git
cd push_swap_visualizer
mkdir build && cd build
cmake ..
make

# Utiliser
./bin/visualizer
```

## Conseils d'optimisation

{: .tip }
>
**Utilisez les opérations doubles** (ss, rr, rrr) quand c'est possible pour économiser des mouvements.

{: .tip }
>
**Chunk size optimal** : Pour 100 nombres, utilisez 20. Pour 500, utilisez 35-40.

{: .tip }
>
**Rotation intelligente** : Toujours choisir le chemin le plus court (rotate vs reverse rotate).

{: .warning }
>
**Attention à l'indexation** : L'index doit être calculé correctement (0 à n-1) pour que l'algorithme fonctionne.

## Erreurs fréquentes

<details>
<summary>Mauvaise gestion des doublons</summary>

**Problème** : Ne pas détecter les doublons dans les arguments

    **Solution** : Vérifier tous les arguments entre eux
    ```c
    // Vérifier chaque paire
    for (i = 1; i < argc; i++)
        for (j = i + 1; j < argc; j++)
            if (ft_atoi(argv[i]) == ft_atoi(argv[j]))
                return (0);
    ```
</details>

  <details>
<summary>Dépassement d'INT</summary>

**Problème** : Ne pas vérifier les limites de INT_MIN et INT_MAX

    **Solution** : Utiliser `long` pour parser puis vérifier
    ```c
    long num = ft_atol(argv[i]);
    if (num < INT_MIN || num > INT_MAX)
        return (0);
    ```
</details>

  <details>
<summary>Fuites mémoire</summary>

**Problème** : Oublier de libérer les nœuds de la liste

    **Solution** : Fonction de libération complète
    ```c
    void free_stack(t_stack *stack)
    {
        t_node *current;
        t_node *next;

        if (!stack)
            return;

        current = stack->top;
        while (current)
        {
            next = current->next;
            free(current);
            current = next;
        }
        free(stack);
    }
    ```
</details>

  <details>
<summary>Mauvais calcul de coût</summary>

**Problème** : Ne pas utiliser le chemin le plus court

    **Solution** : Comparer position vs (size - position)
    ```c
    if (pos <= size / 2)
        cost = pos;        // rotate
    else
        cost = -(size - pos);  // reverse rotate (négatif)
    ```
</details>

## Makefile

```makefile
NAME = push_swap
BONUS = checker

CC = gcc
CFLAGS = -Wall -Wextra -Werror

SRCS = src/main.c \
       src/parsing.c \
       src/stack_init.c \
       src/operations/swap.c \
       src/operations/push.c \
       src/operations/rotate.c \
       src/operations/reverse.c \
       src/algorithm/sort_small.c \
       src/algorithm/sort_large.c \
       src/algorithm/utils.c \
       src/utils/stack_utils.c \
       src/utils/error.c

BONUS_SRCS = bonus/checker.c \
             src/parsing.c \
             src/stack_init.c \
             src/operations/swap.c \
             src/operations/push.c \
             src/operations/rotate.c \
             src/operations/reverse.c \
             src/utils/stack_utils.c \
             src/utils/error.c

OBJS = $(SRCS:.c=.o)
BONUS_OBJS = $(BONUS_SRCS:.c=.o)

LIBFT = libft/libft.a

all: $(NAME)

$(NAME): $(OBJS) $(LIBFT)
	$(CC) $(CFLAGS) $(OBJS) $(LIBFT) -o $(NAME)

$(BONUS): $(BONUS_OBJS) $(LIBFT)
	$(CC) $(CFLAGS) $(BONUS_OBJS) $(LIBFT) -o $(BONUS)

$(LIBFT):
	make -C libft

bonus: $(BONUS)

clean:
	rm -f $(OBJS) $(BONUS_OBJS)
	make -C libft clean

fclean: clean
	rm -f $(NAME) $(BONUS)
	make -C libft fclean

re: fclean all

.PHONY: all bonus clean fclean re
```

## Cas de test importants

<div class="tabs-container">
  <div class="tab-buttons"></div>
  <div id="déjà-trié" class="tab-content">
```bash
    # Ne doit rien afficher
    ./push_swap 1 2 3 4 5
    # Output: (rien)
    ```
  </div>
  <div id="ordre-inversé" class="tab-content">
```bash
    # Pire cas
    ./push_swap 5 4 3 2 1
    ```
  </div>
  <div id="nombres-négatifs" class="tab-content">
```bash
    ./push_swap -5 -2 0 3 1
    ./push_swap -2147483648 0 2147483647
    ```
  </div>
</div>
</div>

## Améliorations possibles

<details>
<summary>Pré-tri dans B</summary>

Au lieu de pousser aléatoirement, pousser en gardant B trié

    - Économise des rotations lors du retour vers A
    - Réduit le nombre total d'opérations
</details>

  <details>
<summary>Optimisation des rotations doubles</summary>

Détecter quand on peut utiliser rr ou rrr

    ```c
    // Au lieu de ra + rb, utiliser rr
    if (cost_a > 0 && cost_b > 0)
        use_rr_optimization();
    ```
</details>

  <details>
<summary>Meilleure sélection de chunks</summary>

Adapter la taille des chunks dynamiquement

    ```c
    if (size <= 100)
        chunk_size = 20;
    else if (size <= 250)
        chunk_size = 30;
    else
        chunk_size = 40;
    ```
</details>

  <details>
<summary>Algorithme A* ou Greedy amélioré</summary>

Pour les perfectionnistes qui veulent le minimum absolu d'opérations

    - Plus complexe à implémenter
    - Peut réduire de 10-15% le nombre d'opérations
</details>

## Stratégies selon la taille

### 3 nombres (max 3 ops)

```
Simple comparaisons et conditions
→ Toujours possible en 2-3 opérations max
```

### 5 nombres (max 12 ops)

```
1. Pousser les 2 plus petits vers B (4-6 ops)
2. Trier les 3 dans A (0-2 ops)
3. Ramener de B vers A (2 ops)
Total: 6-10 opérations
```

### 100 nombres (objectif < 700)

```
1. Indexation (0 ops, juste calcul)
2. Push par chunks de 20 (~180-200 ops)
3. Sort des 3 derniers (2 ops)
4. Retour optimisé de B vers A (~450-500 ops)
Total: ~650-700 opérations
```

### 500 nombres (objectif < 5500)

```
1. Indexation
2. Push par chunks de 35-40 (~900-1000 ops)
3. Sort des 3 derniers (2 ops)
4. Retour optimisé de B vers A (~4000-4500 ops)
Total: ~5000-5500 opérations
```

## Exemple complet simplifié

Voici un exemple pour trier `3 2 1` :

```bash
# État initial
A: [3, 2, 1]
B: []

# pb - pousser 3 vers B
A: [2, 1]
B: [3]

# sa - swap A
A: [1, 2]
B: [3]

# pa - ramener 3
A: [3, 1, 2]
B: []

# ra - rotate A
A: [1, 2, 3]
B: []

# RÉSULTAT: Trié en 4 opérations
```

## Ressources

<div class="card-container">
  <div class="project-card">
  <h3>Visualiseur</h3>
  <p>Voir les mouvements en temps réel</p>
  <a href="https://github.com/o-reo/push_swap_visualizer" class="btn btn-primary">Voir plus</a>
</div>

  <div class="project-card">
  <h3>Tester</h3>
  <p>Testeur automatique complet</p>
  <a href="https://github.com/LeoFu9487/push_swap_tester" class="btn btn-primary">Voir plus</a>
</div>

  <div class="project-card">
  <h3>Algorithme Turk</h3>
  <p>Explication détaillée de l'algorithme</p>
  <a href="https://medium.com/@ayogun/push-swap-c1f5d2d41e97" class="btn btn-primary">Voir plus</a>
</div>

  <div class="project-card">
  <h3>Listes chaînées</h3>
  <p>Comprendre les listes chaînées en C</p>
  <a href="https://www.learn-c.org/en/Linked_lists" class="btn btn-primary">Voir plus</a>
</div>
</div>

## Astuces de debugging

```c
// Fonction pour afficher l'état des stacks
void print_stacks(t_stack *a, t_stack *b)
{
    t_node *current_a = a->top;
    t_node *current_b = b->top;

    printf("\n--- STACKS ---\n");
    printf("A: ");
    while (current_a)
    {
        printf("%d ", current_a->value);
        current_a = current_a->next;
    }
    printf("\nB: ");
    while (current_b)
    {
        printf("%d ", current_b->value);
        current_b = current_b->next;
    }
    printf("\n--------------\n\n");
}

// Fonction pour compter les opérations
int count_operations(char *operations_file)
{
    int fd;
    char *line;
    int count;

    fd = open(operations_file, O_RDONLY);
    count = 0;
    while (get_next_line(fd, &line) > 0)
    {
        count++;
        free(line);
    }
    close(fd);
    return (count);
}
```

## Conclusion

Push Swap est un projet d'algorithmie complexe qui demande :
- Compréhension des structures de données (listes chaînées)
- Conception d'algorithmes optimisés
- Analyse de la complexité
- Gestion rigoureuse de la mémoire

{: .check }
>
Une fois maîtrisé, vous aurez développé une excellente intuition pour l'optimisation d'algorithmes sous contraintes !

{: .note }
>
Ne vous découragez pas si vos premiers essais dépassent les limites. L'optimisation se fait par itérations successives.

{: .tip }
>
**Conseil final** : Commencez par un algorithme simple qui fonctionne, puis optimisez progressivement !
