# ★★★★★定型文★★★★★
import os
import sqlite3
from flask import Flask, render_template,request,redirect, session
import flask
# Flaskのインポート

app = Flask(__name__)
# アンダーバー2つ

# sessionを使うには、secret_keyが必要
app.secret_key="sunabaco"
# ★★★★★★★★★★★★★★★

@app.route("/")
def add_gettt():
    return redirect("/list")

# ★★★★★質問追加★★★★★
@app.route("/add")
def add_get():
    return render_template("add.html")

@app.route("/add",methods=["POST"])
def add_post():
    # HTMLから送られてきたデータを取得、変数flaskに格納
    task=request.form.get("tpl_task")
    upload = request.files['upload']
    # uploadで取得したファイル名をlower()で全部小文字にして、ファイルの最後尾の拡張子が'.png', '.jpg', '.jpeg'ではない場合、returnさせる。
    if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        conn=sqlite3.connect("flask.db")
        # DBにテータを追加
        # DBに接続
        conn=sqlite3.connect("flask.db")
        # SQL文を実行
        c=conn.cursor()
        c.execute("insert into task values(null,?,?,?)",(task,0,"no_img.png"))
        # 情報を書き込み
        conn.commit()
        # DBを閉じる
        c.close()
        # ホームページにリダイレクト
        return redirect("/list")
    conn=sqlite3.connect("flask.db")
    # DBにテータを追加
    # DBに接続
    conn=sqlite3.connect("flask.db")
    # SQL文を実行
    c=conn.cursor()
    # 下の def get_save_path()関数を使用して "./static/img/" パスを戻り値として取得する。
    save_path = get_save_path()
    # パスが取得できているか確認
    print(save_path)
    # ファイルネームをfilename変数に代入
    filename = upload.filename
    # 画像ファイルを./static/imgフォルダに保存。 os.path.join()は、パスとファイル名をつないで返してくれます。
    upload.save(os.path.join(save_path,filename))
    # ファイル名が取れることを確認、あとで使うよ
    print(filename)
    c.execute("insert into task values(null,?,?,?)",(task,0,filename))
    # 情報を書き込み
    conn.commit()
    # DBを閉じる
    c.close()
    # ホームページにリダイレクト
    return redirect("/list")

#課題4の答えはここも
def get_save_path():
    path_dir = "./static/img"
    return path_dir


@app.route("/list")
def list():
    # DBに接続
    conn=sqlite3.connect("flask.db")
    # SQL文を実行
    c=conn.cursor()
    c.execute("SELECT * FROM task WHERE flag=0")
    # 配列に格納
    task_list_py=[]
    # 辞書型に追加
    for row in c.fetchall():
        task_list_py.append({"tpl_id":row[0],"tpl_task":row[1],"tpl_flag":row[2],"tpl_img":row[3]})
    # DBを閉じる
    c.close()
    # task_list_pyを出力
    print("ここからテストプリントです")
    print(task_list_py)
    # HTMLに渡す
    return render_template("list.html",tpl_task_list=task_list_py)
    # テスト用記述 breakpoint() そこから先は実行されません
# ★★★★★★★★★★★★★★★


# ★★★★★Q&Aリスト★★★★★
@app.route("/QAlist")
def QAlist():
    # DBに接続
    conn=sqlite3.connect("flask.db")
    # SQL文を実行
    c=conn.cursor()
    c.execute("SELECT * FROM task WHERE NOT flag=0")
    # 配列に格納
    task_list_py=[]
    # 辞書型に追加
    for row in c.fetchall():
        task_list_py.append({"tpl_id":row[0],"tpl_task":row[1],"tpl_flag":row[2],"tpl_img":row[3]})
    print(task_list_py)
    # DBを閉じる
    c.close()
    # HTMLに渡す
    return render_template("Q&Alist.html",tpl_task_list=task_list_py)
# ★★★★★★★★★★★★★★★


