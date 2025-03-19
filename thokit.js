class ThoKit {
	constructor() {
		this.tailo_accent_marks = ["", "", "\u0301", "\u0300", "", "\u0302", "\u030c", "\u0304", "\u030d", "\u030b"];
		/**
		 * 臺羅（Tâi-lô）調符列表，其中引歷（index）0 元素放空，紲落來是九個聲調（含高升調）个調符
		 */
		this.poj_accent_marks = ["", "", "\u0301", "\u0300", "", "\u0302", "\u030c", "\u0304", "\u030d", "\u0306"];
		/**
		 * 白話字（Pe̍h-ōe-jī）調符列表，其中引歷（index）0 元素放空，紲落來是九個聲調（含高升調）个調符
		 *
		 * 着注意，傳統白話字本身無定義陽上調、高升調（「第九調」）符
		 */
		this.entering_endings = "ptkhPTKH";
		/**
		 * 入聲塞音韻尾
		 */
		this.normalization_forms = ["NFC", "NFD"];
		/**
		 * Unicode 个[正則化形式](https://unicode.org/reports/tr15/#Norm_Forms)
		 *
		 * - NFD (Normalization Form D)：規範分解（Decomposition），調符佮字母各佔一个 Unicode 碼位
		 * - NFC (Normalization Form C)：規範組合（Composition），調符佮字母儘可能鬥做伙
		 *
		 * 無建議用兼容式个 NFKC、NFKD，因爲這解共 POJ 个 ⁿ/ᴺ 轉換做 n/N
		 */
		this.poj_standards = ["campbell", "douglas"]
	}
	addDefaultToneNumber(segmental_syllable) {
		// 陰平佮陰入音節添數字調（默認免寫出來）
		return segmental_syllable + (this.entering_endings.includes(segmental_syllable.slice(-1)) ? "4" : "1");
	}
	replaceAccents(text, accent_marks) {
		// 調符分解，然後轉數字調
		text = text.normalize("NFD");
		for (let idx = 0; idx < accent_marks.length; idx++) {
			const accent = accent_marks[idx];
			if (accent && text.includes(accent)) {
				text = text.replace(new RegExp(accent, 'g'), String(idx));
			}
		}
		return text;
	}
	tailoUnicode2Ascii(text, accent_marks = this.tailo_accent_marks) {
		/**
		 * 臺羅 Unicode 轉 ASCII
		 * @param {string} text - 輸入个臺羅 Unicode 文本，帶 Unicode 調符
		 * @param {[string]} accent_marks - 調符數組
		 * @returns {string} - 轉換後个臺羅 ASCII 文本，帶數字調
		 */
		text = this.replaceAccents(text, accent_marks);
		text = text.replace(/(\d)([a-z]+)([^a-z]|$)/gi, (match, p1, p2, p3) => {
			return p2 + p1 + p3;
		}); // 數字調放後壁
		text = text.replace(/([a-zA-Z]+)([^\da-zA-Z]|$)/g, (match, p1, p2) => {
			return this.addDefaultToneNumber(p1) + p2;
		}); // 添陰平、陰入數字調
		return text;
	}
	pojSpecialLetterUnicode2Ascii(text) {
		text = text.replace(/ⁿ/g, "nn").replace(/ᴺ/g, "NN");
		if (text.toUpperCase() === text) {
			text = text.replace(/\u0358/g, "O");
		} else {
			text = text.replace(/\u0358/g, "o");
		}
		return text;
	}
	pojUnicode2Ascii(text, standard = null, accent_marks = this.poj_accent_marks) {
		/**
		 * 白話字 Unicode 轉 ASCII
		 * @param {string} text - 輸入个白話字 Unicode 文本，帶 Unicode 調符
		 * @param {[string]} accent_marks - 調符數組
		 * @returns {string} - 轉換後个白話字 ASCII 文本，帶數字調
		 *
		 * 請注意，即个函數着考慮一對多映射，譬論講：
		 * `O͘ => (OO|Oo)`（全大寫 | 首字母大寫）个轉換結果不唯一。
		 * 本函數佇所有字母攏大寫个時，默認轉換做頭一種。孤 `O͘` 或者帶聲調仍然轉換做頭一種。
		 */
		if (standard) {
			if (!this.poj_standards.includes(standard)) {
				throw new Error(`Invalid standard: ${standard}`);
			}
		}
		if (standard === "campbell") {
			text = text.replace(/(h)(ⁿ|ᴺ)/gi, "$2$1");
		}
		text = this.replaceAccents(text, accent_marks);
		text = this.pojSpecialLetterUnicode2Ascii(text);
		if (text.toUpperCase() === text) {
			text = text.replace(/\u0358/g, "O");
		} else {
			text = text.replace(/\u0358/g, "o");
		}
		text = text.replace(/(\d)([a-z]+)([^a-z]|$)/gi, (match, p1, p2, p3) => {
			return p2 + p1 + p3;
		}); // 數字調放後壁
		text = text.replace(/([a-zA-Z]+)([^\da-zA-Z]|$)/g, (match, p1, p2) => {
			return this.addDefaultToneNumber(p1) + p2;
		}); // 添陰平、陰入數字調
		if (standard == "campbell") {
			text = text.replace(/(m|n|ng)(oo)(nn)/ig, "$1$2")
			text = text.replace(/(o)(o)(nn)/g, "$1$3");
		}
		return text;
	}
	pojAscii2TailoAscii(text) {
		/**
		 * 白話字 ASCII 轉臺羅 ASCII
		 * @param {string} text - 輸入个白話字 ASCII 文本，帶數字調
		 * @returns {string} - 轉換後个臺羅 ASCII 文本，帶數字調
		 */
		text = text.replace(/ch/g, "ts")
			.replace(/Ch/g, "Ts")
			.replace(/CH/g, "TS");
		text = text.replace(/o([ae])/g, "u$1");
		text = text.replace(/O([ae])/ig, "U$1");
		text = text.replace(/e(ng|k)/g, "i$1");
		text = text.replace(/E(ng|k)/ig, "I$1");
		return text;
	}
	tailoAscii2PojAscii(text) {
		/**
		 * 臺羅 ASCII 轉白話字 ASCII
		 * @param {string} text - 輸入个臺羅 ASCII 文本，帶數字調
		 * @returns {string} - 轉換後个白話字 ASCII 文本，帶數字調
		 */
		text = text.replace(/ts/g, "ch")
			.replace(/Ts/g, "Ch")
			.replace(/TS/g, "CH");
		text = text.replace(/u([ae])/g, "o$1");
		text = text.replace(/U([ae])/ig, "O$1");
		text = text.replace(/i(ng|k)/g, "e$1");
		text = text.replace(/I(ng|k)/ig, "E$1");
		return text;
	}
	moveTailoToneNumber(syllable) {
		/**
		 * 臺羅數字標調徙位
		 */
		if (/[aeiou]/i.test(syllable)) {
			syllable = syllable.replace(/([aeiou])(r?m?n*h?g?p?t?k?)(\d)/i, "$1$3$2");
			return syllable.replace(/([aeo])([iueo])(\d)/i, "$1$3$2");
		}
		syllable = syllable.replace(/(n)(gh?)(\d)/i, "$1$3$2");
		syllable = syllable.replace(/(m)(h?)(\d)/i, "$1$3$2");
		return syllable;
	}
	tailoAscii2Unicode(text, support_poj_letters = false, accent_marks = this.tailo_accent_marks, normalization = "NFC") {
		/**
		 * 臺羅 ASCII 轉 Unicode
		 * @param {string} text - 輸入个臺羅 ASCII 文本，帶數字調
		 * @param {[string]} accent_marks - 調符數組
		 * @param {string} normalization - Unicode 正則化形式，默認做 "NFC"（可選）
		 * @returns {string} - 轉換後个臺羅 Unicode 文本，帶 Unicode 調符
		 */
		if (support_poj_letters) {
			text = this.pojAscii2TailoAscii(text);
		}
		if (!this.normalization_forms.includes(normalization)) {
			throw new Error(`Invalid normalization form: ${normalization}`);
		}

		// 數字調徙位
		text = text.replace(/[a-zA-Z]+\d/g, (match) => this.moveTailoToneNumber(match));

		// 數字調轉 Unicode 調符
		text = text.replace(/([aeioumn])(\d)/gi, (match, p1, p2) => {
			return p1 + accent_marks[parseInt(p2)];
		});

		return text.normalize(normalization);
	}
	_movePojToneNumber(syllable) {
		/**
		 * 白話字數字標調徙位（無處理 o 介音）
		 */
		if (/[ae]/i.test(syllable)) {
			return syllable.replace(/([ae])([a-z]*)(\d)/i, "$1$3$2");
		} else if (/[o]/i.test(syllable)) {
			return syllable.replace(/(o)([a-z]*)(\d)/i, "$1$3$2");
		} else if (/[u]/i.test(syllable)) {
			return syllable.replace(/(u)([a-z]*)(\d)/i, "$1$3$2");
		} else if (/[i]/i.test(syllable)) {
			return syllable.replace(/(i)([a-z]*)(\d)/i, "$1$3$2");
		}
		syllable = syllable.replace(/(n)(gh?)(\d)/i, "$1$3$2");
		syllable = syllable.replace(/(m)(h?)(\d)/i, "$1$3$2");
		return syllable;
	}
	movePojToneNumber(syllable, standard = null) {
		/**
		 * 白話字數字標調徙位
		 */
		syllable = this._movePojToneNumber(syllable);
		if (standard === "campbell") {
			/**
			 * 甘爲霖白話字標調規則
			 *     介音 o：([a-z])o([ae])\d 或者 ([a-z])o([ae])(nn)\d，標 o；若無標 a、e
			 *     ainnh8：標 i
			 */
			syllable = syllable.replace(/([a-z])(o)([ae])(\d)(nn)?([^a-z]|$)/i, "$1$2$4$3$5$6")
				.replace(/(a)(8)(i)(nnh)/i, "$1$3$2$4");
		} else {
			syllable = syllable.replace(/(o)([ae])(\d)(nn)?([^a-z]|$)/i, "$1$3$2$4$5");
		}
		return syllable;
	}
	pojSpecialLetterAscii2Unicode(text) {
		// oo => o͘
		text = text.replace(/(o)([\u0301\u0300\u0302\u030c\u0304\u030d\u0306]?)(o)/gi, "$1$2\u0358");

		// NN => ᴺ, nn => ⁿ
		text = text.replace(/NN(h?)([^G\u0301\u0300\u0302\u030c\u0304\u030d\u0306]|$)/g, "ᴺ$1$2")
			.replace(/nn(h?)([^g\u0301\u0300\u0302\u030c\u0304\u030d\u0306]|$)/gi, "ⁿ$1$2");
		return text;
	}
	pojAscii2Unicode(text, standard = null, support_tailo_letters = false, support_N = false, accent_marks = this.poj_accent_marks, normalization = "NFC") {
		/**
		 * POJ ASCII 轉 Unicode
		 * @param {string} text - 輸入个白話字 ASCII 文本，帶數字調
		 * @param {string} standard - 白話字標準（可選）
		 * @param {boolean} support_N - 敢支持 -N 轉做 -nn，默認無（解佮大寫 -NN 衝突）
		 * @param {[string]} accent_marks - 調符數組
		 * @param {string} normalization - Unicode 正則化形式，默認做 "NFC"
		 * @returns {string} - 轉換後个白話字 Unicode 文本，帶 Unicode 調符
		 */
		if (standard) {
			if (standard !== "campbell") {
				throw new Error(`Invalid standard: ${standard}`);
			}
		}
		if (support_tailo_letters) {
			console.log(text)
			text = this.tailoAscii2PojAscii(text);
			console.log(text)
		}
		if (!this.normalization_forms.includes(normalization)) {
			throw new Error(`Invalid normalization form: ${normalization}`);
		}

		text = text.replace(/ou/g, "oo")
			.replace(/Ou/g, "Oo")
			.replace(/OU/g, "OO")
			.replace(/hnn/g, "nnh")
			.replace(/HNN/g, "NNH");

		// 支持大寫 N 轉換做 nn
		if (support_N) {
			text = text.replace(/([aeiou])N/g, "$1nn");
		}

		if (standard === "campbell") {
			/**
			 * 臺羅 vs 甘爲霖白話字
			 *     tsh => chh
			 *     ts([^ie]) => ts
			 *     ts([ie]) => ch
			 *     onn => o͘ⁿ
			 *     moo/ngoo => mo͘/ngo͘
			 *     noo => no͘ⁿ
			*/
			text = text.replace(/([^o])onn/g, "$1oonn")
				.replace(/([^o])Onn/g, "$1Oonn")
				.replace(/([^O])ONN/g, "$1OONN")
				.replace(/(n)(oo)([^n])/g, "$1$2nn$3")
				.replace(/(N)(oo)([^n])/g, "$1$2nn$3")
				.replace(/(N)(OO)([^N])/g, "$1$2NN$3")
				.replace(/(m|ng)(oo)(nn)/gi, "$1$2")
				.replace(/ch([^eih])/g, "ts$1")
				.replace(/Ch([^eih])/g, "Ts$1")
				.replace(/CH([^EIH])/g, "TS$1")
				.replace(/ts([eih])/g, "ch$1")
				.replace(/Ts([eih])/g, "Ch$1")
				.replace(/TS([EIH])/g, "CH$1");
		}

		text = text.replace(/[a-zA-Z]+\d/g, (match) => this.movePojToneNumber(match, standard));

		text = text.replace(/([aeioumn])(\d)/gi, (match, p1, p2) => {
			return p1 + accent_marks[parseInt(p2)];
		});

		text = this.pojSpecialLetterAscii2Unicode(text);

		text = text.normalize(normalization);

		if (standard === "campbell") {
			text = text.replace(/(ⁿ|ᴺ)(h)/gi, "$2$1");
		}

		return text;
	}
	moveTailoToneAccent(syllable) {
		/**
		 * 臺羅調符徙位
		 */
		if (/[aeiou]/i.test(syllable)) {
			syllable = syllable.replace(/([aeiou])(r?m?n*h?g?p?t?k?)([\u0301\u0300\u0302\u030c\u0304\u030d\u030b])/i, "$1$3$2");
			return syllable.replace(/([aeo])([iueo])([\u0301\u0300\u0302\u030c\u0304\u030d\u030b])/i, "$1$3$2");
		}
		syllable = syllable.replace(/(n)(gh?)([\u0301\u0300\u0302\u030c\u0304\u030d\u030b])/i, "$1$3$2");
		syllable = syllable.replace(/(m)(h?)([\u0301\u0300\u0302\u030c\u0304\u030d\u030b])/i, "$1$3$2");
		return syllable;
	}
	pojUnicode2TailoUnicode(text, poj_standard = null, normalization = "NFC") {
		/**
		 * POJ Unicode 轉 臺羅 Unicode
		 * @param {string} text - 輸入个白話字 Unicode 文本
		 * @param {string} poj_standard - 白話字標準（可選）
		 * @param {string} normalization - Unicode 正則化形式，默認做 "NFC"
		 * @returns {string} - 轉換後个臺羅 Unicode 文本
		 */
		text = text.normalize("NFD").replace("\u0306", "\u030b");
		text = this.pojSpecialLetterUnicode2Ascii(text);
		if (poj_standard === "campbell") {
			text = text.replace(/(h)(nn)/gi, "$2$1");
			text = text.replace(/(m|n|ng)(o)([\u0301\u0300\u0302\u030c\u0304\u030d\u030b]?)(o)(nn)/gi, "$1$2$3$4");
			text = text.replace(/(o)([\u0301\u0300\u0302\u030c\u0304\u030d\u030b]?)(o)(nn)/gi, "$1$2$4")
		}
		text = text.replace(/([\u0301\u0300\u0302\u030c\u0304\u030d\u030b])([a-z]+)([^a-z]|$)/gi, (match, p1, p2, p3) => {
			return p2 + p1 + p3;
		}); // 調符放後壁

		text = this.pojAscii2TailoAscii(text);

		text = text.replace(/[a-zA-Z]+[\u0301\u0300\u0302\u030c\u0304\u030d\u030b]/g, (match) => this.moveTailoToneAccent(match));

		return text.normalize(normalization);
	}
	pojUnicode2TailoUnicodeCascade(text, poj_standard = null, normalization = "NFC") {
		/**
		 * POJ Unicode 轉 臺羅 Unicode（級聯版，效率較下）
		 * @param {string} text - 輸入个白話字 Unicode 文本
		 * @param {string} poj_standard - 白話字標準（可選）
		 * @param {string} normalization - Unicode 正則化形式，默認做 "NFC"
		 * @returns {string} - 轉換後个臺羅 Unicode 文本
		 */
		text = this.pojUnicode2Ascii(text, poj_standard);
		text = this.pojAscii2TailoAscii(text);
		return this.tailoAscii2Unicode(text, normalization = normalization);
	}
	_movePojToneAccent(syllable) {
		/**
		 * 白話字調符徙位（無處理 o 介音）
		 */
		if (/[ae]/i.test(syllable)) {
			return syllable.replace(/([ae])([a-z]*)([\u0301\u0300\u0302\u030c\u0304\u030d\u0306])/i, "$1$3$2");
		} else if (/[o]/i.test(syllable)) {
			return syllable.replace(/(o)([a-z]*)([\u0301\u0300\u0302\u030c\u0304\u030d\u0306])/i, "$1$3$2");
		} else if (/[u]/i.test(syllable)) {
			return syllable.replace(/(u)([a-z]*)([\u0301\u0300\u0302\u030c\u0304\u030d\u0306])/i, "$1$3$2");
		} else if (/[i]/i.test(syllable)) {
			return syllable.replace(/(i)([a-z]*)([\u0301\u0300\u0302\u030c\u0304\u030d\u0306])/i, "$1$3$2");
		}
		syllable = syllable.replace(/(n)(gh?)([\u0301\u0300\u0302\u030c\u0304\u030d\u0306])/i, "$1$3$2");
		syllable = syllable.replace(/(m)(h?)([\u0301\u0300\u0302\u030c\u0304\u030d\u0306])/i, "$1$3$2");
		return syllable;
	}
	movePojToneAccent(syllable, standard = null) {
		/**
		 * 白話字調符徙位
		 */
		syllable = this._movePojToneAccent(syllable);
		if (standard === "campbell") {
			/**
			 * 甘爲霖白話字標調規則
			 *     介音 o：([a-z])o([ae])\d 或者 ([a-z])o([ae])(nn)\d，標 o；若無標 a、e
			 *     ainnh8：標 i
			 */
			syllable = syllable.replace(/([a-z])(o)([ae])([\u0301\u0300\u0302\u030c\u0304\u030d\u0306])(nn)?([^a-z]|$)/i, "$1$2$4$3$5$6")
				.replace(/(a)(8)(i)(nnh)/i, "$1$3$2$4");
		} else {
			syllable = syllable.replace(/(o)([ae])([\u0301\u0300\u0302\u030c\u0304\u030d\u0306])(nn)?([^a-z]|$)/i, "$1$3$2$4$5");
		}
		return syllable;
	}
	tailoUnicode2PojUnicode(text, poj_standard = null, normalization = "NFC") {
		/**
		 * 臺羅 Unicode 轉白話字 Unicode
		 * @param {string} text - 輸入个臺羅 Unicode 文本
		 * @param {string} poj_standard - 白話字標準（可選）
		 * @param {string} normalization - Unicode 正則化形式，默認做 "NFC"
		 * @returns {string} - 轉換後个白話字 Unicode 文本
		 */
		text = text.normalize("NFD").replace("\u030b", "\u0306");
		text = text.replace(/([\u0301\u0300\u0302\u030c\u0304\u030d\u0306])([a-z]+)([^a-z]|$)/gi, (match, p1, p2, p3) => {
			return p2 + p1 + p3;
		}); // 調符放後壁
		text = this.tailoAscii2PojAscii(text);
		text = text.replace(/[a-zA-Z]+[\u0301\u0300\u0302\u030c\u0304\u030d\u0306]/g, (match) => this.movePojToneAccent(match, poj_standard));

		text = this.pojSpecialLetterAscii2Unicode(text);

		return text.normalize(normalization);
	}
	tailoUnicode2PojUnicodeCascade(text, poj_standard = null, normalization = "NFC") {
		/**
		 * 臺羅 Unicode 轉白話字 Unicode（級聯版，效率較下）
		 * @param {string} text - 輸入个臺羅 Unicode 文本
		 * @param {string} poj_standard - 白話字標準（可選）
		 * @param {string} normalization - Unicode 正則化形式，默認做 "NFC"
		 * @returns {string} - 轉換後个白話字 Unicode 文本
		 */
		text = this.tailoUnicode2Ascii(text);
		text = this.tailoAscii2PojAscii(text);
		return this.pojAscii2Unicode(text, poj_standard, normalization = normalization);
	}
	greet() {
		console.log('THOKIT 桃橘 is initialized...')
	}
}

// 條件導出
if (typeof module !== 'undefined' && module.exports) {
	// Node.js 環境
	module.exports = { ThoKit };
} else if (typeof window !== 'undefined') {
	// 瀏覽器環境
	window.ThoKit = ThoKit;
}

export { ThoKit };
