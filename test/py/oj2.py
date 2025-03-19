import time
from thokit import ThoKit

thokit = ThoKit()

if __name__ == "__main__":
    with open("./test/data/tailo.asc.txt", "r", encoding="utf-8") as f:
        src_lines = f.readlines()
    start_time = time.time()
    tgt_lines = list(map(thokit.tailoAscii2Ipa, src_lines))
    end_time = time.time()
    print("Time for tla2Ipa: %.6fs" % (end_time - start_time))
    with open("./test/data/ipa.tla2ipa.hyp", "w", encoding="utf-8") as f:
        f.writelines(tgt_lines)
