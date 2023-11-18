from fastapi import FastAPI
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import db
from models import User, Task, Score
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title='MoreField',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．',
)

app.mount("/templates/static", StaticFiles(directory="templates/static"), name="static")

# new テンプレート関連の設定 (jinja2)
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用


@app.get("/")
def index(request: Request):
    user = db.session.query(User).filter(User.username == 'admin').first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()
    score = db.session.query(Score).all()
    db.session.close()
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'user': user,
                                       'task': task,
                                       'score': score})


@app.get("/moa")
async def admin(request: Request):
    user = db.session.query(User).filter(User.username == 'admin').first()
    score = db.session.query(Score).all()
    db.session.close()

    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'user': user,
                                       'score': score})
