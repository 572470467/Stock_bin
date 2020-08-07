from flask import Flask, jsonify
import time
import random
app = Flask(__name__)
zt=[([0,1,0,1,1],[1,1,0,1,0]),([0,1,0,1,1],[0,1,0,0,1]),([1,1,1,0,0],[1,0,1,1,1]),([1,0,1,1,0],[1,1,0,1,0])]
icon=[{'CSD':[1,1,1,1],'ZD':[0,0,0,0],'QG':[0,0],'XZT':[0,0]},{'CSD':[0,0,0,0],'ZD':[1,1,1,1],'QG':[0,0],'XZT':[0,0]},{'CSD':[0,0,0,0],'ZD':[0,0,0,0],'QG':[1,1],'XZT':[1,1]}]
releasestart = {'a':0, 'b':0}
releaseend = {'a':0, 'b':0}
releaseactive = {'a': False, 'b': False}
def CSV():
    for i in range(4):
        time.sleep(1)
        print(i)

def random_status():
    m=random.randrange(4)
    d=zt[m]
    return d

def Icon():
    m=random.randrange(3)
    d=icon[m]
    return d

@app.route('/level')
def group_b():
    d=random_status()
    return jsonify(d)

@app.route('/scale/<groupid>')
def scale_read(groupid):
    if groupid in releasestart.keys():
        if releaseactive[groupid]:
            amt = time.time() - releasestart[groupid]
            #print(time.time()-releasestart[groupid])
        else:
            amt = releaseend[groupid] - releasestart[groupid]
            #print(releasestart[groupid])
        d = {'status': 'OK', 'reading': amt, 'started':releasestart[groupid]}
    else:
        d = {'status': 'Error', 'reading': -1, 'started': -1}
    return jsonify(d)

@app.route('/measure/<cs>/<ms>')
def measure_read(cs,ms):
    if ms!=0:
        return str(CSV())

@app.route('/icon')
def op_mix_status():
    d=Icon()
    return jsonify(d)
    #return str(Icon())
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)


