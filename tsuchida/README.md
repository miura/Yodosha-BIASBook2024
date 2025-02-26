Micro-Managerによる顕微鏡制御

本文掲載のPythonスクリプトを収録しています。但し、本文では (繰り返しになるため)
省略したセットアップも各ファイルに追加してあります。

実行するには Python (CPython) の仮想環境 (virtual environment) 内で
以下のコマンドにより pymmcore-plus と napari をインストールしてください。

```sh
python -m pip install "pymmcore-plus[cli]" "napari[all]"

mmcore install
```

各スクリプトは`python`コマンドで直接実行できる形になっていますが、
MDA使用例以外のコードは対話的に使用する例なので、一行ずつ入力して
結果を見ることを想定しています (これには、Jupyterを使用するのも
よいでしょう)。
