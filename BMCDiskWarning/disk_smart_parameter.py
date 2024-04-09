ST4000DM000_NECESSARY_LIST = (
    "smart_1_raw", "smart_3_raw", "smart_4_raw", "smart_5_raw", "smart_7_raw", "smart_9_raw", "smart_10_raw",
    "smart_12_raw", "smart_183_raw", "smart_184_raw", "smart_187_raw", "smart_188_raw", "smart_189_raw",
    "smart_190_raw", "smart_191_raw", "smart_192_raw", "smart_193_raw", "smart_194_raw", "smart_197_raw",
    "smart_198_raw", "smart_199_raw", "smart_240_raw", "smart_241_raw", "smart_242_raw",
)

ST4000DM000_REALIST = (
    "smart_1_raw", "smart_4_raw", "smart_5_raw", "smart_7_raw", "smart_9_raw",
    "smart_12_raw", "smart_183_raw", "smart_184_raw", "smart_187_raw", "smart_188_raw", "smart_189_raw",
    "smart_190_raw", "smart_192_raw", "smart_193_raw", "smart_194_raw", "smart_197_raw",
    "smart_198_raw", "smart_199_raw", "smart_240_raw", "smart_241_raw", "smart_242_raw",
)  # 移除了两个完全没变化的

ST12000NM0008_NECESSARY_LIST = (
    "smart_1_raw", "smart_3_raw", "smart_4_raw", "smart_5_raw", "smart_7_raw", "smart_9_raw", "smart_10_raw",
    "smart_12_raw", "smart_18_raw", "smart_187_raw", "smart_188_raw", "smart_190_raw", "smart_192_raw", "smart_193_raw",
    "smart_194_raw", "smart_195_raw", "smart_197_raw", "smart_198_raw", "smart_199_raw", "smart_200_raw",
    "smart_240_raw", "smart_241_raw", "smart_242_raw",
)

ST12000NM0008_REALIST = (
    "smart_1_raw", "smart_4_raw", "smart_5_raw", "smart_7_raw", "smart_9_raw",
    "smart_12_raw", "smart_187_raw", "smart_188_raw", "smart_190_raw", "smart_192_raw", "smart_193_raw",
    "smart_194_raw", "smart_195_raw", "smart_197_raw", "smart_198_raw", "smart_199_raw",
    "smart_240_raw", "smart_241_raw", "smart_242_raw",
)

XGBOOST_SELECT = {
    "ST4000NM000":(20, 3, 19, 13, 4, 18),
    "ST12000NM0008": (10, 18, 13, 3, 16, 4)
}

PARAMETER_NUM = {"ST4000DM000": len(ST4000DM000_REALIST), "ST12000NM0008": len(ST12000NM0008_REALIST)}
