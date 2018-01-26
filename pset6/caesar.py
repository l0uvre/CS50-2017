import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: ./caesar k\n")
        exit(1)
    else:
        pText = input("plaintext: ")
        print("ciphertext: ", end = "")

        key = int(sys.argv[1])
        for char in pText:
            if char.isalpha():
                if char.islower():
                    print("{}".format(chr((ord(char) + key - 97) % 26 + 97)), end = "")
                else:
                    print("{}".format(chr((ord(char) + key - 65) % 26 + 65)), end = "")
            else:
                print(char, end = "")
        print()
        exit(0)

if __name__ == '__main__':
    main()