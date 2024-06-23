#include "shell.h"
#define TOK_DELIM " \t\r\n\a"

/**
 * shell_tokenize - break a string into separated tokens using a set of delimiters
 * @line: line from standard input returned from shell_read_line function
 * Return: array of tokens (strings)
 */
char **shell_tokenize(char *line)
{
    int bufsize = shell_word_delim_count(line, ' '), i = 0;
    char **tokens = NULL;
    char *token = NULL;
    tokens = malloc(sizeof(char *) * (bufsize + 1));
    if (!tokens)
    {
        free(tokens);
        perror("allocation error");
        exit(EXIT_FAILURE);
    }
    token = strtok(line, TOK_DELIM);
    while (token != NULL)
    {
        tokens[i] = token;
        i++;
        token = strtok(NULL, TOK_DELIM);
    }
    tokens[i] = NULL;
    return (tokens);
}