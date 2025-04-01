#include <stdio.h>
#include <locale.h>

int cycle(int n, int m){ //цикл

    while (m != 0){
        int ostatok = n % m;
        n = m;
        m = ostatok;
    }
    return n;
}

int recursion(int n, int m){ //рекурсия

    if (m == 0){
        return n;
    }
    return recursion(m, n % m);
}

int main(){

    setlocale(LC_ALL, "RU");

    int n, m;

    printf("Введите первое натуральное число: ");
    scanf("%i", &n);
    printf("Введите второе натуральное число: ");
    scanf("%i", &m);

    int nod1 = cycle(n, m);
    int nod2 = recursion(n, m);

    printf("Цикл: %i\n", nod1);
    printf("Рекурсия: %i", nod2);
    return 0;
}
