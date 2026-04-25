const fs = require("fs");
const stateFile = "/tmp/n8n_clockify_last_id.txt";
let lastId = "";
try {
  lastId = fs.readFileSync(stateFile, "utf8").trim();
} catch (e) {}

const items = $input.all();

// タイマー実行中（end=null）のエントリを除外
const completed = items.filter(item => item.json.timeInterval.end !== null);

if (completed.length === 0) return [];

// Clockify APIは新しい順で返す。lastIdの位置を探す
const lastIndex = completed.findIndex(item => item.json.id === lastId);

if (lastIndex === 0) {
  // 最新エントリが前回と同じ → 新規なし
  return [];
}

// lastIdより新しいエントリだけ取得
// lastIdが見つからない場合も全件を新規として処理
// ※last_idは後段（Day One登録後）で更新する。ここで更新すると
//   Google Calendar認証エラー等でlast_idだけ進んで塩漬け化するため。
return lastIndex === -1 ? completed : completed.slice(0, lastIndex);