
from konlpy.tag import Mecab


class KnlyMD:

    def pos_tagger(doc, mode, idx=False):
        mecab = Mecab()
        if mode == 'pos':
            result = mecab.pos(doc)
            if idx:
                units = result
                result = []; ptr = 0
                for unit in units:
                    if doc[ptr] == " ":
                        result.append((" ", "SPACE", ptr))
                        ptr += 1
                    unit = list(unit)
                    unit.append(ptr)
                    result.append(tuple(unit))
                    ptr += len(unit[0])
        elif mode == 'noun':
            result = mecab.nouns(doc)
        return result
