---
layout: default
title: "Minitalk"
description: "Communication client-serveur avec signaux Unix"
icon: "satellite-dish"
---

# 📡 Minitalk

<img src="https://img.shields.io/badge/Score-125%2F100-success" alt="Score" />
<img src="https://img.shields.io/badge/Language-C-blue" alt="Language" />
<img src="https://img.shields.io/badge/Type-Unix%20Signals-green" alt="Type" />

## Introduction

**Minitalk** est un projet qui implémente un système de communication entre un client et un serveur en utilisant uniquement les signaux Unix SIGUSR1 et SIGUSR2.

<div class="project-card">
  <h3>Voir sur GitHub</h3>
  <p>Accéder au repository GitHub</p>
  <a href="https://github.com/NikoStano/minitalk" class="btn btn-primary">Voir plus</a>
</div>

{: .note }
> 
Ce projet vous apprend les bases de la communication inter-processus (IPC) et la manipulation des signaux Unix.


## Objectifs pédagogiques

<div class="steps-container">
  <div class="step">
  <h4>Signaux Unix</h4>
  <p>Comprendre et utiliser les signaux SIGUSR1 et SIGUSR2</p>
</div>
  
  <div class="step">
  <h4>Communication bit par bit</h4>
  <p>Transmettre des données en envoyant des bits individuellement</p>
</div>
  
  <div class="step">
  <h4>Gestion asynchrone</h4>
  <p>Gérer la réception de signaux de manière asynchrone</p>
</div>
  
  <div class="step">
  <h4>Encodage/Décodage</h4>
  <p>Convertir des caractères en bits et vice versa</p>
</div>
</div>

## Fonctionnement

### Principe de base

```
CLIENT                          SERVEUR
  |                                |
  |  -- SIGUSR1 (bit 0) -->        |
  |  -- SIGUSR2 (bit 1) -->        |
  |  -- SIGUSR1 (bit 0) -->        |
  |  ...  (8 bits = 1 char)        |
  |                                |
  |  <-- ACK (SIGUSR1) --          |
```

### Les signaux Unix

<details>
<summary>SIGUSR1</summary>

<Accordion title="SIGUSR1">
    Signal utilisateur 1
    - Dans minitalk : représente le bit **0**
    - Peut être envoyé avec `kill(pid, SIGUSR1)`
</details>
  
  <details>
<summary>SIGUSR2</summary>

Signal utilisateur 2
    - Dans minitalk : représente le bit **1**
    - Peut être envoyé avec `kill(pid, SIGUSR2)`
</details>


### Encodage d'un caractère

Un caractère est encodé sur 8 bits :

```
Caractère 'A' = 65 en décimal = 01000001 en binaire

Transmission :
bit 7 (LSB) : 1 → SIGUSR2
bit 6       : 0 → SIGUSR1
bit 5       : 0 → SIGUSR1
bit 4       : 0 → SIGUSR1
bit 3       : 0 → SIGUSR1
bit 2       : 0 → SIGUSR1
bit 1       : 1 → SIGUSR2
bit 0 (MSB) : 0 → SIGUSR1
```

## Architecture du projet

```
minitalk/
├── src/
│   ├── server.c          # Serveur
│   ├── client.c          # Client
│   └── utils.c           # Fonctions utilitaires
├── bonus/
│   ├── server_bonus.c    # Serveur avec bonus
│   └── client_bonus.c    # Client avec bonus
├── includes/
│   └── minitalk.h
├── libft/
└── Makefile
```

## Structures de données

```c
// Header minitalk.h
#ifndef MINITALK_H
# define MINITALK_H

# include <signal.h>
# include <unistd.h>
# include <stdlib.h>
# include "libft.h"

// Structure pour le serveur
typedef struct s_server
{
    int     bit_count;
    char    current_char;
}   t_server;

// Structure pour le client (bonus)
typedef struct s_client
{
    int     ack_received;
}   t_client;

// Fonctions
void    send_char(int pid, char c);
void    handle_signal_server(int sig, siginfo_t *info, void *context);
void    handle_signal_client(int sig);

#endif
```

## Implémentation du serveur

### Main du serveur

