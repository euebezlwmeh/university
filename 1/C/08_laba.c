#include <stdio.h>
#include <ctype.h>
#include <conio.h>
int main()
{
    int check_for_a=0,check_for_check=0;
    char a=' ';
    while (1){
        /*кнопка DELETE в виндовс это два символа имеющих порядковый номер -32 и 83 соответственно
        сначала мы проверяем подался ли нам -32, если подался то ставим check_for_a==1
        затем делаем if если check_for_check==1 проверяем на то что символ на 83 порядковому номеру
        первый раз этот if не сработает, он нужен для того чтобы понять был -32 или нет
        если был, то ставим check_for_check=1 и в следующий раз уже проверяем на число 83
        если не равно 83 то обнуляем все чеки*/
        a=getch();
        if (a==-32){
            check_for_a=1;
        }
        if (check_for_a==1){
            if (check_for_check==1){
                if (a==83){
                    break;
                } else{
                    check_for_check=0;
                    check_for_a=0;
                }
            } else{
                check_for_check=1;
            }
        }
        
        if (!iscntrl(a)) { //проверка на функциональную клавишу
            printf("%c ",a); //если не функционалка то выводим символ
        } else {
            printf("%i ",a); //если функционалка выводим её код
        }
    }
    return 0;
}
