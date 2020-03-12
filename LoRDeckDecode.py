""" Python implementation of Legends of Runeterra deck decoder
    Decks are encoded by grouping VarInts into an array and then base32 encoding into a string
    This program decodes the strings and returns the cards and amounts in the deck
"""

import base64, json

def main():
    #Deck code to be decoded
    deckcode = "CEBAIAIEBAITINQHAECQWFRGFMYDCNICAEAQIDICAECQOKABAEAQKOA"

    #Faction identifiers
    factions = ["DE", "FR", "IO", "NX", "PZ", "SI"]
    
    #Load json data for cards
    data = loadCards()

    #pythons base32 decoder needs correct padding
    deckcode = padDeckcode(deckcode)

    #Print decoded string as hex grouped in bytes (optional)
    #decodeHex(deckcode)

    #convert to a bytearray
    byte_list = bytearray(base64.b32decode(deckcode))

    #Format is first nibble and version is second
    deck_format = byte_list[0] >> 4
    deck_version = byte_list[0] & 0xF
    print("Deck Format and Version", deck_format, deck_version)
    del byte_list[:1]

    #Display cards which which have three copies first
    for i in range(3, 0, -1):
        num_of_groups = varInts(byte_list)
        print("\n===", i, "Copies ===")

        for x in range(num_of_groups):
            num_of_faction = varInts(byte_list)
            set_num = varInts(byte_list)
            faction = varInts(byte_list)

            #Individual cards in faction
            for y in range(num_of_faction):
                card = varInts(byte_list)
                
                #Convert card to seven character Runeterra card code
                card = str(set_num).zfill(2) + factions[faction] + str(card).zfill(3)
                #print(card)

                #Output actual card name from json data
                for dict in data:
                    if dict["cardCode"] == card:
                        print(dict['name'], "x", i)

def varInts(deck_bytes):
    current_loc = 0
    byte = 0
    output = 0

    for i in range(len(deck_bytes)):
        byte += 1

        #Check all but MSB
        current = deck_bytes[i] & 0x7F
        output |= current << current_loc

        #Check if more to follow
        if (i & 0x80) != 0x80:
            del deck_bytes[:byte]
            return output

        current_loc += 7

def padDeckcode(deckcode):
    padding = 8 - (len(deckcode) % 8)
    if padding > 0 and padding != 8:
        deckcode += "=" * padding
    return deckcode

def decodeHex(deckcode):
    decoded = base64.b32decode(deckcode)
    decoded_hex = " ".join(decoded.hex()[i:i+2] for i in range(0, len(decoded.hex()), 2)).upper()
    print(decoded_hex)

def loadCards():
    with open('set1-en_us.json', encoding="utf8") as f:
        data = json.load(f)
    return data

main()