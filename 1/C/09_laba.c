#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int digit(char c) { // цифра или нет
    return c >= '0' && c <= '9';
}


int sumIntegersInString(const char *c) { //суммирование целых чисел в строке
    int sum = 0;
    while (*c) {
        while (*c && !digit(*c)) {
            c++;
        }

        // Считываем число и прибавляем его к сумме
        if (digit(*c)) {
            sum += atoi(c); //Функция atoi (ASCII to integer, из ASCII в целое число) используется для приведения строки в числовой вид.
            while (digit(*c)) {
                c++;
            }
        }
    }
    return sum;
}

int main() {
    char inputString[256];

    printf("Введите строку: ");
    fgets(inputString, sizeof(inputString), stdin);

    int result = sumIntegersInString(inputString);

    printf("Сумма целых чисел в строке: %d\n", result);

    return 0;
}
