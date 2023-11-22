from __future__ import annotations
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse, FileResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from models import User, Score
from fastapi.staticfiles import StaticFiles
from logging import getLogger, StreamHandler
import db
import re
from sqlalchemy import func
from sqlalchemy.engine.row import Row
from datetime import datetime
import gc

app = FastAPI(
    title='MoreField',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．',
)

app.mount("/templates/static", StaticFiles(directory="templates/static"), name="static")

# new テンプレート関連の設定 (jinja2)
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用


logger = getLogger("uvicorn.app")
logger.addHandler(StreamHandler())
logger.setLevel("INFO")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse('/templates/static/favicon.ico')


@app.get("/")
async def index(request: Request):
    user = db.session.query(User).filter(User.username == 'admin').first()
    score: list[Row] = db.session.query(
        Score.id,
        Score.player_name,
        Score.kind,
        func.sum(Score.point).label('point'),
        Score.tag,
        Score.date.label('date')).group_by(Score.player_name, Score.tag).all()
    new_score = []
    for s in score:
        ns = s._asdict()
        ns['date'] = ns['date'].strftime('%Y-%m-%d %H:%M:%S')
        new_score.append(ns)
        del s
        gc.collect()
    db.session.close()
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'user': user,
                                       'score': new_score})


@app.get("/moa")
async def moa(request: Request):
    user = db.session.query(User).filter(User.username == 'admin').first()
    score = db.session.query(Score).all()
    db.session.close()
    for s in score:
        s.date = s.date.strftime('%Y-%m-%d %H:%M:%S')

    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'user': user,
                                       'score': score})


@app.post("/moa")
async def postmoa(request: Request):
    pattern = re.compile(r"^([0-9])*")
    data = await request.form()
    if pattern.fullmatch(data.get("point")) is None:
        logger.info("invalid point")
        return RedirectResponse(url=app.url_path_for("moa"), status_code=status.HTTP_303_SEE_OTHER)
    score = Score(player_name=data.get("player_name"),
                  kind=data.get("kind"),
                  point=data.get("point"),
                  tag=data.get("tag"),
                  date=datetime.now())
    db.session.add(score)
    db.session.commit()
    db.session.close()

    return RedirectResponse(url=app.url_path_for("moa"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/moa/delete/{id}")
async def delete_score(request: Request):
    score = db.session.query(Score).filter(Score.id == request.path_params['id']).first()
    db.session.delete(score)
    db.session.commit()
    db.session.close()
    logger.info("delete score id: %s", request.path_params['id'])

    return RedirectResponse(url=app.url_path_for("moa"), status_code=status.HTTP_303_SEE_OTHER)
