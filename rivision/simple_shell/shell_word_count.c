#include "shell.h"

/**
 * shell_word_count - count the number of words in a string
 * @str: pointer to the string to count words
 * Return: the number of words in the string
 */

int shell_word_count(char *str)
{
    int count = 0;
    int is_word = 0;

    while (*str)
    {
        if (*str == ' ' || *str == '\n' || *str == '\t')
        {
            is_word = 0;
        }
        else if (is_word == 0)
        {
            is_word = 1;
            count++;
        }
        str++;
    }
    return count;
}