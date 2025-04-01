// 7 варик
#include <stdio.h>
#include <math.h>
#include <locale.h>

int main()
{
    setlocale(LC_ALL, "rus");
    float h, x = -1;
    printf("Введите шаг изменения аргумента x: ");
    scanf("%f", &h);

    printf("\tx\t\tf(x)\n");
    printf("-------------------------\n");

    while (x < 1 + h/2)
    {
        float f = exp(-2 * sin(x));
        printf("%f\t%f\n", x, f);
        x += h;
    }

    printf("\nx\t\tf(x)\n");
    printf("-------------------------\n");

    for (x = 1 + h/2; x < 2.1; x += h)
    {
        float f = pow(x, 2) - (1 / tan(x));
        printf("%f\t%f\n", x, f);
    }
}
