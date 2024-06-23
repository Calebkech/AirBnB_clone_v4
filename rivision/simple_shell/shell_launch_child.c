#include "shell.h"

/**
 * shell_launch_child - fork process and launch command execution
 * @args: pointer to strings of arguments
 * @directories: string of path
 * Return: always 1 to continue the loop
 */
int shell_launch_child(char **args, char **directories)
{
    pid_t pid;
    int status;
    pid = fork();
    if (pid == 0)
    {
        shell_run_command(args, directories);
    }
    if (args)
        free(args);
    if (pid < 0)
    {
        perror("Error:");
    }
    else
    {
        wait(&status);
    }
    return (1);
}