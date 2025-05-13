// gcc -o 6_2 6_2.c -lm -lpthread -O3

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>
#include <time.h>

#define EPSILON 1e-3
#define MAX_ITER 100000000
#define THREADS 4

typedef struct {
    long double a;
    long double b;
    long double result;
} IntegrationTask;

long double f(long double x) {
    if (x >= -1.0 && x <= 1.0) {
        return expl(-2.0 * sinl(x));
    } else if (x > 1.0 && x <= 2.0) {
        return x * x - 1.0 / tanl(x);
    }
    return 0.0;
}

long double trapezoidal_rule(long double a, long double b, int n) {
    long double h = (b - a) / n;
    long double sum = (f(a) + f(b)) / 2.0;
    
    for (int i = 1; i < n; i++) {
        sum += f(a + i * h);
    }
    
    return sum * h;
}

long double adaptive_integration(long double a, long double b) {
    int n = 2;
    long double prev_result = 0.0;
    long double result = trapezoidal_rule(a, b, n);
    
    for (int i = 0; i < MAX_ITER; i++) {
        n *= 2;
        prev_result = result;
        result = trapezoidal_rule(a, b, n);
        
        if (fabsl(result - prev_result) < EPSILON) {
            break;
        }
    }
    
    return result;
}

void* thread_integrate(void* arg) {
    IntegrationTask* task = (IntegrationTask*)arg;
    task->result = adaptive_integration(task->a, task->b);
    return NULL;
}

long double parallel_integration(long double a, long double b) {
    pthread_t threads[THREADS];
    IntegrationTask tasks[THREADS];
    long double segment = (b - a) / THREADS;
    long double total = 0.0;
    
    for (int i = 0; i < THREADS; i++) {
        tasks[i].a = a + i * segment;
        tasks[i].b = tasks[i].a + segment;
        pthread_create(&threads[i], NULL, thread_integrate, &tasks[i]);
    }

    for (int i = 0; i < THREADS; i++) {
        pthread_join(threads[i], NULL);
        total += tasks[i].result;
    }
    
    return total;
}

int main() {
    struct timespec start, end;
    long double result;
    
    // Последовательное вычисление
    clock_gettime(CLOCK_MONOTONIC, &start);
    result = adaptive_integration(-1.0, 2.0);
    clock_gettime(CLOCK_MONOTONIC, &end);
    
    double seq_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    
    clock_gettime(CLOCK_MONOTONIC, &start);
    result = parallel_integration(-1.0, 2.0);
    clock_gettime(CLOCK_MONOTONIC, &end);
    
    double par_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    printf("Параллельный результат: %.20Lf\n", result);
    
    return 0;
}