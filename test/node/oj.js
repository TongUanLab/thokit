const { ThoKit } = require('../../dist/thokit.cjs');


const fs = require('fs');
const { performance } = require('perf_hooks');

const thokit = new ThoKit();

const receipts = {
	"poj_a2u": {
		"src": "./test/data/poj.asc.txt",
		"tgt": "./test/data/poj.uni.hyp",
		"ref": "./test/data/poj.uni.txt",
		"fn": thokit.pojAscii2Unicode.bind(thokit),
	},
	"poj_u2a": {
		"src": "./test/data/poj.uni.txt",
		"tgt": "./test/data/poj.asc.hyp",
		"ref": "./test/data/poj.asc.txt",
		"fn": thokit.pojUnicode2Ascii.bind(thokit),
	},
	"tl_a2u": {
		"src": "./test/data/tailo.asc.txt",
		"tgt": "./test/data/tailo.uni.hyp",
		"ref": "./test/data/tailo.uni.txt",
		"fn": thokit.tailoAscii2Unicode.bind(thokit),
	},
	"tl_u2a": {
		"src": "./test/data/tailo.uni.txt",
		"tgt": "./test/data/tailo.asc.hyp",
		"ref": "./test/data/tailo.asc.txt",
		"fn": thokit.tailoUnicode2Ascii.bind(thokit),
	},
	"poja2tla": {
		"src": "./test/data/poj.asc.txt",
		"tgt": "./test/data/tailo.asc.poja2tla.hyp",
		"ref": "./test/data/tailo.asc.txt",
		"fn": thokit.pojAscii2TailoAscii.bind(thokit),
	},
	"tla2poja": {
		"src": "./test/data/tailo.asc.txt",
		"tgt": "./test/data/poj.asc.tla2poja.hyp",
		"ref": "./test/data/poj.asc.txt",
		"fn": thokit.tailoAscii2PojAscii.bind(thokit),
	},
	"poju2tlu": {
		"src": "./test/data/poj.uni.txt",
		"tgt": "./test/data/tailo.uni.poju2tlu.hyp",
		"ref": "./test/data/tailo.uni.txt",
		"fn": thokit.pojUnicode2TailoUnicode.bind(thokit),
	},
	"tlu2poju": {
		"src": "./test/data/tailo.uni.txt",
		"tgt": "./test/data/poj.uni.tlu2poju.hyp",
		"ref": "./test/data/poj.uni.txt",
		"fn": thokit.tailoUnicode2PojUnicode.bind(thokit),
	}
};

/**
 * 判斷轉換結果着毋着
 * @param {boolean} strict - 是否嚴格模式
 * @param {string} mode - 模式名
 */
function judge(strict = true, mode = "") {
	let total = 0;
	let correct = 0;

	if (mode) {
		// 處理單个模式
		const srcContent = fs.readFileSync(receipts[mode]["src"], "utf-8").split("\n");
		const refContent = fs.readFileSync(receipts[mode]["ref"], "utf-8").split("\n");
		const fn = receipts[mode]["fn"];

		if (srcContent.length !== refContent.length) {
			throw new Error(`Source and reference files have different lengths for mode: ${mode}`);
		}

		const startTime = performance.now();
		const tgtLines = srcContent.map((line) => fn(line));
		const endTime = performance.now();

		console.log(`Time for ${mode}: ${((endTime - startTime) / 1000).toFixed(6)}s`);

		for (let i = 0; i < srcContent.length; i++) {
			if (tgtLines[i] === refContent[i]) {
				correct++;
			}
		}

		fs.writeFileSync(receipts[mode]["tgt"], tgtLines.join("\n"), "utf-8");
		total = srcContent.length;
	} else {
		// 處理所有模式
		let total_time = 0;
		for (const _mode in receipts) {
			const srcContent = fs.readFileSync(receipts[_mode]["src"], "utf-8").split("\n");
			const refContent = fs.readFileSync(receipts[_mode]["ref"], "utf-8").split("\n");
			const fn = receipts[_mode]["fn"];

			// if (srcContent.length !== refContent.length) {
			// 	throw new Error(`Source and reference files have different lengths for mode: ${_mode}`);
			// }

			const startTime = performance.now();
			const tgtLines = srcContent.map((line) => fn(line));
			const endTime = performance.now();
			total_time += (endTime - startTime) / 1000
			console.log(`Time for ${_mode}: ${((endTime - startTime) / 1000).toFixed(6)}s`);

			let _correct = 0;
			for (let i = 0; i < srcContent.length; i++) {
				if (tgtLines[i] === refContent[i]) {
					_correct++;
				}
			}

			const accuracy = _correct / srcContent.length;
			console.log(`Accuracy: ${accuracy.toFixed(6)}`);

			fs.writeFileSync(receipts[_mode]["tgt"], tgtLines.join("\n"), "utf-8");
			total += srcContent.length;
			correct += _correct;
		}
		console.log(`Total time: ${total_time.toFixed(6)}s`)
	}

	console.log(`Overall accuracy: ${(correct / total).toFixed(6)}`);
}


if (require.main === module) {
	judge();
}
