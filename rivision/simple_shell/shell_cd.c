#include "shell.h"

/**
 * shell_getenv - get the value of an environment variable
 * @name: name of the environment variable
 * @envp: pointer to the environment variables
 * Return: char* with the matching path
 */

int shell_cd(char **args)
{
    int check;

    if (args[1] == NULL)
    {
        puts("Expected argument to cd");
        return 1;
    }

    check = chdir(args[1]);
    if (check != 0)
    {
        perror("Error:");
    }

    free(args); /* Perform the free operation here, after the last usage of args */

    return 1;
}