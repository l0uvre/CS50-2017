#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    printf("O hai! How much change is owed?\n");
    float change = get_float();
    
    while (change <= 0)
    {
        printf("O hai! How much change is owed?\n");
        change = get_float();
    }

    int changeA = round(change*100);
    int count = 0;
    
    

    while (changeA > 0)
    {
        if (changeA >= 25)
        {
            changeA -= 25;
            count++;
            continue;
            
        } 
        else if (changeA < 25 && changeA > 9)
        {
            changeA -= 10;
            count++;
            continue;
            
        }
        else if (changeA < 10 && changeA > 4)
        {
            changeA -= 5;
            count++;
            continue;
        }
        else 
        {
            changeA -= 1;
            count++;
            continue;
        }
    }

    printf("%i\n", count);
}