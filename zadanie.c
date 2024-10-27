#include <stdio.h>

int main()
{
    printf("Hello World");
 
  
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
 

  
       
