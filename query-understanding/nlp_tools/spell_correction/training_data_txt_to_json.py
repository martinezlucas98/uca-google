import json
def word_frecuency_of_crea_total():
    print("obteniendo datos....")
    word_frequency = {} # {'hola': 1232332, 'el': 1203033}
    with open('./dataset/spanish_words_frequency.txt', 'r', encoding='latin-1' ) as spanish_file:
        all_lines = spanish_file.read()
        separate_in_lines = all_lines.split('\n')[1:]
    
        
        for line in separate_in_lines:
            tokens_of_the_line = line.split()
            word = tokens_of_the_line[1]
            frecuency_of_the_word = int(tokens_of_the_line[2].replace(',', ''))
            
            if(frecuency_of_the_word < 100):
                break

            word_frequency[word] = frecuency_of_the_word


    with open("./dataset/training_data_spanish.json", "w") as outfile:
        json.dump (word_frequency, outfile, indent=4)

        
      
word_frecuency_of_crea_total()  


