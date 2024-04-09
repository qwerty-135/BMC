from torch import nn

INPUT_SIZE = 21
HIDDEN_SIZE = 40
# BATCH_SIZE = 20
OUTPUT_SIZE = 1
EPOCH = 50
LR = 1e-2
# TIME_STEP = 15
DROP_RATE = 0.2
LAYER = 3
MODEL = "RNN-20"


class Predictor(nn.Module):
    def __init__(self):
        super(Predictor, self).__init__()
        self.rnn = nn.RNN(
            input_size=INPUT_SIZE,
            hidden_size=HIDDEN_SIZE // 2,
            num_layers=LAYER,
            dropout=DROP_RATE,
            bidirectional=True,
            batch_first=True,  # 为True则输入输出格式为（Batch，seq_len，feature），否则Batch和Seq_len颠倒
        )
        self.hidden_out = nn.Linear(HIDDEN_SIZE, OUTPUT_SIZE)  # 最后一个时序的输出接一个全连接层
        self.dropout = nn.Dropout(p=DROP_RATE)
        self.h_s = None
        self.h_c = None

    def forward(self, x):  # X是输入数据集
        x, h = self.rnn(x)
        x = self.hidden_out(x)
        x = self.dropout(x)
        return x