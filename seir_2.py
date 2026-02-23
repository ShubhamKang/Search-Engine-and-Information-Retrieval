import sys
from bs4 import BeautifulSoup
import urllib.request


def fetching_page(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req)
    return page.read()

def fetching_body(page_data):
    if page_data.body:
        body_content = page_data.body
        text_parts = body_content.stripped_strings
        body_text = " ".join(text_parts)
        # print(body_text)
        return body_text
    else:
        return ""
    
def word_frequency_counter(page_data):
    word_freq_dict = {}
    if page_data is None:
        return {}
    
    page_data = page_data.lower()
    words_list = page_data.split()

    for words in words_list:
        updated_word = ""

        for ch in words:
            if ch.isalnum():
                updated_word+=ch
        if updated_word != "":
            if updated_word in word_freq_dict:
                word_freq_dict[updated_word] +=1
            else:
                word_freq_dict[updated_word] = 1

    return word_freq_dict   

def hashcode_generation(word):
    m = (2)**(64)
    p = 53
    hash_value = 0
    for i in range(len(word)):
        char_v = ord(word[i]) * (p**i)
        hash_value += char_v
    hash_value = hash_value % m

    bin_repre = format(hash_value, "064b")
    return bin_repre

def simhash_generation(word_freq_dict):
    initial_vec = [0]*64

    stopping_words_set = {'his', 'needn', 'the', 're', 'for', "they've", 'do', 'an', 'under', 'on', 'our', 'having', 'myself', 'these', 'theirs', "shouldn't", 'at', "we'd", 'don', 'a', 'out', "he'll", 'and', "weren't", 'some', "mustn't", 'more',
    'they', 'y', 'doesn', 'while', 'what', 'any', "i'm", 'as', 'over', "they're", 'into', 'couldn', 'were', "couldn't", 'did', 'will', 'then', 'hadn', 'won', 'yourselves', 'with', 'once', "didn't", 'their', 'up', 'it', 'am', 
    'other', 'doing', "needn't", 'if', "she's", "you'll", "should've", 'shouldn', 'again', 'ma', 'herself', "aren't", 'now', 'or', 'himself', 'wasn', 'your', 'yours', "don't", 'me', 'ours', "it'd", "they'd", "isn't", 'can', 
    'them', "hadn't", "i'd", "she'd", 'was', "i'll", 'against', 'itself', 'off', 'down', 'be', 'isn', 'aren', 'her', 'not', 'ourselves', 'him', 'but', 'of', 't', 'those', 'wouldn', 'where', 'below', 'after', 's', "that'll", 
    "they'll", "i've", 'when', 'hers', "she'll", 'been', 'until', 'ain', 'through', 'than', 'just', 'we', 'why', 'mustn', "doesn't", 'shan', 'because', 'weren', 'i', "mightn't", 'he', 'between', 'before', "he'd", 'my', "we're", 
    "you'd", 'should', 'this', 'she', "wasn't", 'who', 'yourself', "it'll", 'about', 'whom', 'hasn', 'very', 'by', 'only', 'both', 'had', 'there', 'in', 'o', 'has', 'further', 'here', 'haven', 'such', 'so', 've', 'didn', 'its',
    'from', 'is', "he's", 'does', 'm', "it's", "won't", 'same', "shan't", "we'll", 'being', 'have', 'most', "you've", 'few', "haven't", 'how', 'nor', 'mightn', 'are', "wouldn't", 'themselves', "hasn't", 'to', 'll', 'you', 'too',
    'during', 'which', "you're", 'own', 'd', 'above', 'each', 'all', 'no', "we've", 'that'}  

    for word in word_freq_dict:
        if word in stopping_words_set:
            continue
        else:
            freq = word_freq_dict[word]
            hash_val = hashcode_generation(word)

            for i in range(64):
                if hash_val[i] == '1':
                    initial_vec[i] += freq
                else:
                    initial_vec[i] -= freq

    simhash_list = []
    for i in initial_vec:
        if i > 0:
            simhash_list.append('1')
        else:
            simhash_list.append('0')
    simhash = "".join(simhash_list)
    return simhash

def counting_common_bits(simhash_1,simhash_2):
    common_bits = 0
    for i in range(64):
        if simhash_1[i] == simhash_2[i]:
            common_bits+=1
    return common_bits


if len(sys.argv) < 3:
    print("Enter the two url's in the command line")
    sys.exit()
else:
    url_1 = sys.argv[1]
    url_2 = sys.argv[2]

try:

    html_text_1 = fetching_page(url_1)
    html_text_2 = fetching_page(url_2)

    web_page_data_1 = BeautifulSoup(html_text_1,'html.parser')
    web_page_data_2 = BeautifulSoup(html_text_2,'html.parser')

    body_text_1 = fetching_body(web_page_data_1)
    body_text_2 = fetching_body(web_page_data_2)

    freq_dict_1 = word_frequency_counter(body_text_1)
    freq_dict_2 = word_frequency_counter(body_text_2)

    simhash_url_1 = simhash_generation(freq_dict_1)
    simhash_url_2 = simhash_generation(freq_dict_2)

    common_bits = counting_common_bits(simhash_url_1,simhash_url_2)

    print(common_bits)



except Exception as e:
    print("Error occured while scrapping", e)
