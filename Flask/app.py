from flask import Flask, render_template, request
import numpy as np 
import pandas as pd 
import math
import seaborn as sns
from urllib.parse import urlparse
from tld import get_tld
import os.path
import re
import pickle

app = Flask(__name__)
app.config['SECRET_KEY']='marox';


@app.route("/")

def home():
    return render_template("index.html")


def entropy(url):
    string = url.strip()
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy = sum([(p * math.log(p) / math.log(2.0)) for p in prob])
    return entropy

#First Directory Length
def fd_length(url):
    urlpath= urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0
    
def tld_length(tld):
    try:
        return len(tld)
    except:
        return -1
    
def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits

def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters

def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')

def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        
        return -1
    else:
       
        return 1
    
def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return -1
    else:
        return 1
    
def suspicious_words(url):
    match = re.search('PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr',
                      url)
    if match:
        return 1
    else:
        return 0
    
def get_features(url):
    urls = []
    url = str(url)
    urls.append(url)
    df = pd.DataFrame(columns=["link"])
    df["link"] = urls
    df["entropy"] = df['link'].apply(lambda i:entropy(i))
    df['url_length'] = df['link'].apply(lambda i: len(str(i)))
    df['hostname_length'] = df['link'].apply(lambda i: len(urlparse(i).netloc))
    df['path_length'] = df['link'].apply(lambda i: len(urlparse(i).path))
    df['fd_length'] = df['link'].apply(lambda i: fd_length(i))
    df['tld'] = df['link'].apply(lambda i: get_tld(i,fail_silently=True))
    df['tld_length'] = df['tld'].apply(lambda i: tld_length(i))
    df['count-'] = df['link'].apply(lambda i: i.count('-'))
    df['count@'] = df['link'].apply(lambda i: i.count('@'))
    df['count?'] = df['link'].apply(lambda i: i.count('?'))
    df['count%'] = df['link'].apply(lambda i: i.count('%'))
    df['count.'] = df['link'].apply(lambda i: i.count('.'))
    df['count='] = df['link'].apply(lambda i: i.count('='))
    df['count#'] = df['link'].apply(lambda i: i.count('#'))
    df['count+'] = df['link'].apply(lambda i: i.count('+'))
    df['count$'] = df['link'].apply(lambda i: i.count('$'))
    df['count!'] = df['link'].apply(lambda i: i.count('!'))
    df['count*'] = df['link'].apply(lambda i: i.count('*'))
    df['count,'] = df['link'].apply(lambda i: i.count(','))
    df['count//'] = df['link'].apply(lambda i: i.count('//'))
    df['count-http'] = df['link'].apply(lambda i : i.count('http'))
    df['count-https'] = df['link'].apply(lambda i : i.count('https'))
    df['count-www'] = df['link'].apply(lambda i: i.count('www'))
    df['count-digits']= df['link'].apply(lambda i: digit_count(i))
    df['count-letters']= df['link'].apply(lambda i: letter_count(i))
    df['count_dir'] = df['link'].apply(lambda i: no_of_dir(i))
    df['use_of_ip'] = df['link'].apply(lambda i: having_ip_address(i))
    df['short_url'] = df['link'].apply(lambda i: shortening_service(i))
    df['sus_url'] = df['link'].apply(lambda i: suspicious_words(i))
    df = df.drop(['link','url_length','tld','short_url',], axis=1)
    
    return df                   



@app.route('/model', methods=['GET','POST'])
def model():
    url = request.form['search']
    
    results = get_features(url)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
        
    df = scaler.transform(results)

    with open('best_model_pkl', 'rb') as pickle_file:
         model_pkl = pickle.load(pickle_file)
         
    pos=0
    neg=0
    pred=model_pkl.predict(df)
    print(pred)
    if(pred==0):    
        pos=pos+1
    if(pred==1):
         neg=neg+1

    if(pos>neg):    
        res="URL seems to be safe"
    else:
        res="URL seems to be not safe"    
    
    return render_template("index.html",Result=res)
    
if __name__ == "__main__":
    
    
    app.run()