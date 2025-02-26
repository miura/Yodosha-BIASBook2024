# 『型で実践する生物画像解析　ImageJ・Python・napari』サポートサイト

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14930301.svg)](https://doi.org/10.5281/zenodo.14930301)

教科書からこちらのサイトに来た方は、特定の項目を探しているのではないかと思う。
以下の目次からその項目を探し、リンク先を参照してほしい。

## 環境構築など

### Fijiの基本的な操作方法

1. [Fijiのインストールの仕方](instructions/InstallingFiji.md)
2. [FIjiを最新状態にする方法](instructions/UpdatingFiji.md)
3. [Update Siteを使ってFijiにプラグインを追加する方法](instructions/InstallingPluginViaUpdateSites.md)
4. [選択領域の保存の仕方](instructions/savingROI.md)

### 深層学習のための環境

1. [PythonのGPU環境構築](kawai/PythonのGPU環境構築.md)

## コードとサンプル画像へのリンク

1. 基礎編
   1. 序論 ――生物画像解析の枠組みを理解する（三浦　耕太）
   2. Jythonの基礎知識と書き方（三浦　耕太）
      1. [コード](miura/JythonBasics)
   3. napariの基礎知識と書き方（黄　承宇）
      1. [コード（ノートブック）](huang/code/sample_code.ipynb)
      2. [サンプル画像](huang/code/sample_images)
   4. Google Colaboratoryの利用法 ――クラウドPythonプログラミング（戸田　陽介）
2. 実践編
   1. 核膜に移行するタンパク質の動態の測定（三浦　耕太）
      1. [コード](miura/module_Nucleus)
      1. [サンプル画像へのリンク](miura/module_Nucleus/README.md)
   2. 電子顕微鏡画像のミトコンドリア分節化と形状のクラスタリング解析（河合　宏紀）
      1. [ノートブック](kawai/kawai.ipynb)
   3. 腫瘍血管における三次元管状構造ネットワークの分析（三浦　耕太）
      1. [コードとサンプル画像](miura/module_bloodVessels)
   4. 細胞移動を定量するための粒子追跡（トラッキング）（塚田　祐基）
      1. [コード](/tsukada/)
      2. [サンプル画像](/tsukada/croped_sample.tif)
   5. 細胞周期の蛍光プローブFucciの時系列データ解析（平塚　徹）
      1. [コード](hiratsuka/)
      1. [サンプル画像](hiratsuka/README.md)
   6. 甲殻類モデル生物Parhyale hawaiensisの脚再生過程の細胞動態解析（菅原　皓）
      1. [コード](sugawara/module_Mastodon)
      1. [サンプル画像](sugawara/README.md)
   7. イネのデジタルカメラ画像によるバイオマスの推定（戸田　陽介）
      1. [ノートブック](toda/実験医学（戸田担当分）.md)
   8. Micro-Managerによる顕微鏡制御（土田マーク彰・塚田　祐基）
      1. [コード](tsuchida/)
3. 論文投稿編
   1. 論文投稿のための画像解析の再現性チェックリストとGitHubの活用（三浦　耕太）
      1. [リンクなど](miura/reproducibleMethods.md)
   2. 画像データレポジトリ ―種類と使い方―（遠里　由佳子，京田　耕司,　 大浪　修一）
4. 発展編
   1. イメージングデータの次世代ファイルフォーマット（京田　耕司，大浪　修一）
   2. 生物画像解析の専門家ネットワークとGloBIAS（三浦　耕太）
5. 付録
   1. 分節化のための機械学習ツールのリスト
   2. 日英対訳表