```c
#include "minitalk.h"

t_server g_server;

int main(void)
{
    struct sigaction sa;
    
    // Initialiser la structure globale
    g_server.bit_count = 0;
    g_server.current_char = 0;
    
    // Afficher le PID
    ft_putstr_fd("Server PID: ", 1);
    ft_putnbr_fd(getpid(), 1);
    ft_putchar_fd('\n', 1);
    
    // Configurer sigaction
    sa.sa_sigaction = handle_signal_server;
    sa.sa_flags = SA_SIGINFO;  // Pour recevoir info sur l'émetteur
    sigemptyset(&sa.sa_mask);
    
    // Enregistrer les handlers
    sigaction(SIGUSR1, &sa, NULL);
    sigaction(SIGUSR2, &sa, NULL);
    
    // Boucle infinie
    while (1)
        pause();  // Attend un signal
    
    return (0);
}
```

### Handler de signaux

```c
void handle_signal_server(int sig, siginfo_t *info, void *context)
{
    (void)context;
    
    // Décaler le caractère actuel d'un bit vers la gauche
    g_server.current_char <<= 1;
    
    // Si SIGUSR2, mettre le bit à 1
    if (sig == SIGUSR2)
        g_server.current_char |= 1;
    
    // Incrémenter le compteur de bits
    g_server.bit_count++;
    
    // Si on a reçu 8 bits (un caractère complet)
    if (g_server.bit_count == 8)
    {
        // Afficher le caractère
        ft_putchar_fd(g_server.current_char, 1);
        
        // Si c'est '\0', fin du message
        if (g_server.current_char == '\0')
            ft_putchar_fd('\n', 1);
        
        // Réinitialiser
        g_server.bit_count = 0;
        g_server.current_char = 0;
    }
    
    // Bonus : envoyer un ACK au client
    kill(info->si_pid, SIGUSR1);
}
```

## Implémentation du client

### Main du client

```c
#include "minitalk.h"

int main(int argc, char **argv)
{
    int     server_pid;
    char    *message;
    int     i;
    
    if (argc != 3)
    {
        ft_putendl_fd("Usage: ./client [server_pid] [message]", 2);
        return (1);
    }
    
    // Récupérer le PID du serveur
    server_pid = ft_atoi(argv[1]);
    message = argv[2];
    
    // Vérifier le PID
    if (server_pid <= 0)
    {
        ft_putendl_fd("Error: Invalid PID", 2);
        return (1);
    }
    
    // Envoyer chaque caractère
    i = 0;
    while (message[i])
    {
        send_char(server_pid, message[i]);
        i++;
    }
    
    // Envoyer le caractère null de fin
    send_char(server_pid, '\0');
    
    return (0);
}
```

### Envoi d'un caractère

```c
void send_char(int pid, char c)
{
    int bit;
    int i;
    
    i = 7;  // Commencer par le bit de poids fort
    while (i >= 0)
    {
        // Extraire le bit i
        bit = (c >> i) & 1;
        
        // Envoyer le signal correspondant
        if (bit == 0)
            kill(pid, SIGUSR1);
        else
            kill(pid, SIGUSR2);
        
        // Petite pause pour éviter la perte de signaux
        usleep(100);  // 100 microsecondes
        
        i--;
    }
}
```

## Version bonus

### Ajout d'un ACK (acknowledgement)

Le client attend une confirmation du serveur après chaque bit :

```c
// Variable globale pour le client
t_client g_client;

int main(int argc, char **argv)
{
    struct sigaction sa;
    int     server_pid;
    char    *message;
    int     i;
    
    if (argc != 3)
    {
        ft_putendl_fd("Usage: ./client [server_pid] [message]", 2);
        return (1);
    }
    
    // Configurer le handler pour recevoir les ACK
    sa.sa_handler = handle_signal_client;
    sa.sa_flags = 0;
    sigemptyset(&sa.sa_mask);
    sigaction(SIGUSR1, &sa, NULL);
    
    server_pid = ft_atoi(argv[1]);
    message = argv[2];
    
    // Envoyer le message
    i = 0;
    while (message[i])
    {
        send_char_with_ack(server_pid, message[i]);
        i++;
    }
    send_char_with_ack(server_pid, '\0');
    
    ft_putendl_fd("Message sent successfully!", 1);
    
    return (0);
}

void handle_signal_client(int sig)
{
    (void)sig;
    g_client.ack_received = 1;
}

void send_char_with_ack(int pid, char c)
{
    int bit;
    int i;
    
    i = 7;
    while (i >= 0)
    {
        bit = (c >> i) & 1;
        
        g_client.ack_received = 0;
        
        if (bit == 0)
            kill(pid, SIGUSR1);
        else
            kill(pid, SIGUSR2);
        
        // Attendre l'ACK
        while (!g_client.ack_received)
            usleep(10);
        
        i--;
    }
}
```

