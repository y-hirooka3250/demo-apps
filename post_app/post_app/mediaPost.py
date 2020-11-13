import os
import sys
import mariadb

import pytz
import datetime

from flask import Flask, render_template, request, jsonify, redirect, send_from_directory
from werkzeug.utils import secure_filename


app = Flask(__name__)
# 画像のアップロード先のディレクトリ
UPLOAD_FOLDER = './uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["JSON_AS_ASCII"] = False

# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])


@app.route('/post', methods=['GET'])
def get():
    return render_template('post.html', \
        title = '記事投稿(v2) v202009240951', \
        message = '掲載する画像を選択して下さい。', \
        flag = False)

@app.route('/post/upload', methods=['POST'])
def upload_post():
    '''
    画像アップロード
    '''

    # ファイルのリクエストパラメータを取得
    f = request.files.get('image')
    title = request.form['title']
    text = request.form['sentence']

    if f:
        # ファイル名を取得
        filename = secure_filename(f.filename)

        # ファイルを保存するディレクトリを指定
        filepath = filename

        # ファイルを保存する
        f.save(filepath)
        image = '/post_app/post_app/' + filename

        file_flg = 2
    else:
        image = ''
        file_flg = 1

    host_aa = 'mariadb.default.svc.cluster.local'
    data_base = 'mydb'
    user_aa ='myuser'
    password_aa = 'mypass'

    # DB接続
    conn = mariadb.connect(
        user=user_aa,
        password=password_aa,
        host=host_aa,
        port=3306,
        database=data_base
    )
    cursor = conn.cursor()

    # 登録用データの作成
    article_title = title
    #image = '/post_app/post_app/' + filename
    now = datetime.datetime.now(pytz.timezone('UTC'))
    article_text = text
    #file_flg = 2 

    try:
        # 登録処理実行
        # sql_str="INSERT INTO mydb.article VALUES(%s, %s, %s, %s, %s, %s)" % (1, article_title, article_text, image, file_flg, now)
        # sql_str = "INSERT INTO article (article_title, article_text, image, flag, last_update_timestamp) VALUES (?, ?, ?, ?, ?)", (article_title, article_text, image, file_flg, now)
        cursor.execute(
            "INSERT INTO article (article_title, article_text, image, flag, last_update_timestamp) VALUES (?, ?, ?, ?, ?)",
            (article_title, article_text, image, file_flg, now))
    except mariadb.Error as e: 
        # DB切断
        cursor.close()
        conn.close()

        sys.stderr.write("*** mariadb() *** abend ***\n")
        
        return render_template('post.html', \
            title = '記事投稿(同期)', \
            message = 'DBの登録に失敗しました。', \
            flag = False)

    conn.commit()

    # DB切断
    cursor.close()
    conn.close()

    return render_template('post.html', \
        title = '記事投稿(同期)v1.0', \
        message = '記事の投稿が完了しました', \
        flag = False)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)


