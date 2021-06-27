# 验证码生成器
import random
from os import listdir


def random_verification_code():
    code_list = listdir("./verification/")
    n = len(code_list)
    ans = ""  # 验证码答案
    path_list = []
    for i in range(4):
        code_index = random.randint(0, n-1)
        ans += code_list[code_index][0]
        path_list.append('./verification/%s' % code_list[code_index])
    return ans, path_list


if __name__ == "__main__":
    pass


