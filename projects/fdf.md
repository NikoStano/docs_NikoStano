---
layout: default
title: "FdF - Fil de Fer"
description: "Affichage wireframe 3D avec projection isométrique"
icon: "cube"
---

# 🎨 FdF (Fil de Fer)

<img src="https://img.shields.io/badge/Score-125%2F100-success" alt="Score" />
<img src="https://img.shields.io/badge/Language-C-blue" alt="Language" />
<img src="https://img.shields.io/badge/Graphics-MiniLibX-purple" alt="Graphics" />

## Introduction

**FdF** (Fil de Fer) est votre premier projet graphique. Vous devez créer une représentation 3D en wireframe d'un paysage à partir d'une carte 2D de hauteurs.

<div class="project-card">
  <h3>Voir sur GitHub</h3>
  <p>Accéder au repository GitHub</p>
  <a href="https://github.com/NikoStano/FdF" class="btn btn-primary">Voir plus</a>
</div>

{: .note }
> 
Ce projet introduit les concepts de graphisme 3D, transformations matricielles, projection isométrique et utilisation de la MiniLibX.


## Objectifs pédagogiques

<div class="steps-container">
  <div class="step">
  <h4>Graphisme en C</h4>
  <p>Apprendre à utiliser la MiniLibX pour afficher des pixels et des lignes</p>
</div>
  
  <div class="step">
  <h4>Mathématiques 3D</h4>
  <p>Comprendre les transformations matricielles et les projections</p>
</div>
  
  <div class="step">
  <h4>Parsing de fichiers</h4>
  <p>Lire et interpréter des fichiers de carte (format .fdf)</p>
</div>
  
  <div class="step">
  <h4>Optimisation</h4>
  <p>Gérer l'affichage fluide de grandes cartes</p>
</div>
</div>

## Format du fichier .fdf

Les cartes sont stockées dans des fichiers texte avec l'extension `.fdf` :

```
0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
0  0 10 10  0  0 10 10  0  0  0 10 10 10 10 10  0  0  0
0  0 10 10  0  0 10 10  0  0  0  0  0  0  0 10 10  0  0
0  0 10 10  0  0 10 10  0  0  0  0  0  0  0 10 10  0  0
0  0 10 10 10 10 10 10  0  0  0  0 10 10 10 10  0  0  0
0  0  0 10 10 10 10 10  0  0  0 10 10  0  0  0  0  0  0
0  0  0  0  0  0 10 10  0  0  0 10 10  0  0  0  0  0  0
0  0  0  0  0  0 10 10  0  0  0 10 10 10 10 10 10  0  0
0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
```

- Chaque nombre représente une altitude (coordonnée Z)
- Les espaces séparent les valeurs
- Les lignes représentent les coordonnées Y
- Les colonnes représentent les coordonnées X

### Avec couleurs (bonus)

```
0,0xFF0000  0,0x00FF00  0,0x0000FF
10,0xFFFFFF 10,0x000000 10,0xFF00FF
```

Format : `altitude,0xCOULEUR`

## Concepts mathématiques

### Projection isométrique

La projection isométrique transforme un point 3D en point 2D :

```c
// Formules de projection isométrique
x' = (x - y) * cos(0.523599)  // 0.523599 rad = 30°
y' = (x + y) * sin(0.523599) - z

// Ou simplifié
x' = (x - y) * 0.866  // cos(30°) ≈ 0.866
y' = (x + y) * 0.5 - z  // sin(30°) = 0.5
```

### Algorithme de Bresenham

Pour dessiner des lignes entre les points :

```c
void draw_line(t_data *data, t_point p1, t_point p2)
{
    int dx = abs(p2.x - p1.x);
    int dy = abs(p2.y - p1.y);
    int sx = (p1.x < p2.x) ? 1 : -1;
    int sy = (p1.y < p2.y) ? 1 : -1;
    int err = dx - dy;
    
    while (1)
    {
        mlx_pixel_put(data->mlx, data->win, p1.x, p1.y, 0xFFFFFF);
        
        if (p1.x == p2.x && p1.y == p2.y)
            break;
            
        int e2 = 2 * err;
        if (e2 > -dy)
        {
            err -= dy;
            p1.x += sx;
        }
        if (e2 < dx)
        {
            err += dx;
            p1.y += sy;
        }
    }
}
```

{: .warning }
> 
N'utilisez PAS `mlx_pixel_put` pour chaque pixel ! C'est beaucoup trop lent. Utilisez plutôt une image en mémoire avec `mlx_put_image_to_window`.


## Architecture du projet