### Support Unicode (bonus)

Pour envoyer des caractères Unicode, utiliser `wchar_t` :

```c
#include <wchar.h>
#include <locale.h>

void send_wchar(int pid, wchar_t wc)
{
    int bit;
    int i;
    
    // Un wchar_t fait 32 bits
    i = 31;
    while (i >= 0)
    {
        bit = (wc >> i) & 1;
        
        if (bit == 0)
            kill(pid, SIGUSR1);
        else
            kill(pid, SIGUSR2);
        
        usleep(100);
        i--;
    }
}

// Dans le serveur
void handle_signal_unicode(int sig, siginfo_t *info, void *context)
{
    static wchar_t  current_wchar = 0;
    static int      bit_count = 0;
    
    (void)context;
    
    current_wchar <<= 1;
    
    if (sig == SIGUSR2)
        current_wchar |= 1;
    
    bit_count++;
    
    if (bit_count == 32)  // 32 bits pour un wchar_t
    {
        ft_putwchar_fd(current_wchar, 1);
        
        if (current_wchar == L'\0')
            ft_putchar_fd('\n', 1);
        
        bit_count = 0;
        current_wchar = 0;
    }
    
    kill(info->si_pid, SIGUSR1);
}
```

## Compilation

```makefile
NAME = minitalk
SERVER = server
CLIENT = client
BONUS_SERVER = server_bonus
BONUS_CLIENT = client_bonus

CC = gcc
CFLAGS = -Wall -Wextra -Werror

SRCS_SERVER = src/server.c src/utils.c
SRCS_CLIENT = src/client.c src/utils.c
SRCS_BONUS_SERVER = bonus/server_bonus.c src/utils.c
SRCS_BONUS_CLIENT = bonus/client_bonus.c src/utils.c

OBJS_SERVER = $(SRCS_SERVER:.c=.o)
OBJS_CLIENT = $(SRCS_CLIENT:.c=.o)
OBJS_BONUS_SERVER = $(SRCS_BONUS_SERVER:.c=.o)
OBJS_BONUS_CLIENT = $(SRCS_BONUS_CLIENT:.c=.o)

LIBFT = libft/libft.a

all: $(SERVER) $(CLIENT)

$(SERVER): $(OBJS_SERVER) $(LIBFT)
	$(CC) $(CFLAGS) $(OBJS_SERVER) $(LIBFT) -o $(SERVER)

$(CLIENT): $(OBJS_CLIENT) $(LIBFT)
	$(CC) $(CFLAGS) $(OBJS_CLIENT) $(LIBFT) -o $(CLIENT)

$(BONUS_SERVER): $(OBJS_BONUS_SERVER) $(LIBFT)
	$(CC) $(CFLAGS) $(OBJS_BONUS_SERVER) $(LIBFT) -o $(BONUS_SERVER)

$(BONUS_CLIENT): $(OBJS_BONUS_CLIENT) $(LIBFT)
	$(CC) $(CFLAGS) $(OBJS_BONUS_CLIENT) $(LIBFT) -o $(BONUS_CLIENT)

$(LIBFT):
	make -C libft

bonus: $(BONUS_SERVER) $(BONUS_CLIENT)

clean:
	rm -f $(OBJS_SERVER) $(OBJS_CLIENT) $(OBJS_BONUS_SERVER) $(OBJS_BONUS_CLIENT)
	make -C libft clean

fclean: clean
	rm -f $(SERVER) $(CLIENT) $(BONUS_SERVER) $(BONUS_CLIENT)
	make -C libft fclean

re: fclean all

.PHONY: all bonus clean fclean re
```

## Utilisation

```bash
# Terminal 1 : Lancer le serveur
./server
# Output: Server PID: 12345

# Terminal 2 : Envoyer un message
./client 12345 "Hello 42!"
# Le serveur affiche: Hello 42!

# Envoyer un long message
./client 12345 "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

# Envoyer des caractères spéciaux
./client 12345 "Bonjour! 你好 🚀"  # (avec bonus Unicode)
```

## Tests

### Test basique

