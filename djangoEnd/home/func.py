import os
import time
import subprocess
import threading
import pickle
import pandas as pd
import json

scriptDir = os.path.abspath(os.path.dirname(__file__))
fileName = '/capture.csv'
capFile = scriptDir + fileName

def packetCap():
    # params ---
    password='letmein'
    iface='wlan0'
    # secs=10 # add -a duration:{secs} to $cmd

    cmd = f"echo {password} | sudo -S tshark -T fields -e frame.number -e frame.time -e frame.len -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -e ip.len -e tcp.len -e tcp.srcport -e tcp.dstport -e _ws.col.Info -E header=y -E separator=\"$\" -E quote=n -E occurrence=f > {capFile} -i {iface}"
    proc = subprocess.run([cmd], shell=True)
	# p = subprocess.run(cmd, shell=True)
    print(proc)

def readCaptured(capFile):
    with open(capFile, "r") as f:
        data = f.read().splitlines()
    return data


def makeItLive(capFile, period=1):
    data = readCaptured(capFile)
    while True:
        time.sleep(period)
        new_data = readCaptured(capFile)
        yield new_data[len(data):]
        data = new_data

def analyzePackets():
    # previous values to check if attack logging is being repeated
    prev_mac_source = ''
    prev_mac_dest = ''
    prev_prediction = 0
    scanDict = {}

    # attack type dictionary - key -> prediction, value -> attack type
    attack_type = {
        0: 'Normal',
        1: 'Wrong Setup',
        2: 'DDOS',
        3: 'Data Type Probing',
        4: 'Scan Attack',
        5: 'MITM'
    }

    # specify file name of machine learning model - pickle file
    filename = 'nbad_model'
    infile = open(filename, 'rb')
    rf_model = pickle.load(infile)

    # Returns the Path your .py file is in
    # workpath = os.path.dirname(os.path.abspath(__file__))
    # logfile = open(os.path.join(workpath, "capture.csv"), "r")

    x = makeItLive(capFile)

    for lines in x:
        # while(len([lines for lines in x]) <= 1):
        # continue
        # lines will be a list of new lines added at the end
        # Analyze and use modedata=pd.read_csv(line ,encoding='unicode_escape')
        # data=pd.read_csv(lines, encoding='unicode_escape')
        # lines = data.head()
        lines = lines[1:]
        for line in lines:
            # text = line.decode(errors='replace')
            # line = str.encode('utf-8').strip()
            line = line.rstrip("\n")[1:]
            returnLog = line  # storing in temp var to return as log
            # line = line.strip()
            line = line.split('$')
            # print(line)
            # line contains data separated with $
            # the number of columns is 13
            # however some dataframes will show len < 13 because the data is written incompletely by tshark
            # every few seconds 1 dataframe will be dropped

            if len(line) == 13:  # ----------------------------------------------------------- data cleaning

                line[1] = line[1].split(' ')[3].replace(':', '').replace('.', '')  # pre time
                line[3] = int(line[3].replace(':', ''), 16)  # pre eth src
                line[4] = int(line[4].replace(':', ''), 16)  # pre eth dst
                try:
                    line[5] = float(line[5].replace('.', ''))  # pre ip src
                except Exception as ex:
                    line[5] = 0
                try:
                    line[6] = float(line[6].replace('.', ''))  # pre ip dst
                except Exception as ex:
                    line[6] = 0
                try:
                    line[7] = int(line[7])  # pre protocol
                except Exception as ex:
                    line[7] = -1
                try:
                    line[8] = int(line[8])  # pre ip length
                except Exception as ex:
                    line[8] = 0
                try:
                    line[9] = int(line[9])  # tcp length
                except Exception as ex:
                    line[9] = 0
                try:
                    line[10] = int(line[10])  # tcp source port
                except Exception as ex:
                    line[10] = 0
                try:
                    line[11] = int(line[11])  # tcp destination port
                except Exception as ex:
                    line[11] = 0
                value = -99

                # ------------------------------------------------------------------------ data preprocessing

                if(line[-1].startswith("GET / HTTP/1.1 ")):  # NORMAL DATA
                    value = -99

                elif (line[-1].startswith("GET")):  # WRONG SETUP / DATA TYPE PROBING
                    a = line[-1].split("=")
                    try:  # if = hasn't been read, index 1 doesn't exist
                        b = (a[1].split(" "))
                        try:
                            # check if float data is sent, if string it is data type probing
                            value = float(b[0])
                        except Exception as ex:
                            value = -3
                    except Exception as ex:
                        value = -99

                elif(line[-1].startswith("Echo")):  # DDOS
                    value = -2

                elif (line[-1].startswith("Who")):  # SCAN
                    ethSrc = line[3]
                    timeStamp = int(line[1])
                    if ethSrc in scanDict:  # check if eth src in scan dict
                        # if yes, check if time diff is greater than 2 sec
                        if timeStamp - scanDict[ethSrc][0] > 2000000000 and scanDict[ethSrc][1] > 150:
                            value = -4  # scan attack detected
                            # update timestamp and frequency
                            scanDict[ethSrc] = [timeStamp, 0]
                        else:  # if diff less than 2 sec
                            scanDict[ethSrc][1] += 1  # update frequency
                    else:  # eth src not in scanDict
                        value = -99  # pass - reduntant detection
                        # create dict record for eth src with time stamp, frequency as value
                        scanDict[ethSrc] = [timeStamp, 0]

                elif "duplicate " in line[-1]:  # MITM
                    value = -5
                else:
                    value = -99
                line[-1] = value

                # ------------------------------------------------------------------------ prediction

                # ip_df = pd.DataFrame([line[1:]])
                ip_df = pd.DataFrame([line[1:]])
                # print(ip_df)
                prediction = rf_model.predict(ip_df)[0]
                # print(prediction)
                # print(attack_type[prediction])

                # append a row of value and prediction to the resultfile.csv - used for classification report
                # csv_writer.writerow([value_to_label.get(value, 0), prediction])

                if prediction != 0:
                    # print('attack: ' + str(prediction))
                    # still a string to this point
                    returnLog = returnLog.split('$')

                    # check if attack is being repeated for same mac source and dest
                    if not (prev_mac_source == returnLog[3] and prev_mac_dest == returnLog[4] and prev_prediction == prediction):

                        text_data=json.dumps({
                            'attack.type': attack_type[prediction],
                            'frame.number': returnLog[0],
                            'frame.time': returnLog[1],
                            'frame.len': returnLog[2],
                            'eth.src': returnLog[3],
                            'eth.dst': returnLog[4],
                            'ip.src': returnLog[5],
                            'ip.dst': returnLog[6],
                            'ip.proto': returnLog[7],
                            'ip.len': returnLog[8],
                            'tcp.len': returnLog[9],
                            'tcp.srcport': returnLog[10],
                            'tcp.dstport': returnLog[11],
                            '_ws.col.Info': returnLog[12]
                        })
                        # set prev values - to prevent overloading of front end
                        # print(attack_type[prediction])
                        print(text_data)
                        prev_mac_source = returnLog[3]
                        prev_mac_dest = returnLog[4]
                        prev_prediction = prediction

if __name__ == '__main__':
    tshark_thread = threading.Thread(target=packetCap, name='tshark')
    tshark_thread.start()
    time.sleep(2)
    analyzePackets()
