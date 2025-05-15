CC = gcc

CFLAGS = -Wall -g $(shell pkg-config --cflags gtk+-3.0)

LIBS = $(shell pkg-config --libs gtk+-3.0) -lsqlite3

SRC = 4.c

TARGET = a.exe

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)
