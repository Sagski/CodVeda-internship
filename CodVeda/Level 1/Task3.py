filename = input("Enter the file name you want to count the words of in .txt: ")

try:
  content = open(filename, 'r')
  words = content.read().split()
  word_count = len(words)
  content.close()
  print(f"The number of words in the file is: {word_count}")

except FileNotFoundError:
    print("The file was not found. Please check the file name and try again.")