```bash
# Test simple
./server &
SERVER_PID=$!
./client $SERVER_PID "Test"
kill $SERVER_PID
```

### Test de performance

```bash
#!/bin/bash

# test_performance.sh

./server &
SERVER_PID=$!
sleep 1

# Tester avec différentes tailles
echo "Testing with short message..."
time ./client $SERVER_PID "Hello"

echo "Testing with medium message..."
time ./client $SERVER_PID "Lorem ipsum dolor sit amet"

echo "Testing with long message..."
LONG_MSG=$(python3 -c "print('A' * 1000)")
time ./client $SERVER_PID "$LONG_MSG"

kill $SERVER_PID
```

### Test de robustesse

```bash
#!/bin/bash

# test_stress.sh

./server &
SERVER_PID=$!
sleep 1

# Envoyer plusieurs messages rapidement
for i in {1..10}; do
    ./client $SERVER_PID "Message $i" &
done

wait

kill $SERVER_PID
```

## Fonctions autorisées

<details>
<summary>Liste des fonctions autorisées</summary>

- `write`
  - `ft_printf` (ou équivalent)
  - `signal` ou `sigaction`
  - `sigemptyset`
  - `sigaddset`
  - `kill`
  - `getpid`
  - `malloc`
  - `free`
  - `pause`
  - `sleep`
  - `usleep`
  - `exit`
</details>

## Concepts clés

### Signaux Unix

<details>
<summary>signal() vs sigaction()</summary>

<Accordion title="signal() vs sigaction()">
    **signal()** : Simple mais comportement non défini
    ```c
    signal(SIGUSR1, handler);  // À éviter
    ```
    
    **sigaction()** : Recommandé, comportement défini
    ```c
    struct sigaction sa;
    sa.sa_handler = handler;
    sa.sa_flags = 0;
    sigemptyset(&sa.sa_mask);
    sigaction(SIGUSR1, &sa, NULL);
    ```
</details>
  
  <details>
<summary>SA_SIGINFO</summary>

Flag permettant de recevoir des informations sur l'émetteur
    
    ```c
    struct sigaction sa;
    sa.sa_sigaction = handler_with_info;  // Pas sa_handler !
    sa.sa_flags = SA_SIGINFO;
    sigaction(SIGUSR1, &sa, NULL);
    
    void handler_with_info(int sig, siginfo_t *info, void *context)
    {
        pid_t sender_pid = info->si_pid;  // PID de l'émetteur
        // ...
    }
    ```
</details>
  
  <details>
<summary>pause() vs sleep()</summary>

**pause()** : Attend un signal (recommandé pour le serveur)
    ```c
    while (1)
        pause();  // CPU idle
    ```
    
    **usleep()** : Attente active (pour le client)
    ```c
    usleep(100);  // 100 microsecondes
    ```
</details>


### Manipulation de bits

```c
// Extraire le bit i d'un nombre
int get_bit(char c, int i)
{
    return ((c >> i) & 1);
}

// Mettre le bit i à 1
char set_bit(char c, int i)
{
    return (c | (1 << i));
}

// Mettre le bit i à 0
char clear_bit(char c, int i)
{
    return (c & ~(1 << i));
}

// Inverser le bit i
char toggle_bit(char c, int i)
{
    return (c ^ (1 << i));
}

// Décalage à gauche
char shift_left(char c)
{
    return (c << 1);
}

// Décalage à droite
char shift_right(char c)
{
    return (c >> 1);
}
```

### Exemple de conversion bit par bit

```c
// Convertir un caractère en binaire (affichage)
void print_bits(unsigned char c)
{
    int i;
    
    i = 7;
    while (i >= 0)
    {
        if ((c >> i) & 1)
            ft_putchar_fd('1', 1);
        else
            ft_putchar_fd('0', 1);
        i--;
    }
    ft_putchar_fd('\n', 1);
}

// Exemple d'utilisation
int main(void)
{
    print_bits('A');  // Output: 01000001
    print_bits('B');  // Output: 01000010
    print_bits('*');  // Output: 00101010
    return (0);
}
```

## Erreurs fréquentes

<details>
<summary>Signaux perdus</summary>

<Accordion title="Signaux perdus">
    **Problème** : Le serveur ne reçoit pas tous les signaux si envoyés trop rapidement
    
    **Solution** : Ajouter un délai entre chaque signal
    ```c
    kill(pid, SIGUSR1);
    usleep(100);  // Attendre 100 microsecondes
    ```
    
    Ou utiliser un système d'ACK (bonus)
