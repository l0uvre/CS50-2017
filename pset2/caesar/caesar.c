#include <stdio.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2) {
    printf("Usage: ./caesar k\n");
    return 1;
    }


    printf("plaintext: ");
    string pText = get_string();
    printf("ciphertext: ");

    int key = atoi(argv[1]);
    for (int i = 0, n = strlen(pText); i < n; i++)
    {
      if (isalpha(pText[i]))
      {
          if (islower(pText[i]))
          {
            printf("%c", ((pText[i] - 97) + key)%26 + 97);
          }
          else
          {
            printf("%c", ((pText[i] - 65) + key)%26 + 65);
          }
      }
      else
      {
        printf("%c", pText[i]);
      }

    }



  printf("\n");
  return 0;
}
