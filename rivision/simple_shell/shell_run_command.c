#include "shell.h"

/**
 * shell_run_command - execute the commands or try to execute args[0]
 * @args: arguments from input
 * @directories: string of paths
 * Return: always exit_success when done complete
 */
int shell_run_command(char **args, char **directories)
{
    int i = 0;
    char *eval_cmd = NULL;

    for (i = 1; directories[i] != NULL; i++)
    {
        eval_cmd = malloc(sizeof(char) * (strlen(directories[i]) + strlen(args[0]) + 2));
        shell_strcpy(eval_cmd, directories[i]);
        eval_cmd = shell_strcat(eval_cmd, "/");
        eval_cmd = shell_strcat(eval_cmd, args[0]);
        if (access(eval_cmd, X_OK) == 0)
        {
            if (execve(eval_cmd, args, NULL) == -1)
            {
                perror("execve error");
                exit(EXIT_FAILURE);
            }
        }
        free(eval_cmd);
    }
    if (directories[i] == NULL)
    {
        free(directories);
        if (access(args[0], X_OK) == 0)
        {
            if (execve(args[0], args, NULL) == -1)
            {
                perror("execve error");
                exit(EXIT_FAILURE);
            }
        }
    }
    exit(EXIT_SUCCESS);
}