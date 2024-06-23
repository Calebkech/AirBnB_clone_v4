#include "shell.h"
/**
 * shell_strcmp - compares string 1 with string 2
 * Description: compares two strings
 * Return: 0 if equal or not 0 if are different
 * @str1: first string
 * @str2: second string
 */

int shell_strcmp(char *str1, char *str2)
{
	while (*str1 != '\0')
	{
		if (*str1 != *str2)
		{
			return (*str1 - *str2);
		}
		str1++;
		str2++;
	}
	return (0);
}