</details>
  
  <details>
<summary>Ordre des bits inversé</summary>

**Problème** : Le message s'affiche mal
    
    **Solution** : Vérifier l'ordre d'envoi (MSB ou LSB first)
    ```c
    // Envoyer du bit de poids fort au bit de poids faible
    i = 7;  // Commencer à 7
    while (i >= 0)
    {
        send_bit((c >> i) & 1);
        i--;
    }
    ```
</details>
  
  <details>
<summary>Variables globales non réinitialisées</summary>

**Problème** : Le serveur ne traite qu'un seul message
    
    **Solution** : Réinitialiser après chaque caractère
    ```c
    if (bit_count == 8)
    {
        ft_putchar_fd(current_char, 1);
        bit_count = 0;        // Réinitialiser
        current_char = 0;     // Réinitialiser
    }
    ```
</details>
  
  <details>
<summary>PID invalide</summary>

**Problème** : Le client crash ou ne trouve pas le serveur
    
    **Solution** : Valider le PID
    ```c
    pid = ft_atoi(argv[1]);
    if (pid <= 0 || kill(pid, 0) == -1)
    {
        ft_putendl_fd("Error: Invalid PID", 2);
        return (1);
    }
    ```
</details>
  
  <details>
<summary>Pas de gestion du '\0'</summary>

**Problème** : Le serveur ne sait pas quand le message se termine
    
    **Solution** : Toujours envoyer le '\0' à la fin
    ```c
    // Dans le client
    while (message[i])
    {
        send_char(pid, message[i]);
        i++;
    }
    send_char(pid, '\0');  // Important !
    ```
</details>


## Optimisations

### Réduire le délai

```c
// Au lieu de usleep(100) constant
void send_char_optimized(int pid, char c)
{
    int bit;
    int i;
    
    i = 7;
    while (i >= 0)
    {
        bit = (c >> i) & 1;
        
        if (bit == 0)
            kill(pid, SIGUSR1);
        else
            kill(pid, SIGUSR2);
        
        // Délai adaptatif
        usleep(50);  // Plus rapide !
        
        i--;
    }
}
```

### Envoyer plusieurs bits par signal (avancé)

```c
// Utiliser plus de 2 signaux (non standard)
// Attention : dépasse les requirements du sujet
#define SIGNAL_BASE SIGRTMIN

void send_multi_bit(int pid, int value)
{
    kill(pid, SIGNAL_BASE + value);  // value entre 0 et 31
}
```

## Améliorations bonus avancées

### 1. Compression simple

```c
// Compresser les séquences répétitives
void send_compressed(int pid, char *msg)
{
    int i;
    int count;
    char current;
    
    i = 0;
    while (msg[i])
    {
        current = msg[i];
        count = 1;
        
        // Compter les répétitions
        while (msg[i + 1] == current && count < 255)
        {
            count++;
            i++;
        }
        
        // Si répété, envoyer count puis char
        if (count > 3)
        {
            send_char(pid, 0xFF);  // Marqueur de compression
            send_char(pid, count);
            send_char(pid, current);
        }
        else
        {
            // Sinon envoyer normalement
            while (count--)
                send_char(pid, current);
        }
        i++;
    }
    send_char(pid, '\0');
}
```

### 2. Checksum pour vérifier l'intégrité

```c
// Calculer un checksum simple
unsigned char calculate_checksum(char *msg)
{
    unsigned char sum;
    int i;
    
    sum = 0;
    i = 0;
    while (msg[i])
    {
        sum += msg[i];
        i++;
    }
    return (sum);
}

// Client envoie le message puis le checksum
void send_with_checksum(int pid, char *msg)
{
    unsigned char checksum;
    int i;
    
    i = 0;
    while (msg[i])
    {
        send_char(pid, msg[i]);
        i++;
    }
    send_char(pid, '\0');
    
    // Envoyer le checksum
    checksum = calculate_checksum(msg);
    send_char(pid, checksum);
}
```

### 3. Affichage de progression

