// N (1000) — количество кругов, которые нужно упаковать в квадрат.
// radius (0.05) — радиус каждого круга.
// L (10) — длина стороны квадрата, в который упаковываются круги.

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>

typedef struct {
    double x;
    double y;
} Point;

typedef struct {
    Point center;
    double radius;
} Circle;

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

void pack_circles_sequential(int N, double radius, double L, Circle* circles) {
    int placed = 0;
    double grid_step = 2 * radius;
    
    for (double y = radius; y <= L - radius && placed < N; y += grid_step) {
        for (double x = radius; x <= L - radius && placed < N; x += grid_step) {
            Circle new_circle = {{x, y}, radius};
            
            if (is_valid_position(new_circle, circles, placed, L)) {
                circles[placed] = new_circle;
                placed++;
            }
        }
    }
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
    
    pack_circles_sequential(N, radius, L, circles);
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_taken = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("Последовательная упаковка %d кругов:\n", N);

    for (int i = 0; i < 5 && i < N; i++) {
        printf("Круг %d: (%.2f, %.2f)\n", i+1, circles[i].center.x, circles[i].center.y);
    }

    free(circles);
    return 0;
}