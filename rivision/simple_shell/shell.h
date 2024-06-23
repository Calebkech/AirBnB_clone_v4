#ifndef SHELL_H
#define SHELL_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <signal.h>
#include <sys/wait.h>
#include <netinet/in.h>

/*delimiter */
#define ENVDELIM ":="

/* lifetime cicle */
char *shell_read_line(void);
char **shell_tokenize(char *line);
char **shell_set_env(char **envp);
char *shell_getenv(const char *name, char **envp);
char **shell_fullpath(char *path, char *envdelim);
int shell_execute(char **args, char **directories);
int shell_run_command(char **args, char **directories);

/* child processes */
int shell_launch_child(char **args, char **directories);
int shell_run_command(char **args, char **directories);

/* BUILT-INS */
int shell_cd(char **args);
int shell_help(void);
int shell_exit(void);

/* string functions */
char *shell_strcat(char *str1, char *str2);
int shell_puts(char *string);
int shell_putchar(char c);
int shell_word_count(char *str);
int shell_strlen(char *str);
int shell_strcmp(char *str1, char *str2);
char *shell_strcpy(char *dest, char *src);
int shell_word_delim_count(char *string, char delim);

/* custom functions */
char *shell_read_line(void);
char *shell_getline(void);

/* helper functions */
void shell_handle_ctrlc(int n);

#endif