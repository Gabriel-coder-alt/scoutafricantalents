class string_to_bytes:
    
    def __init__(self, text):
        self.text = text

    def convert_to_bytes(self):
        arrays = bytes(self.text, 'utf-8')

        for array in arrays:
            print(array, end='')

letters = input('Enter a string of text:')
food = string_to_bytes(letters)
print(food.convert_to_bytes())