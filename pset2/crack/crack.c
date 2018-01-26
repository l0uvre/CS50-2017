#define _XOPEN_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <cs50.h>

static const char alphabet[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

int main(int argc, string argv[])
{
  if (argc != 2)
  {
      printf("Usage: ./crack hash\n");
      return 1;
  }

  //getting salt for crypt() function.
  string hash_code = argv[1];
  char salt[3];
  strncpy(salt, hash_code, 2);
  salt[2] = '\0';

  //initialing a test password no longer than four chars for brute_force.
  char test_pd[5] = {'\0','\0','\0','\0','\0'};

  for (int i = 0; i < 52; i++)
  {
    test_pd[0] = alphabet[i];
    if (strcmp(argv[1], crypt(test_pd, salt))== 0)
    {
      printf("%s\n", test_pd);
      return 0;
    }
  }

  for (int i = 0; i < 52; i++)
  {
    test_pd[0] = alphabet[i];
    for (int j = 0; j < 52; j++)
    {
      test_pd[1] = alphabet[j];
      if (strcmp(argv[1], crypt(test_pd, salt))== 0)
      {
        printf("%s\n", test_pd);
        return 0;
      }
    }
  }

  for (int i = 0; i < 52; i++)
  {
    test_pd[0] = alphabet[i];
    for (int j = 0; j < 52; j++)
    {
      test_pd[1] = alphabet[j];
      for (int k = 0; k < 52; k++)
      {
        test_pd[2] = alphabet[k];
        if (strcmp(argv[1], crypt(test_pd, salt))== 0)
        {
          printf("%s\n", test_pd);
          return 0;
        }
      }

    }
  }


  for (int i = 0; i < 52; i++)
  {
    test_pd[0] = alphabet[i];
    for (int j = 0; j < 52; j++)
    {
      test_pd[1] = alphabet[j];
      for (int k = 0; k < 52; k++)
      {
        test_pd[2] = alphabet[k];

        for (int l = 0; l < 52; l++)
        {
          test_pd[3] = alphabet[l];
          if (strcmp(argv[1], crypt(test_pd, salt))== 0)
          {
            printf("%s\n", test_pd);
            return 0;
          }
        }

      }

    }

  }

  printf("Password not found\n");
  return 0;
}