```
fdf/
├── src/
│   ├── main.c              # Point d'entrée
│   ├── parsing.c           # Lecture du fichier .fdf
│   ├── init.c              # Initialisation MLX
│   ├── draw.c              # Dessin (Bresenham)
│   ├── projection.c        # Transformations 3D
│   ├── hooks.c             # Gestion événements
│   └── utils.c             # Fonctions utilitaires
├── includes/
│   └── fdf.h               # Header principal
├── maps/                   # Fichiers .fdf de test
│   ├── 42.fdf
│   ├── pyramide.fdf
│   └── test_maps/
├── libft/                  # Votre libft
├── minilibx/               # MiniLibX
└── Makefile
```

## Structures de données

```c
// Point en 3D
typedef struct s_point
{
    int     x;
    int     y;
    int     z;
    int     color;
}   t_point;

// Données de la map
typedef struct s_map
{
    int     width;
    int     height;
    int     **z_matrix;
    int     **colors;
    int     z_min;
    int     z_max;
}   t_map;

// Données MLX
typedef struct s_data
{
    void    *mlx;
    void    *win;
    void    *img;
    char    *addr;
    int     bits_per_pixel;
    int     line_length;
    int     endian;
    t_map   *map;
    
    // Paramètres de vue
    int     zoom;
    int     offset_x;
    int     offset_y;
    float   z_scale;
    float   angle_x;
    float   angle_y;
    float   angle_z;
}   t_data;
```

## Parsing du fichier

<div class="tabs-container">
<div class="tab-buttons">
  <div id="lecture" class="tab-content">
```c
    t_map *parse_map(char *filename)
    {
        int     fd;
        char    *line;
        t_map   *map;
        
        fd = open(filename, O_RDONLY);
        if (fd < 0)
            return (NULL);
        
        map = init_map();
        
        // Première lecture : compter lignes et colonnes
        map->height = count_lines(fd);
        close(fd);
        
        fd = open(filename, O_RDONLY);
        line = get_next_line(fd);
        map->width = count_values(line);
        
        // Allouer la matrice
        map->z_matrix = allocate_matrix(map->width, map->height);
        
        // Deuxième lecture : remplir la matrice
        fill_matrix(fd, map);
        
        close(fd);
        return (map);
    }
    ```
</div>
  
  <div id="extraction-des-valeurs" class="tab-content">
```c
    void fill_matrix(int fd, t_map *map)
    {
        char    *line;
        char    **values;
        int     y;
        int     x;
        
        y = 0;
        while ((line = get_next_line(fd)) != NULL)
        {
            values = ft_split(line, ' ');
            x = 0;
            while (values[x])
            {
                map->z_matrix[y][x] = ft_atoi(values[x]);
                
                // Bonus : couleurs
                if (ft_strchr(values[x], ','))
                    map->colors[y][x] = get_color(values[x]);
                else
                    map->colors[y][x] = 0xFFFFFF;
                    
                free(values[x]);
                x++;
            }
            free(values);
            free(line);
            y++;
        }
    }
    ```
</div>
  
  <div id="extraction-couleur" class="tab-content">
```c
    int get_color(char *str)
    {
        char    *color_str;
        int     color;
        
        color_str = ft_strchr(str, ',');
        if (!color_str)
            return (0xFFFFFF);
        
        color_str++; // Sauter la virgule
        
        if (color_str[0] == '0' && color_str[1] == 'x')
            color = ft_atoi_base(color_str + 2, 16);
        else
            color = ft_atoi(color_str);
        
        return (color);
    }
    ```
</div>
</div>
</div>

## Initialisation MiniLibX

```c
t_data *init_mlx(t_map *map)
{
    t_data *data;
    
    data = malloc(sizeof(t_data));
    if (!data)
        return (NULL);
    
    // Initialiser MLX
    data->mlx = mlx_init();
    if (!data->mlx)
        return (NULL);
    
    // Créer la fenêtre
    data->win = mlx_new_window(data->mlx, 1920, 1080, "FdF");
    
    // Créer l'image
    data->img = mlx_new_image(data->mlx, 1920, 1080);
    data->addr = mlx_get_data_addr(data->img, 
                                    &data->bits_per_pixel,
                                    &data->line_length, 
                                    &data->endian);
    
    // Paramètres de vue par défaut
    data->map = map;
    data->zoom = 20;
    data->offset_x = 960;
    data->offset_y = 540;
    data->z_scale = 1.0;
    data->angle_x = 0;
    data->angle_y = 0;
    data->angle_z = 0;
    
    return (data);
}
```

## Projection et dessin

### Projection isométrique

