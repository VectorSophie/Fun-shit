def totalcode(arrcode):
    total = 0
    for i in range(11):
        digit = int(arrcode[i])
        if i % 2 == 0:
            total += 3 * digit
        else:
            total += digit
    return (10 - (total % 10)) % 10

def barcode_scan(barcode):
    arrcode = list(barcode)
    if 'x' in arrcode:
        if arrcode.count('x') == 1:
            print("Damaged barcode. Scanning...")
            damage = arrcode.index('x')
            if damage == 11:
                print("Last digit damaged")
                print("Calculating last digit...")
                tots = totalcode(arrcode)
                print(f"{tots} is the last digit.")
                arrcode[11] = str(tots)
                print("Full barcode:", "".join(arrcode))
            else:
                suffix = "st" if damage == 0 else "nd" if damage == 1 else "rd" if damage == 2 else "th"
                print(f"{damage + 1}{suffix} digit damaged")
                print("Calculating...")
                for guess in range(10):
                    tempcode = arrcode.copy()
                    tempcode[damage] = str(guess)
                    tots = totalcode(tempcode)
                    if tots == int(tempcode[11]):
                        print(f"{guess} is the recovered digit")
                        print("Full barcode:", "".join(tempcode))
                        break
                else:
                    print("Invalid barcode")
        else:
            print("Invalid barcode")
    else:
        tots = totalcode(arrcode)
        if tots == int(arrcode[11]):
            print("Barcode accepted")
        else:
            print("Invalid barcode")
            
print(barcode_scan('0421x0005264'))
            
            


