#include <stdio.h>

int main()
{
Zadanie 1
    printf("Hello World");
 

Zadanie 2
    double first ;
    double second ;
    char op;

    printf("Select a operator(+,-,*,/):");
    scanf("%c",&op);
    printf("write Number");
    scanf("%lf",&first);
    printf("write second Number");
    scanf("%lf",&second);
    switch(op){
        case '+':
        printf("%lf",first + second);
        break;
        case '-':
         printf("%lf",first - second);
         break;
           case '*':
         printf("%lf",first * second);
         break;
           case '/':
         printf("%lf",first / second);
         break;
         default:
         printf("something went wrong");
    }

Zadanie 3
#include <stdio.h>

int main()
{
   
    double first ;
    double second ;

    printf("write Number ");
    scanf("%lf",&first);
    printf("write second Number ");
    scanf("%lf",&second);
   
    
    if(first == second){
        printf("\n Number have yhe same value");
    }
    else if(first > second){
        printf("%lf",first);
    }else if(first < second){
        printf("%ls\f",second);
        
    }
   
    }


Zadanie 4
#include <stdio.h>

int main()
{
   
    double first ;
    double second ;
        double last ;


    printf("write Number ");
    scanf("%lf",&first);
    printf("write second Number ");
    scanf("%lf",&second);
    printf("write Last Number");
    scanf("%lf",&last);
   
    
    if(first == second && second == last){
        printf("\n Number have the same value");
    }
    else if(first > second && last){
        printf("%lf",first  );
         printf("\n First Have yhe bigger value");
    
    }else if(second > first && last){
        printf("%lf",second  );
         printf("\n Second Have yhe bigger value");
    }
    else if(last > first && second){
          printf("%lf",last  );
         printf("\n Last Number  Have yhe bigger value");    }
   
    }
 
 

  
       