```c
t_point project(t_point point, t_data *data)
{
    t_point projected;
    
    // Appliquer le zoom
    point.x *= data->zoom;
    point.y *= data->zoom;
    point.z *= data->zoom * data->z_scale;
    
    // Projection isométrique
    projected.x = (point.x - point.y) * cos(0.523599);
    projected.y = (point.x + point.y) * sin(0.523599) - point.z;
    
    // Centrer
    projected.x += data->offset_x;
    projected.y += data->offset_y;
    
    projected.color = point.color;
    
    return (projected);
}
```

### Rotation (bonus)

```c
t_point rotate_x(t_point point, float angle)
{
    t_point rotated;
    
    rotated.x = point.x;
    rotated.y = point.y * cos(angle) - point.z * sin(angle);
    rotated.z = point.y * sin(angle) + point.z * cos(angle);
    rotated.color = point.color;
    
    return (rotated);
}

t_point rotate_y(t_point point, float angle)
{
    t_point rotated;
    
    rotated.x = point.x * cos(angle) + point.z * sin(angle);
    rotated.y = point.y;
    rotated.z = -point.x * sin(angle) + point.z * cos(angle);
    rotated.color = point.color;
    
    return (rotated);
}

t_point rotate_z(t_point point, float angle)
{
    t_point rotated;
    
    rotated.x = point.x * cos(angle) - point.y * sin(angle);
    rotated.y = point.x * sin(angle) + point.y * cos(angle);
    rotated.z = point.z;
    rotated.color = point.color;
    
    return (rotated);
}
```

### Dessin optimisé

```c
void my_mlx_pixel_put(t_data *data, int x, int y, int color)
{
    char *dst;
    
    // Vérifier les limites
    if (x < 0 || x >= 1920 || y < 0 || y >= 1080)
        return;
    
    dst = data->addr + (y * data->line_length + x * (data->bits_per_pixel / 8));
    *(unsigned int*)dst = color;
}

void draw_line_fast(t_data *data, t_point p1, t_point p2)
{
    int dx = abs(p2.x - p1.x);
    int dy = abs(p2.y - p1.y);
    int sx = (p1.x < p2.x) ? 1 : -1;
    int sy = (p1.y < p2.y) ? 1 : -1;
    int err = dx - dy;
    int color;
    
    while (1)
    {
        // Interpolation de couleur (bonus)
        color = get_gradient_color(p1, p2, dx, dy);
        my_mlx_pixel_put(data, p1.x, p1.y, color);
        
        if (p1.x == p2.x && p1.y == p2.y)
            break;
            
        int e2 = 2 * err;
        if (e2 > -dy)
        {
            err -= dy;
            p1.x += sx;
        }
        if (e2 < dx)
        {
            err += dx;
            p1.y += sy;
        }
    }
}
```

### Rendu complet

```c
void render(t_data *data)
{
    int x;
    int y;
    t_point p1;
    t_point p2;
    
    // Effacer l'image
    ft_bzero(data->addr, 1920 * 1080 * 4);
    
    y = 0;
    while (y < data->map->height)
    {
        x = 0;
        while (x < data->map->width)
        {
            // Créer le point
            p1.x = x;
            p1.y = y;
            p1.z = data->map->z_matrix[y][x];
            p1.color = data->map->colors[y][x];
            
            // Projeter
            p1 = project(p1, data);
            
            // Ligne horizontale
            if (x < data->map->width - 1)
            {
                p2.x = x + 1;
                p2.y = y;
                p2.z = data->map->z_matrix[y][x + 1];
                p2.color = data->map->colors[y][x + 1];
                p2 = project(p2, data);
                draw_line_fast(data, p1, p2);
            }
            
            // Ligne verticale
            if (y < data->map->height - 1)
            {
                p2.x = x;
                p2.y = y + 1;
                p2.z = data->map->z_matrix[y + 1][x];
                p2.color = data->map->colors[y + 1][x];
                p2 = project(p2, data);
                draw_line_fast(data, p1, p2);
            }
            x++;
        }
        y++;
    }
    
    // Afficher l'image
    mlx_put_image_to_window(data->mlx, data->win, data->img, 0, 0);
}
```

## Gestion des événements

