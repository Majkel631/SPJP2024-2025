// Online C compiler to run C program online
#include <stdio.h>

int main() {
    
    
        // Tworzymy tablicę o stałej wielkości 10
    int liczba, i;
    int n = 20;
    int tablica[22] ={1,2,3,4,5,6,7,8,9,0,10,11,12,13,14,15,16,17,18,19,20};
    char op;
    printf("\n choose something\n");
    scanf(" %c", &op);
    switch(op){
       case 'e':
       printf("program end successfuly");
       break;
       case 'w':
         for (int i =0; i<= 20;i ++){
             printf("%d",tablica[i]);
         }
        break;
        case '0':
        printf("error");
        case 'd':{
           
    printf("ddaj liczbe do tablicy:\n");
    for (i = 0; i < 1; i++) {
        scanf("%d", &liczba);
        tablica[i] = liczba;
    }
    // Wyświetlamy wprowadzone liczby
    printf("\nWprowadzone liczby to:\n");
    for (i = 0; i < 20; i++) {
        printf("%d ", tablica[i]);
    }
       break; }
        case 'D':{
           for (i = 0; i < 2; i++) {
        scanf("%d", &liczba);
        tablica[i] = liczba;
    }
    printf("\nWprowadzone liczby to:\n");
    for (i = 0; i < 20; i++) {
        printf("%d ", tablica[i]);
    };
        break;
        }
        case 'u': {
            printf("d");
        }case 's':{
            printf("delete number from list");
           for (int i =0; i<= 20;i ++){
             printf("\n %d",tablica[i]);
         }break;
       
        }
    }  
     return 0;
    }

 

  
       
