# Fijiを最新状態にする方法

20241021 三浦　耕太



Fijiのメニューから[Help > Update]を選ぶと、図1のようなプログレスバーのついた小さなウィンドウが現れ、しばらく現在のFijiのアップデート状況をウェブ上で確認する作業が自動的に始まる。



![image-20241021032746950](figs/scanningUpdates.png)

図1　アップデート状況をスキャンしているウィンドウ



この作業のあとに、図2のような"ImageJ Updater"という名前のウィンドウが表示される。

![image-20241020173940739](figs/ImageJUpdaterWindow.png)

図2 ImageJ Updaterのウィンドウ



これは、自分のFijiにインストールされているさまざまなライブラリやプラグインのアップデート状況を確認した結果であり、"Name"の列がそのライブラリやプラグインの名前、""Status/Action"が更新状況、"Update Site"が、そのライブラリやプラグインが管理されているサーバーの略称である。更新状況が"Update it"になっている行は、そのライブラリないしプラグインにより新しいバージョンがあるので、更新が可能であることを示している。このまま"Apply Changes"というボタンをクリックすれば、更新が始まる。更新が完了すると、"Updated Successfully. Please restart ImageJ!"とその旨が表示されるので"OK"ボタンをクリックし、Fijiを再起動すれば、Fijiそのものとプラグインが最新になった状態でFijiを使うことができる。

もし図2のウィンドウになにも表示されていないなば、すべてが最新状態ということなので、"Cancel"のボタンを押して、更新作業を中止すればよい。

なお、ImageJ Updaterに"Install it"と表示されている行は、新たに追加されるライブラリやプラグインで、これはFiji全体のシステムで新たに必要になったライブラリや、すでにインストールしているプラグインが新たに依存するようになったライブラリであり、これは上の更新作業と同時に新たにインストールされる。