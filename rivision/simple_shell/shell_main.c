#include "shell.h"

/**
 * main - entry point
 * Description: take environment variables and initiate the loop
 * @argc: number of arguments
 * @argv: aguments vector
 * @envp: environment variables
 * Return: always 0 when finish
 */
int main(int argc, char **argv, char **envp)
{
	char *line = NULL, **args = NULL;
	int status = 1, interactive = 0;
	/* dont need argc and argv */
	/* pointer to array of string with the directories. i.e. "usr/bin" */
	char **directories = NULL;

	/* set environement variables */
	directories = shell_set_env(envp);
	(void)argc;
	(void)argv;
	interactive = (isatty(STDIN_FILENO));
	/* loop until exit */
	while (status)
	{
		if (interactive == 1)
		{
			shell_puts("$ ");
		}
		else
		{
			status = 0;
		}
		/* Ctrl + C signal ignored*/
		/* SIGINT: program interrupt signal or Ctrl + c */
		/* SIG_IGN: signal to ignore */
		signal(SIGINT, shell_handle_ctrlc);
		line = shell_read_line();
		args = shell_tokenize(line);
		status = shell_execute(args, directories);
		if (line)
		free(line);
		if (interactive == 0)
			free(directories);
	}
	free(directories);
	return (0);
}