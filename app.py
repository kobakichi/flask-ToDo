from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'#データベースの名前作成
db = SQLAlchemy(app)#データベースをインスタンス化

class Post(db.Model):#データベースをクラスで宣言、設計
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)


@app.route('/', methods=['GET', 'POST'])#トップページでGETとPOSTメソッドを受け取る指示
def index():
    if request.method == 'GET':#データベースへのデータ保存処理
        posts = Post.query.order_by(Post.due).all()#完了期限が迫っているものから表示させる
        return render_template('index.html', posts=posts)
    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')

        due = datetime.strptime(due, '%Y-%m-%d')
        new_post = Post(title=title, detail=detail, due=due)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

@app.route('/create')#タスク作成画面表示
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')#タスクの詳細画面表示
def read(id):
    post = Post.query.get(id)

    return render_template('detail.html', post=post)

@app.route('/delete/<int:id>')#タスクの削除処理
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])#トップページでGETとPOSTメソッドを受け取る指示
def update(id):#編集を行う処理
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)