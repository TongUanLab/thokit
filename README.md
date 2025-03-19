# THOKIT / 桃橘

「**桃橘**」（**THOKIT，Tong-uán Hokkien Orthography toolKIT**）是東苑實驗室个閩南方言拼寫方案處理工具套件。

「桃橘」漢字號名取漳州話 Thô-kit，毋過若讀做泉廈腔 Thô-kiat 嘛解使着。

## 支持个編程語言

- Python
- JavaScript

## 主要功能

- 臺羅/白話字个數字式（ASCII）/閏符式（Unicode）互轉
- 臺羅數字式/白話字數字式互轉
- 臺羅閏符式/白話字閏符式互轉
- 支持全大寫處理
- 支持加種白話字標準
- 支持自定義羅馬字調符

## 開始

### Python

``` python
from thokit import ThoKit
thokit = ThoKit()

print(thokit.tailoAscii2Unicode('Sann1 TE2 khoo3 khuah4; lang5 lau6 phinn7 tit8. Hann9?'))
print(thokit.pojAscii2Unicode('SANN te2 khoo3 khuah; lang5 lau6 phinn7 tit8. Hann9?'))
```

### HTML

``` html
<script type="module">
  import { ThoKit } from '../../thokit.js';
  const thokit = new ThoKit();
  console.log(thokit.tailoAscii2Unicode('Sann1 TE2 khoo3 khuah4; lang5 lau6 phinn7 tit8. Hann9?'))
  console.log(thokit.pojAscii2Unicode('SANN te2 khoo3 khuah; lang5 lau6 phinn7 tit8. Hann9?'))
</script>
```

### Node.js

``` bash
npm install
npm run build
```

``` js
const { ThoKit } = require('./dist/thokit.cjs');
const thokit = new ThoKit();

console.log(thokit.tailoAscii2Unicode('Sann1 TE2 khoo3 khuah4; lang5 lau6 phinn7 tit8. Hann9?'))
console.log(thokit.pojAscii2Unicode('SANN te2 khoo3 khuah; lang5 lau6 phinn7 tit8. Hann9?'))
```

## 測試

### Python

``` python
python test/py/oj.py
```

### HTML

試用 `test/html/demo.html`（着注意 `thokit.js` 个導入），或者「韻彙」網站搭个[頁面](https://unlui.enatsu.top/tool/thokit)。

### Node.js

``` bash
node test/node/oj.js
```

## 白話字標準說明

THOKIT 今支持下底兩款白話字標準，字母佮標調規則小可有縒。

### 默認標準

大致照信望愛台語客語輸入法（FHL Taigi-Hakka IME）白話字个拼寫方式。

TL => default POJ

- `ts/tsh` => `ch/chh`
- `ua/ue` => `oa/oe`
- `ing/ik` => `eng/ek`
- `nn` => `ⁿ`
- `NN`（`nn` 个大寫） => `ᴺ`
- `oo` => `o͘`
- `nnh` => `ⁿh`
- `a̋ (a9)` => `ă`

佮信望愛輸入法个主要差異：

- `auh8/aunnh8`：`a̍uh/a̍uⁿh`
  - `ta̍uh-ta̍uh-á` (o)
  - `tau̍h-tau̍h-á` (x)
- `ere` 佮 `irinn` （老泉腔）調符放咧央元音

### 甘爲霖標準（`'campbell'`）

照甘爲霖《廈門音新字典》（1913）个拼寫方式佮標調規則。

TL => Campbell POJ

- ⚠️ `nnh` => `hⁿ`
- `ch/chh`：
  - `tsh` => `chh`
  - ⚠️ `tsa, tso, tsu` => `tsa, tso, tsu`
  - `tsi, tse` => `chi, che`
- `oa/oe`：頭前接聲母，後壁無接元音或者塞音韻尾，標 `o`；若無標 `a/e`
  - ⚠️ `uā, uē, uānn` => `oā, oē, oāⁿ`
  - `tuā, tuē, tuānn` => `tōa, tōe, tōaⁿ`
  - `ua̍h, hua̍h, uāi, uān，huāi, huān` => `oa̍h, hoa̍h, oāi, oān, hoāi, hoān`
- `onn` => `o͘ⁿ`
- `moo/ngoo` => `mo͘/ngo͘`
- `noo` => `no͘ⁿ`
- ⚠️ `a̍innh` => `ai̍hⁿ`

## 授權協議

MIT
