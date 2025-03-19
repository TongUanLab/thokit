import time
from thokit import ThoKit

thokit = ThoKit()

receipts = {
    "poj_a2u": {
        "src": "./test/data/poj.asc.txt",
        "tgt": "./test/data/poj.uni.hyp",
        "ref": "./test/data/poj.uni.txt",
        "fn": thokit.pojAscii2Unicode,
    },
    "poj_u2a": {
        "src": "./test/data/poj.uni.txt",
        "tgt": "./test/data/poj.asc.hyp",
        "ref": "./test/data/poj.asc.txt",
        "fn": thokit.pojUnicode2Ascii,
    },
    "tl_a2u": {
        "src": "./test/data/tailo.asc.txt",
        "tgt": "./test/data/tailo.uni.hyp",
        "ref": "./test/data/tailo.uni.txt",
        "fn": thokit.tailoAscii2Unicode,
    },
    "tl_u2a": {
        "src": "./test/data/tailo.uni.txt",
        "tgt": "./test/data/tailo.asc.hyp",
        "ref": "./test/data/tailo.asc.txt",
        "fn": thokit.tailoUnicode2Ascii,
    },
    "poja2tla": {
        "src": "./test/data/poj.asc.txt",
        "tgt": "./test/data/tailo.asc.poja2tla.hyp",
        "ref": "./test/data/tailo.asc.txt",
        "fn": thokit.pojAscii2TailoAscii,
    },
    "tla2poja": {
        "src": "./test/data/tailo.asc.txt",
        "tgt": "./test/data/poj.asc.tla2poja.hyp",
        "ref": "./test/data/poj.asc.txt",
        "fn": thokit.tailoAscii2PojAscii,
    },
    "poju2tlu": {
        "src": "./test/data/poj.uni.txt",
        "tgt": "./test/data/tailo.uni.poju2tlu.hyp",
        "ref": "./test/data/tailo.uni.txt",
        "fn": thokit.pojUnicode2TailoUnicode,
    },
    "tlu2poju": {
        "src": "./test/data/tailo.uni.txt",
        "tgt": "./test/data/poj.uni.tlu2poju.hyp",
        "ref": "./test/data/poj.uni.txt",
        "fn": thokit.tailoUnicode2PojUnicode,
    },
}


def judge(strict=True, mode=""):
    total, correct = 0, 0
    if mode:
        with open(receipts[mode]["src"], "r", encoding="utf-8") as fi:
            src_lines = fi.readlines()
        with open(receipts[mode]["ref"], "r", encoding="utf-8") as fr:
            ref_lines = fr.readlines()
        fn = receipts[mode]["fn"]
        assert len(src_lines) == len(ref_lines)
        start_time = time.time()
        tgt_lines = list(map(fn, src_lines))
        end_time = time.time()
        print("Time for %s: %.6fs" % (mode, end_time - start_time))
        for i in range(total):
            if tgt_lines[i] == ref_lines[i]:
                correct += 1
        with open(receipts[mode]["tgt"], "w", encoding="utf-8") as fo:
            fo.writelines(tgt_lines)
        total = len(src_lines)
    else:
        total_time = 0
        for _mode in receipts:
            with open(receipts[_mode]["src"], "r", encoding="utf-8") as fi:
                src_lines = fi.readlines()
            with open(receipts[_mode]["ref"], "r", encoding="utf-8") as fr:
                ref_lines = fr.readlines()
            fn = receipts[_mode]["fn"]
            assert len(src_lines) == len(ref_lines)
            start_time = time.time()
            tgt_lines = list(map(fn, src_lines))
            end_time = time.time()
            total_time += end_time - start_time
            print("Time for %s: %.6fs" % (_mode, end_time - start_time))
            (
                _total,
                _correct,
            ) = (
                len(src_lines),
                0,
            )
            for i in range(_total):
                if tgt_lines[i] == ref_lines[i]:
                    _correct += 1
            print("Accuracy: %.6f" % (_correct / _total))
            with open(receipts[_mode]["tgt"], "w", encoding="utf-8") as fo:
                fo.writelines(tgt_lines)
            total += _total
            correct += _correct
        print("Total time: %.6fs" % (total_time))
    print("Overall accuracy: %.6f" % (correct / total))


if __name__ == "__main__":
    judge()
