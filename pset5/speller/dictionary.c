/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"
#include "string.h"

#define HASHTABLE_SIZE 65536

/**
 * Build linked lists for hash_table for load function.
 */
typedef struct node
{
  char word[LENGTH + 1];
  struct node *next;
}
node;

node* hash_table[HASHTABLE_SIZE];
int words_number;

/**
 * Hashing function
 * Adapted from https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9nlkn/?st=j6u73xvu&sh=601e8593.
 */
int hashing (const char *string)
{
  unsigned int hash = 0;
  for (int i = 0, count = strlen(string); i < count; i++) {
    hash = (hash << 2) ^ string[i];
  }
  return hash % HASHTABLE_SIZE;
}

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    char copy[LENGTH + 1];
    strcpy(copy, word);

    for (int i = 0; copy[i] != '\0'; i++) {
      copy[i] = tolower(copy[i]);
    }
    int index = hashing(copy);

    if (hash_table[index] == NULL)
    {
      return false;
    } else
    {
      node *current = hash_table[index];

      if (strcmp(current->word, copy) == 0)
      {
        return true;
      }

      while (current->next != NULL)
      {
        if (strcmp(current->word, copy) == 0)
        {
          return true;
        }
        current = current->next;
      }
    }

    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    FILE *fp = fopen(dictionary, "r");
    if (fp == NULL)
    {
      printf("Can't load.\n");
      return false;
    }

    int index;
    char word[LENGTH + 1];

    while (fscanf(fp, "%s\n", word) != EOF)
    {
      index = hashing(word);
      node *new_node = malloc(sizeof(node));
      if (new_node == NULL)
      {
        unload();
        return false;
      }

      strcpy(new_node->word, word);

      if (hash_table[index] == NULL)
      {
        hash_table[index] = new_node;
        new_node->next = NULL;
      }
      else
      {
        node *current = hash_table[index];
        while (current != NULL)
        {
          if (current->next == NULL) {
            current->next = new_node;
            break;
          }
          current = current->next;

        }
      }
      words_number++;
    }
    fclose(fp);

    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return words_number;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for (int i = 0; i < HASHTABLE_SIZE; i++) {
      node *cursor = hash_table[i];

      while (cursor != NULL) {
        node *temp = cursor;
        cursor = cursor->next;
        free(temp);
      }
    }
    return true;
}
