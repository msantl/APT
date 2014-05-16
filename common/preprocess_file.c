#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

char buff[1024];

int main(int argc, char **argv) {
    assert(argc == 3);
    char *c;
    FILE *input = fopen(argv[1], "r");
    FILE *output = fopen(argv[2], "w");

    memset(buff, 0, sizeof buff);

    while (fgets(buff, sizeof buff, input)) {
        if (!isprint(*buff)) continue;

        if (strncmp(buff, "<s>", 3) == 0 ||
            strncmp(buff, "</s>", 4) == 0 ||
            ('a' <= *buff && *buff <= 'z') ||
            ('A' <= *buff && *buff <= 'Z')) {

            for (c = buff; *c && *c != ' ' && *c != '\t' && *c != '\n'; ++c) {
                fprintf(output, "%c", tolower(*c));
            }   fprintf(output, " ");

        }

        if (strncmp(buff, "</s>", 4) == 0) {
            fprintf(output, "\n");
        }

        memset(buff, 0, sizeof buff);
    }

    fclose(input);
    fclose(output);
    return 0;
}
