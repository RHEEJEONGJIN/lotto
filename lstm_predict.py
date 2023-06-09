from utils import *
from data_loader import data_loader


# 번호 뽑기
def gen_numbers_from_probability(nums_prob):

    ball_box = []

    for n in range(45):
        ball_count = int(nums_prob[n] * 100 + 1)
        ball = np.full((ball_count), n+1) #1부터 시작
        ball_box += list(ball)

    selected_balls = []

    while True:
        
        if len(selected_balls) == 6:
            break
        
        ball_index = np.random.randint(len(ball_box), size=1)[0]
        ball = ball_box[ball_index]

        if ball not in selected_balls:
            selected_balls.append(ball)

    return selected_balls


def predict_lstm():
    # 데이터 로드
    x_samples, y_samples, train_idx, val_idx = data_loader()

    model = tf.keras.models.load_model("models/lstm.h5")

    xs = x_samples[-1].reshape(1, 1, 45)
    ys_pred = model.predict_on_batch(xs)
    # print(ys_pred[0])
    numbers = gen_numbers_from_probability(ys_pred[0])
    numbers.sort()

    print('receive numbers', numbers)

    tf.keras.backend.clear_session()

    return numbers


if __name__ == "__main__":
    predict_lstm()