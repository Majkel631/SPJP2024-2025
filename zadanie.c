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
  
       
