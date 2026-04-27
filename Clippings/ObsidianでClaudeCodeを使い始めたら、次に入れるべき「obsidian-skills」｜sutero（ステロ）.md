---
title: "ObsidianでClaudeCodeを使い始めたら、次に入れるべき「obsidian-skills」｜sutero（ステロ）"
source: "https://note.com/sutero/n/n1e44caafe742"
author:
  - "[[sutero（ステロ）]]"
published: 2026-04-16
created: 2026-04-27
description: "先日、ObsidianにClaudianを導入して快適になったという投稿をした。  ありがたいことに、思った以上に読んでもらえて嬉しい限り。  前述の投稿では、CLAUDE.mdという設定ファイルにObsidianの記法やリンクの作り方を書いておけば、Claude Codeがそれに従ってくれる、ということをを書いている。  今回は、その次のステップの話。   トークン消費という現実  Claudianを導入し、ObsidianでClaudeCodeを使い始めると、これまで以上に、色々やりたくなる。  ファイルの整理、リンクの構築、リストの作成、URLの取得と要約などなど、やれそう！っ"
tags:
  - "clippings"
---
先日、ObsidianにClaudianを導入して快適になったという投稿をした。

<iframe data-src="https://note.com/embed/notes/ncdf112dba547" src="https://note.com/embed/notes/ncdf112dba547" height="234px"></iframe>

ありがたいことに、思った以上に読んでもらえて嬉しい限り。

前述の投稿では、CLAUDE.mdという設定ファイルにObsidianの記法やリンクの作り方を書いておけば、Claude Codeがそれに従ってくれる、ということをを書いている。

今回は、その次のステップの話。

## トークン消費という現実

Claudianを導入し、ObsidianでClaudeCodeを使い始めると、これまで以上に、色々やりたくなる。

ファイルの整理、リンクの構築、リストの作成、URLの取得と要約などなど、やれそう！って思うと、頼んだり指示したり。

あれもこれもと試しているのと同時に、仕事でも使っていることもあり、トークン消費で制限にかかるように。

以前はOpusモデルでガンガン使っていても全然平気だったのが、特に3月の終わり頃から、急激に制限がかかるようになる。

使用量は特に増えていない。

Sonnetメインに切り替えてもそうなる。

Anthropic社も内部のエラー等を認めて、謝罪とお詫びのクレジット配布まで行っているものの、トークン消費が厳しい状況は続いている。

こうなると、限られたトークンをどう賢く使うか、という話になってくる。

## CLAUDE.mdが膨らんでいた

トークン消費を見直す中で気付いたのが、CLAUDE.mdの肥大化。

CLAUDE.mdは、ClaudeCodeが毎回最初に読み込む設定ファイル。

Obsidianの記法はこう書いて、リンクはこう作って、フォルダ構成はこうで、と色々書き込んでいたら、かなりの分量になっていた。

毎回読み込まれるということは、毎回その分のトークンを消費しているということ。

ちょっとした質問をするだけでも、CLAUDE.mdの全文が読み込まれる。

これは無駄が多い。

## obsidian-skillsという選択肢

そこで活用し始めたのが「obsidian-skills」。

Obsidian CEOのkepano（Steph Ango）が自ら公開している、AIエージェント向けのスキルセット。

<iframe allowfullscreen="" allow="autoplay *; encrypted-media *; ch-prefers-color-scheme *" src="https://cdn.iframe.ly/gzbQxHch?v=1&amp;app=1"></iframe>

ClaudeCodeには「Agent Skills」という仕組みがある。

CLAUDE.mdに全部書くのではなく、スキルとして分離しておけば、必要な時だけ参照される。

つまり、毎回読み込まれるCLAUDE.mdとは違って、トークン消費を抑えることが可能に。

obsidian-skillsには5つのスキルが含まれている。

- **obsidian-markdown** ：Wikiリンク・コールアウト・プロパティ等のObsidian記法
- **obsidian-bases** ：.baseファイルの作成・編集（フィルター・数式・ビュー）
- **defuddle** ：WebページをクリーンなMarkdownに変換
- **json-canvas** ：.canvasファイルの作成・編集
- **obsidian-cli** ：Obsidianを直接操作するCLI

Obsidianの作者自身が、AIエージェントと連携させるために作っているという点で、安心感があるし、安定して動くだろうと想像出来る。

## CLAUDE.mdを半分以下にできた

obsidian-skillsを導入してから、CLAUDE.mdの内容を見直した。

毎回必ず使う指示だけを残して、それ以外はスキル参照に切り替える。

例えば、Obsidianの記法に関する指示は、obsidian-markdownスキルがカバーしてくれるので、CLAUDE.mdにはスキル参照とだけ。

結果、CLAUDE.mdのボリュームは半分以下になった。

毎回のトークン消費が減って、その分、本来やりたい作業にトークンを使えるように。

## 便利な3つのスキル

5つ全部入れているが、日常的に使っているのは3つ。

### obsidian-markdown：これはマスト

ClaudeCodeに何か指示すると、出力がObsidian形式になってくれる。

