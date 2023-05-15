import json 
import time
import requests
import pandas as pd 
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime, timezone

from database_crud import CRUD
db = CRUD()


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
    # firstWinamnt = [] 
    
    for i in tqdm(range(minDrwNo, maxDrwNo+1, 1)):  # tqdm : 시간의 경과에 따라 진행률 보여줌
        now =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        req_url = "https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo=" + str(i)
        req_html = requests.get(req_url)
        req_soup = BeautifulSoup(req_html.text, 'html.parser')
        req_data = req_soup.find('div', {'class': 'win_result'})
        lottoTimes = req_data.findAll('h4')[0].text.split("회")[0]

        req_api_url = "http://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i) 
        req_api_lotto = requests.get(req_api_url)
        lottoNo = req_api_lotto.json() 
        drwtNo1 = lottoNo['drwtNo1']
        drwtNo2 = lottoNo['drwtNo2']
        drwtNo3 = lottoNo['drwtNo3']
        drwtNo4 = lottoNo['drwtNo4']
        drwtNo5 = lottoNo['drwtNo5']
        drwtNo6 = lottoNo['drwtNo6']
        bnusNo = lottoNo['bnusNo']
        totSellamnt = lottoNo['totSellamnt']
        drwNoDate = datetime.strptime(f"{lottoNo['drwNoDate']} 00:00:00", '%Y-%m-%d %H:%M:%S')
        firstAccumamnt = lottoNo['firstAccumamnt']
        firstPrzwnerCo = lottoNo['firstPrzwnerCo']
        # firstWinamnt = lottoNo['firstWinamnt']

        # lotto_dict = {
        #     "lotto_times":lottoTimes,
        #     "draw_time":drwNoDate, 
        #     "num1":drwtNo1, 
        #     "num2":drwtNo2, 
        #     "num3":drwtNo3, 
        #     "num4":drwtNo4, 
        #     "num5":drwtNo5, 
        #     "num6":drwtNo6, 
        #     "bonus":bnusNo,
        #     "sales_amount":totSellamnt, 
        #     "winning_amount":firstAccumamnt, 
        #     "winner_count":firstPrzwnerCo, 
        #     # "1등수령액":firstWinamnt,
        #   } 
        # print(f'{lottoTimes}, {drwtNo1}, {drwtNo2}, {drwtNo3}, {drwtNo4}, {drwtNo5}, {drwtNo6}, {bnusNo}, TIMESTAMP \'{drwNoDate}\', TIMESTAMP \'{now}\', {firstAccumamnt}, {firstPrzwnerCo}, {totSellamnt}')
        # break

        db.insertDB(
            schema='public',
            table='LottoHistory',
            colum='lotto_times, num1, num2, num3, num4, num5, num6, bonus, draw_time, create_time, winning_amount, winner_count, sales_amount',
            data=f'{lottoTimes}, {drwtNo1}, {drwtNo2}, {drwtNo3}, {drwtNo4}, {drwtNo5}, {drwtNo6}, {bnusNo}, TIMESTAMP \'{drwNoDate}\', TIMESTAMP \'{now}\', {firstAccumamnt}, {firstPrzwnerCo}, {totSellamnt}'
        )
        time.sleep(0.5)

    # df_lotto = pd.DataFrame(lotto_dict) 
    # return df_lotto


def total_croling():
    latest_url = "https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo="
    latest_html = requests.get(latest_url)
    latest_soup = BeautifulSoup(latest_html.text, 'html.parser')
    latest_data = latest_soup.find('div', {'class': 'win_result'})
    latest_time = latest_data.findAll('h4')[0].text.split("회")[0]
    print('latest_time', latest_time)
    getLottoWinInfo(1, int(latest_time))


def latest_croling():
    latest_url = "https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo="
    latest_html = requests.get(latest_url)
    latest_soup = BeautifulSoup(latest_html.text, 'html.parser')
    latest_data = latest_soup.find('div', {'class': 'win_result'})
    latest_time = latest_data.findAll('h4')[0].text.split("회")[0]
    print('latest_time', latest_time)
    getLottoWinInfo(int(latest_time), int(latest_time))


if __name__ == "__main__":
    latest_croling()
