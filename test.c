#include <stdio.h>

int main(void) {
    FILE *fp;
    char filename[100] = "./input/input_10.txt";
    char input[10];

    if ((fp = fopen(filename, "r"))==NULL) {
        printf("error in reading file");
    }

    fgets(input, sizeof(input), fp);
    printf("%s\n", input);

    fclose(fp);
}