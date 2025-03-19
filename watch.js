// watch.js
const chokidar = require('chokidar');
const { exec } = require('child_process');

// 監聽 src/thokit.js 文件
const watcher = chokidar.watch('src/thokit.js', {
  persistent: true,
});

// 文件變化時重新生成導出文件
watcher.on('change', (path) => {
  console.log(`文件已修改: ${path}`);
  exec('npm run build', (err, stdout, stderr) => {
    if (err) {
      console.error('構建失败:', err);
      return;
    }
    console.log('構建成功:', stdout);
  });
  exec('npm run test', (err, stdout, stderr) => {
    if (err) {
      console.error('測試失败:', err);
      return;
    }
    console.log('測試成功:', stdout);
  });
});

console.log('當咧監聽 src/thokit.js...');