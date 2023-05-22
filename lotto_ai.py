from utils import *
from data_loader import data_loader


class Lotto:
    def __init__(self) -> None:
        self.x_samples, self.y_samples, self.train_idx, self.val_idx = data_loader()
        self.model = tf.keras.models.load_model("models/lstm.h5")


    def clear_cache(self) -> None:
        tf.keras.backend.clear_session()


    def reload_data(self) -> None:
        """
        데이터 다시 로드
        """
        self.x_samples, self.y_samples, self.train_idx, self.val_idx = data_loader()
    

    def train(self) -> None:
        # 데이터 로드
        x_samples, y_samples, train_idx, val_idx = self.x_samples, self.y_samples, self.train_idx, self.val_idx

        # 모델을 정의합니다.
        model = keras.Sequential([
            keras.layers.LSTM(128, batch_input_shape=(1, 1, 45), return_sequences=False, stateful=True),
            keras.layers.Dense(45, activation='sigmoid')
        ])

        # 모델을 컴파일합니다.
        opt = tf.keras.optimizers.experimental.AdamW(
            learning_rate=0.001,
            weight_decay=0.004,
        )
        model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

        # 매 에포크마다 훈련과 검증의 손실 및 정확도를 기록하기 위한 변수
        train_loss = []
        train_acc = []
        val_loss = []
        val_acc = []

        # 최대 100번 에포크까지 수행
        for epoch in tqdm(range(200)):

            model.reset_states() # 중요! 매 에포크마다 1회부터 다시 훈련하므로 상태 초기화 필요

            batch_train_loss = []
            batch_train_acc = []
            
            for i in range(train_idx[0], train_idx[1]):
                
                xs = x_samples[i].reshape(1, 1, 45)
                ys = y_samples[i].reshape(1, 45)
                
                loss, acc = model.train_on_batch(xs, ys) #배치만큼 모델에 학습시킴

                batch_train_loss.append(loss)
                batch_train_acc.append(acc)

            train_loss.append(np.mean(batch_train_loss))
            train_acc.append(np.mean(batch_train_acc))

            batch_val_loss = []
            batch_val_acc = []

            for i in range(val_idx[0], val_idx[1]):

                xs = x_samples[i].reshape(1, 1, 45)
                ys = y_samples[i].reshape(1, 45)
                
                loss, acc = model.test_on_batch(xs, ys) #배치만큼 모델에 입력하여 나온 답을 정답과 비교함
                
                batch_val_loss.append(loss)
                batch_val_acc.append(acc)

            val_loss.append(np.mean(batch_val_loss))
            val_acc.append(np.mean(batch_val_acc))

            print('epoch {0:4d} train acc {1:0.3f} loss {2:0.3f} val acc {3:0.3f} loss {4:0.3f}'.format(epoch, np.mean(batch_train_acc), np.mean(batch_train_loss), np.mean(batch_val_acc), np.mean(batch_val_loss)))

        model.save("models/lstm.h5")
        
        tf.keras.backend.clear_session()

        self.model = tf.keras.models.load_model("models/lstm.h5")


    def predict(self) -> list:
        x_samples = self.x_samples

        xs = x_samples[-1].reshape(1, 1, 45)
        ys_pred = self.model.predict_on_batch(xs)

        numbers = self.gen_numbers_from_probability(ys_pred[0])
        numbers.sort()

        print('receive numbers', numbers)

        return numbers
    

    def gen_numbers_from_probability(self, nums_prob : list) -> list:

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