```c
// Client affiche une barre de progression
void send_with_progress(int pid, char *msg)
{
    int total;
    int sent;
    int percent;
    int i;
    
    total = ft_strlen(msg);
    sent = 0;
    
    ft_putstr_fd("Sending: [", 1);
    
    i = 0;
    while (msg[i])
    {
        send_char(pid, msg[i]);
        sent++;
        
        // Calculer le pourcentage
        percent = (sent * 100) / total;
        
        // Afficher la progression
        ft_putstr_fd("\rSending: [", 1);
        display_progress_bar(percent);
        ft_putstr_fd("] ", 1);
        ft_putnbr_fd(percent, 1);
        ft_putstr_fd("%", 1);
        
        i++;
    }
    send_char(pid, '\0');
    ft_putendl_fd("\nDone!", 1);
}

void display_progress_bar(int percent)
{
    int i;
    int filled;
    
    filled = percent / 2;  // Barre de 50 caractères
    i = 0;
    while (i < 50)
    {
        if (i < filled)
            ft_putchar_fd('=', 1);
        else
            ft_putchar_fd(' ', 1);
        i++;
    }
}
```

## Debugging

### Afficher les signaux reçus

```c
void handle_signal_debug(int sig, siginfo_t *info, void *context)
{
    static int bit_count = 0;
    static char current_char = 0;
    
    (void)context;
    
    // Afficher le signal reçu
    if (sig == SIGUSR1)
        ft_putstr_fd("0", 1);
    else
        ft_putstr_fd("1", 1);
    
    current_char <<= 1;
    if (sig == SIGUSR2)
        current_char |= 1;
    
    bit_count++;
    
    if (bit_count == 8)
    {
        ft_putstr_fd(" = '", 1);
        ft_putchar_fd(current_char, 1);
        ft_putendl_fd("'", 1);
        
        bit_count = 0;
        current_char = 0;
    }
    
    kill(info->si_pid, SIGUSR1);
}
```

### Tester la latence

```c
#include <sys/time.h>

double get_time_ms(void)
{
    struct timeval tv;
    
    gettimeofday(&tv, NULL);
    return (tv.tv_sec * 1000.0 + tv.tv_usec / 1000.0);
}

void send_with_timing(int pid, char *msg)
{
    double start;
    double end;
    int len;
    
    start = get_time_ms();
    
    // Envoyer le message
    len = 0;
    while (msg[len])
    {
        send_char(pid, msg[len]);
        len++;
    }
    send_char(pid, '\0');
    
    end = get_time_ms();
    
    ft_putstr_fd("Sent ", 1);
    ft_putnbr_fd(len, 1);
    ft_putstr_fd(" chars in ", 1);
    ft_putnbr_fd((int)(end - start), 1);
    ft_putendl_fd(" ms", 1);
}
```

## Cas de test

<div class="tabs-container">
<div class="tab-buttons">
  <div id="messages-simples" class="tab-content">
```bash
    ./client $PID "Hello"
    ./client $PID "42"
    ./client $PID "A"
    ./client $PID ""  # Message vide
    ```
</div>
  
  <div id="caractères-spéciaux" class="tab-content">
```bash
    ./client $PID "Hello\nWorld"
    ./client $PID "Tab\there"
    ./client $PID "Quote: \"test\""
    ./client $PID "Backslash: \\"
    ```
</div>
  
  <div id="messages-longs" class="tab-content">
```bash
    # Générer un message de 1000 caractères
    MSG=$(python3 -c "print('A' * 1000)")
    ./client $PID "$MSG"
    
    # Message de 10000 caractères
    MSG=$(python3 -c "print('X' * 10000)")
    ./client $PID "$MSG"
    ```
</div>
  
  <div id="unicode-(bonus)" class="tab-content">
```bash
    ./client $PID "Émojis: 🚀 🎉 ❤️"
    ./client $PID "中文测试"
    ./client $PID "Français: café, crème"
    ./client $PID "Math: π ≈ 3.14"
    ```
</div>
  
  <div id="test-de-stress" class="tab-content">
```bash
    # Envoyer plusieurs messages en parallèle
    for i in {1..10}; do
        ./client $PID "Message $i" &
    done
    wait
    ```
</div>
</div>
</div>

## Conseils

{: .tip }
> 
**Commencez simple** : Faites d'abord fonctionner la version basique avant d'ajouter les bonus.


{: .tip }
> 
**Testez bit par bit** : Utilisez `print_bits()` pour vérifier que les bits sont corrects.


