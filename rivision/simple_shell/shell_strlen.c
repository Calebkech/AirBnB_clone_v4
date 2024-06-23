#include "shell.h"

/**
 * shell_strlen - custom function to get the length of a string
 * @str: pointer to the string to be measured
 * Return: the length of a string
 */

int shell_strlen(char *str)
{
	int len = 0;

	while (*(str + len))
	{
		len++;
	}
	return (len);
}