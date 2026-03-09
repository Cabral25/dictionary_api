

dictionary = {'word': 'casa', 'meaning': 'estrutura para habitação', 'examples': ''}
dictionary_updated = {'word': 'casa', 'meaning': 'estrutura para morar', 'examples': ''}

for key, value in dictionary_updated.items():
    setattr(dictionary, key, value)

print(dictionary.get('meaning'))