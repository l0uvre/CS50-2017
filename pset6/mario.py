import sys

def main():
    height = int(input("Height: "))
    while height > 23 or height <= 0:
        if height == 0:
            exit(1);
        else:
            height = int(input("Height: "))
    pyramid(int(height))


def pyramid(h):
    for i in range(h):
        for j in range(0, h - i - 1):
            print(" ", end="")

        for k in range(0, i + 1):
            print("#", end="")

        print()


if __name__ == "__main__":
    main()
