import re
import unicodedata
from typing import List, Union, Dict


class ThoKit:
    def __init__(self) -> None:
        self.tailo_accent_marks = [
            "",
            "",
            "\u0301",
            "\u0300",
            "",
            "\u0302",
            "\u030c",
            "\u0304",
            "\u030d",
            "\u030b",
        ]
        """
        臺羅（Tâi-lô）調符列表，其中引歷（index）0 元素放空，紲落來是九個聲調（含高升調）个調符
        """
        self.poj_accent_marks = [
            "",
            "",
            "\u0301",
            "\u0300",
            "",
            "\u0302",
            "\u030c",
            "\u0304",
            "\u030d",
            "\u0306",
        ]
        """
        白話字（Pe̍h-ōe-jī）調符列表，其中引歷（index）0 元素放空，紲落來是九個聲調（含高升調）个調符

        着注意，傳統白話字本身無定義陽上調、高升調（「第九調」）符
        """
        self.ipa_tone_cateɡory_symbols = [
            "",
            "꜀",
            "꜂",
            "꜄",
            "꜆",
            "꜁",
            "꜃",
            "꜅",
            "꜇",
            "",
        ]
        """
        國際音標調類符號
        """
        self.ipa_tone_cateɡory_numbers = [
            "",
            "1",
            "3",
            "5",
            "7",
            "2",
            "4",
            "6",
            "8",
            "9",
        ]
        """
        國際音標調類數字
        """
        self.entering_endings = "ptkhPTKH"
        """
        入聲塞音韻尾
        """
        self.normalization_forms = ["NFC", "NFD"]
        """
        Unicode 个[正則化形式](https://unicode.org/reports/tr15/#Norm_Forms)

        - NFD (Normalization Form D)：規範分解（Decomposition），調符佮字母各佔一个 Unicode 碼位
        - NFC (Normalization Form C)：規範組合（Composition），調符佮字母儘可能鬥做伙

        ``` python
        >>> import unicodedata
        >>> syllable = unicodedata.normalize('NFD', 'á'); [char for char in syllable], [hex(ord(char)) for char in syllable], len(syllable)
        (['a', '́'], ['0x61', '0x301'], 2) # 'á' (U+00E1) => 'a' (U+0061) + '́' (U+0301)
        >>> syllable = unicodedata.normalize('NFC', 'a'+'\u0301'); syllable, hex(ord(syllable)), len(syllable)
        ('á', 1) # 'a' (U+0061) + '́' (U+0301) => 'á' (U+00E1)
        >>> len(unicodedata.normalize('NFC', 'a̍h'))
        3 # 陽入符組合式無獨立碼位，NFC 之後猶原不變
        ```

        無建議用兼容式个 NFKC、NFKD，因爲這解共 POJ 个 ⁿ/ᴺ 轉換做 n/N
        """
        self.poj_standards = ["campbell", "douglas", "barclay"]

    def addDefaultToneNumber(self, segmental_syllable: str) -> str:
        """
        陰平佮陰入音節添數字調（默認免寫出來）
        """
        return segmental_syllable + (
            "4" if segmental_syllable[-1] in self.entering_endings else "1"
        )

    def replaceAccents(self, text: str, accent_marks: list) -> str:
        """
        調符分解，然後轉數字調
        """
        text = unicodedata.normalize("NFD", text)
        for idx, accent in enumerate(accent_marks):
            if accent and accent in text:
                text = text.replace(accent, str(idx))
        return text

    def tailoUnicode2Ascii(self, text: str, accent_marks: List[str] = []) -> str:
        """
        臺羅 Unicode 轉 ASCII

        參數：
            text (str): 輸入个臺羅 Unicode 文本，帶 Unicode 調符
            accent_marks (List[str]): 調符數組
        返回：
            str: 轉換後个臺羅 ASCII 文本，帶數字調
        """
        if not accent_marks:
            accent_marks = self.tailo_accent_marks
        text = self.replaceAccents(text, accent_marks)
        text = re.sub(
            "(\d)([a-z]+)([^a-z]|$)", r"\2\1\3", text, flags=re.IGNORECASE
        )  # 數字調放後壁
        text = re.sub(
            "([a-zA-Z]+)([^\da-zA-Z]|$)",
            lambda x: self.addDefaultToneNumber(x.group(1)) + x.group(2),
            text,
        )  # 添陰平、陰入數字調
        return text

    def pojSpecialLetterUnicode2Ascii(self, text: str, standard: str) -> str:
        is_upper = text.upper().replace("ⁿ", "ᴺ") == text # 因爲 ᴺ 个緣故，袂使用 text.isupper()
        text = text.replace("ⁿ", "nn").replace("ᴺ", "NN")
        text = re.sub("^(O[\u0300-\u030f]?)\u0358$", r"\1o", text)
        text = text.replace("\u0358", "O") if is_upper else text.replace("\u0358", "o")
        if standard == "douglas":
            text = text.replace("ɵ", "o").replace("Ɵ", "O")
            if not is_upper:
                text = re.sub("o([\u0300-\u030f]?)\u0308", r"e\1r", text)
                text = re.sub("O([\u0300-\u030f]?)\u0308", r"E\1r", text)
                text = re.sub("u([\u0300-\u030f]?)\u0308", r"i\1r", text)
                text = re.sub("U([\u0300-\u030f]?)\u0308", r"I\1r", text)
                text = re.sub("ɛ", "ee", text)
                text = re.sub("Ɛ", "Ee", text)
                text = re.sub("i\u0308", r"y", text, flags=re.IGNORECASE)
            else:
                text = re.sub("^O([\u0300-\u030f]?)\u0308$", r"E\1r", text)
                text = re.sub("O([\u0300-\u030f]?)\u0308", r"E\1R", text)
                text = re.sub("^U([\u0300-\u030f]?)\u0308$", r"I\1r", text)
                text = re.sub("U([\u0300-\u030f]?)\u0308", r"I\1R", text)
                text = re.sub("^Ɛ([\u0300-\u030f]?)$", r"E\1e", text)
                text = re.sub("Ɛ([\u0300-\u030f]?)", r"E\1E", text)
                text = re.sub("I\u0308", r"Y", text)
        return text

    def pojUnicode2Ascii(
        self, text: str, standard: str = None, accent_marks: List[str] = []
    ) -> str:
        """
        白話字 Unicode 轉 ASCII

        參數：
            text (str): 輸入个白話字 Unicode 文本，帶 Unicode 調符
            accent_marks (List[str]): 調符數組
        返回：
            str: 轉換後个白話字 ASCII 文本，帶數字調

        請注意，即个函數着考慮一對多映射，譬論講：
        `O͘ => (OO|Oo)`（全大寫 | 首字母大寫）个轉換結果不唯一。
        本函數佇所有字母攏大寫个時，默認轉換做頭一種。孤 `O͘` 或者帶聲調轉換做後一種。
        """
        if standard:
            assert standard in self.poj_standards
        if not accent_marks:
            accent_marks = self.poj_accent_marks
        is_upper = text.upper().replace("ⁿ", "ᴺ") == text  # 因爲 ᴺ 个緣故，袂使用 text.isupper()
        text = unicodedata.normalize("NFD", text)
        if standard in ["campbell", "barclay", "douglas"]:
            text = re.sub("(h)(ⁿ|ᴺ)", r"\2\1", text, flags=re.IGNORECASE)

        text = self.pojSpecialLetterUnicode2Ascii(text, standard=standard)
        text = self.replaceAccents(text, accent_marks)
        text = re.sub(
            "(\d)([a-z]+)([^a-z]|$)", r"\2\1\3", text, flags=re.IGNORECASE
        )  # 數字調放後壁
        text = re.sub(
            "([a-zA-Z]+)([^\da-zA-Z]|$)",
            lambda x: self.addDefaultToneNumber(x.group(1)) + x.group(2),
            text,
        )  # 添陰平、陰入數字調
        if standard == "campbell":
            text = re.sub("(m|n|ng)(oo)(nn)", r"\1\2", text)
            text = re.sub("(o)(o)(nn)", r"\1\3", text)
        elif standard in ["douglas", "barclay"]:
            text = re.sub("([iI])e([nt])([^ng]|$)", r"\1a\2\3", text)
            text = re.sub("(I)E([NT])([^NG]|$)", r"\1A\2\3", text)
            text = text.replace("oo", "ou").replace("Oo", "Ou").replace("OO", "OU")
            text = text.replace("ts", "ch").replace("Ts", "Ch").replace("TS", "CH")
            text = text.replace("nnh", "hnn").replace("NNH", "HNN")
        if is_upper:
            text = text.upper()
        return text

    def pojAscii2TailoAscii(self, text: str) -> str:
        """
        白話字 ASCII 轉臺羅 ASCII

        參數：
            text (str): 輸入个白話字 ASCII 文本，帶數字調
        返回：
            str: 轉換後个臺羅 ASCII 文本，帶數字調
        """
        text = text.replace("ch", "ts").replace("Ch", "Ts").replace("CH", "TS")
        text = re.sub("o([ae])", r"u\1", text)
        text = re.sub("O([ae])", r"U\1", text, flags=re.IGNORECASE)
        text = re.sub("e(ng|k)", r"i\1", text)
        text = re.sub("E(ng|k)", r"I\1", text, flags=re.IGNORECASE)
        return text

    def tailoAscii2PojAscii(self, text: str) -> str:
        """
        臺羅 ASCII 轉白話字 ASCII

        參數：
            text (str): 輸入个臺羅 ASCII 文本，帶數字調
        返回：
            str: 轉換後个白話字 ASCII 文本，帶數字調
        """
        text = text.replace("ts", "ch").replace("Ts", "Ch").replace("TS", "CH")
        text = re.sub("u([ae])", r"o\1", text)
        text = re.sub("U([ae])", r"O\1", text, flags=re.IGNORECASE)
        text = re.sub("i(ng|k)", r"e\1", text)
        text = re.sub("I(ng|k)", r"E\1", text, flags=re.IGNORECASE)
        return text

    def moveTailoToneNumber(self, syllable: str) -> str:
        """
        臺羅數字標調徙位
        """
        if re.search("[aeiou]", syllable, flags=re.IGNORECASE):
            syllable = re.sub(
                "([aeiou])(r?m?n*h?g?p?t?k?)(\d)",
                r"\1\3\2",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
            return re.sub(
                "([aeo])([iueo])(\d)", r"\1\3\2", syllable, count=1, flags=re.IGNORECASE
            )
        syllable = re.sub(
            "(n)(gh?)(\d)", r"\1\3\2", syllable, count=1, flags=re.IGNORECASE
        )
        syllable = re.sub(
            "(m)(h?)(\d)", r"\1\3\2", syllable, count=1, flags=re.IGNORECASE
        )
        return syllable

    def tailoAscii2Unicode(
        self,
        text: str,
        support_poj_letters: bool = False,
        accent_marks: List[str] = [],
        normalization: str = "NFC",
    ) -> str:
        """
        臺羅 ASCII 轉 Unicode

        參數：
            text (str): 輸入个臺羅 ASCII 文本，帶數字調
            accent_marks (List[str]): 調符數組
            normalization (str，可選): Unicode 正則化形式，默認做 "NFC"
        返回：
            str: 轉換後个臺羅 Unicode 文本，帶 Unicode 調符
        """
        if support_poj_letters:
            text = self.pojAscii2TailoAscii(text)
        if not accent_marks:
            accent_marks = self.tailo_accent_marks
        assert normalization in self.normalization_forms
        text = re.sub(
            "[a-zA-Z]+\d", lambda x: self.moveTailoToneNumber(x.group(0)), text
        )  # 數字調徙位
        text = re.sub(
            "([aeioumn])(\d)",
            lambda x: x.group(1) + accent_marks[int(x.group(2))],
            text,
            flags=re.IGNORECASE,
        )  # 數字調轉 Unicode 調符
        return unicodedata.normalize(normalization, text)

    def _movePojToneNumber(self, syllable: str) -> str:
        """
        白話字數字標調徙位（無處理 o 介音）
        """
        if "a" in syllable or "e" in syllable or "A" in syllable or "E" in syllable:
            return re.sub(
                "([ae])([a-z]*)(\d)", r"\1\3\2", syllable, count=1, flags=re.IGNORECASE
            )
        elif "o" in syllable or "O" in syllable:
            return re.sub(
                "(o)([a-z]*)(\d)", r"\1\3\2", syllable, count=1, flags=re.IGNORECASE
            )
        elif "u" in syllable or "U" in syllable:
            return re.sub(
                "(u)([a-z]*)(\d)", r"\1\3\2", syllable, count=1, flags=re.IGNORECASE
            )
        elif "i" in syllable or "I" in syllable:
            return re.sub(
                "(i)([a-z]*)(\d)", r"\1\3\2", syllable, count=1, flags=re.IGNORECASE
            )
        syllable = re.sub(
            "(n)(gh?)(\d)", r"\1\3\2", syllable, count=1, flags=re.IGNORECASE
        )
        syllable = re.sub(
            "(m)(h?)(\d)", r"\1\3\2", syllable, count=1, flags=re.IGNORECASE
        )
        return syllable

    def movePojToneNumber(self, syllable, standard: str = None):
        """
        白話字數字標調徙位
        """
        syllable = self._movePojToneNumber(syllable)
        if standard == "campbell":
            """
            甘爲霖白話字標調特殊規則
                介音 o：([a-z])o([ae])\d 或者 ([a-z])o([ae])(nn)\d，標 o；若無標 a、e
                ainnh8：標 i
            """
            syllable = re.sub(
                "([a-z])(o)([ae])(\d)(nn)?([^a-z]|$)",
                r"\1\2\4\3\5\6",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
            syllable = re.sub(
                "(a)(8)(i)(nnh)", r"\1\3\2\4", syllable, count=1, flags=re.IGNORECASE
            )
        elif standard == "douglas":
            """
            杜嘉德《廈英大辭典》白話字標調一般規則
                介音 o：oe/oee，標 o
                ainn/ainnh：標 i
            """
            syllable = re.sub(
                "(o)(e)(\d)",
                r"\1\3\2",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
            syllable = re.sub(
                "(a)(\d)(i)(nn)", r"\1\3\2\4", syllable, count=1, flags=re.IGNORECASE
            )
        elif standard == "barclay":
            """
            巴克禮《增補廈英大辭典》白話字標調一般規則
                介音 o：
                  - ([a-z])o(a)\d 或者 ([a-z])o(a)(nn)\d，標 o；若無標 a
                  - oe，標 o

                按：若嚴格依《增補廈英大辭典》
                - 非零聲母+oa(h?)(ⁿ?)，多數標 o，少數標 a；
                - 非零聲母+oan/oat，標 o 或 a 兩可（b-/t-/kh-/g-/ts-/chh-/h-/l- 多標 o，k-/s- 多標 a）；
                - 非零聲母+oai，標 o 或 a 兩可（h- 多標 o，k- 多標 a， kh- 五五開）
                - 非零聲母+oaiⁿ，標 o 或 a 兩可（s- 標 o，k-/h- 多標 a）
                - 零聲母+oa(.*)，多數標 a，少數標 o；
                - oe，多數標 o，少數標 e
            """
            syllable = re.sub(
                "(o)(e)(\d)",
                r"\1\3\2",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
            syllable = re.sub(
                "([a-z])(o)(a)(\d)(nn)?([^a-z]|$)",
                r"\1\2\4\3\5\6",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
        else:
            """
            現代白話字標調特殊規則
                介音 o：oa, oe, oaⁿ, oeⁿ（不論是否零聲母）, 標 o；否則標 a、e
            """
            syllable = re.sub(
                "(o)([ae])(\d)(nn)?([^a-z]|$)",
                r"\1\3\2\4\5",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
        return syllable

    def pojSpecialLetterAscii2Unicode(self, text, standard: str = None) -> str:
        text = re.sub(
            "(o)([\u0300-\u030f]?)(o)",
            "\\1\\2\u0358",
            text,
            flags=re.IGNORECASE,
        )  # oo => o͘

        text = re.sub(
            "NN(h)?([^G\u0300-\u030f]|$)",
            r"ᴺ\1\2",
            text,
        )  # NN => ᴺ

        text = re.sub(
            "nn(h)?([^g\u0300-\u030f]|$)",
            r"ⁿ\1\2",
            text,
            flags=re.IGNORECASE,
        )  # nn => ⁿ
        if standard == "douglas":
            text = re.sub("o([\u0300-\u030f]?\u0358)", r"ɵ\1", text)
            text = re.sub("O([\u0300-\u030f]?\u0358)", r"Ɵ\1", text)
            text = re.sub(
                "i([\u0300-\u030f]?)(r)",
                "u\\1\u0308",
                text,
            )
            text = re.sub(
                "I([\u0300-\u030f]?)(r)", "U\\1\u0308", text, flags=re.IGNORECASE
            )
            text = re.sub(
                "e([\u0300-\u030f]?)(r)",
                "o\\1\u0308",
                text,
            )
            text = re.sub(
                "E([\u0300-\u030f]?)(r)", "O\\1\u0308", text, flags=re.IGNORECASE
            )
            text = re.sub("e([\u0300-\u030f]?)(e)", "ɛ\\1", text)
            text = re.sub("E([\u0300-\u030f]?)(e)", "Ɛ\\1", text)
            text = re.sub("y([oh\d])", "i\u0308\\1", text)
            text = re.sub("Y([oh\d])", "I\u0308\\1", text, flags=re.IGNORECASE)
        return text

    def pojAscii2Unicode(
        self,
        text: str,
        standard: str = None,
        case_spelling: bool = True,
        support_tailo_letters=False,
        support_N=False,
        accent_marks: List[str] = [],
        normalization: str = "NFC",
    ) -> str:
        """
        白話字 ASCII 轉 Unicode

        參數：
            text (str): 輸入个白話字 ASCII 文本，帶數字調
            standard（str，可選）：白話字標準
            support_N（bool，可選）：敢支持 -N 轉做 -nn，默認無（解佮大寫 -NN 衝突）
            accent_marks (List[str]): 調符數組
            normalization (str，可選): Unicode 正則化形式，默認做 "NFC"
        返回：
            str: 轉換後个白話字 Unicode 文本，帶 Unicode 調符
        """
        if standard:
            assert standard in self.poj_standards
        if support_tailo_letters:
            text = self.tailoAscii2PojAscii(text)
        if not accent_marks:
            accent_marks = self.poj_accent_marks
        assert normalization in self.normalization_forms
        text = (
            text.replace("ou", "oo")
            .replace("Ou", "Oo")
            .replace("OU", "OO")
            .replace("hnn", "nnh")
            .replace("HNN", "NNH")
        )
        if support_N:  # 支持大寫 N 轉換做 nn
            text = re.sub("([aeiou])N", r"\1nn", text)
        if standard == "campbell" and case_spelling:
            """
            臺羅 vs 甘爲霖白話字
                tsh => chh
                ts([^ie]) => ts
                ts([ie]) => ch
                onn => o͘ⁿ
                moo/ngoo => mo͘/ngo͘
                noo => no͘ⁿ
            """
            text = re.sub("([^o])onn", r"\1oonn", text)
            text = re.sub("([^o])Onn", r"\1Oonn", text)
            text = re.sub("([^O])ONN", r"\1OONN", text)
            text = re.sub("(n|N)(oo)([^n])", r"\1\2nn\3", text)
            text = re.sub("(N)(OO)([^N])", r"\1\2NN\3", text)
            text = re.sub("(m|ng)(oo)(nn)", r"\1\2", text, flags=re.IGNORECASE)
            text = re.sub("ch([^eih])", r"ts\1", text)
            text = re.sub("Ch([^eih])", r"Ts\1", text)
            text = re.sub("CH([^EIH])", r"TS\1", text)
            text = re.sub("ts([eih])", r"ch\1", text)
            text = re.sub("Ts([eih])", r"Ch\1", text)
            text = re.sub("TS([EIH])", r"CH\1", text)
        elif standard in ["douglas", "barclay"] and case_spelling:
            """
            臺羅 vs 甘爲霖/巴克禮白話字
                tsh => chh
                ts([^ie]) => ts
                ts([ie]) => ch
                onn => o͘ⁿ
                另 m/n/ng 後韻母是否加 ⁿ 兩可，故不予強制轉換
            """
            text = re.sub("ch([^eih])", r"ts\1", text)
            text = re.sub("Ch([^eih])", r"Ts\1", text)
            text = re.sub("CH([^EIH])", r"TS\1", text)
            text = re.sub("ts([eih])", r"ch\1", text)
            text = re.sub("Ts([eih])", r"Ch\1", text)
            text = re.sub("TS([EIH])", r"CH\1", text)
            text = re.sub("([iI])a([nt])([^ng]|$)", r"\1e\2\3", text)
            text = re.sub("(I)A([NT])([^NG]|$)", r"\1E\2\3", text)
        text = re.sub(
            "[a-zA-Z]+\d", lambda x: self.movePojToneNumber(x.group(0), standard), text
        )

        text = re.sub(
            "([aeioumn])(\d)",
            lambda x: x.group(1) + accent_marks[int(x.group(2))],
            text,
            flags=re.IGNORECASE,
        )

        text = self.pojSpecialLetterAscii2Unicode(text, standard)

        if standard in ["campbell", "barclay"]:
            text = re.sub("(ⁿ|ᴺ)(h)", r"\2\1", text, flags=re.IGNORECASE)
        elif standard == "douglas":
            text = re.sub("(ⁿ|ᴺ)(h)", r"\2\1", text, flags=re.IGNORECASE)

        return unicodedata.normalize(normalization, text)

    def moveTailoToneAccent(self, syllable: str) -> str:
        """
        臺羅調符徙位
        """
        if re.search("[aeiou]", syllable, flags=re.IGNORECASE):
            syllable = re.sub(
                "([aeiou])(r?m?n*h?g?p?t?k?)([\u0300-\u030f])",
                r"\1\3\2",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
            return re.sub(
                "([aeo])([iueo])([\u0300-\u030f])",
                r"\1\3\2",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
        syllable = re.sub(
            "(n)(gh?)([\u0300-\u030f])",
            r"\1\3\2",
            syllable,
            count=1,
            flags=re.IGNORECASE,
        )
        syllable = re.sub(
            "(m)(h?)([\u0300-\u030f])",
            r"\1\3\2",
            syllable,
            count=1,
            flags=re.IGNORECASE,
        )
        return syllable

    def pojUnicode2TailoUnicode(
        self, text: str, poj_standard: str = None, normalization: str = "NFC"
    ) -> str:
        """
        白話字 Unicode 轉臺羅 Unicode

        參數:
            text (str): 輸入个白話字 Unicode 文本
            standard（str，可選）：白話字標準
            normalization (str，可選): Unicode 正則化形式，默認做 "NFC"
        返回：
            str: 轉換後个臺羅 Unicode 文本
        """
        text = unicodedata.normalize("NFD", text).replace("\u0306", "\u030b")

        text = self.pojSpecialLetterUnicode2Ascii(text, standard=poj_standard)
        if poj_standard == "campbell":
            text = re.sub(r"(h)(nn)", r"\2\1", text, flags=re.IGNORECASE)
            text = re.sub(
                r"(m|n|ng)(o)([\u0300-\u030f]?)(o)(nn)",
                r"\1\2\3\4",
                text,
                flags=re.IGNORECASE,
            )
            text = re.sub(
                r"(o)([\u0300-\u030f]?)(o)(nn)",
                r"\1\2\4",
                text,
                flags=re.IGNORECASE,
            )
        text = re.sub(
            r"([\u0300-\u030f])([a-z]+)([^a-z]|$)",
            r"\2\1\3",
            text,
            flags=re.IGNORECASE,
        )
        text = self.pojAscii2TailoAscii(text)
        text = re.sub(
            r"[a-zA-Z]+[\u0300-\u030f]",
            lambda match: self.moveTailoToneAccent(match.group(0)),
            text,
        )

        return unicodedata.normalize(normalization, text)

    def pojUnicode2TailoUnicodeCascade(
        self, text: str, poj_standard: str = None, normalization: str = "NFC"
    ) -> str:
        """
        白話字 Unicode 轉臺羅 Unicode（級聯版，效率較下）

        參數:
            text (str): 輸入个白話字 Unicode 文本
            standard（str，可選）：白話字標準
            normalization (str，可選): Unicode 正則化形式，默認做 "NFC"
        返回：
            str: 轉換後个臺羅 Unicode 文本
        """
        text = self.pojUnicode2Ascii(text, standard=poj_standard)
        text = self.pojAscii2TailoAscii(text)
        return self.tailoAscii2Unicode(text, normalization)

    def _movePojToneAccent(self, syllable: str) -> str:
        """
        白話字調符徙位（無處理 o 介音）
        """
        if "a" in syllable or "e" in syllable or "A" in syllable or "E" in syllable:
            return re.sub(
                "([ae])([a-z]*)([\u0300-\u030f])",
                r"\1\3\2",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
        elif "o" in syllable or "O" in syllable:
            return re.sub(
                "(o)([a-z]*)([\u0300-\u030f])",
                r"\1\3\2",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
        elif "u" in syllable or "U" in syllable:
            return re.sub(
                "(u)([a-z]*)([\u0300-\u030f])",
                r"\1\3\2",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
        elif "i" in syllable or "I" in syllable:
            return re.sub(
                "(i)([a-z]*)([\u0300-\u030f])",
                r"\1\3\2",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
        syllable = re.sub(
            "(n)(gh?)([\u0300-\u030f])",
            r"\1\3\2",
            syllable,
            count=1,
            flags=re.IGNORECASE,
        )
        syllable = re.sub(
            "(m)(h?)([\u0300-\u030f])",
            r"\1\3\2",
            syllable,
            count=1,
            flags=re.IGNORECASE,
        )
        return syllable

    def movePojToneAccent(self, syllable, standard: str = None):
        """
        白話字調符徙位
        """
        syllable = self._movePojToneAccent(syllable)
        if standard == "campbell":
            """
            甘爲霖白話字標調規則
                介音 o：([a-z])o([ae])\d 或者 ([a-z])o([ae])(nn)\d，標 o；若無標 a、e
                ainnh8：標 i
            """
            syllable = re.sub(
                "([a-z])(o)([ae])([\u0300-\u030f])(nn)?([^a-z]|$)",
                r"\1\2\4\3\5\6",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
            syllable = re.sub(
                "(a)(8)(i)(nnh)", r"\1\3\2\4", syllable, count=1, flags=re.IGNORECASE
            )
        else:
            syllable = re.sub(
                "(o)([ae])([\u0300-\u030f])(nn)?([^a-z]|$)",
                r"\1\3\2\4\5",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
        return syllable

    def tailoUnicode2PojUnicode(
        self, text: str, poj_standard: str = None, normalization: str = "NFC"
    ) -> str:
        """
        臺羅 Unicode 轉白話字 Unicode

        參數:
            text (str): 輸入个臺羅 Unicode 文本
            standard（str，可選）：白話字標準
            normalization (str，可選): Unicode 正則化形式，默認做 "NFC"
        返回：
            str: 轉換後个白話字 Unicode 文本
        """
        text = unicodedata.normalize("NFD", text).replace("\u030b", "\u0306")

        text = re.sub(
            r"([\u0300-\u030f])([a-z]+)([^a-z]|$)",
            r"\2\1\3",
            text,
            flags=re.IGNORECASE,
        )  # 調符放後壁

        text = self.tailoAscii2PojAscii(text)

        text = re.sub(
            r"[a-zA-Z]+[\u0300-\u030f]",
            lambda match: self.movePojToneAccent(match.group(0), poj_standard),
            text,
        )

        text = self.pojSpecialLetterAscii2Unicode(text, standard=poj_standard)

        return unicodedata.normalize(normalization, text)

    def tailoUnicode2PojUnicodeCascade(
        self, text: str, poj_standard: str = None, normalization: str = "NFC"
    ) -> str:
        """
        臺羅 Unicode 轉白話字 Unicode（級聯版，效率較下）

        參數:
            text (str): 輸入个臺羅 Unicode 文本
            standard（str，可選）：白話字標準
            normalization (str，可選): Unicode 正則化形式，默認做 "NFC"
        返回：
            str: 轉換後个白話字 Unicode 文本
        """
        text = self.tailoUnicode2Ascii(text)
        text = self.tailoAscii2PojAscii(text)
        return self.pojAscii2Unicode(text, poj_standard, normalization=normalization)

    def moveIpaNasal(self, syllable: str) -> str:
        """
        國際音標鼻化標誌徙位
        """
        if "\u0303" in syllable and re.search("[aeiou]", syllable, flags=re.IGNORECASE):
            syllable = re.sub(
                "([aeiou])(r?)(\u0303)",
                r"\1\3\2",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
            return re.sub(
                "([aeo])([iueo])(\u0303)",
                r"\1\3\2",
                syllable,
                count=1,
                flags=re.IGNORECASE,
            )
        return syllable

    def addIpaToneMarks(
        self, segmental_syllable: str, tone: int, tone_marks: Union[str, List[str]]
    ) -> str:
        if not tone_marks:
            tone_marks = "ipa_tone_cateɡory_symbols"
        if type(tone_marks) == str:
            assert tone_marks in [
                "ipa_tone_cateɡory_symbols",
                "ipa_tone_cateɡory_numbers",
            ]
            if tone_marks == "ipa_tone_cateɡory_symbols":
                return (
                    self.ipa_tone_cateɡory_symbols[tone] + segmental_syllable
                    if tone in [1, 2, 5, 6]
                    else segmental_syllable + self.ipa_tone_cateɡory_symbols[tone]
                )
            else:
                assert eval(f"self.{tone_marks}")
                return segmental_syllable + eval(f"self.{tone_marks}")[tone]
        else:
            return segmental_syllable + tone_marks[tone]

    def tailoAscii2Ipa(
        self, text: str, tone_marks: Union[str, List[str], Dict[int, str]] = None
    ) -> str:
        """
        臺羅 ASCII 轉寬式國際音標
        聲調干焦處理做調類
        無處理「第九調」
        [TODO] 輕聲處理
        [TODO] 自定義轉換規則
        """
        text = text.lower().replace("-", " ")
        text = re.sub(
            "([a-z]+)([^\da-z]|$)",
            lambda x: self.addDefaultToneNumber(x.group(1)) + x.group(2),
            text,
        )  # 添陰平、陰入數字調
        text = re.sub(
            "([a-z]+)(\d)",
            lambda x: self.addIpaToneMarks(x.group(1), int(x.group(2)), tone_marks),
            text,
        )
        text = re.sub("([aeiou]r?)nn", "\\1\u0303", text)
        text = re.sub("([a-z]+)\u0303", lambda x: self.moveIpaNasal(x.group(0)), text)
        text = text.replace("ng", "ŋ").replace("g", "ɡ").replace("j", "dz")
        text = re.sub("([ptks])h", r"\1ʰ", text)
        text = re.sub("o([nŋk])", r"ɔ\1", text)
        text = (
            text.replace("oo", "ɔ")
            .replace("ir", "ɯ")
            .replace("er", "ə")
            .replace("ee", "ɛ")
        )
        return text
