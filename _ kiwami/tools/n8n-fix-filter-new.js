const fs = require("fs");
const path = require("path");
const os = require("os");
const stateDir = path.join(os.homedir(), ".n8n-state");
const stateFile = path.join(stateDir, "clockify_last_id.txt");
let lastId = "";
try {
  lastId = fs.readFileSync(stateFile, "utf8").trim();
} catch (e) {}

const items = $input.all();

// タイマー実行中（end=null）のエントリを除外
const completed = items.filter(item => item.json.timeInterval.end !== null);

if (completed.length === 0) return [];

// 初回起動 or 状態ファイル消失（旧 /tmp/ 配置時代の再起動消失対策）
// → 全件再投入による Day One 重複を避けるため、現在の最新IDで状態を初期化して終了
if (!lastId) {
  try { fs.mkdirSync(stateDir, { recursive: true }); } catch (e) {}
  fs.writeFileSync(stateFile, completed[0].json.id);
  return [];
}

// Clockify APIは新しい順で返す。lastIdの位置を探す
const lastIndex = completed.findIndex(item => item.json.id === lastId);

if (lastIndex === 0) {
  // 最新エントリが前回と同じ → 新規なし
  return [];
}

// lastIdがページ外（API page sizeを超える滞留が発生）→ 全件再投入は重複の元なので空を返す
// 想定外の状態なので、復旧は手動（lastId を直近の取りこぼし1つ前のIDに書き換えて再処理）
if (lastIndex === -1) {
  return [];
}

// lastIdより新しいエントリだけ取得
// ※last_idは後段（Day One登録後）で更新する。ここで更新すると
//   Google Calendar認証エラー等でlast_idだけ進んで塩漬け化するため。
return completed.slice(0, lastIndex);
