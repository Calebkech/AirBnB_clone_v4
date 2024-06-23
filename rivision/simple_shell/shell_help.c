#include "shell.h"

/**
 * shell_help - display custom help in the standard output
 * Return: always 1 to continue the loop
 */
int shell_help(void)
{
    int i;
    char *builtin_str[] = {
        "cd",
        "help",
        "exit",
        NULL
    };

    shell_puts("This Simple Shell is for a Holberton School project\n");
    shell_puts("Type program names and arguments, and hit enter.\n");
    shell_puts("The following are built-ins:\n");
    for (i = 0; builtin_str[i]; i++)
    {
        shell_puts(builtin_str[i]);
        shell_putchar('\n');
    }
    shell_puts("Use the man command for information on other programs.\n");

    return (1);
}