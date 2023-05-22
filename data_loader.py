from utils import *


# 당첨번호를 원핫인코딩벡터(ohbin)으로 변환
def numbers2ohbin(numbers):

    ohbin = np.zeros(45) #45개의 빈 칸을 만듬

    for i in range(6): #여섯개의 당첨번호에 대해서 반복함
        ohbin[int(numbers[i])-1] = 1 #로또번호가 1부터 시작하지만 벡터의 인덱스 시작은 0부터 시작하므로 1을 뺌
    
    return ohbin

# 원핫인코딩벡터(ohbin)를 번호로 변환
def ohbin2numbers(ohbin):

    numbers = []
    
    for i in range(len(ohbin)):
        if ohbin[i] == 1.0: # 1.0으로 설정되어 있으면 해당 번호를 반환값에 추가한다.
            numbers.append(i+1)
    
    return numbers


def data_loader() -> list:
    """
    list -> [x_samples, y_samples, train_idx, val_idx]
    """
    db = CRUD()
    # DB에서 데이터 불러오기
    data = db.readDB(schema='public',table='LottoHistory',colum='lotto_times, num1, num2, num3, num4, num5, num6, bonus, draw_time, create_time, winning_amount, winner_count, sales_amount')
    dataframe_lotto = pd.DataFrame(data, columns=['lotto_times', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus', 'draw_time', 'create_time', 'winning_amount', 'winner_count', 'sales_amount'])

    # Pandas table에서 실제 사용할 데이터만 선택
    dataframe_actual = dataframe_lotto.loc[:,['num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus', 'winning_amount', 'winner_count', 'sales_amount']]

    # 전체 row 길이
    row_count = len(dataframe_actual)

    # 원핫 인코딩 적용
    numbers = dataframe_actual.loc[:, ['num1', 'num2', 'num3', 'num4', 'num5', 'num6']].to_numpy(int)
    ohbins = list(map(numbers2ohbin, numbers))

    x_samples = ohbins[0:row_count-1]
    y_samples = ohbins[1:row_count]

    # 데이터 나누기
    train_idx = (0, int(row_count*0.9))
    val_idx = (int(row_count*0.9)+1, len(x_samples))

    return [x_samples, y_samples, train_idx, val_idx]