#include <stdio.h>
#include <math.h>
#include <locale.h>

#define EPSILON 1e-3

long double expr(long double n);

int main(){

    setlocale(LC_ALL, "rus");

    int N = 100000;

    long double I1 = expr(N);
    long double I2 = expr(2*N);

    while((fabs(I2-I1)/3)>EPSILON){
       I1 = expr(N);
       I2 = expr(2*N);
       N *= 2;
    }
    printf("Интеграл при 2*n равен: %Lf", I2);
    return 0;
}

long double expr(long double n){
    
    long double h, x1 = -1, x2 = 1, sum1 = 0, sum2 = 0, step1 = 0, step2 = 0;
    h = 2/n;
    
    while (x1 < 1 + h/2)
    {
        long double f = exp(-2 * sinf(x1));
        x1 += h;
        step1 = h * (f + h / 2); 
        sum1 += step1; 
    }

    for (x2 = 1 + h/2; x2 <= 2; x2 += h)
    {
        long double f = pow(x2, 2) - (1 / tan(x2));
        step2 = h * (f + h / 2); 
        sum2 += step2; 
    }
    
    long double sum = sum1 + sum2;
    return sum;
}