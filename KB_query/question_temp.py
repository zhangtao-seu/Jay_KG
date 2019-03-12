# encoding=utf-8

"""
@desc:
设置问题模板，为每个模板设置对应的SPARQL语句。demo提供如下模板：

"""
from refo import finditer, Predicate, Star, Any, Disjunction
import re

# TODO SPARQL前缀和模板
SPARQL_PREXIX = u"""
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://www.semanticweb.org/张涛/ontologies/2019/1/untitled-ontology-32#>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
             u"SELECT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"



class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token.decode("utf-8"))
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num




class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_album(word_object):
        #周杰伦的专辑
        select = u"?x"
        sparql = None

        for w in word_object:
            if w.pos == pos_person:
                e = u" :{person} :release ?o."\
                    u" ?o :album_name ?x.".format(person=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql
    @staticmethod
    def has_content(word_object):
        #晴天的歌词
        select = u"?o"
        sparql = None

        for w in word_object:
            if w.pos == pos_song:
                e = u" :{song} :song_content ?o.".format(song=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql

    @staticmethod
    def person_inroduction(word_object):
        # 周杰伦的介绍
        select = u"?o"
        sparql = None

        for w in word_object:
            if w.pos == pos_person:
                e = u" :{person} :singer_introduction ?o.".format(person=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql

    @staticmethod
    def stay_album(word_object):
        # 以父之名是哪个专辑的歌曲
        select = u"?x"
        sparql = None

        for w in word_object:
            if w.pos == pos_song:
                e = u" :{song} :include_by ?o."\
                    u" ?o :album_name ?x.".format(song=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql

    @staticmethod
    def release_album(word_object):
        # 叶惠美是哪一年发行的
        select = u"?o"
        sparql = None

        for w in word_object:
            if w.pos == pos_album:
                e = u" :{album} :album_release_date ?o." .format(album=w.token.decode('utf-8'))
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql







# TODO 定义关键词
pos_person = "nr"
pos_song = "nz"
pos_album = "nz"

person_entity = (W(pos=pos_person))
song_entity = (W(pos=pos_song))
album_entity = (W(pos=pos_album))


singer = (W("歌手") | W("歌唱家") | W("艺术家") | W("艺人") | W("歌星"))
album = (W("专辑") | W("合辑") | W("唱片"))
song = (W("歌") | W("歌曲"))

category = (W("类型") | W("种类"))
several = (W("多少") | W("几部"))

higher = (W("大于") | W("高于"))
lower = (W("小于") | W("低于"))
compare = (higher | lower)

birth = (W("生日") | W("出生") + W("日期") | W("出生"))
birth_place = (W("出生地") | W("出生"))
english_name = (W("英文名") | W("英文") + W("名字"))
introduction = (W("介绍") | W("是") + W("谁") | W("简介"))
person_basic = (birth | birth_place | english_name | introduction)

song_content = (W("歌词") | W("歌") | W("内容"))
release = (W("发行") | W("发布") | W("发表") | W("出"))
movie_basic = (introduction | release)

when = (W("何时") | W("时候"))
where = (W("哪里") | W("哪儿") | W("何地") | W("何处") | W("在") + W("哪"))

# TODO 问题模板/匹配规则
"""
1.周杰伦的专辑都有什么？
2.晴天的歌词是什么？
3.周杰伦的生日是哪天？
4.以父之名是哪个专辑里的歌曲？
5.叶惠美是哪一年发行的？
"""
rules = [
    Rule(condition_num=2, condition=person_entity + Star(Any(), greedy=False) + album + Star(Any(), greedy=False), action=QuestionSet.has_album),
    Rule(condition_num=2, condition=song_entity + Star(Any(), greedy=False) + song_content + Star(Any(), greedy=False),
         action=QuestionSet.has_content),
    Rule(condition_num=2, condition=person_entity + Star(Any(), greedy=False) + introduction + Star(Any(), greedy=False),
         action=QuestionSet.person_inroduction),
    Rule(condition_num=2, condition=song_entity + Star(Any(), greedy=False) + album + Star(Any(), greedy=False),
         action=QuestionSet.stay_album),
    Rule(condition_num=2, condition=song_entity + Star(Any(), greedy=False) + release + Star(Any(), greedy=False),
         action=QuestionSet.release_album),

]

