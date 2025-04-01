#include <stdio.h>
#include <math.h>
#include <locale.h>

float expr(float n);

int main(){

    setlocale(LC_ALL, "rus");
    
    float e, n;

    printf("Введите количество шагов n: ");
    scanf("%f", &n);

    printf("Введите необходимую точность e: ");
    scanf("%f", &e);

    float I1 = expr(n);
    float I2 = expr(2*n);

    while((fabs(I2-I1)/3)>e){
       I1 = expr(n);
       I2 = expr(2*n);
       n *= 2;
    }
    printf("Интеграл при n равен: %f\n", I1);
    printf("Интеграл при 2*n равен: %f", I2);
    return 0;
}

 float expr(float n){
    
    float h, x1 = -1, x2 = 1, sum1 = 0, sum2 = 0, step1 = 0, step2 = 0;
    h = 2/n;
    
    while (x1 < 1 + h/2)
    {
        float f = exp(-2 * sinf(x1));
        x1 += h;
        step1 = h * (f + h / 2); 
        sum1 += step1; 
    }

    for (x2 = 1 + h/2; x2 <= 2; x2 += h)
    {
        float f = pow(x2, 2) - (1 / tan(x2));
        step2 = h * (f + h / 2); 
        sum2 += step2; 
    }
    
    float sum = sum1 + sum2;
    return sum;
}