{: .tip }
> 
**Augmentez progressivement** : Testez d'abord avec un seul caractère, puis un mot, puis des phrases.


{: .warning }
> 
**Attention aux variables globales** : Utilisez-les avec précaution, réinitialisez-les correctement.


{: .warning }
> 
**usleep() minimal** : Ne descendez pas en dessous de 50 microsecondes, sinon risque de perte de signaux.


## Ressources

<div class="card-container">
  <div class="project-card">
  <h3>man signal</h3>
  <p>```bash
    man 2 signal
    man 2 sigaction
    man 2 kill
    ```
    Documentation des signaux Unix</p>
</div>
  
  <div class="project-card">
  <h3>Signaux Unix</h3>
  <p>Guide complet sur les signaux</p>
  <a href="https://www.gnu.org/software/libc/manual/html_node/Signal-Handling.html" class="btn btn-primary">Voir plus</a>
</div>
  
  <div class="project-card">
  <h3>Bit Manipulation</h3>
  <p>Opérateurs de manipulation de bits</p>
  <a href="https://www.tutorialspoint.com/cprogramming/c_bitwise_operators.htm" class="btn btn-primary">Voir plus</a>
</div>
  
  <div class="project-card">
  <h3>IPC</h3>
  <p>Communication inter-processus</p>
  <a href="https://www.geeksforgeeks.org/inter-process-communication-ipc/" class="btn btn-primary">Voir plus</a>
</div>
</div>

## Schéma de fonctionnement

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT                               │
│                                                              │
│  Message: "Hi"                                              │
│                                                              │
│  'H' = 72 = 01001000                                        │
│                                                              │
│  Envoi bit par bit:                                         │
│  0 → SIGUSR1 ──────────────────────────┐                   │
│  1 → SIGUSR2 ──────────────────────────┼───────┐           │
│  0 → SIGUSR1 ──────────────────────────┼───────┼──┐        │
│  0 → SIGUSR1 ──────────────────────────┼───────┼──┼──┐     │
│  1 → SIGUSR2 ──────────────────────────┼───────┼──┼──┼──┐  │
│  0 → SIGUSR1 ──────────────────────────┼───────┼──┼──┼──┼─┐│
│  0 → SIGUSR1 ──────────────────────────┼───────┼──┼──┼──┼─││
│  0 → SIGUSR1 ──────────────────────────┼───────┼──┼──┼──┼─││
│                                         │       │  │  │  │ ││
└─────────────────────────────────────────┼───────┼──┼──┼──┼─││
                                          ↓       ↓  ↓  ↓  ↓ ↓↓
┌─────────────────────────────────────────────────────────────┐
│                         SERVEUR                              │
│                                                              │
│  Réception:                                                 │
│  bit_count = 0, char = 00000000                            │
│                                                              │
│  SIGUSR1 → char = 00000000 (bit 0)                         │
│  SIGUSR2 → char = 00000001 (bit 1)                         │
│  SIGUSR1 → char = 00000010 (bit 0)                         │
│  SIGUSR1 → char = 00000100 (bit 0)                         │
│  SIGUSR2 → char = 00001001 (bit 1)                         │
│  SIGUSR1 → char = 00010010 (bit 0)                         │
│  SIGUSR1 → char = 00100100 (bit 0)                         │
│  SIGUSR1 → char = 01001000 (bit 0)                         │
│                                                              │
│  bit_count = 8 → Afficher: 'H' (72)                        │
│  Réinitialiser: bit_count = 0, char = 0                    │
│                                                              │
│  ... Répéter pour 'i' ...                                   │
│  ... Répéter pour '\0' ...                                  │
│                                                              │
│  Output final: "Hi"                                         │
└─────────────────────────────────────────────────────────────┘
```

## Conclusion

Minitalk est un excellent projet pour comprendre :
- La communication inter-processus
- Les signaux Unix
- La manipulation de bits
- La programmation asynchrone

{: .check }
> 
Une fois maîtrisé, vous aurez acquis des bases solides en communication système qui vous serviront pour les projets futurs !


{: .note }
> 
Les concepts appris ici (signaux, IPC, manipulation de bits) sont fondamentaux en programmation système et vous serviront tout au long de votre carrière.


{: .tip }
> 
**Conseil final** : Prenez le temps de bien comprendre comment les signaux fonctionnent avant de coder. Un bon schéma vaut mieux que 1000 lignes de code !
