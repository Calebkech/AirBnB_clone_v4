#include "shell.h"

/**
 * shell_handle_ctrlc - ignore Ctrl-C input and print prompt again
 * @n: takes in int from signal
 */
void shell_handle_ctrlc(int n)
{
    (void)n;
    write(STDOUT_FILENO, "\n$ ", 3);
}