Wikiリンク、コールアウト、プロパティ（YAML frontmatter）など、Obsidian固有の記法をClaude Codeが理解した上で書いてくれるので、出力されたものをそのまま使える。

入れていないと、標準的なMarkdownで出力されてしまい、後から手動でObsidian記法に直すって、手間も時間も余計にかかるし。

これを入れるだけで解決するので、マスト。

### obsidian-bases：Notionで挫折したリストが簡単に

Obsidianには「Bases」という機能があって、.baseファイルでデータベース的なリストを作成可能になっている。

このbaseファイルを、読書リストや買い物リストとして、活用中。

昔、Notionを使っていた時に、データベース機能でリストを作ろうとして挫折というか面倒でやらなくなってしまった経験が。

現在はnotionにもAIが導入されているので、もっと簡単に出来るとは思うけれど、当時は、ひとつずつ手動で項目を入れていく作業が面倒で、結局使わなくなった。

obsidian-basesスキルを入れておくと、ClaudeCodeが.baseファイルの構造を理解してくれる。

読んだ本のAmazonのURLを渡すか、Obsidian Web Clipperで取り込んだファイルを指定して「読書リストに入れて」と言うだけ。

あの時、挫折したことが、こんなに簡単にできるのか、と。

### defuddle：URL取得のトークン節約

URLを渡し「この内容を参照して」「要約して」と頼むことは結構多い。

ただ、Webページをそのまま取得すると、ナビゲーションやフッター、広告など、本文以外の情報も大量に含まれて、トークンを無駄に消費してしまう。

defuddleは、Webページから本文だけをクリーンなMarkdownに変換してくれるスキル。

余計な情報を除去した状態で取得できるので、トークン消費がかなり抑えられる。

トークンが厳しい状況では、この差は大きい。

## 残り2つは入れておくだけ

json-canvas（.canvasファイルの作成・編集）とobsidian-cli（ObsidianのCLI操作）は、正直ほとんど使っていない。

ただ、obsidian-skillsとして5つセットでGitHubに公開されているし、スキルは必要な時だけ参照される仕組みなので、入れておいても邪魔にはならない。

使う場面が来た時にすでに入っている、という状態にしておけば良い。

## 導入方法

導入は簡単で、GitHubからダウンロードして、Obsidianのvault内に配置するだけ。

1. [https://github.com/kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) からリポジトリをダウンロード
2. vault内の \`.claude/skills/\` フォルダに、使いたいスキルのフォルダを配置
3. 完了

CLAUDE.mdの編集も、設定ファイルの書き換えも不要。

配置するだけでClaudeCodeが認識してくれる。

GitHubがよく分からないという人は、Claudianで「obsidian-skillsを導入して」と頼めば、ダウンロードから配置までやってくれる。

あと、obsidian-markdownとdefuddleはほぼ毎回使うスキルなので、CLAUDE.mdに以下のような一文を入れておくのがオススメ。

```javascript
- Obsidian記法：'obsidian-markdown' スキル
- 外部URL取得：'defuddle' スキル
```

Opusモデルだとスキルの存在を自分で見つけて使ってくれることが多いが、それ以外のモデルだとスキルを飛ばすことが結構ある。

一文書いておくだけで確実に使ってくれるようになるので、これは記述しておいて損はない。

## 追加セットアップが必要なスキル

5つのうち、 **defuddle** と **obsidian-cli** だけは追加のセットアップが必要。

**defuddle** は、CLIをインストールする。

```
npm install -g defuddle-cli
```

これだけ。

**obsidian-cli** は、Obsidianの設定から組み込みCLI機能を有効にする。

「Obsidianについて」セクションの最下部に「コマンドラインインターフェースを有効にします」があるので、オンにするだけ。

以前はCatalystライセンスが必要だったが、v1.12.7（2026年3月）から全ユーザーに無料開放されている。

## まず入れてみよう

ObsidianでClaudeCodeを使い始めたばかりの人も、しばらく使っている人も、obsidian-skillsは入れておいて損はない。

配置するだけで導入できるし、トークン消費の改善にも繋がる。

Obsidianの作者自身が、AIエージェントとの連携を前提に作っているスキルセットなので、言わば純正みたいな感じでもあるし。

CLAUDE.mdに色々書き込む前に、まずこれを入れてみるのがいい。

<iframe height="210" data-src="https://note.com/embed/notes/n2be437e390a2" src="https://note.com/embed/notes/n2be437e390a2"></iframe>

---

[**Obsidian×AI　自分だけの知識のデータベースをつくる情報収集・活用テクニック** *amzn.to*](https://amzn.to/4cobzeA)

[*2,893円* (2026年04月16日 18:50時点](https://amzn.to/4cobzeA)

[

Amazon.co.jpで購入する

](https://amzn.to/4cobzeA)

[**Obsidian×AI 自動化の教科書: CursorやClaude Codeでメモを資産に！ ChatGPT・Gemini連携で新時代の情報管理術** *amzn.to*](https://amzn.to/4eqdphF)

[*800円* (2026年04月16日 19:18時点](https://amzn.to/4eqdphF)

[

Amazon.co.jpで購入する

](https://amzn.to/4eqdphF)