# ★★★★★Aリスト★★★★★
@app.route("/alist/<int:id>")
def alist(id):
    # DBに接続
    conn=sqlite3.connect("flask.db")
    # SQL文を実行
    c=conn.cursor()
    c.execute("SELECT * FROM answer WHERE question_id=?",(id,))
    # 配列に格納
    task_list_py=[]
    # 辞書型に追加
    for row in c.fetchall():
        task_list_py.append({"tpl_id":row[0],"tpl_answer":row[1],"tpl_question_id":row[2],"tpl_img":row[3]})
    # DBを閉じる
    c.close()
    # HTMLに渡す
    return render_template("Alist.html",tpl_task_list=task_list_py)
# ★★★★★★★★★★★★★★★


# ★★★★★回答★★★★★
@app.route("/answer/<int:id>")
# idを受け取り
def answer_get(id):
    # DBに接続
    conn=sqlite3.connect("flask.db")
    # SQL文を実行
    c=conn.cursor()
    c.execute("SELECT task FROM task WHERE id=?",(id,))
    # DBからデータを取得
    task=c.fetchone()
    task=task[0]
    # DBからデータを取得
    # DBを閉じる
    c.close()
    # 配列に格納
    global item
    item={"tpl_id":id,"tpl_task":task}
    return render_template("answer.html",tpl_task=item)

@app.route("/answer",methods=["POST"])
def answer_post():
    # HTMLから送られてきたデータを取得、変数flaskに格納
    answer=request.form.get("tpl_answer")
    upload = request.files['upload']
    # uploadで取得したファイル名をlower()で全部小文字にして、ファイルの最後尾の拡張子が'.png', '.jpg', '.jpeg'ではない場合、returnさせる。
    if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        conn=sqlite3.connect("flask.db")
        # DBにテータを追加
        # DBに接続
        conn=sqlite3.connect("flask.db")
        # SQL文を実行
        c=conn.cursor()
        c.execute("insert into answer values(null,?,?,?)",(answer,item["tpl_id"],"no_img.png"))
        c.execute("UPDATE task SET flag = flag + 1 WHERE id=?",(item["tpl_id"],))
        # 情報を書き込み
        conn.commit()
        # DBを閉じる
        c.close()
        # ホームページにリダイレクト
        return redirect("/list")
    # DBにテータを追加
    # DBに接続
    conn=sqlite3.connect("flask.db")
    # SQL文を実行
    c=conn.cursor()
    # 下の def get_save_path()関数を使用して "./static/img/" パスを戻り値として取得する。
    save_path = get_save_path()
    # パスが取得できているか確認
    print(save_path)
    # ファイルネームをfilename変数に代入
    filename = upload.filename
    # 画像ファイルを./static/imgフォルダに保存。 os.path.join()は、パスとファイル名をつないで返してくれます。
    upload.save(os.path.join(save_path,filename))
    # ファイル名が取れることを確認、あとで使うよ
    print(filename)
    c.execute("insert into answer values(null,?,?,?)",(answer,item["tpl_id"],filename))
    c.execute("UPDATE task SET flag = flag + 1 WHERE id=?",(item["tpl_id"],))
    # 情報を書き込み
    conn.commit()
    # DBを閉じる
    c.close()
    # ホームページにリダイレクト
    return redirect("/list")

#課題4の答えはここも
def get_save_path():
    path_dir = "./static/img"
    return path_dir

@app.route("/aanswer/<int:id>")
# idを受け取り
def aanswer_get(id):
    # DBに接続
    conn=sqlite3.connect("flask.db")
    # SQL文を実行
    c=conn.cursor()
    c.execute("SELECT task FROM task WHERE id=?",(id,))
    # DBからデータを取得
    task=c.fetchone()
    task=task[0]
    # DBを閉じる
    c.close()
    # 配列に格納
    global aitem
    aitem={"tpl_id":id,"tpl_task":task}
    return render_template("aanswer.html",tpl_task=aitem)

