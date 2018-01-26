#include <stdio.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>

int main(int argc, string argv[])
{
  if (argc != 2) {
    printf("Usage: ./vigenere k\n");
    return 1;
  }
  bool isChar = true;
  int argv1_len = strlen(argv[1]);

  for (int i = 0; i < argv1_len; i++) {
    if (!isalpha(argv[1][i]))
    {
      isChar = false;
    }
  }

  if (!isChar) {
    printf("Usage: ./vigenere k\n");
    return 1;
  }

  else
  {
    printf("plaintext: ");
    string pText = get_string();
    printf("ciphertext: ");

    int count = 0;
    char key = argv[1][count % argv1_len];
    for (int i = 0, n = strlen(pText); i < n; i++) {
      if (isalpha(pText[i])) {
        if (isupper(key)) {
          if (islower(pText[i])) {
            printf("%c", ((pText[i] - 97) + (key - 'A'))%26 + 97);
          }
          else
          {
            printf("%c", ((pText[i] - 65) + (key - 'A'))%26 + 65);
          }
          count++;
        }

        if (islower(key)) {
          if (islower(pText[i])) {
            printf("%c", ((pText[i] - 97) + (key - 'a'))%26 + 97);
          }
          else
          {
            printf("%c", ((pText[i] - 65) + (key - 'a'))%26 + 65);
          }
          count++;
        }
      }
      else
      {
          printf("%c", pText[i]);
      }

      key = argv[1][count % argv1_len];
    }
  }

  printf("\n");
  return 0;
}
