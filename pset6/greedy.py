
def main():
    change = float(input("O hai! How much change is owed? "))
    while change < 0:
        change = float(input("O hai! How much change is owed? "))

    change_alt = round(change * 100)
    count = 0
    while change_alt > 0:
        if change_alt >= 25:
            change_alt -= 25
            count += 1
            continue
        elif change_alt >= 10:
            change_alt -= 10
            count += 1
            continue
        elif change_alt >= 5:
            change_alt -= 5
            count += 1
            continue
        else:
            change_alt -= 1
            count += 1
            continue
    print("{}".format(count))

if __name__ == '__main__':
    main()
