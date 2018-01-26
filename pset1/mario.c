#include <cs50.h>
#include <stdio.h>

void pyramid(int h);

int main(void)
{
    printf("Height: ");
    int height = get_int();
    
    
    while (height > 23 || height <=0)
    {
        if (height == 0)
        {
            return 0;
        }
        
        printf("Height: ");
        height = get_int();
    } 
    
    pyramid(height);
    
    
}

void pyramid(int h)
{
    for (int i = 0; i < h; i++)
    {
        for (int j = h - i - 1; j > 0; j--)
        {
            printf(" ");
        }
        
        for (int k = i; k >= 0; k--)
        {
            printf("#");
        }
        
        printf("#\n");
    }
}