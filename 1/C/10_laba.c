#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#include <time.h>

void zapolnenie(int rows, int cols, int* arr){

srand(time(0));
for (int i = 0; i < rows; i++){
    for (int j = 0; j < cols; j++){
        *(arr + i * cols + j) = rand() % 100;
    }
}
}

void printf_matrix_before(int rows, int cols, int* arr){

for (int i = 0; i < rows; i++){
    for (int j = 0; j < cols; j++){
        printf("%i ", *(arr + i * cols + j));
    }
    printf("\n");
}
}

void printf_matrix_after(int rows, int cols, int* arr, int* transposed){
  for (int i = 0; i < cols; i++) {
    for (int j = 0; j < rows; j++) {
      printf("%d ", *(transposed + i * rows + j));
  }
    printf("\n");
  }
}

void transpose(int rows, int cols, int* arr, int* transposed) {
  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      *(transposed + j * rows + i) = *(arr + i * cols + j);
    }
  }
}

void obnulenie(int rows, int cols, int* arr){

for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
        if (i != j && i != j - 1 && i != j + 1) {
            *(arr + i * cols + j) = 0;
        }
    }
}
}

void modification(int rows, int cols, int* arr, int* transposed, int num) {
int sum = 0;

for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
        if (i == j || i == j - 1 || i == j + 1) {
            sum += *(arr + i * cols + j);
        }
    }
}

if (sum > num) {
    transpose(rows, cols, arr, transposed);
    printf_matrix_after(rows, cols, arr, transposed);
} else {
    obnulenie(rows, cols, arr);
    printf_matrix_before(rows, cols, arr);
}
}

int main()
{

  setlocale(LC_ALL, "rus");
  
  int rows, cols, num;
  
  printf("Enter the number of items in the row and column: ");
  scanf("%i %i", &rows, &cols);
  printf("Enter the specified number: ");
  scanf("%i", &num);
  
  int* arr = (int*)malloc(rows * cols * sizeof(int));
  zapolnenie(rows, cols, arr);
  
  int* transposed = (int*)malloc(rows * cols * sizeof(int));
  
  printf("Array up to:\n");
  printf_matrix_before(rows, cols, arr);
  
  printf("Array after:\n");
  modification(rows, cols, arr, transposed, num);
  
  free(arr);
  free(transposed);
  
  return 0;
}
