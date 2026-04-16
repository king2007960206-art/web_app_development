from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 開發階段自動建立資料表
        db.create_all()
    app.run(debug=True)
