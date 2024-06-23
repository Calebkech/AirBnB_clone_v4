#include "shell.h"

/**
 * shell_set_env - get the environment variables
 *
 * @envp: pointer to the environment variables
 * Return: pointer to array of paths
 */
char **shell_set_env(char **envp)
{
    char *path = shell_getenv("PATH", envp);
    char **path_parsed = shell_fullpath(path, ENVDELIM);

    return path_parsed;
}