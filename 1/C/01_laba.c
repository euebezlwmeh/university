//7. Вывести частное наименьшей суммы цифр параметров a, b и второго параметра.
#include <stdio.h>
#include <math.h>

int main()
{
    int a, b, Sum_a, Sum_b;
    float res;

    printf("Enter a: ");
    scanf("%d", &a);
    int a1 = a;

    if (a < 0)
    {
        a = abs(a);
    }

    while (a > 0)
    {
        Sum_a += a % 10;
        a /= 10;
    }

    printf("Enter b: ");
    scanf("%d", &b);
    int b1 = b;

    if (b < 0)
    {
        b = abs(b);
    }

    while (b > 0)
    {
        Sum_b += b % 10;
        b /= 10;
    }

    printf("Sum of a = %d\n", Sum_a);
    printf("Sum of b = %d\n", Sum_b);

    if (Sum_a < Sum_b)
    {
        if (b1 == 0)
        {
            printf("division by 0!");
        }
        res = (float)Sum_a / b1;
        printf("%d / %d == %f", Sum_a, b1, res);
    }
    else
    {
        if (a1 == 0)
        {
            printf("division by 0!");
        }
        res = (float)Sum_b / a1;
        printf("%d / %d == %f", Sum_b, a1, res);
    }
    return 0;
}
