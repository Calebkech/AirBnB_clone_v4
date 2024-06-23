#include "shell.h"

/**
 * shell_word_delim_count - count the words without the ':' separator, ascii 58
 * @str: pointer to the string to count words separeted with delim
 * @delim: delimiter for tokenize strings
 * Return: the number of words in string
 */

int shell_word_delim_count(char *str, char delim)
{
	int index = 0, word_count = 0;

	if (str)
	{
		for (; str[index] != '\0'; index++)
		{
			if (str[index] == delim)
				word_count++;
		}
		word_count++;
	}
	return (word_count);
}