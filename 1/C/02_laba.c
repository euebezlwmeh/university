// 7. y = (x - 2) * sqrt( (1 + x) / (1 - x) ), z = log( pow(y, 2) - 1 )
#include <stdio.h>
#include <math.h>

int main()
{
    double x;
    printf("Enter x {-0.76 < x < 1.0 }:");
    scanf("%lf", &x);
    double y = (x - 2) * sqrt( (1 + x) / (1 - x) );
    double z = log( pow(y, 2) - 1 );

    if (-1 < x && x < 1)
    {
        printf("y(x) = %lf\nz(y) = %lf\n", y, z);
    }
    else
    {
        printf("x value is incorrect!\n");
    }
    return 0;
}
