/*     Двумерные массивы

Размеры массива вводить с клавиатуры, массив заполнить случайными числами.
Необходимые расчёты и модификации реализовать в виде функций.

7. Транспонировать матрицу(поменять местами строки и столбцы),
если сумма элементов главной диагонали и двух соседних    
больше заданного числа, и обнулить остальные элементы иначе.   */

#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#include <time.h>

void zapolnenie(int rows, int cols, int arr[][cols]){

    srand(time(0));
    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j++){
            arr[i][j] = rand() % 100;
        }
    }
}

void printf_matrix_before(int rows, int cols, int arr[][cols]){

    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j++){
            printf("%i ", arr[i][j]);
        }
        printf("\n");
    }
}

 printf_matrix_after(int rows, int cols, int arr[][cols], int transposed[][rows]){
    for (int i = 0; i < cols; i++) {
        for (int j = 0; j < rows; j++) {
            printf("%d ", transposed[i][j]);
        }
        printf("\n");
 }
 }

void transpose(int rows, int cols, int arr[][cols], int transposed[][rows]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            transposed[j][i] = arr[i][j];
        }
    }
}

void obnulenie(int rows, int cols, int arr[][cols]){

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (i != j && i != j - 1 && i != j + 1) {
                arr[i][j] = 0;
            }
        }
    }
}

void modification(int rows, int cols, int arr[][cols], int transposed[][rows], int num) {
    int sum = 0;
   
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (i == j || i == j - 1 || i == j + 1) {
                sum += arr[i][j];
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

int main(){

    setlocale(LC_ALL, "rus");
   
    int rows, cols, num;
   
    printf("Введите количество элементов в строке и столбце: ");
    scanf("%i %i", &rows, &cols);
    printf("Введите заданное число: ");
    scanf("%i", &num);
   
    int arr[rows][cols];
    zapolnenie(rows, cols, arr);

    int transposed[cols][rows];

    printf("Массив до:\n");
    printf_matrix_before(rows, cols, arr);

    printf("Массив после:\n");
    modification(rows, cols, arr, transposed, num);
}
