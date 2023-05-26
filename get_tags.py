from get_tags_google import get_tags_google
from get_tags_clarifai import get_tags_clarifai
from googletrans import Translator


translator = Translator()

def main(file_path):
    # Pass the file path to the scripts and get their output
    output1 = get_tags_google(file_path)
    output2 = get_tags_clarifai(file_path)

    # Combine the two dictionaries
    combined = {**output1, **output2}

    # Sort the items in the combined dictionary by value in descending order
    sorted_items = sorted(combined.items(), key=lambda item: item[1], reverse=True)

    # Print the sorted items
    for word, score in sorted_items:
        try:
            translation = translator.translate(word, dest='ru')
            print(f'{translation.text}: {score}')
        except Exception as e:
            try:
                translation = translator.translate(word, dest='ru')
                print(f'{translation.text}: {score}')
            except Exception as e:
                print(f'{word}: {score}')  # Print the word and score without translation

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <file_path>', file=sys.stderr)
        sys.exit(1)

    main(sys.argv[1])
