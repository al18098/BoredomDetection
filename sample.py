import serial
import pygame.mixer
import time

hima = 0
BPM = 0
IBI = 0
BPM_prev = 0
IBI_prev = 0
checker = 0
pNN_n = 0
pNN_C = 0
datalist = 0
pNN_aver = 0.0
pNN_data = []
pNN_index = []

music = ["Music/曲1.mp3",
        "Music/曲2.mp3",
        "Music/曲3.mp3"]
music_list = 0

def map_range(value, start1, stop1, start2, stop2):
    return (value -start1) / (stop1 - start1) * (stop2 - start2) + start2

ser = serial.Serial('COM5', 115200)

while(1):
    seris = ser.readline()
    ses = seris.decode('utf-8')
    if(ses[0] == 'S'):
        sensor = float(ses[1:4])
    if(ses[0] == 'B'):
        BPM = float(ses[1:4])
        #print(BPM)
    if(ses[0] == 'Q'):
        IBI = float(ses[1:4])
        #print(IBI)
    

    if(BPM >= 200):
        BPM = 200
    

    if(BPM != 0 and IBI != 0):
        if(BPM == BPM_prev and IBI == IBI_prev):
            checker = 1
        if(checker != 1):
            if(BPM_prev != 0 and IBI_prev != 0):
                pNN_n = IBI - IBI_prev
                if(pNN_C != 30):
                    if(pNN_n * pNN_n >= 2500):
                        pNN_data.append(1)
                    else:
                        pNN_data.append(0)
                    pNN_C += 1
                if(pNN_C == 30):
                    if(pNN_n * pNN_n >= 2500):
                        del pNN_data[0]
                        pNN_data.append(1)
                    else:
                        del pNN_data[0]
                        pNN_data.append(0)
                    datalist = 1
                if(datalist == 1):
                    i = 0
                    while(i < 30):
                        pNN_aver = pNN_aver + pNN_data[i]
                        i+=1
                    pNN_aver = pNN_aver / 30.0
                    print('{:.9f}'.format(pNN_aver))

                    if(pNN_aver >= 0.3):
                        print('confortable')
                        hima += 1
                    if(pNN_aver < 0.3):
                        print('unconfortable')
                        hima = 0
                    pNN_index.append(pNN_aver)
                    if(hima == 150):
                        # mixerモジュールの初期化
                        pygame.mixer.init()
                        # 音楽ファイルの読み込み
                        pygame.mixer.music.load(music[music_list])
                        # 音楽再生、および再生回数の設定(-1はループ再生)
                        pygame.mixer.music.play(-1)

                        time.sleep(60)
                        # 再生の終了
                        pygame.mixer.music.stop()
                        hima=0
                        music_list += 1
                        if music_list == len(music) :
                            music_list = 0
                        
                    
                    
            IBI_prev = IBI
            BPM_prev = BPM
        checker = 0
    



    time.sleep(0.015)