```c
int key_hook(int keycode, t_data *data)
{
    // ESC : quitter
    if (keycode == 53)
        close_window(data);
    
    // Zoom
    if (keycode == 69)  // +
        data->zoom += 2;
    if (keycode == 78)  // -
        data->zoom -= 2;
    
    // Déplacement
    if (keycode == 126) // Up
        data->offset_y -= 10;
    if (keycode == 125) // Down
        data->offset_y += 10;
    if (keycode == 123) // Left
        data->offset_x -= 10;
    if (keycode == 124) // Right
        data->offset_x += 10;
    
    // Hauteur Z
    if (keycode == 1)   // S
        data->z_scale -= 0.1;
    if (keycode == 13)  // W
        data->z_scale += 0.1;
    
    // Rotation (bonus)
    if (keycode == 0)   // A
        data->angle_z -= 0.1;
    if (keycode == 2)   // D
        data->angle_z += 0.1;
    
    // Redessiner
    render(data);
    
    return (0);
}

int mouse_hook(int button, int x, int y, t_data *data)
{
    // Molette : zoom
    if (button == 4)  // Scroll up
        data->zoom += 2;
    if (button == 5)  // Scroll down
        data->zoom -= 2;
    
    render(data);
    return (0);
}

int close_window(t_data *data)
{
    mlx_destroy_image(data->mlx, data->img);
    mlx_destroy_window(data->mlx, data->win);
    exit(0);
    return (0);
}
```

## Main et boucle

```c
int main(int argc, char **argv)
{
    t_map   *map;
    t_data  *data;
    
    if (argc != 2)
    {
        ft_putendl_fd("Usage: ./fdf <map.fdf>", 2);
        return (1);
    }
    
    // Parser la carte
    map = parse_map(argv[1]);
    if (!map)
    {
        ft_putendl_fd("Error: Invalid map", 2);
        return (1);
    }
    
    // Initialiser MLX
    data = init_mlx(map);
    if (!data)
    {
        ft_putendl_fd("Error: MLX initialization failed", 2);
        return (1);
    }
    
    // Premier rendu
    render(data);
    
    // Hooks
    mlx_key_hook(data->win, key_hook, data);
    mlx_mouse_hook(data->win, mouse_hook, data);
    mlx_hook(data->win, 17, 0, close_window, data);
    
    // Boucle principale
    mlx_loop(data->mlx);
    
    return (0);
}
```

## Fonctionnalités bonus

<details>
<summary>Rotation 3D</summary>

<Accordion title="Rotation 3D">
    Rotation sur les 3 axes avec les touches du clavier
    
    ```c
    // Combiner les rotations
    point = rotate_x(point, data->angle_x);
    point = rotate_y(point, data->angle_y);
    point = rotate_z(point, data->angle_z);
    ```
</details>
  
  <details>
<summary>Projection parallèle</summary>

Ajouter d'autres types de projection
    
    ```c
    // Projection parallèle
    projected.x = point.x;
    projected.y = point.y;
    // z n'affecte pas la position, seulement la couleur
    ```
</details>
  
  <details>
<summary>Gradient de couleurs</summary>

Interpoler les couleurs entre les points
    
    ```c
    int get_gradient_color(t_point p1, t_point p2, int current, int total)
    {
        int r = ((p1.color >> 16) & 0xFF) * (total - current) / total +
                ((p2.color >> 16) & 0xFF) * current / total;
        int g = ((p1.color >> 8) & 0xFF) * (total - current) / total +
                ((p2.color >> 8) & 0xFF) * current / total;
        int b = (p1.color & 0xFF) * (total - current) / total +
                (p2.color & 0xFF) * current / total;
        
        return ((r << 16) | (g << 8) | b);
    }
    ```
</details>
  
  <details>
<summary>Menu d'aide</summary>

Afficher les contrôles à l'écran
    
    ```c
    mlx_string_put(data->mlx, data->win, 10, 10, 0xFFFFFF, "Controls:");
    mlx_string_put(data->mlx, data->win, 10, 30, 0xFFFFFF, "+/- : Zoom");
    mlx_string_put(data->mlx, data->win, 10, 50, 0xFFFFFF, "Arrows : Move");
    mlx_string_put(data->mlx, data->win, 10, 70, 0xFFFFFF, "W/S : Height");
    mlx_string_put(data->mlx, data->win, 10, 90, 0xFFFFFF, "ESC : Quit");
    ```
</details>


## Compilation

```makefile
NAME = fdf

CC = gcc
CFLAGS = -Wall -Wextra -Werror
MLXFLAGS = -lmlx -framework OpenGL -framework AppKit  # macOS
# MLXFLAGS = -lmlx -lXext -lX11 -lm  # Linux

SRCS = src/main.c \
       src/parsing.c \
       src/init.c \
       src/draw.c \
       src/projection.c \
       src/hooks.c \
       src/utils.c

OBJS = $(SRCS:.c=.o)

LIBFT = libft/libft.a

all: $(NAME)

$(NAME): $(OBJS) $(LIBFT)
	$(CC) $(CFLAGS) $(OBJS) $(LIBFT) $(MLXFLAGS) -o $(NAME)

$(LIBFT):
	make -C libft

clean:
	rm -f $(OBJS)
	make -C libft clean

fclean: clean
	rm -f $(NAME)
	make -C libft fclean

re: fclean all

.PHONY: all clean fclean re
```

