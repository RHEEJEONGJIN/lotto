from utils import *
from data_loader import data_loader


def train_lstm():
    # 데이터 로드
    x_samples, y_samples, train_idx, val_idx = data_loader()

    # 모델을 정의합니다.
    model = keras.Sequential([
        keras.layers.LSTM(128, batch_input_shape=(1, 1, 45), return_sequences=False, stateful=True),
        keras.layers.Dense(45, activation='sigmoid')
    ])

    # 모델을 컴파일합니다.
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

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

if __name__ == "__main__":
    train_lstm()