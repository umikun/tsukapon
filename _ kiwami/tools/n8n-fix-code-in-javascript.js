const { execSync } = require("child_process");
const fs = require("fs");
const stateFile = "/tmp/n8n_clockify_last_id.txt";

// Filter Newの出力（Clockifyデータ）を直接参照
const clockifyItems = $("Filter New").all();

for (const item of clockifyItems) {
  const c = item.json.project?.clientName || "";
  const p = item.json.project?.name || "";
  const d = item.json.description || "";
  const start = new Date(item.json.timeInterval.start);
  const end = new Date(item.json.timeInterval.end);
  const dur = item.json.timeInterval.duration;
  const hours = dur.match(/(\d+)H/);
  const mins = dur.match(/(\d+)M/);
  const h = hours ? parseFloat(hours[1]) : 0;
  const m = mins ? parseFloat(mins[1]) : 0;
  const total = (h + m / 60).toFixed(1);
  const fmt = (dt) => {
    return dt.toLocaleDateString("en-US", {
      month: "long",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
      timeZone: "Asia/Tokyo"
    });
  };
  const lines = [
    "【" + c + "：" + p + "】" + d,
    "",
    "> Start：" + fmt(start),
    "> End：" + fmt(end),
    "> 作業時間：" + total + "h",
    "",
    "Location：ウィズハイム天神山"
  ];
  const entry = lines.join("\n");
  const tmp = "/tmp/dayone_entry.txt";
  fs.writeFileSync(tmp, entry);
  const shellEscape = (s) => "'" + String(s).replace(/'/g, "'\\''") + "'";
  const tagsOpt = c ? " --tags " + shellEscape(c) : "";
  execSync("cat " + tmp + " | /usr/local/bin/dayone new --journal work" + tagsOpt);
}

// Google Calendar + Day One 両方への登録が全件成功した時点で
// last_id を最新IDに更新する（Clockify APIは新しい順で返るため [0] が最新）
if (clockifyItems.length > 0) {
  fs.writeFileSync(stateFile, clockifyItems[0].json.id);
}

return $input.all();