## Tests

```bash
# Exécuter avec différentes cartes
./fdf maps/42.fdf
./fdf maps/pyramide.fdf
./fdf maps/julia.fdf

# Tester avec valgrind
valgrind --leak-check=full ./fdf maps/test.fdf
```

## Cartes de test

<div class="tabs-container">
<div class="tab-buttons">
  <div id="pyramide-simple" class="tab-content">
```
    0 0 0 0 0
    0 1 1 1 0
    0 1 2 1 0
    0 1 1 1 0
    0 0 0 0 0
    ```
</div>
  
  <div id="escaliers" class="tab-content">
```
    0 0 0 0 0 0 0
    0 1 1 1 1 1 0
    0 1 2 2 2 1 0
    0 1 2 3 2 1 0
    0 1 2 2 2 1 0
    0 1 1 1 1 1 0
    0 0 0 0 0 0 0
    ```
</div>
  
  <div id="avec-couleurs" class="tab-content">
```
    0,0xFF0000 0,0x00FF00 0,0x0000FF
    0,0xFFFF00 10,0xFFFFFF 0,0xFF00FF
    0,0x00FFFF 0,0xFF8800 0,0x8800FF
    ```
</div>
</div>
</div>

## Conseils

{: .tip }
> 
**Commencez petit** : Testez d'abord avec une carte 5x5 avant de passer aux grandes cartes.


{: .tip }
> 
**Dessinez sur papier** : Schématisez les transformations mathématiques pour mieux les comprendre.


{: .tip }
> 
**Optimisez tôt** : Utilisez une image en mémoire dès le début, pas `mlx_pixel_put`.


{: .warning }
> 
**Gestion mémoire** : N'oubliez pas de libérer toutes vos allocations à la fermeture.


## Erreurs fréquentes

<details>
<summary>Affichage trop lent</summary>

<Accordion title="Affichage trop lent">
    **Problème** : Utilisation de `mlx_pixel_put` directement
    
    **Solution** : Utiliser une image en mémoire (`mlx_new_image` et `mlx_get_data_addr`)
</details>
  
  <details>
<summary>Carte centrée incorrectement</summary>

**Problème** : Mauvais calcul de l'offset
    
    **Solution** : Calculer le centre en fonction de la taille de la carte
    ```c
    offset_x = (WIN_WIDTH - (map->width * zoom)) / 2;
    offset_y = (WIN_HEIGHT - (map->height * zoom)) / 2;
    ```
</details>
  
  <details>
<summary>Segfault lors du parsing</summary>

**Problème** : Mauvaise gestion des lignes de tailles différentes
    
    **Solution** : Vérifier que toutes les lignes ont le même nombre de valeurs
</details>
  
  <details>
<summary>Fuites mémoire</summary>

**Problème** : Matrices et split non libérés
    
    **Solution** : Free systématique après chaque allocation
</details>


## Ressources

<div class="card-container">
  <div class="project-card">
  <h3>MiniLibX Docs</h3>
  <p>Documentation complète de la MiniLibX</p>
  <a href="https://harm-smits.github.io/42docs/libs/minilibx" class="btn btn-primary">Voir plus</a>
</div>
  
  <div class="project-card">
  <h3>Bresenham Algorithm</h3>
  <p>Comprendre l'algorithme de Bresenham</p>
  <a href="https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm" class="btn btn-primary">Voir plus</a>
</div>
  
  <div class="project-card">
  <h3>Isometric Projection</h3>
  <p>Projection isométrique expliquée</p>
  <a href="https://en.wikipedia.org/wiki/Isometric_projection" class="btn btn-primary">Voir plus</a>
</div>
  
  <div class="project-card">
  <h3>3D Rotations</h3>
  <p>Matrices de rotation 3D</p>
  <a href="https://en.wikipedia.org/wiki/Rotation_matrix" class="btn btn-primary">Voir plus</a>
</div>
</div>

## Conclusion

FdF est un projet fascinant qui combine mathématiques, graphisme et optimisation. Vous apprendrez des concepts qui vous serviront pour tous les futurs projets graphiques !

{: .check }
> 
Une fois maîtrisé, vous aurez les bases pour aborder des projets plus complexes comme cub3D ou miniRT.


{: .note }
> 
Prenez le temps de comprendre les transformations mathématiques, c'est la clé pour réussir ce projet !
