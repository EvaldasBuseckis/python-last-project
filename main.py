class Word:
    def __init__(self, word: str) -> None:
        self.word = word

    def letter_count(self):
        return len(self.word)

    def letter_selector(self, letter:int) -> int:
        return self.word[letter]

def input_word():
    word = input("iveskite zodi: ")
    return word


# word_1 = input_word()
# word_2 = Word(input_word())

# print(word_2.letter_selector(2))
def test(word):
    zodis = Word(word)

    mistakes = 0

    wrong_letters = []
    good_letters = []
    while mistakes < 10:
        a = input("iveskite raide: ")

        if  a in word:
            if a not in good_letters:
                good_letters.append(a)
            print(f"you found it, your answers: {good_letters} ")
        else:
            if a not in wrong_letters:

                wrong_letters.append(a)
                mistakes += 1
                print(f"jau spetos klaidingos raides: {wrong_letters}")
                print(f"jus padarete {mistakes} klaidas")
            else:
                print(f"sita jau spejai, bet uz durnuma gauni papildoma klaida")
                mistakes += 1
                
        

test(input_word())

    






def good_answer(word: str) -> str:
    if input_word() == word:
        print("atspejai")
    else:
        print("neatspejai")
    # if 




# print (input_word())
# good_answer("gaidis")
