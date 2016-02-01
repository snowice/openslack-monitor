from collections import defaultdict
from collections import namedtuple
import logging

from pyleus.storm import SimpleBolt

log = logging.getLogger('counter')

Counter = namedtuple("Counter", "word count") # 输出是两个字段


class CountWordsBolt(SimpleBolt):

    OUTPUT_FIELDS = Counter # 输出是两个字段

    def initialize(self):
        # 在bolt启动的时候初始化
        # bolt是作为单例一直运行的
        self.words = defaultdict(int)


    def process_tuple(self, tup):
        word, = tup.values # 获得上游的word
        self.words[word] += 1 # 计数
        log.debug("{0} {1}".format(word, self.words[word]))
        # 注意这里输出到下游的是两个字段 word 与 word的计数
        self.emit((word, self.words[word]), anchors=[tup])


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/tmp/word_count_count_words.log',
        format="%(message)s",
        filemode='a',
    )

    CountWordsBolt().run()