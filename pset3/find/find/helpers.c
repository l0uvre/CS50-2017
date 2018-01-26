/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    if (n <= 0) {
      return false;
    }

    int bottom = 0;
    int top = n - 1;
    int medium = (bottom + top)/2;

    while (top >= bottom)
    {
      if (values[medium] == value)
      {
        return true;
      }
      else if (values[medium] > value)
      {
        top = medium - 1;
        medium = (top + bottom)/2;
      }
      else
      {
        bottom = medium + 1;
        medium = (top + bottom)/2;
      }
    }

    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    int max = values[0];
    for (int i = 0; i < n; i++)
    {
      if (values[i] >= max)
      {
        max = values[i];
      }
    }

    int buffer_array[max + 1];
    for (int i = 0; i < max + 1; i++)
    {
      buffer_array[i] = 0;
    }

    for (int i = 0; i < n; i++)
    {
      buffer_array[values[i]]++;
    }

    for (int i = 0; i < max + 1; i++)
    {
      buffer_array[i + 1] += buffer_array[i];
    }

    int output[n];

    for (int i = 0; i < n; i++)
    {
      output[buffer_array[values[i]] - 1] = values[i];
      buffer_array[values[i]]--;
    }

    for (int i = 0; i < n; i++) {
      values[i] = output[i];
    }
    return;
}
