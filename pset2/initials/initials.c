#include <stdio.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>

int main(void)
{
    string s = get_string();
    
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (i == 0)
        {
            if (s[0] == 32)
            {
                continue;
            }
            else 
            {
                printf("%c",toupper(s[i]));
            }
        }
        
        else if (s[i - 1] == ' ' && s[i] != ' ')
        {
            printf("%c",toupper(s[i]));
        }
    }
    
    printf("\n");
    
    return 0;
    
}