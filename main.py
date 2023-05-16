from flask import Flask, jsonify, request
import platform
import random
import sys
import os




linux = "tgpt \"__q__\"  > __reply__"
CUR = []


def install_tgpt():
    os.system("curl -sSL https://raw.githubusercontent.com/aandrew-me/tgpt/main/install | bash -s /usr/local/bin")

if not os.path.exists("/usr/local/bin/tgpt"):
    install_tgpt()


def run_id():
    global CUR
    while True:
        r =  random.randint(999999,999999999999)
        if r not in CUR:
            CUR.append(r)
            return r


def read_reply(id_):
    f = open("." + str(id_), "r")
    txt  = f.read()
    f.close()
    
    os.remove("." + str(id_))

    txt = txt.split("\n")
    
    new = ""
    n = 0
    for e in txt:
        if e != '':
            new +=  e
        else:
            new += "\n"

    return new[:-1]


def generate(q):
    id_ = run_id()
    os.system(linux.replace("__q__", q).replace("__reply__", "." + str(id_) ))
    rep = read_reply(id_)
    CUR.remove(id_)
    rep = rep.replace("\n\u28fe", "")
    for e in "Loading\u28fd Loading\u28fb Loading\u28bf Loading\u287f Loading\u28df Loading\u28ef Loading\u28f7 Loading\u28fe Loading\n".split(" "):
        rep =  rep.replace(e, "")
    
    while rep.startswith(" "):
        rep = rep[1:]

    return rep

app = Flask(__name__)

@app.route('/generate')
def gen():
    data = generate(request.headers['prompt'].replace('"', "'"))
    return jsonify({'return': data})


app.run()

