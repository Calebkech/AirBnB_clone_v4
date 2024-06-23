#include "shell.h"

/**
 * shell_read_line - Reads a line from the standard input
 * Return: Pointer to the line entered
 */
char *shell_read_line(void)
{
    char *input = NULL;
    size_t buffer_size = 0;

    if (getline(&input, &buffer_size, stdin) == -1)
    {
        free(input);
        if (feof(stdin))
        {
            exit(EXIT_SUCCESS);
        }
        else
        {
            perror("getline failure\n");
            exit(EXIT_FAILURE);
        }
    }
    return input;
}