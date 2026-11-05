# 九星気学盤(スマホアプリ版)

年盤・月盤・日盤と、生年月日からの吉方・凶方を表示するアプリです。
サーバーは不要で、ファイルを公開するだけで使えます。電波がなくても開けます。

## ファイル
- index.html … アプリ本体
- manifest.webmanifest … アプリの名前・アイコンの設定
- sw.js … オフラインで開くための設定
- icons/ … アイコン

## GitHub Pagesで公開する(無料)
1. https://github.com でアカウントを作り、新しいリポジトリを作ります(名前は例: kigaku、Publicにします)。
2. 「Add file」→「Upload files」で、このフォルダの中身(index.html、manifest.webmanifest、sw.js、icons フォルダ)をすべてアップロードして「Commit changes」を押します。
3. リポジトリの「Settings」→「Pages」を開き、「Source」を「Deploy from a branch」、Branchを「main」・「/ (root)」にして「Save」を押します。
4. 数分後に、https://(ユーザー名).github.io/kigaku/ で開けるようになります。

## スマホのホーム画面に追加する
- iPhone: Safariで上のURLを開き、共有ボタン →「ホーム画面に追加」。
- Android: Chromeで開き、メニュー →「アプリをインストール」または「ホーム画面に追加」。

追加したアイコンから開くと、アドレスバーのない全画面で動きます。一度開けば、電波がなくても使えます。

## 自分のサイトに置く場合
このフォルダの中身を、サーバーの好きなフォルダ(例: /kigaku/)にそのままアップロードします。https:// で開ける場所に置いてください(http:// ではオフライン機能が動きません)。

## 内容を更新したとき
index.html を差し替えたら、sw.js の 2行目 `VERSION = 'kigaku-v1'` の数字を上げます(例: kigaku-v2)。そうしないと、スマホに古い版が残ることがあります。
