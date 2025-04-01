#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <locale.h>

void generation(int arr[], int size) {
    srand(time(0));
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 100; // генерируем случайное число от 0 до 99
    }
}

int search_index(int arr[], int size, int target) {
    for (int i = 0; i < size; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}

void turning(int arr[], int start, int end) {
    while (start < end) {
        int a = arr[start];
        arr[start] = arr[end];
        arr[end] = a;
        start++;
        end--;
    }
}

void reverse(int arr[], int size, int index) {
    if (index >= 0 && index < size) {
        turning(arr, 0, index - 1); //изменение до индекса
        turning(arr, index + 1, size - 1); //после
    } else {
        turning(arr, 0, size - 1); //изменение всего массива
    }
}



int main() {
   
    setlocale(LC_ALL, "rus");
   
    int size;
    printf("Введите количество элементов: ");
    scanf("%d", &size);

    int arr[size];
    generation(arr, size);

    printf("Массив до:\n");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    int target;
    printf("Введите искомый элемент: ");
    scanf("%d", &target);

    int index = search_index(arr, size, target);

    printf("Первое вхождение элемента %d: %d\n", target, index);

    reverse(arr, size, index);

    printf("Массив после:\n");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }

    return 0;
}
