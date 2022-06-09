from urllib import response
import requests, json

headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

def autocomplete_gpp(sentence = ''):
    """
    For now this function scrap from google scholare autocomplete results and return it
    """
    # client param could be replaced with firefox or other browser
    url = "https://scholar.google.com/scholar_complete?q=" + sentence + "&hl=es&as_sdt=0%2C5&btnG="
    response = requests.get(url, headers=headers)


    return json.loads(response.text)['l']
    
   

if __name__ == "__main__":
    print(autocomplete_gpp(sentence="hola"))
    print(autocomplete_gpp(sentence="estudiantes"))
    print(autocomplete_gpp(sentence="horarios de o"))
    print(autocomplete_gpp(sentence=""))
