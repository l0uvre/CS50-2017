#include <stdio.h>
#include <stdint.h>

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{

  if (argc != 2) {
    fprintf(stderr, "Usage : ./recover forensicedJPEG \n");
    return 1;
  }

  FILE *inptr = fopen(argv[1], "r");
  FILE *img = NULL;

  if (inptr == NULL) {
    fprintf(stderr, "forensic image cannot be opened.\n");
    return 2;
  }


  BYTE buffer[512];
  fread(&buffer, sizeof(buffer), 1, inptr);


  char filename[8];
  int count = 0;

  while(buffer[0] != 0xff || buffer[1] != 0xd8 ||
  buffer[2] != 0xff || ((buffer[3] & 0xf0) != 0xe0))
  {
    fread(&buffer, sizeof(buffer), 1, inptr);
  }

  while (buffer[0] == 0xff && buffer[1] == 0xd8 &&
  buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0))
  {
    sprintf(filename, "%03i.jpg", count);
    img = fopen(filename, "w");
    fwrite(&buffer, sizeof(buffer), 1, img);
    do {
      if(fread(&buffer, sizeof(buffer), 1, inptr) == 1)
      {
        if (buffer[0] != 0xff || buffer[1] != 0xd8 ||
        buffer[2] != 0xff || ((buffer[3] & 0xf0) != 0xe0)) {
          fwrite(&buffer, sizeof(buffer), 1, img);
        }

      }
      else
      {
        fclose(img);
        fclose(inptr);
        return 0;
      }
    } while(buffer[0] != 0xff || buffer[1] != 0xd8 ||
    buffer[2] != 0xff || ((buffer[3] & 0xf0) != 0xe0));

    fclose(img);
    count++;

  }

  fclose(inptr);
  return 0;
}
