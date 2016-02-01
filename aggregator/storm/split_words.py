import logging

from pyleus.storm import SimpleBolt

log = logging.getLogger('splitter')


class SplitWordsBolt(SimpleBolt):

    OUTPUT_FIELDS = ["word"] # 定义输出的字段只有一个，名为word

    def process_tuple(self, tup):
        line, = tup.values # 接收到上游的tuple
        log.debug(line)
        for word in line.split():
            log.debug(word)
            # 这里bolt用于跟踪tuple的参数是anchors
            # 并且需要把上游的tuple传入
            # 把word传给下游
            self.emit((word,), anchors=[tup])


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/tmp/word_count_split_words.log',
        format="%(message)s",
        filemode='a',
    )
    SplitWordsBolt().run()