# 速習 napari ―基礎知識と書き方

黄承宇
Cheng-Yu Huang

ケンブリッジ大学大学院生理学、発生及び神経生物研究科
Department of Physiology, Development and Neuroscience, University of Cambridge

近年，生物画像解析の分野は急速に進歩しており、複雑な多次元データに対応できる画像可視化ツールの需要が増大している。その中で、Napariは特に注目される新しい画像可視化ツールである。Napariは、画像（Image）、点群（Points）、ラベル（Labels）、形状（Shapes）、トラック（Tracks）など、さまざまなデータ形式に対応しており、これらを直感的に表示できる。また、NapariはPython上で構築されたオープンソースソフトウェアであり、ユーザーフレンドリーでカスタマイズ可能である。さらに、Pythonのエコシステムを活かし、多くの科学的ライブラリと連携することで、幅広い機能を提供している。

本章では、まずcondaを使用してNapariを実行するためのPython環境をセットアップする方法を説明する。その後、PythonコーディングのためのインターフェースであるJupyterノートブックを紹介し、データサイエンスで広く利用されるパッケージを取り上げながら、Napariの基本的な知識と使用方法を実践的に学んでいく。

# はじめの一歩
## Python環境のセットアップ
### Anaconda/Minicondaのインストール
Pythonパッケージ管理ツールであるconda (https://conda.io/projects/conda/en/latest/index.html) を使用してPython環境を設定する。condaにはAnacondaとMinicondaの二つのバージョンがあり、どちらも本章および後の章で必要なPython環境を提供する。Anacondaにはパッケージ管理のためのGUI（グラフィカルユーザーインターフェース）が付属しているが、Minicondaにはそれがない。Minicondaでは（Anacondaでも可能だが）コマンドラインでパッケージを管理する。Anacondaはプログラミング初心者向けの追加機能を多く含むため、Minicondaよりも多くのストレージを必要とする（約4.4 GB対約480 MB）。詳細についてはこちら(https://docs.anaconda.com/distro-or-miniconda/)を参照されたい。本チュートリアルでは、すべてをコマンドラインで行うため、Minicondaで十分である。ダウンロードリンクはこちら(https://docs.anaconda.com/miniconda/#miniconda-latest-installer-links)である。

### Minicondaで仮想環境(venv)を作成する
次に、condaを使って仮想環境（virtual environment, venv）を作成する。venvは、異なるプロジェクトごとに必要なパッケージを分けて管理するためのツールである。これにより、各プロジェクトに独立したワークベンチを作成し、プロジェクトごとの依存関係を管理できる。多くの場合、異なるプロジェクトには異なるパッケージが必要であるため、プロジェクト間のパッケージコンフリクトを防ぎ、パッケージをプロジェクト単位で管理するためにvenvを使用する。さらに、Python環境が破損した場合でも、環境を削除して再作成することが可能である。

では、コマンドラインを使用して環境を作成する。Python環境のインストールに関する詳細なチュートリアルはこちら(https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)で見つけることができる。まず、エクスプローラーで “anaconda prompt (miniconda3)” を見つけてクリックする。図1のような画面が現れる。

![図1](figures\1_anaconda_prompt_start.png)

*図1: Anaconda Promptのスタート画面*

図1のプロンプト中の`(base)`は、ベース、デフォルトの環境にいることを意味している。次に、napari-envという名前の環境を作成する。環境を作成するには、次のコマンドを実行する：

```bash
conda create -y -n napari-env -c conda-forge python=3.11
```

ここでは、Python 3.11の環境を作成する。condaが続行するかどうか尋ねる場合`proceed([y]/n)? `には、`y`を入力する。インストールが完了すると、`done`と表示される（図2A）。次に、環境を conda activate コマンドでアクセスする（図2B）。コマンドラインの始まりが
`(base)`から`(napari-env)`に変わる（図2C）。これは、`napari-env`の仮想環境に入ったことを意味する。

![図2](figures\2_entering_napari_env.png)

*図2: Napari-env 仮想環境に入る*

### napariとJupyterノートブックおよびその他のパッケージのインストール

`(napari-env)`に入ったら、まずnapariをインストールする：

```bash
python -m pip install "napari[all]"
```
インストールが終わると、図2Cの`(napari-env) … >` が再び表示される。

次に、他の画像解析や画像処理に頻繁に使われるパッケージをインストールする。これには、コーディングやnapariとのインターフェースに使用するjupyter、画像処理やマトリックス計算を含む数値演算のためのnumpy、作図のためのmatplotlib、科学計算のためのscipy、画像処理に使われる多くのアルゴリズムを含むscikit-image、及び表形式データの操作のためのpandasが含まれている。これらのパッケージをインストールするには、次のコマンドを実行する：

```bash
pip3 install numpy matplotlib scipy scikit-image jupyter pandas
```
`proceed([y]/n)? `と表示されたら、`y`を入力し、<kbd>Enter</kbd>キーを押す。

以上で環境インストール手順は終了である。

ここで紹介している方法以外にも、yamlファイル（環境設定ファイル）を使用して環境をインストールすることも可能である。その方法については、後の章で紹介される。

## 次回napari-env環境に戻る方法

コマンドウィンドウを閉じて、再度前回作成した環境に戻りたい場合がある。しかし、コマンドプロンプトを再起動するたびに、常に`(base)`環境に戻ってしまう。
`(napari-env)`環境に戻るには、次のコマンドを入力し、エンターキーを押す：

```bash
conda activate napari-env
```

環境名を異なる名前にした場合や、作成した仮想環境の一覧を確認したい場合は、次のコマンドを入力して<kbd>Enter</kbd>キーを押す：

```bash
conda env list
```
現在の環境には`*`が表示される。

他にも多くのcondaコマンドがあり、仮想環境の情報表示や削除などに使用できる。詳細は、こちら(https://docs.conda.io/projects/conda/en/4.6.0/user-guide/tasks/manage-environments.html)のウェブサイトを参照してほしい。

# Napariを起動する

このセクションでは、Napariの基本的な使い方を紹介する。

## 方法１ - コマンドラインから起動する

Napariを起動する方法はいくつかある。一つ目の方法は、コマンドライン(Anaconda Prompt)で`napari`と入力してエンターキーを押すことである。次のコマンドを入力してエンターキーを押す：

```bash
napari
```
これにより、図3のようにNapariビューアが開く。画像を読み込むには、トップバーのFileメニューをクリックし、Open File(s)を選択する。画像を選択し、Openをクリックすると、画像が表示される。また、別の方法として、画像を直接ドラッグアンドドロップすることも可能である。ビューアの各部分の機能については、次のセクションで説明する。

![図3](figures\3_napari_gui.png)

*図3:Napari スタート画面*


## 方法２ - JupyterノートブックからPythonスクリプトで起動する

NapariはPythonスクリプトからも起動できる。PythonのIDE（統合開発環境）であるJupyterノートブックを使用して、Napariを起動する方法について説明する。Jupyterでは、コードとその結果を同じ場所に表示できるため、データの可視化に適している。

また、コードとドキュメンテーションの両方を含むノートブックを作成することができるため、コードの再利用性が高まり、他の人との共有や科学文献のコードシェアリングにも便利である。実際、この章自体もJupyterノートブックで執筆されており、その後この本の形式にエクスポートされた。

このセクションでは、まずJupyterノートブックの基本的な使い方を紹介する。このツールは後の章でも使用するため、役立つであろう。最後に、Napariから画像を呼び出す方法の例を示す。

### Jupyterノートブックを起動する

ここでは、Jupyter Lab内でJupyter ノートブックを開く※1。

Jupyter Labを起動するには、次のコマンドを実行する：

```bash
jupyter lab
```
図４のようなページが表示される。

![図4](figures\4_jupyter_notebook.png)

*図4: Jupyter Lab スタートアップページ*

次に、この章で作成するスクリプトと、使うサンプル画像を保存するフォルダを作成する。まず、図4Aをクリックして新しいフォルダを作成し、フォルダ名を `napari-tutorial` とする。フォルダをクリックして開く。次に、図4Bをクリックして新しいJupyterノートブックを作成する。作成された新しい `.ipynb`ファイルを右クリックして、名前を`getting_started.ipynb`に変更する。これで、Jupyter Labのウィンドウは図5のようになる。

![図5](figures\5_jupyter_editor.png)

*図5: Jupyter エディター*

図５Aをクリックして左のパネルを閉じ、コーディングを始める。

> ※1
>
> この章ではJupyter Labを通じてJupyter ノートブックを走らせているが、この他でもいくつかのインターフェースがある。その中で、一番お勧めするのがVisual Studio Code(https://code.visualstudio.com/)だ。無償ソフトウェアで、Python以外にも他の言語をサポートしているところが魅力的だ。また、Visual Studio Code自身にもプラグインエコシステムが存在しており、html/cssで作ったウェブページの可視化や、ChatGPTでサポートされているGithub Copilot(https://github.com/features/copilot, 有償だが、学生ならばGithubで在学登録すれば無料で使える)搭載できるため、コーダーの間で愛用されている。


### JupyterでのHello World

前の章でいくつかの簡単なPythonプログラミングの構文について学んだ。ここでは、それをJupyterで試してみる。
図５Bに次のコードを入力する：

コードセル01
```python
print("Hello World!")
```
そして、図5Cをクリックするか、ショートカット <kbd>Shift</kbd> + <kbd>Enter</kbd> を押すと、コードが実行され、期待通り `Hello World!` が表示される。

Jupyterノートブックでは、コードはブロックに分割されており、それぞれのブロックを「セル」と呼ぶ。さらにコードの「セル」を追加するには、現在のセルを選択して上部バーの + 記号 (図５D) をクリックするか、ショートカットキー <kbd>b</kbd> を押す。もし <kbd>a</kbd> を押すと、新しいセルが現在のセルの上に作成される。


### コードを走らせた順序による問題の解消

Jupyterノートブックではコードセルを自由な順序で実行できるため、これが原因で問題が発生する可能性がある。ここでは、そのエラーについて説明する。
デモとして、現在のコードセルの下に三つの新しいコードセルを作成し、以下のコードを入力しよう。

コードセル02
```python
i = 1
```
コードセル03
```python
i = i + 1
```
コードセル04
```python
print(i)
```
続いて、コードセル02 -> 03 -> 04を実行させると`2`が出るに違いない。でも、もしコードセル03を何回も実行(<kbd>Ctrl</kbd> + <kbd>Enter</kbd>で一つのセルにとどもって実行できる)して、コードセル04を実行したら、別の答えが出てくる。このようなメカニズムで、ある時、期待外れの結果やエラーが出てくるかもしれない。もしこのような場合がありましたら、Jupyterのカーネル(Kernel)をリスタートして、全ての変数をリセットしよう。Jupyterカーネルとは、コードを実行しその結果を返すバックエンドのエンジンである。Jupyter ノートブックのトップバーの[Kernel >Restart Kernel]か、図5Eをクリックすれば、カーネルをリセットできる。

### Jupyterでのドキュメンテーション作成

前述のように、Jupyterノートブックの利点の一つは、ドキュメントとコードを一つのファイルにまとめることができる点である。先ほどは、Pythonのコードを入力するためのコードセルの作成方法を紹介した。ここでは、Jupyterで「マークダウン（Markdown）」セルを作成する方法を説明する。
	
Markdownは、テキストを簡単にフォーマット作成できる軽量マークアップ言語である。Markdownを使うことで、見出し、リスト、リンク、画像、表などを簡単な構文で追加できる。ドキュメント、ウェブページ、Jupyterノートブックなどで広く使われている。
	
マークダウンセルを作成するには、はじめに一つのセルを選択それか作成し、上部バーのドロップダウンメニュー(図5E)をクリックし、「Markdown」を選択するか、ショートカット<kbd>m</kbd> (**m**arkdown) を押してそのセルをマークダウンに変更する（コードセルに戻すには <kbd>y</kbd> (p**y**thon) を押す）。

ノートブックにタイトルをつけてみよう。新しいセルを今のセルの上に作り(ショートカット<kbd>a</kbd>)、マークダウンセルに変え、次の内容を入力する：

```markdown
# JupyterでNapariを起動する
Jupyterノートブックから*Napari*を起動する方法を説明する。
## Hello World
次のセルでは **「Hello World!」** を表示する。
```

実行ボタンをクリックするか、<kbd>Ctrl</kbd> + <kbd>Enter</kbd>を押す。図６のように表示される。

![図6](figures\6_markdown_edit.png)

*図6: Jupyter でのマークダウン編集*

ご覧の通り、テキストはタイトル（`#`）、サブタイトル（`##`）としてフォーマットされている。さらに、`*` でテキストを囲むことで斜体、`**` で囲むことで太字にすることができる。これ以外にも、`###` を使用してサブサブタイトルを作成することができる。また、`*` を使って箇条書きリストを、`1.` を使って番号付きリストを、`---` を使って水平線を作成することができる。ついでに、図6Aをクリックすると、このノートブックの目次が現れる。Markdownの構文について詳しくは、このチートシート(https://www.markdownguide.org/cheat-sheet/)を参照してください。この章をフォローする共に、各セクションのコードの前にマークダウンで少なくともサブタイトルを入れるようにお勧めする。※2

ここまで、いくつかのJupyterノートブックでのショートカットを学んできた。表１によく使うJupyterショートカットを整理した。さらにショートカットを知りたい場合は、上部バーの[Help　> Show Keyboard Shortcuts]を参照すること。すべてのショートカットを覚える必要はないが、その存在を知っておくと便利である。Jupyterノートブックを頻繁に使うようになると、自然に身についてくるだろう。

> ※2
>
> この章で使われるコードは皆、ここ(https://github.com/miura/Yodosha-BIASBook2024/tree/main/huang/code)にアップロードされている。ただコードを走らせて結果を見ることも良いが、ここではコードを一行一行理解しながら入力したほうが、知識の習得に助かるだろう

| ショートカット        | 意味                                     |
|-----------------------|------------------------------------------|
| <kbd>a</kbd>          | セルを上に挿入する                       |
| <kbd>b</kbd>          | セルを下に挿入する                       |
| ダブル<kbd>d</kbd>   | 選択したセルを削除する                   |
| <kbd>Shift</kbd> + <kbd>Enter</kbd> | セルを実行して次のセルに移動する         |
| <kbd>Ctrl</kbd> + <kbd>Enter</kbd>  | セルを実行する                           |
| <kbd>y</kbd>          | セルをコードセルに変える（python）       |
| <kbd>m</kbd>          | セルをマークダウンセルに変える（markdown）|

表１:よく使うJupyterショートカット

---

演習　Hello Worldのセルの下に新しいマークダウンセルを作成し、セルに「Napariでの画像表示」というサブタイトルを書いてみよう。

---

### JupyterでNapariを起動する

次に、JupyterノートブックからNapariを起動する。まず、skimage.data モジュールからサンプル画像を読み込む。新しいセルを作成し、次のコードを入力する:

コードセル05
```python
# skimageから3D画像を読み込む
from skimage.data import cells3d

# 画像のサイズを取得
shape = cells3d().shape
print(f'画像のサイズ: {shape}')
```
次の出力が表示される：

`画像のサイズ: (60, 2, 256, 256)`

この出力から、画像が4次元の配列であることがわかる。最初の次元（dim 0）は60で、これはスタック内に60枚の画像があることを意味する。第2の次元は2で、各画像に2つのチャンネルがあることを示している。第3および第4の次元は256で、各画像のサイズが256x256ピクセルであることを示している。

このままNapariで画像を表示することもできるが、画像を個々のチャンネルに分けて別々に表示する方が便利である。次のセルコードを入力する:

コードセル06
```python
# 画像を個々のチャンネルに分離
cell3d_ch0 = cells3d()[:, 0, :, :]
cell3d_ch1 = cells3d()[:, 1, :, :]

# 画像のサイズを取得
shape = cell3d_ch0.shape
print(f'画像のサイズ: {shape}')
```

次に、Napariを起動し、二つのチャンネルに分けた画像をNapariに追加してみる。次のセルに下のコードを入力してみよう。

コードセル07
```python
# napariをインポート
import napari

# napariのビューアを作成
viewer = napari.Viewer()

# 画像を追加
channel_0_img = viewer.add_image(cell3d_ch0, colormap='magenta', name='channel 0')
channel_1_img= viewer.add_image(cell3d_ch1, colormap='green', name='channel 1')
```

Napariのビューアが表示される。`channel 0` と `channel 1` レイヤーの透明度（Opacity）、コントラスト（Contrast Limit）、およびガンマ（Gamma）を調整してみて、図７のような画像が見えるように確認してみよう。また、画像の拡大・縮小にはマウスのホイールを使用してみると良い。

![図7](figures\7_napari_viewer_with_labels.png)

*図7：Napariビューアと、各パーツの名前。英語の名前はNapari正式ドキュメンテーションに載っているものと同じとなる。この章では、ここで定義した名前を使って説明していく*

上の図では、ビューアの各エリアに対応する名前がラベル付けされている。先ほどの調整で、Napariビューアのキャンバス（Canvas）、レイヤーリスト（Layer List）、レイヤーコントロール（Layer Control）の機能を探索した。ウィンドウの各部分に関する詳細は、こちら(https://napari.org/stable/tutorials/fundamentals/viewer.html#layout-of-the-viewer)で確認できる。

コードセル07をもう一度確認してほしい。Napariのビューアがオブジェクト指向プログラミングの概念を利用していることに注意する必要がある（前の章を参照）。そのため、画像や画像関連のデータはレイヤー(Layer)として作成されたビューアオブジェクトに追加されている。ここでは、viewer.add_image() メソッドを使って画像レイヤーを追加した。次のセクションでは、他のレイヤーの追加方法についても説明する。

顕微鏡の設計と光学的のリミットにより、3D画像のほとんどは異方性(anisotropic)であり、x、y、zの各軸のピクセルサイズが異なることが多い。この画像もその一例だ。skimage.data.cell3dのドキュメンテーション(https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.cells3d)を確認すると、z、y、x軸のピクセルサイズ（それぞれ0.29、0.26、0.26 µm）がわかる。これらのサイズを視覚化するため、z、y、x軸のスケーリングを下のコードで行う。

コードセル08
```python
viewer.layers['channel 0'].scale = [0.29, 0.26, 0.26]
viewer.layers['channel 1'].scale = [0.29, 0.26, 0.26]
```

---

演習: 図7の各部分のスライダーやボタンをそれぞれクリックして、その機能を試してみよう。画像を三次元モードで表示し、下の図のように画像を回転させてみよう。

ヒント: 軸を表示するには、[View > Axis > Axis Visible] を選択する。

![図8](figures\8_cells3d_rotated.png)

*図8: Napariビューアでの立体画像可視化*

---

作業が完了したら、以下のコマンドを実行してNapariビューアを閉じる。

コードセル09
```python
# Napariビューアを閉じる
viewer.close()
```

## ついでに: matplotlib での画像表示

次のセクションに進む前に、matplotlibを使った画像の表示方法をカバーしたい。matplotlibはPythonの作図用パッケージで、データの可視化に広く使用されている。プロット、ヒストグラム、パワースペクトル、棒グラフ、エラーチャート、散布図などを作成することができる。Napariが開発される前は、matplotlibが画像の可視化に最も人気のあるライブラリの一つであり、現在でも他のアプリケーションで広く使用されている。ここでは、matplotlibを使って画像を表示する方法を紹介する。

前のセルの下に新しいセルを作成し、次のコードを入力しよう。

コードセル10
```python
# skimageからcell画像を読み込む
from skimage.data import cell

# matplotlib.pyplotをpltとしてインポート
from matplotlib import pyplot as plt

# cell画像を表示
plt.imshow(cell())

# 画像のタイトルを設定
plt.title('cell')
```
図9のような画像が現れる。

![図9](figures\9_matplotlib.png)

*図9: matplotlibでの画像可視化*

以前使用した二つのチャンネルの画像(cells3d)を、matplotlib.pyplot.imshow を使って表示してみよう。matplotlib.pyplot.imshowでは2Dの画像しか表示できないため、ここではnumpy.maxで最大値投影（max intensity projection)を通じて3D画像を2Dに圧縮する。次のコードを入力してみよう:

```python
import numpy as np

cell2d_ch0 = np.max(cell3d_ch0, axis=0)
cell2d_ch1 = np.max(cell3d_ch1, axis=0)

# 画像の表示
plt.subplot(1, 2, 1)
plt.imshow(cell2d_ch0)
plt.title('Channel 0')
plt.subplot(1, 2, 2)
plt.imshow(cell2d_ch1)
plt.title('Channel 1')
```

図１０のような画像が現れる。

![図9](figures\10_matplotlib_cells3d.png)

*図10: cells3dをmatplotlibでの可視化*

Napariが登場する前は、Matplotlibが画像可視化の最も人気のあるライブラリであった。しかし、Matplotlibでは3D可視化のために作られてなかった事と、また、複数の画像を重ねて表示することも難しい。この点が、Napariの画像可視化における優位性を際立たせている。だが、2D画像の可視化や作図などではMatplotlibは今でも主流ですので言及しておきたい。

次のセクションでは、Napariのもう一つの大きな利点として、Napariビューアにさまざまなタイプのデータ‐レイヤーを追加する方法について学ぶ。

# Napari Layer(レイヤー)の紹介

次に、Napariビューアのレイヤー機能を探っていく。先述の通り、Napariビューアはオブジェクト指向ビューアであり、データはレイヤーとしてビューアに追加される。前のセクションでは、`viewer.add_image()`メソッドを使用して画像レイヤーをビューアに追加した。このセクションでは、ラベル、ポイント、トラック、シェイプなど、他のさまざまなタイプのレイヤーをビューアに追加する方法について詳しく見ていく。

## Labels Layer(ラベルレイヤー)
### NapariにLabels Layerを追加する

ラベルは画像に含まれたピクセルを注記するために使用される。ラベルは整数配列として表現され、各整数が画像の異なる領域を表す。例えば、あるグループのピクセルがみんな同じ細胞核を表していたら、そのピクセルたちは同じ数字にラベリングされる。画像をラベルする過程をセグメンテーション(Segmentation)と呼ぶ。Napariでは、ラベルは`viewer.add_labels()`メソッドを使ってレイヤーとしてビューアに追加される。次の例では、前のセクションの画像を閾値処理(Thresholding)でセグメンテーションして、得られたラベルをビューアに追加する。ワークフローは図１１のようになる。セグメンテーションワークフローのデザインについては、後の章(実践編 型１)で深く説明される。

では、コーディングをはじめよう。次のセルに、下のコードを入力しよう。

![図11](figures\11_segmentation_workflow.png)

*図11:セグメンテーションワークフロー*

コードセル12
```python
# 必要なライブラリをインポート
import napari
from skimage.filters import gaussian, threshold_otsu

# napariのビューアを作成
viewer = napari.Viewer()

# 2D画像を追加
viewer.add_image(cell2d_ch0, colormap='magenta', name='channel 0')
viewer.add_image(cell2d_ch1, colormap='green', name='channel 1')

# cell2d_ch1に対してガウスぼかしを適用
cell2d_ch1_blurred = gaussian(cell2d_ch1, sigma=1)
viewer.add_image(cell2d_ch1_blurred, colormap='green', name='channel 1 blurred')

# 大津の閾値処理を適用
thresh = threshold_otsu(cell2d_ch1_blurred)
cell2d_ch1_thresholded = cell2d_ch1_blurred > thresh
viewer.add_image(cell2d_ch1_thresholded, colormap='viridis', name='channel 1 thresholded')
```

---

演習: 図12のように`cell2d_ch1_thresholded` には、多くの細胞中の穴やデブリがセグメントされている。この画像を使って、次のセルにモルフォロジー操作(Morphological Operation)（ここでは、穴埋めと開操作）を適用して細胞の形を整え、その後、ラベルを作成して `viewer.add_labels()` でNapariビューアに追加するコードを書いてみよう。答えは下にありますが、考えて試してみてほしい。

ヒント: 図11で示したように、`skimage.morphology`モジュールの `binary_fill_holes()` と `binary_opening()` メソッドを使用する。ラベリングは、`skimage.measure`モジュールの `label()` メソッドを使用すること。

![図12](figures\12_thresholding_result.png)

*図12: 二値化の結果。多くの細胞中の穴やデブリがセグメントされている。*

---

コードセル13
```python
# 必要なライブラリをインポート
from scipy.ndimage import binary_fill_holes
from skimage.morphology import opening, disk
from skimage.measure import label

# cell2d_ch1_thresholdedに穴埋め操作を適用
cell2d_ch1_filled = binary_fill_holes(cell2d_ch1_thresholded)
viewer.add_image(cell2d_ch1_filled, colormap='viridis', name='channel 1 filled')

# 開操作を適用
cell2d_ch1_opened = opening(cell2d_ch1_filled, disk(5))
viewer.add_image(cell2d_ch1_opened, colormap='viridis', name='channel 1 opened')

# 連結成分解析を適用
cell2d_ch1_labeled = label(cell2d_ch1_opened)
label_layer = viewer.add_labels(cell2d_ch1_labeled, name='channel 1 labeled')
```

図１３のような画像が表示される。ラベルは異なる色で表示され、異なる領域を区別している。ラベルの透明度とコントラストを調整して、画像を見てみよう。Napariでは、レイヤーのプロパティによって、異なるコントロールツールが表示される。ラベルの場合、Eraser、Fillなどのツールが表示される。これらのツールを使って、ラベルを編集することができる。

![図13](figures\13_labelling_result.png)

*図13: ラベリングの結果。*

---
演習: ラベルを注意深く見ると、一部のラベルが正しくないことに気づくかもしれない。レイヤーコントロールツールを使って、各細胞が異なるラベル（色）を持つようにラベルを編集してみよう(ヒント1)。また、以下(図１4)に示すようにラベルのボーダーを表示する方法を探してみてほしい(ヒント2)。最後に、各処理ごとの結果をタイルで示してみよう(ヒント3)。

*ヒント 1: こちらのサイト（https://napari.org/stable/howtos/layers/labels.html#editing-using-the-tools-in-the-gui) を参照すると良いでしょう。
** ヒント 2: contour の数値を変更してみてください。
***　ヒント3：ビューアボタンのそれぞれを試してみてください。

![図14](figures\14_labelling_result2.png)

*図14:ラベリングの順序をパネルで表す*

---

### ラベルを保存する

手動でラベルを編集した後、後での分析のためにラベルを保存したい場合、次のコードを実行して、Napariビューアからノートブックにラベル変数を取り戻すことができる。

コードセル14
```python
from skimage.measure import label
from skimage.io import imsave
import matplotlib.pyplot as plt
import numpy as np

# ラベルレイヤーからラベルデータを取得
labeled_image = label_layer.data

# Napariビューアを閉じる
viewer.close()

# 再ラベリング前のユニークなラベルを表示
unique_labels = np.unique(labeled_image)
print(f'再ラベリング前のユニークなラベル: {unique_labels}')

# 画像を再ラベリング
cell2d_ch1_relabel = label(labeled_image)

# 再ラベリング後のユニークなラベルを表示
unique_labels = np.unique(cell2d_ch1_relabel)
print(f'再ラベリング後のユニークなラベル: {unique_labels}')

# 再ラベリングされた画像を表示
plt.imshow(cell2d_ch1_relabel)
plt.colorbar()
plt.title('Channel 1 Relabeled')
plt.show()

# 再ラベリングされた画像を保存
imsave('cell2d_ch1_relabel.tif', cell2d_ch1_relabel)
```
![図15](figures\15_relabelling_result.png)

*図15:再ラベリングの結果*


図15と “再ラベリング前と後のユニークなラベル”がアウトプットとしてでてくるだろう。前のコードセルでは、`label_layer = viewer.add_labels(...` を使ってラベルを表示しましたので、ここでは `label_layer.data` を使ってラベルをビューアオブジェクトから取得した。手動でラベリングを行う過程でラベルを削除したり、新しいIDでラベルを追加したため、「リラベリング前のユニークなラベル」の番号が連続していないことがわかる。理想的には、ラベル番号が 1, 2, 3 ... n で、nがラベルの数(ここでは細胞核の数)となるべきだ。これを実現するために、`skimage.measure` の `label` 関数を使用してラベル番号を再割り当てした。最後に、`plt.imshow` でラベル画像を表示し、`skimage.io.imsave` で画像を保存した。保存時に `UserWarning: cell2d_ch1_relabel.tif is a low contrast image` という警告が表示されることがあるが、これはラベル画像のグレースケールが通常の画像に比べて非常に少ないためである。警告を無視したい場合は、関数に `check_contrast=False` を追加して無効にすることができる。

### Regionpropsの紹介

次に進む前に、`skimage.measure.regionprops_table`（または単に `regionprops`）について触れておきたい。この関数は、ラベルによって画像のプロパティを測定するのに役立つ。以下に画像特徴抽出の例コードを示す。`regionprops` と `regionprops_table` の詳細や測定可能な項目については、ドキュメンテーション(https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.regionprops)を確認してほしい。

`regionprops` 以外に、ここではもう一つのライブラリである `pandas` も使用した。Pandas はテーブルデータの処理に広く使用されるライブラリであり、データサイエンティストにとって学ぶべき最も重要なライブラリの一つである。Pandas は、コードの出力で示されるように、テーブルデータの可視化や、テーブル内のデータを簡単かつ迅速に修正するのにも役立つ。詳細については、Pandas (https://pandas.pydata.org/)のドキュメンテーションやネット上のチュートリアルを確認することをお勧めする。

コードセル15
```python
import pandas as pd
from skimage.measure import regionprops_table

# 抽出するプロパティを定義
properties = ['label', 'area', 'centroid', 'max_intensity', 'mean_intensity', 'min_intensity']

# プロパティを抽出し、DataFrameに変換
props_df = pd.DataFrame(regionprops_table(cell2d_ch1_relabel, cell2d_ch1, properties=properties))

# DataFrameの最初の数行を表示
props_df.head()
```

![図16](figures\16_pandas_df_head.png)

*図16:Pandas dataframeの最初の数行の表示*

図16のようにPandasのdf.head()によって測定の結果がテーブルフォーマットでJupyter ノートブックで示してくれる。
Regionprops の測定結果で、図1７のような簡単なグラフを作れる:

コードセル16
```Python
# 面積のヒストグラムを作成する
plt.hist(props_df['area'])
plt.xlabel('Area [pixels]')
plt.ylabel('Cell count')
plt.title('Cell Area Distribution')
```

![図17](figures\17_area_histogram.png)

*図17:細胞の面積分布*

このセクションでは、手動きでラベリングしながらNapariのlabels Layerを試したが、今ではたくさんの機械学習に基づいたセグメンテーション方法が存在している。例えば、Cellpose（https://cellpose.readthedocs.io/en/latest/）とStarDist(https://github.com/stardist/stardist)。これらのソフトウェア・アルゴリズムは後の章で詳しく説明される。


## Points Layer (点群レイヤー)

このセクションでは、粒子トラッキングの例を通じて、Napariのポイントレイヤーについて学ぶ。粒子の重心を検出し、これらの点をNapariで画像上に表示し、点を編集する方法を学ぶ。
	
このセクションおよび次のセクションで使用する画像は、実践編・型２の章でトラッキング学習に使用するものである。ここでは、オブジェクトを手動でトラッキングする。その後、実践編・型２でトラッキングの原理と自動トラッキングソフトウェアの使用方法について詳しく学ぶ。
	
まず、このリンク(https://github.com/miura/Yodosha-BIASBook2024/tree/main/huang/code/sample_images)からサンプル画像(`particle_tracking_sample.tif`)をダウンロードし、Jupyterノートブックと同じフォルダの中に`sample_images`フォルダーを作って、そこに配置する。画像を直接Jupyterの左半分(図５)のファイルエクスプローラーにドラッグアンドドロップもできる。

次に、以下のコードを実行して、Napariで画像を開く。

コードセル17
```Python
from skimage.io import imread
import napari

# 画像の読み込み
sample_image = imread('sample_images/particle_tracking_sample.tif')

# 画像の形状を表示
print(f'sample_image の画像サイズ: {sample_image.shape}')

# 画像をnapariで表示
viewer = napari.Viewer()
viewer.add_image(sample_image, name='sample_image')

# タイムラプス視覚化のため、時間の次元をスケーリング
viewer.layers['sample_image'].scale = [15, 1, 1]
```
### 点の重心を探す

次に、粒子の重心を検出する。

---

演習：粒子の重心を検出するプログラムを書いてみよう。図18の例のワークフローを参考にしてほしい。参考の答えはコードセル17にある。

ヒント：このタスクには、前のセクションで示した大津の閾値処理方法と regionprops_table を使用できる。

![図18](figures\18_centroid_detection_workflow.png)

*図18：粒子重心を検出するワークフロー*

---

コードセル17
```python
import numpy as np
import pandas as pd
from skimage.filters import gaussian, threshold_otsu
from skimage.measure import label, regionprops_table

# 閾値処理されたラベル画像を格納するリスト
labeled_images = []

max_label_last_time_point = 0

# 各時間ポイントで閾値処理とラベリングを適用
for time_point in range(sample_image.shape[0]):
    # ガウスフィルターで画像をスムージング
    smoothed_image = gaussian(sample_image[time_point], sigma=1)
    
    # 大津の閾値処理を適用
    thresholded_image = smoothed_image > threshold_otsu(smoothed_image)
    
    # 連結成分解析（ラベリング）を実行
    labeled_image = label(thresholded_image)
    
    # 時間ポイント間でラベルが一意になるよう調整
    labeled_image_unique = labeled_image + max_label_last_time_point
    labeled_image_unique[labeled_image == 0] = 0
    labeled_images.append(labeled_image_unique)
    
    # 最大ラベルを更新
    max_label_last_time_point = np.max(labeled_image_unique)

# リストをNumPy配列に変換
labeled_images = np.array(labeled_images)

# Napariでラベル付けされた画像を表示
viewer.add_labels(labeled_images, name='labeled_images')
viewer.layers['labeled_images'].scale = [15, 1, 1]

# ラベル付けされた領域の重心を取得
properties = ['label', 'centroid']
props_df = pd.DataFrame(regionprops_table(labeled_images, properties=properties))

# データフレームの最初の数行を表示
props_df.head()
```

![図19](figures\19_centroid_dataframe.png)

*図19：粒子重心を表示するpandas テーブル*

図19のようなpandasテーブルが表示される。

### NapariにPoints Layerを追加する
すべてのROIの重心が取得できたので、次のステップでは、Napariが受け入れる形式に変換します。

Napariが受け入れる形式は次の通りです(https://napari.org/stable/howtos/layers/points.html を参考)：
`points = np.array([[100, 100], [200, 200], [300, 100]])`
見た通り、points変数のサイズ(dimension)はNxD, Nはポイントの数、Dは次元数となる。
それでは、先ほど取得したDataframeをこの形式に変換します

コードセル18
```python
# データフレームを次の形式に再整形します：
# points = np.array([[0, 100, 100], [1, 200, 200], [2, 300, 100]])
centroid_0 = np.array(props_df['centroid-0'].to_list())
centroid_1 = np.array(props_df['centroid-1'].to_list())
centroid_2 = np.array(props_df['centroid-2'].to_list())

# セントロイド座標を結合
points = np.column_stack((centroid_0, centroid_1, centroid_2))
points
```
これで、NapariにPoint Layerとしてインポートする準備が整いた:

コードセル19
```python
# ポイントをNapariビューアにポイントレイヤーとして追加する
points_layer = viewer.add_points(points, size=10, name='centroids')

# ポイントレイヤーのスケールをイメージレイヤーと同じように調整する
viewer.layers['centroids'].scale = [15, 1, 1]
```

図20のような表示が確認できるはずです。ポイントがラベルに隠され見えるかもしれない。

![図20](figures\20_points_layer_display.png)

*図20: ポイントレイヤーの表示*

---

演習: よく見れば、ROIが二つ重なってしまった場合がある。各粒子に対応するようにポイントを修正せよ。修正後、ポイントレイヤーのコントロールパネルで、ポイントの色を個々の粒子に対応させる（フレーム6以降に分裂したもの）。最終的には、図21のようになる。

![図21](figures\21_points_layer_correction.png)

*図21: ポイントレイヤー修正後の結果*

---

以下のスクリプトは、ポイントの色を抽出し、それをIDに変換する。

コードセル20
```python
# ポイントとフェイスカラーを取得する
new_points = points_layer.data
points_face_color = points_layer.face_color

# ポイントフェイスカラー配列内のユニークな行を識別する
unique_colors = np.unique(points_face_color, axis=0)

# ポイントフェイスカラーをcolor_idに変更する
color_id = np.zeros(len(points_face_color), dtype=int)
for i, color in enumerate(unique_colors):
    color_id[(points_face_color == color).all(axis=1)] = i

# DataFrameにcolor_idを追加する
new_points_df = pd.DataFrame(new_points)
new_points_df['color_id'] = color_id

# Dim-0, 1, 2をt,y,xに名前を変える
new_points_df.columns = ['t', 'y', 'x', 'color_id']

# データフレームの最初の数行を表示する
new_points_df.head()
```

![図22](figures\22_new_com_dataframe.png)

*図22:新しく整理した粒子重心のdataframe*

図22のようなPandas テーブルが出てくる。選んだカラーによって、color_idが違うオーダーになっているかもしれませんが。

NapariのPoints Layerの解説はこれで終了である。Points Layerでは、ポイントに「特徴」を追加するなど、他にもいくつかの操作が可能である（色を追加する方法に非常に似ている）。詳細については、Napariのドキュメントの点群レイヤーに関する部分を確認することを推奨する。
	
Napariのビューアはまだ閉じないでほしい。次のセクションでは、点群レイヤーを接続し、「トラック」レイヤーを導入する。



## Tracks Layer (トラックレイヤー)
### Tracks変数の作成

以下では、先ほど作成した点を接続し、それをトラック(Tracks)に変換する。Napariでは、Tracks Layerへの入力データは、トラックIDとN個の点をD次元座標で含むNxD+1のNumPy配列またはリストでなければならない。Tracksデータ管理の詳細は後の章で説明するが、現時点では、2D + 時間のトラックの場合、データは次のように配置する必要があることを覚えておいてほしい。

```bash
   track_id    t    y    x
0         1  ...  ...  ...
1         1  ...  ...  ...
2         2  ...  ...  ...
```
3D + 時間のトラックの場合、データは次のように配置する。
```bash
   track_id    t    y    x    z
0         1  ...  ...  ...  ...
1         1  ...  ...  ...  ...
2         2  ...  ...  ...  ...
```
それでは、データを再編成してトラック形式に変換する。

コードセル21
```python
# Track Dataframeを編成: new_points_dfのcolor_id列を最初の列に移動し、列名を'track_id'に変更
tracks_df = new_points_df[['color_id', 't', 'y', 'x']]
tracks_df.columns = ['track_id', 't', 'y', 'x']
tracks_df.head()
```

![図23](figures\23_track_dataframe.png)

*図23:再編成して作られたトラックdataframe*

### NapariにTracks Layerを追加する

Track 変数が準備できたら、`viewer.add_tracks`でNapariビューアに入れる

コードセル22
```python
# Track　Layerを追加
tracks = viewer.add_tracks(tracks_df, name='tracks')
# Track LayerのスケールをImage Layerと同じように調整する
viewer.layers['tracks'].scale = [15, 1, 1]
```
図24のように、tracksがNapariビューアに現れる。Tracks Layer コントロールパネルの各スライダーとボタン、ドロップダウンリストの機能を試してみよう。フレーム再生ボタン(図７を参考)も試してみるがよい。

![図24](figures\24_tracks_layer_display.png)

*図24:Tracks Layer の表示*


### Tracksの合流、分岐を管理する

Tracksの分岐点(フレーム６)が接続されていないことに気づくだろう。これは、Trackデータの分岐前後でそれぞれを別々のトラックとして扱っているためである。

Tracksのgraph引数を使用して、tracks間の関係（例えば、合流や分岐）を定義することができる。graphはPython Dictionaryとして定義され、キーがtrack_id、値がそのtrackの"親"のtrack_idとなる。例えば、我々のケースでは、track3がtrack0、1、2に分岐する（track3がtrack0、1、2の”親”である）。詳細はtrack章で学ぶが、ここでは次のようにgraphを定義し、`viewer.add_tracks`のインプットとして扱う。

コードセル23
```python
graph = {
    0: [3],
    1: [3],
    2: [3],
}
# グラフをNapari　add_tracksに追加
connected_tracks = viewer.add_tracks(tracks_df, graph=graph, name='connected_tracks')
viewer.layers['connected_tracks'].scale = [15, 1, 1]
```

これでトラックが接続される。トラックを時間軸を3次元目の空間として可視化することもできる (図25)。

![図25](figures\25_tracks_connect.png)

*図25:Tracksを3Dでの表示。分岐している所が連結されていることをハイライトしている。*

コードセル24
```python
# Napariビューアを閉じる
viewer.close()

# トラックデータフレームを保存する
tracks_df.to_csv('tracks.csv', index=False)
```
これで、NapariのTracks Layerのウォークスルーは終了である。このセクションと前のセクションで、粒子追跡の例を通じてNapariのPoints LayerとTracks Layerについて学んだ。ご覧のとおり、手動でのトラッキングは非常に面倒である。2024年8月時点で、Napariコミュニティでは、手動でのトラックの注釈(Manual Track Annotation)を現状よりも容易にする方法を模索し始めており、今後の開発のアップデートに期待が持てる。また、多くの自動トラッキング方法が最近開発されており、後の章で紹介される。このセクションを通じて、その章を楽しみにしてほしい。次に、もう一つよく使われるNapariレイヤーであるShape Layerを紹介する。

## Shape Layer (形レイヤー)

この章で最後に紹介するレイヤーとして、Shapes Layer（形レイヤー）について説明する。その名の通り、このレイヤータイプを使って形状を作成することができる。以下のコードを使用して形状を作成できる(図２6)。

コードセル25
```python
import napari
import numpy as np

# 三角形と長方形の頂点座標を定義
triangle = np.array([[10, 200], [50, 50], [200, 80]])
rectangle = np.array([[40, 40], [40, 80], [80, 80], [80, 40]])

# 三角形と長方形をnapariビューアにShapes Layerとして追加

viewer = napari.Viewer()

# 三角形を追加
triangle_layer = viewer.add_shapes([triangle], shape_type='polygon', edge_color='red', face_color='blue', name='triangle')
# 長方形を追加
rectangle_layer = viewer.add_shapes([rectangle], shape_type='polygon', edge_color='green', face_color='yellow', name='rectangle')
```

![図26](figures\26_shapes_layer_display.png)

*図26: Shapes Layerの表示*

NapariのShapes Layerでは、形を作成するだけでなく、パス (Path) オブジェクトも作成できる。これにより、手動でデータをトレーシング(Tracing)したことに、トレース(Trace)データを表示することが可能になる。例えば、神経の形態分析(例えば、*.swcファイルの可視化)や、後の章、実践編・型3 で説明される血管のトレース可視化にも利用できる。ここでは、実践編・型3で使用する血管画像を手動でトレーシングしてみよう。

https://github.com/miura/Yodosha-BIASBook2024/tree/main/huang/code/sample_images から、画像`blood_vessel_sample.tif`をダウンロードして、前セクションと同じようにノートブックと同じフォルダーの中の`sample_images`フォルダーに画像を移動しよう。

以下のコードを使用してその画像を読み込もう:

コードセル26
```python
# BloodVessels_small.tif を読み込む
from skimage.io import imread
import napari

blood_vessels = imread('sample_images/blood_vessel_sample.tif')

# 画像を表示する
viewer = napari.Viewer()
blood_vessels_image = viewer.add_image(blood_vessels, name='blood_vessels')
```

---

演習: NapariビューアでShapes Layerを作りPath機能で血管をなぞってみよう。

ヒント: レイヤーボタンで新しいShapes Layerを作成できる

---

以下のような結果が得られます:

![図27](figures\27_blood_vessel_tracing.png)

*図27:血管のトレーシングをShapes Layerで表示*


Shapeの名前を'blood_vessel_trace'に変えよう。これは、レイヤーリスト(図７を参考)からレイヤーをダブルクリックして簡単に変えられる。結果をJupyter環境に取り戻すには、次のコマンドを使用します:

コードセル27
```python
# viewer.layers['blood_vessel_trace']からトレースデータを取得
trace_data = viewer.layers['blood_vessel_trace'].data
trace_data_np_array = np.array(trace_data)

# trace_data_np_arrayの形状を確認
print(f'trace_data_np_arrayの形状は: {trace_data_np_array.shape}')

# 次元のサイズが1のため、配列を「squeeze」します
trace_data_np_array_squeezed = np.squeeze(trace_data_np_array)

# trace_data_np_array_squeezedの形状を確認
print(f'trace_data_np_array_squeezedの形状は: {trace_data_np_array_squeezed.shape}')

import pandas as pd

# trace_data_np_array_squeezedからDataFrameを作成
trace_data_df = pd.DataFrame(trace_data_np_array_squeezed, columns=['z', 'y', 'x'])
trace_data_df.head()
# DataFrameをcsvファイルとして保存
trace_data_df.to_csv('trace_data.csv', index=False)
```

試した通り、手動トレースは大変手間のかかる作業である。さらに、同じ人が同じ画像でトレースを行っても、毎回異なる結果になる可能性があり、再現性の問題がある。実践編・型3では、正確かつ自動的にトレースを行う方法について探る。

これまでに、NapariのImage Layer、Labels Layer、Points Layer、Track Layer、Shapes Layerについて紹介した。これらは私の意見では、Napariで最もよく使用されるレイヤーである。さらに、Vectors LayerとSurfaces Layerの2種類もあり、データの視覚化や操作に利用できる。興味がある方は、Napariの公式ウェブサイトで詳細を確認してほしい。


# NapariのPlugins(プラグイン)

NapariもFiji-ImageJのようにプラグインシステムを持っている。このセクションでは、Napariでプラグインをインストールする方法を紹介する。Napariにはプラグインをインストールする方法が二つある。一つは、NapariビューアのGUIにあるNapariプラグインインストーラーを使う方法、もう一つはコマンドラインを使う方法である。ここでは、両方の方法を使って、プレゼンテーションに使う動画を作るのに便利なnapari-animationと、手動3Dトレーシングで便利なnapari-filament-annotatorをインストールする例を紹介する。

## Napariプラグインマネージャーを使ったプラグインのインストール

Napariビューアを開き、[Plugins > Install/Uninstall Plugins]に移動する。インストール可能なプラグインのリストが表示されるので、nnapari-animationプラグインを検索し、インストールボタンをクリックする。

![図28](figures\28_napari_plugin_installer.png)

*図28:NapariのPlugin Installer*

インストールが完了したら、Napariビューアを再起動する。Napariのトップバーの[Plugin]からnapari-animationを探そう。最初のセクションで使用した画像(cells3d)を読み込み、ドキュメンテーションをチェックしながら動画を作ってみよう。Cells3dはNapariのサンプル画像であり、[File > Open Sample > Napari builtins > cells (3D +2Ch)] で開ける。

サンプルで作られた動画は、以下のQRコードで観れる。

![図29](figures\29_make_animation.png)

*図29:Napari-animation pluginのインターフェースとサンプル動画(QRコード)*

## コマンドラインを使ったプラグインのインストール

コマンドラインを使用してプラグインをインストールするには、プラグインのGitHubリポジトリまたはNapari Hub（https://www.napari-hub.org/）を確認する。Napari Hubでは、Napariプラグインを共有・インストールできる。Napari Hubのウェブサイトに移動し、napari-plot-profileを検索する。

![図30](figures\30_napari_hub.png)

*図30:Napari-hubでnapari-plot-profileを捜索*

Napari-plot-profileのページ(https://www.napari-hub.org/plugins/napari-plot-profile)に入り、一番下にInstallation Instructionがある。Pipでのインストールをお勧めしている:
```bash
pip install napari-plot-profile
```
このラインをコピーし、anaconda promptを開けnapari-envに入り(Python環境のセットアップセクションを参考)このコマンドを入力する。インストール後問題なければNapariのトップバーの[Plugin]からnapari-plot-profileが探せるはずだ。もう一回前のサンプル画像を呼び出し、Napari-hub上のドキュメンテーションを見ながら簡単に画像の輝度の測定を行おう。

![図31](figures\31_napari_plot_profile.png)

*図31:napari-plot-profileでの輝度測定*

## その他の便利なNapari Plugins

この他にお勧めしたいNapari Pluginがいくつある。一般的な画像解析の使用に際しては、napari-assistant（https://www.napari-hub.org/plugins/napari-assistant ）をお勧めする。これは、クリック＆トライ方式で画像解析ワークフローを構築するのに役立つ。Fiji-ImageJの方法で画像処理に慣れている場合、非常に便利である。また、`napari-assistant`と併せて`napari-script-editor`（https://www.napari-hub.org/plugins/napari-script-editor ）をインストールすると、ImageJスクリプトレコーダーに相当する機能を実現できる。クリックした操作に対応するPythonコードを生成してくれる。

napari-filament-annotator（https://www.napari-hub.org/plugins/napari-filament-annotator )は、フィラメントデータのラベリングやトレーシングに特化した便利なツールである。また、ディープラーニングベースのセグメンテーションやノイズ除去ツールも複数のNapariプラグインとして利用可能である。例えば、`cellpose-napari`（https://www.napari-hub.org/plugins/cellpose-napari ）や`stardist-napari`(https://www.napari-hub.org/plugins/stardist-napari )、`napari-n2v`（https://www.napari-hub.org/plugins/napari-n2v ）などがある。

これらのプラグインをぜひ自らで試してみてほしい。

もちろん、自分自身のプラグインを開発することも可能であり、そのためのガイドラインがNapariのウェブサイトに掲載されている（https://napari.org/stable/plugins/index.html )。ただし、これはより上級者向けの内容となるため、このチュートリアルではカバーしない。

## エラーが発生した場合

Napariはまだ発展途上であり、バグや問題に遭遇することがあるかもしれない。もし問題が発生した場合は、NapariのドキュメントやGitHubリポジトリを確認してほしい。また、GitHubリポジトリやImage.scで質問することもできる。Napariのコミュニティは非常に活発で助け合いの精神が強いので、必要な場合は遠慮せずに助けを求めてほしい。

# おわりに

この章では，Napariの基本的な使い方について説明した。具体的には，Napariのインストール方法，コマンドラインやJupyterノートブックからの起動方法，Napariビューアに異なる種類のデータレイヤーを追加する方法について取り上げた。また，Napariにプラグインをインストールする方法についても解説した。もしもっと深くNapariとPythonでの画像解析を習いたければ、Robert HaaseさんとDresden PoLのチームが開発したBio-image Analysis Notebooks(https://haesleinhuepf.github.io/BioImageAnalysisNotebooks/intro.html)の参考をお勧めする。

Napariは多次元データの視覚化において強力なツールであり，画像データの探索と解析に使いやすいインターフェースを提供している。この章では，データを手動でラベリングおよびトレーシングする方法に焦点を当てたが，後の章では，自動化されたワークフローを設計し，解析を行う方法について説明する予定である。この章がNapariの良い入門となり，読者が自身のデータを探索し，多次元ビューアでさまざまなデータの側面を検討すること，さらにはNapariコミュニティへの貢献を始めるきっかけとなることを願っている。


