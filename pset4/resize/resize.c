/**
 * Copies a BMP piece by piece, just because.
 */

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./copy n infile outfile\n");
        return 1;
    }

    //get factor
    int n = atoi(argv[1]);
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    if (n < 1 || n > 100)
    {
      fprintf(stderr, "Factor must be in range from 1 to 100.\n");
      return 1;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, bf_resize;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bf_resize = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, bi_resize;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    bi_resize = bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    //determine new biWidth and biHeight
    bi_resize.biWidth = bi.biWidth * n;
    bi_resize.biHeight = bi.biHeight * n;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding_resize = (4 - (bi_resize.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi_resize.biSizeImage = abs(bi_resize.biHeight) * (bi_resize.biWidth * sizeof(RGBTRIPLE)
    + padding_resize);

    bf_resize.bfSize = 14 + 40 + bi_resize.biSizeImage;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf_resize, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi_resize, sizeof(BITMAPINFOHEADER), 1, outptr);



    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        long offset = bi.biWidth * sizeof(RGBTRIPLE);
        for (int m = 0; m < n; m++)
        {
          // iterate over pixels in scanline
          for (int j = 0; j < bi.biWidth; j++)
          {
              // temporary storage
              RGBTRIPLE triple;

              // read RGB triple from infile
              fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

              // write RGB triple to outfile
              for (int l = 0; l < n; l++)
              {
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
              }

          }

          //add padding for resized bmp
          for (int k = 0; k < padding_resize; k++)
          {
              fputc(0x00, outptr);
          }
          //adjust the location of infile pointer
          fseek(inptr, -offset, SEEK_CUR);
        }

        fseek(inptr, offset, SEEK_CUR);
        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);


    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