@app.route("/aanswer",methods=["POST"])
def aanswer_post():
    # HTMLから送られてきたデータを取得、変数flaskに格納
    answer=request.form.get("tpl_answer")
    upload = request.files['upload']
    # uploadで取得したファイル名をlower()で全部小文字にして、ファイルの最後尾の拡張子が'.png', '.jpg', '.jpeg'ではない場合、returnさせる。
    if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        conn=sqlite3.connect("flask.db")
        # DBにテータを追加
        # DBに接続
        conn=sqlite3.connect("flask.db")
        # SQL文を実行
        c=conn.cursor()
        c.execute("insert into answer values(null,?,?,?)",(answer,item["tpl_id"],"no_img.png"))
        c.execute("UPDATE task SET flag = flag + 1 WHERE id=?",(item["tpl_id"],))
        # 情報を書き込み
        conn.commit()
        # DBを閉じる
        c.close()
        # ホームページにリダイレク
        return redirect("/QAlist")
    # DBにテータを追加
    # DBに接続
    conn=sqlite3.connect("flask.db")
    # SQL文を実行
    c=conn.cursor()
    # 下の def get_save_path()関数を使用して "./static/img/" パスを戻り値として取得する。
    save_path = get_save_path()
    # パスが取得できているか確認
    print(save_path)
    # ファイルネームをfilename変数に代入
    filename = upload.filename
    # 画像ファイルを./static/imgフォルダに保存。 os.path.join()は、パスとファイル名をつないで返してくれます。
    upload.save(os.path.join(save_path,filename))
    # ファイル名が取れることを確認、あとで使うよ
    print(filename)
    c.execute("insert into answer values(null,?,?,?)",(answer,aitem["tpl_id"],filename))
    c.execute("UPDATE task SET flag = flag + 1 WHERE id=?",(aitem["tpl_id"],))
    # 情報を書き込み
    conn.commit()
    # DBを閉じる
    c.close()
    # ホームページにリダイレクト
    return redirect("/QAlist")

#課題4の答えはここも
def get_save_path():
    path_dir = "./static/img"
    return path_dir
# ★★★★★★★★★★★★★★★




# ★★★★★削除★★★★★
@app.route("/delete/<int:id>",methods=["POST"])
def delete_post(id):
    print(id)
    # DBに接続
    conn=sqlite3.connect("flask.db")
    # SQL文を実行
    c=conn.cursor()
    # 指定したidのtask削除
    c.execute("DELETE FROM task WHERE id=?",(id,))
    conn.commit()
    c.close()
    return redirect("/list")
# ★★★★★★★★★★★★★★★

# ★★★★★QA削除★★★★★
@app.route("/QAdelete/<int:id>",methods=["POST"])
def QAdelete_post(id):
    print(id)
    # DBに接続
    conn=sqlite3.connect("flask.db")
    # SQL文を実行
    c=conn.cursor()
    # 指定したidのtask削除
    c.execute("DELETE FROM task WHERE id=?",(id,))
    conn.commit()
    c.close()
    return redirect("/QAlist")
# ★★★★★★★★★★★★★★★

# ★★★★★A削除★★★★★
@app.route("/adelete/<int:id>",methods=["POST"])
def adelete_post(id):
    print(id)
    # DBに接続
    conn=sqlite3.connect("flask.db")
    # SQL文を実行
    c=conn.cursor()
    # 指定したidのtask削除
    c.execute("SELECT question_id FROM answer WHERE id=?",(id,))
    # DBからデータを取得
    task=c.fetchone()
    task=task[0]
    print("タスクテストプリント")
    print(task)
    c.execute("DELETE FROM answer WHERE id=?",(id,))
    c.execute("UPDATE task SET flag = flag - 1 WHERE id=?",(task,))
    conn.commit()
    c.close()
    return redirect("/alist/"+str(task))
# ★★★★★★★★★★★★★★★


# ★★★★★定型文★★★★★
# エラーハンドラー
@app.errorhandler(404)
def page_not_found(error):
    return 'ないよ！', 404

if __name__=="__main__":
    app.run(debug=True)
# ★★★★★★★★★★★★★★★