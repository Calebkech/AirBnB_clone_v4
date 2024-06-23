#include "shell.h"

int shell_execute(char **arguments, char **directory_list)
{
    int i = 0, check = 1;
    char *builtin_commands[] = {"cd", "help", "exit", NULL};

    if (arguments[0] == NULL)
    {
        return (1);
    }
    for (i = 0; builtin_commands[i]; i++)
    {
        if (shell_strcmp(builtin_commands[i], arguments[0]) == 0)
            break;
    }
    switch (i)
    {
        case 0:
            check = shell_cd(arguments);
            break;
        case 1:
            check = shell_help();
            break;
        case 2:
            check = shell_exit();
            break;
        default:
            check = shell_launch_child(arguments, directory_list);
            break;
    }
    return (check);
}