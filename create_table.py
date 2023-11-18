from models import User, Task, Score, Base, SQLITE3_NAME
from datetime import datetime

import db
import os


if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):

        # テーブルを作成する
        Base.metadata.create_all(db.engine)

    # サンプルユーザ(admin)を作成
    admin = User(username='admin', password='fastapi', mail='hoge@example.com')
    db.session.add(admin)  # 追加
    db.session.commit()  # データベースにコミット

    # サンプルタスク
    task = Task(
        user_id=admin.id,
        content='〇〇の締め切り',
        deadline=datetime(2019, 12, 25, 12, 00, 00),
    )
    print(task)

    # サンプルスコア
    score = Score(
        id=1,
        player_name='とわえもあ',
        point=3,
        kind='一位',
        tag='第一戦',
        date=datetime(2023, 12, 25, 12, 00, 00),
    )

    db.session.add(score)
    db.session.commit()

    score2 = Score(
        id=2,
        player_name='陽',
        point=2,
        kind='二位',
        tag='第一戦',
        date=datetime(2023, 12, 25, 12, 00, 00),
    )
    db.session.add(score2)
    db.session.commit()

    db.session.close()  # セッションを閉じる
