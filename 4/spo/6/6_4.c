#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>
#include <pthread.h>

#define MAX_THREADS 4

typedef struct {
    double x;
    double y;
} Point;

typedef struct {
    Point center;
    double radius;
} Circle;

typedef struct {
    int thread_id;
    int N;
    double radius;
    double L;
    Circle* circles;
    int* placed;
    pthread_mutex_t* mutex;
} ThreadData;

double distance(Point a, Point b) {
    return sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
}

bool is_valid_position(Circle new_circle, Circle* circles, int count, double square_size) {
    if (new_circle.center.x < new_circle.radius || 
        new_circle.center.x > square_size - new_circle.radius ||
        new_circle.center.y < new_circle.radius || 
        new_circle.center.y > square_size - new_circle.radius) {
        return false;
    }

    for (int i = 0; i < count; i++) {
        if (distance(new_circle.center, circles[i].center) < new_circle.radius + circles[i].radius) {
            return false;
        }
    }

    return true;
}

void* pack_circles_thread(void* arg) {
    ThreadData* data = (ThreadData*)arg;
    double grid_step = 2 * data->radius;
    int placed_local = 0;
    Circle local_circles[data->N / MAX_THREADS + 1];

    double y_start = data->radius + (data->thread_id * (data->L / MAX_THREADS));
    double y_end = y_start + (data->L / MAX_THREADS);
    
    for (double y = y_start; y <= y_end && placed_local < (data->N / MAX_THREADS + 1); y += grid_step) {
        for (double x = data->radius; x <= data->L - data->radius && placed_local < (data->N / MAX_THREADS + 1); x += grid_step) {
            Circle new_circle = {{x, y}, data->radius};
            
            if (is_valid_position(new_circle, data->circles, *data->placed, data->L)) {
                local_circles[placed_local] = new_circle;
                placed_local++;
            }
        }
    }

    pthread_mutex_lock(data->mutex);
    for (int i = 0; i < placed_local; i++) {
        if (*data->placed < data->N) {
            data->circles[*data->placed] = local_circles[i];
            (*data->placed)++;
        }
    }
    pthread_mutex_unlock(data->mutex);
    
    return NULL;
}

void pack_circles_parallel(int N, double radius, double L, Circle* circles) {
    pthread_t threads[MAX_THREADS];
    ThreadData thread_data[MAX_THREADS];
    pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
    int placed = 0;
    
    for (int i = 0; i < MAX_THREADS; i++) {
        thread_data[i].thread_id = i;
        thread_data[i].N = N;
        thread_data[i].radius = radius;
        thread_data[i].L = L;
        thread_data[i].circles = circles;
        thread_data[i].placed = &placed;
        thread_data[i].mutex = &mutex;
        
        pthread_create(&threads[i], NULL, pack_circles_thread, &thread_data[i]);
    }
    
    for (int i = 0; i < MAX_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
    
    pthread_mutex_destroy(&mutex);
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        printf("Использование: %s N radius L\n", argv[0]);
        return 1;
    }

    int N = atoi(argv[1]);
    double radius = atof(argv[2]);
    double L = atof(argv[3]);

    Circle* circles = (Circle*)malloc(N * sizeof(Circle));
    
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    pack_circles_parallel(N, radius, L, circles);
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_taken = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("Параллельная упаковка %d кругов (%d потоков):\n", N, MAX_THREADS);
    
    for (int i = 0; i < 5 && i < N; i++) {
        printf("Круг %d: (%.2f, %.2f)\n", i+1, circles[i].center.x, circles[i].center.y);
    }

    free(circles);
    return 0;
}