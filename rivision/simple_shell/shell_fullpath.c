#include "shell.h"

/**
 * shell_fullpath - Tokenize the path to extract directories
 * and allocate memory for the directories
 * @path: pointer to the path from getenv function
 * @envdelim: the delimiter to parse the path
 * Return: pointer to array of string with every single path
 */
char **shell_fullpath(char *path, char *envdelim)
{
    char *token = NULL;
    int count = shell_word_delim_count(path, ':');
    char **dirs = malloc(sizeof(char *) * (count + 2));
    int i = 0;

    if (!dirs)
    {
        perror("malloc error fullpath 1");
        exit(EXIT_FAILURE);
    }
    token = strtok(path, envdelim);
    while (token != NULL)
    {
        dirs[i] = token;
        token = strtok(NULL, envdelim);
        i++;
    }
    dirs[i] = NULL;
    return dirs;
}