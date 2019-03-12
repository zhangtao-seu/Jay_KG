# encoding=utf-8
# @desc: 定义Word类的结构；定义Tagger类，实现自然语言转为Word对象的方法。

import jieba
import jieba.posseg as pseg

class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos

class Tagger:
    def __init__(self, dict_paths):
        # TODO 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)

    @staticmethod
    def get_word_objects(sentence):
        # 把自然语言转为Word对象
        return [Word(word.encode('utf-8'), tag) for word, tag in pseg.cut(sentence)]

# TODO 用于测试
if __name__ == '__main__':
    tagger = Tagger(['./external_dict/jay.txt'])
    while True:
        s = input()
        for i in tagger.get_word_objects(s):
            print(type(i))
            print(i)
            print (i.token.decode(), i.pos)
