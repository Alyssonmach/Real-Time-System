#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <spawn.h>

// Variavel global de ambiente para spawn()
extern char **environ;

/**
 * @brief Cria um processo filho que é cópia do processo pai.
 */
void test_fork() {
	pid_t pid = fork();
	
	if (pid < 0) {
		perror("fork failed");
		exit(1);
	} else if (pid == 0) {
		printf("Child Process (fork), PID %d\n", getpid());
		exit(0);
	} else {
		printf("Parent Process (fork), PID %d, Child PID: %d\n", getpid(), pid);
		// Espera pelo término do processo filho
		wait(NULL); 
	}
}

/**
 * @brief Cria um novo processo e executa um programa específico.
 */
void test_spawn() {
	pid_t pid;
	char *argv[] = {"/usr/bin/ls", "-l", NULL};

	int status = posix_spawn(&pid, "/usr/bin/ls", NULL, NULL, argv, environ);

	if (status == 0) {
		printf("Child Process (spawn), PID: %d\n ", pid);
		// Espera pelo término do processo filho
		waitpid(pid, NULL, 0);
	} else {
		perror("posix_spawn failed");
	}
}

int main() {
	
	printf("Testing fork()\n");
	test_fork();

	printf("\nTesting posix_spawn()\n");
	test_spawn();

	return 0;
}
