from controllers import app, index, admin


# FastAPIのルーティング用関数
app.add_api_route('/', index)

# FastAPIのルーティング用関数
app.add_api_route('/', index)
app.add_api_route('/admin', admin)
