#include "shell.h"
/**
 * shell_strcat - concatenate two strings (dest + src)
 * @str1: the string to concatenate src
 * @str2: initial string
 * Return: the final and concatenated string
 */
char *shell_strcat(char *str1, char *str2)
{
	unsigned int length1 = 0, length2 = 0, index = 0;
	char *result_str = NULL;

	if (str1)
		length1 = shell_strlen(str1);
	if (str2)
		length2 = shell_strlen(str2);

	result_str = malloc(sizeof(char) * (length1 + length2 + 1));

	for (index = 0; index < length1; index++)
		result_str[index] = str1[index];
	for (; index < length1 + length2; index++)
		result_str[index] = str2[index - length1];

	result_str[index] = '\0'; /* add null terminator */
	return (result_str);
}