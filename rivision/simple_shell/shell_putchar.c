#include "shell.h"

/**
 * shell_putchar - putchar custom function
 * @c: the characer to print
 * Return: print a char to the stdo
 */

int shell_putchar(char c)
{
	return (write(1, &c, 1));
}