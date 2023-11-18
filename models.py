from datetime import datetime

from db import Base

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN

import hashlib

SQLITE3_NAME = "./db1.sqlite3"


class User(Base):
    """
    Userテーブル

    id       : 主キー
    username : ユーザネーム
    password : パスワード
    mail     : メールアドレス
    """
    __tablename__ = 'user'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    username = Column('username', String(256))
    password = Column('password', String(256))
    mail = Column('mail', String(256))

    def __init__(self, username, password, mail):
        self.username = username
        # パスワードはハッシュ化して保存
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.mail = mail

    def __str__(self):
        return str(self.id) + ':' + self.username


class Task(Base):
    """
    toDoタスク

    id       : 主キー
    user_id  : 外部キー
    content  : 内容
    deadline : 締め切り
    date     : 作成日
    done     : タスクを終了したか
    """
    __tablename__ = 'task'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    user_id = Column('user_id', ForeignKey('user.id'))
    content = Column('content', String(256))
    deadline = Column(
        'deadline',
        DateTime,
        default=None,
        nullable=False,
    )
    date = Column(
        'date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
    )
    done = Column('done', BOOLEAN, default=False, nullable=False)

    def __init__(self, user_id: int,
                 content: str,
                 deadline: datetime,
                 date: datetime = datetime.now()):
        self.user_id = user_id
        self.content = content
        self.deadline = deadline
        self.date = date
        self.done = False

    def __str__(self):
        return str(self.id) + \
            ': user_id -> ' + str(self.user_id) + \
            ', content -> ' + self.content + \
            ', deadline -> ' + self.deadline.strftime('%Y/%m/%d - %H:%M:%S') + \
            ', date -> ' + self.date.strftime('%Y/%m/%d - %H:%M:%S') + \
            ', done -> ' + str(self.done)


class Score(Base):
    """
    scoreテーブル

    id         : 主キー
    player_name: ユーザー名
    point      : 点数
    kind       : 区分
    tag        : タグ
    date       : 日付
    """
    __tablename__ = 'score'
    # TODO: columnの追加
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    player_name = Column('player_name', String(256))
    point = Column('point', INTEGER(unsigned=True))
    kind = Column('kind', String(256))
    tag = Column('tag', String(256))

    date = Column(
        'date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
    )

    def __init__(self,
                 #  id: int,
                 player_name: str,
                 point: int,
                 kind: str,
                 tag: str,
                 date: datetime = datetime.now()):
        # self.id = id
        self.player_name = player_name
        self.point = point
        self.kind = kind
        self.tag = tag
        self.date = date

    def __str__(self):
        return str(self.id) + \
            ': id -> ' + str(self.id) + \
            ', player_name -> ' + self.player_name + \
            ', point -> ' + str(self.point) + \
            ', kind -> ' + self.kind + \
            ', tag -> ' + self.tag + \
            ', date -> ' + self.date.strftime('%Y/%m/%d - %H:%M:%S')
