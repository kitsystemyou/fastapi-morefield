from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from models import User, Task, Score
from fastapi.staticfiles import StaticFiles
from logging import getLogger, StreamHandler
import db
import re

app = FastAPI(
    title='MoreField',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．',
)

app.mount("/templates/static", StaticFiles(directory="templates/static"), name="static")

# new テンプレート関連の設定 (jinja2)
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用


logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")


@app.get("/")
async def index(request: Request):
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
async def moa(request: Request):
    user = db.session.query(User).filter(User.username == 'admin').first()
    score = db.session.query(Score).all()
    for s in score:
        s.date = s.date.strftime('%Y-%m-%d %H:%M:%S')
    db.session.close()

    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'user': user,
                                       'score': score})


@app.post("/moa")
async def postmoa(request: Request):
    pattern = re.compile(r"^([0-9])*")
    data = await request.form()
    logger.info("body, request: %s", data.get("player_name"))
    logger.info("body, request: %s", data.get("kind"))
    logger.info("body, request: %s", data.get("point"))
    logger.info("body, request: %s", data.get("tag"))
    if pattern.fullmatch(data.get("point")) is None:
        logger.info("invalid point")
        return RedirectResponse(url=app.url_path_for("moa"), status_code=status.HTTP_303_SEE_OTHER)
    score = Score(player_name=data.get("player_name"),
                  kind=data.get("kind"),
                  point=data.get("point"),
                  tag=data.get("tag"))
    db.session.add(score)
    db.session.commit()
    db.session.close()

    return RedirectResponse(url=app.url_path_for("moa"), status_code=status.HTTP_303_SEE_OTHER)
