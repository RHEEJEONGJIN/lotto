import pandas as pd 
import requests 
from tqdm import tqdm
import json 

def getLottoWinInfo(minDrwNo, maxDrwNo): 
    drwtNo1 = [] 
    drwtNo2 = [] 
    drwtNo3 = [] 
    drwtNo4 = [] 
    drwtNo5 = [] 
    drwtNo6 = []
    bnusNo = [] 
    totSellamnt = [] 
    drwNoDate = [] 
    firstAccumamnt = [] 
    firstPrzwnerCo = [] 
    firstWinamnt = [] 
    
    for i in tqdm(range(minDrwNo, maxDrwNo+1, 1)):  # tqdm : 시간의 경과에 따라 진행률 보여줌
        req_url = "http://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i) 
        req_lotto = requests.get(req_url)
        lottoNo = req_lotto.json() 
        drwtNo1.append(lottoNo['drwtNo1']) 
        drwtNo2.append(lottoNo['drwtNo2']) 
        drwtNo3.append(lottoNo['drwtNo3']) 
        drwtNo4.append(lottoNo['drwtNo4']) 
        drwtNo5.append(lottoNo['drwtNo5']) 
        drwtNo6.append(lottoNo['drwtNo6']) 
        bnusNo.append(lottoNo['bnusNo']) 
        totSellamnt.append(lottoNo['totSellamnt']) 
        drwNoDate.append(lottoNo['drwNoDate']) 
        firstAccumamnt.append(lottoNo['firstAccumamnt']) 
        firstPrzwnerCo.append(lottoNo['firstPrzwnerCo']) 
        firstWinamnt.append(lottoNo['firstWinamnt']) 
        lotto_dict = {#"추첨일":drwNoDate, 
                      "Num1":drwtNo1, 
                      "Num2":drwtNo2, 
                      "Num3":drwtNo3, 
                      "Num4":drwtNo4, 
                      "Num5":drwtNo5, 
                      "Num6":drwtNo6, 
                      "bnsNum":bnusNo 
                      #"총판매금액":totSellamnt, 
                      #"총1등당첨금":firstAccumamnt, 
                      #"1등당첨인원":firstPrzwnerCo, 
                      #"1등수령액":firstWinamnt
                        } 
        
    df_lotto = pd.DataFrame(lotto_dict) 
    return df_lotto



#### pd.read_csv("lotto_win_info.csv")

lotto_df = getLottoWinInfo(1, 923)

lotto_df.to_csv("lotto.csv", index=False)