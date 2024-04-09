ST4000DM000_NECESSARY_LIST = (
    "smart_1_raw", "smart_3_raw", "smart_4_raw", "smart_5_raw", "smart_7_raw", "smart_9_raw", "smart_10_raw",
    "smart_12_raw", "smart_183_raw", "smart_184_raw", "smart_187_raw", "smart_188_raw", "smart_189_raw",
    "smart_190_raw", "smart_191_raw", "smart_192_raw", "smart_193_raw", "smart_194_raw", "smart_197_raw",
    "smart_198_raw", "smart_199_raw", "smart_240_raw", "smart_241_raw", "smart_242_raw",
)

ST4000DM000_REALIST = (
    "smart_1_raw",
    "smart_4_raw", "smart_5_raw", "smart_7_raw", "smart_9_raw", "smart_12_raw",
    "smart_183_raw", "smart_184_raw", "smart_187_raw", "smart_188_raw", "smart_189_raw",
    "smart_190_raw", "smart_192_raw", "smart_193_raw", "smart_194_raw", "smart_197_raw",
    "smart_198_raw", "smart_199_raw", "smart_240_raw", "smart_241_raw", "smart_242_raw",
)  # 移除了三个完全没变化的

ST12000NM0008_NECESSARY_LIST = (
    "smart_1_raw", "smart_3_raw", "smart_4_raw", "smart_5_raw", "smart_7_raw", "smart_9_raw", "smart_10_raw",
    "smart_12_raw", "smart_18_raw", "smart_187_raw", "smart_188_raw", "smart_190_raw", "smart_192_raw", "smart_193_raw",
    "smart_194_raw", "smart_195_raw", "smart_197_raw", "smart_198_raw", "smart_199_raw", "smart_200_raw",
    "smart_240_raw", "smart_241_raw", "smart_242_raw",
)

ST12000NM0008_REALIST = (
    "smart_1_raw",
    "smart_4_raw", "smart_5_raw", "smart_7_raw", "smart_9_raw", "smart_12_raw",
    "smart_187_raw", "smart_188_raw", "smart_190_raw", "smart_192_raw", "smart_193_raw",
    "smart_194_raw", "smart_195_raw", "smart_197_raw", "smart_198_raw", "smart_199_raw",
    "smart_240_raw", "smart_241_raw", "smart_242_raw",
)  # 移除了二个完全没变化的

BACKBLAZE_DISK_RECOMMENDED = (
    "smart_5_raw", "smart_187_raw", "smart_188_raw", "smart_197_raw", "smart_198_raw"
)
XGBOOST_ST4000DM000_DISK_RECOMMENDED = (
    # 0, 8, 13, 15, 7  # 1 187 193 197 184, 第一代结果
    20, 3, 19, 13, 4  # 242 7 241 193 9, 第二代结果
)
XGBOOST_ST12000NM0008_DISK_RECOMMENDED = (
    # 0, 12, 2, 6, 3  # 1 195 5 187 7, 第一代结果
    10, 18, 17, 3, 16  # 193 242 241 7 240, 第二代结果
)
