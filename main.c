#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX(A, B) A>B? A: B

void extract_parameter(FILE*, int*, int*, int*, int*, int***, int**, const int);
void print_matrix(int**, int, int);
int* standard_isd(int**, int*, int, int, int);

int main(void) {
    FILE *fp;
    char filename[128];
    const int SIZE = 100;

    int **H_t, *s;
    int n, k, seed, w;

    /* Read input file */
    sprintf(filename, "./input/input_%d.txt", SIZE);
    if ((fp = fopen(filename, "r"))==NULL) {
        printf("error in reading file");
    }

    extract_parameter(fp, &n, &k, &seed, &w, &H_t, &s, MAX(SIZE/2, 85));
    /*
    printf("H_t : \n");
    print_matrix(H_t, k, n-k);
    printf("syndrome : \n");
    print_matrix(&s, 1, n-k);
    */
    fclose(fp);

    // todo - make
}

void extract_parameter(FILE* fp, int *n, int *k, int *seed, int* w, int ***H_t, int **s, const int SIZE) {
    int *row;   // row of H_t (column of H), length n-k
    char line[SIZE];
    char parameter_name[16];
    int row_index=0, column_index=0;

    while(!feof(fp)) {
        fgets(line, sizeof(line), fp);
        if(strncmp(&line[2], "n", strlen("n"))==0) {
            fgets(line, sizeof(line), fp);
            *n = atoi(line);
        } else if(strncmp(&line[2], "seed", strlen("seed"))==0) {
            fgets(line, sizeof(line), fp);
            *seed = atoi(line);
        } else if(strncmp(&line[2], "w", strlen("w"))==0) {
            fgets(line, sizeof(line), fp);
            *w = atoi(line);
        } else if(strncmp(&line[2], "H^transpose", strlen("H^transpose"))==0) {
            // Read first line to calculate k from its length
            fgets(line, sizeof(line), fp);
            *k = *n - strlen(line) + 1;
            *H_t = (int**)malloc(sizeof(int*)*(*k));

            row = (int*)malloc(sizeof(int)*((*n)-(*k)));
            for(column_index=0; column_index<((*n)-(*k)); column_index++) {
                row[column_index] = line[column_index] - '0';
            }
            // Read remaining lines to construct H_t
            (*H_t)[0] = row;
            for(row_index=1; row_index<*k; row_index++) { 
                row = (int*)malloc(sizeof(int)*((*n)-(*k)));               
                fgets(line, sizeof(line), fp);
                for(column_index=0; column_index<((*n)-(*k)); column_index++) {
                    row[column_index] = line[column_index] - '0';
                }
                (*H_t)[row_index] = row;
            }
        } else if(strncmp(&line[2], "s^transpose", strlen("s^transpose"))==0) {
            fgets(line, sizeof(line), fp);
            *s = (int*)malloc(sizeof(int)*((*n)-(*k)));
            for(column_index=0; column_index<(*n)-(*k); column_index++) {
                (*s)[column_index] = line[column_index] - '0';
            }
        }
    }
}

void print_matrix(int** M, int m, int n) {
    int row, col;

    for(row=0; row<m; row++) {
        for(col=0; col<n; col++)
            printf("%d ", M[row][col]);
        printf("\n");
    }
}

/* Returns an error vector */
int* standard_isd(int**H_T, int *s, int n, int k, int w) {
    int *e;

    // todo

    return e;
}