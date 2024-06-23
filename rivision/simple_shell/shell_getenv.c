#include "shell.h"

/**
 * Custom implementation of getenv function
 * @param name: name of the environment variable
 * @param envp: pointer to the environment variables
 * @return: value of the environment variable or NULL if not found
 */
char *shell_getenv(const char *name, char **envp) {
    if (name == NULL || envp == NULL) {
        return NULL;
    }

    size_t name_len = strlen(name);

    for (int i = 0; envp[i] != NULL; i++) {
        if (strncmp(name, envp[i], name_len) == 0 && envp[i][name_len] == '=') {
            // Return the value part of the environment variable
            return envp[i] + name_len + 1;
        }
    }

    // If no match is found, return NULL
    return NULL;
}