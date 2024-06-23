#include "shell.h"

/**
 * shell_strcpy - copy the string
 * Description: the string pointed to a buffer
 * @destination: the buffer in where copy the string
 * @source: the string to be copied
 * Return: destination
 */

char *shell_strcpy(char *destination, char *source)
{
	int length = 0, index = 0;

	while (source[length] != '\0')
	{
		length++;
	}
	for (index = 0; index <= length; index++)
	{
		destination[index] = source[index];
	}
	return (destination);
}