from googletrans import Translator

translator = Translator()
def translate_word(word):
    try:
        translation = translator.translate(word, dest='ru')
        return translation.text
    except Exception as e:
        try:
            translation = translator.translate(word, dest='ru')
            return translation.text
        except Exception as e:
            print(f'failed translate: {word}: {score}')  
    return ""
