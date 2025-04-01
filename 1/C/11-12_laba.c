#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[50];
    int stars;
    char address[100];
    char phone[15];
    int totalRooms;
    int luxuryRooms;
    int availableRooms;
} Hotel;

void list(){ //меню выбора
    printf("\nMenu\n");
    printf("1. Add hotel\n");
    printf("2. Show all hotels\n");
    printf("3. Delete hotel\n");
    printf("4. Get best hotel\n");
    printf("5. Save data to file\n");
    printf("6. Exit\n");
    printf("Enter your choice: ");
}

Hotel hotels[100]; //массив отелей
int numHotels = 0;

void luxury()
    {
        printf("Luxury rooms: ");                        //люкс номера
        scanf("%d", &hotels[numHotels].luxuryRooms);

        if (hotels[numHotels].totalRooms < hotels[numHotels].luxuryRooms){
        printf("Incorrect value!\n");
        return luxury();
    }
    }
    

void available()
    {
        printf("Available rooms: ");                     //свободные номера
        scanf("%d", &hotels[numHotels].availableRooms);

        if (hotels[numHotels].totalRooms < hotels[numHotels].availableRooms){
        printf("Incorrect value!\n");
        return available();
    }
    }

void new(){

    int code;
    char a, b;

    printf("Enter hotel details:\n");

    printf("Name: ");
    scanf(" %[^\n]", hotels[numHotels].name); /*пропускает все символы до того, как встретится символ новой строки (`\n`). 
                                              Это позволяет считать строку с пробелами, включая пробелы в середине строки.*/
    printf("Stars: ");
    scanf("%d", &hotels[numHotels].stars);

    printf("Address: ");
    scanf(" %[^\n]", hotels[numHotels].address);          

    printf("Phone: ");
    scanf("%s", hotels[numHotels].phone);

    printf("Total rooms: ");
    scanf("%d", &hotels[numHotels].totalRooms); 

    luxury();
    available();
    
    numHotels++;
}

void printHotel(Hotel hotel){ //вывод одного отеля
    printf("\nName: %s\n", hotel.name);
    printf("Stars: %d\n", hotel.stars);
    printf("Address: %s\n", hotel.address);
    printf("Phone: %s\n", hotel.phone);
    printf("Total rooms: %d\n", hotel.totalRooms);
    printf("Luxury rooms: %d\n", hotel.luxuryRooms);
    printf("Available rooms: %d\n\n", hotel.availableRooms);
}
void showAllHotels(){ //вывод списка всех отелей
    int i;
    if (numHotels == 0) {
        printf("The list of hotels is empty\n");
        return;
    }
    printf("\nAll hotels:\n");
    for(i=0; i<numHotels; i++){
        printf("Index: %i", i); printHotel(hotels[i]);
    }
}

void deleteHotel(int index){ //удаление отеля
    int i; 
    if(index >= 0 && index < numHotels){
        for(i=index; i<numHotels-1; i++){
            strcpy(hotels[i].name, hotels[i+1].name);
            hotels[i].stars = hotels[i+1].stars;
            strcpy(hotels[i].address, hotels[i+1].address);
            strcpy(hotels[i].phone, hotels[i+1].phone);
            hotels[i].totalRooms = hotels[i+1].totalRooms;
            hotels[i].luxuryRooms = hotels[i+1].luxuryRooms;
            hotels[i].availableRooms = hotels[i+1].availableRooms;
        }
        numHotels--;
        printf("Hotel deleted successfully.\n");
    }
    else{
        printf("Invalid index.\n");
    }
}

void getBestHotel(){ //лучший отель
    int i, maxAvailableRooms = 0, bestHotelIndex = -1;
    
    for(i=0; i<numHotels; i++){
        if(hotels[i].availableRooms > maxAvailableRooms){
            maxAvailableRooms = hotels[i].availableRooms;
            bestHotelIndex = i;
        }
    }
    
    if(bestHotelIndex >= 0){
        printf("Best hotel with most available rooms:\n");
        printHotel(hotels[bestHotelIndex]);
    }
    else{
        printf("No hotels found.\n");
    }
}

//                             12 лаба

void saveDataToFile(){ //сохранение данных
    FILE *fp;
    int i;
    
    fp = fopen("hotels.dat", "w");
    if(fp == NULL){
        printf("Error opening file.\n");
        return;
    }
    
    fwrite(&numHotels, sizeof(int), 1, fp);
    fwrite(hotels, sizeof(Hotel), numHotels, fp);
    
    fclose(fp);
    printf("Data saved to file successfully.\n");
}

void loadDataFromFile(){ //загрузка данных
    FILE *fp;
    
    fp = fopen("hotels.dat", "r");
    if(fp == NULL){
        printf("File not found.\n");
        return;
    }
    
    fread(&numHotels, sizeof(int), 1, fp);
    fread(hotels, sizeof(Hotel), numHotels, fp);
    
    fclose(fp);
    printf("Data loaded from file successfully.\n");
}

int main()
{
    int choice, index;
    
    loadDataFromFile();
    
    while(1){
        list();
        scanf("%d", &choice);
        printf("\n");
        
        switch(choice){
            case 1:
                new();
                break;
            case 2:
                showAllHotels();
                break;
            case 3:
                printf("Enter the index of the hotel to delete: ");
                scanf("%d", &index);
                deleteHotel(index);
                break;
            case 4:
                getBestHotel();
                break;
            case 5:
                saveDataToFile();
                break;
            case 6:
                printf("Exiting program.\n");
                exit(0);
            default:
                printf("Invalid choice.\n");
        }
    }
    
    return 0;
}
