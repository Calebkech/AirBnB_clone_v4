#include "shell.h"
#include <stdio.h>
#include <stdlib.h>

/**
 * shell_getline - Read a line of input from the user
 * Return: Pointer to the input line
 */
char *shell_getline(void)
{
    char *line = NULL;
    size_t bufsize = 0;
    ssize_t characters_read = getline(&line, &bufsize, stdin);
    if (characters_read == -1) {
        perror("getline failure\n");
        exit(EXIT_FAILURE);
    }
    return line;
}