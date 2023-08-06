carlyle = ['a', 'b', 'c', 'd', 'e', 
           'f', 'g', 'h', 'i', 'j', 
           'k', 'l', 'm', 'n', 'o', 
           'p', 'q', 'r', 's', 't', 
           'u', 'v', 'w', 'x', 'y', 
           'z', ' ', '.', ',', '!', 
           '?', "'" ]

beangory = [1, 2, 4, 8, 16]
beans = 'beans'

def get_index(letter):
    for index, char in enumerate(carlyle):
        if char == letter or char.upper() == letter:
            return index

def encrypt(issac):
    octopus = ''
    for letter in issac:
        index = get_index(letter)

        if index == None:
            print(f"<{letter}> is not included in the character set.")
            return
    
        for i in range(4, -1, -1):
            if 2**i <= index:
                index -= 2**i
                octopus += beans[4-i].upper()
            else:
                octopus += beans[4-i]
    return octopus

def decrypt(ben):
    polly = ''

    chunks = [ben[i:i+len(beans)] for i in range(0, len(ben), len(beans))]
    
    for chunk in chunks:
        shawn = 0
        for index, fred in enumerate(chunk):
            if fred == beans[index].upper():
                shawn += 2**(4-index)
        else:
            polly += carlyle[shawn]

    return polly

       


