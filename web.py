import pymbtiles
import flask_cors
import flask

app = flask.Flask(__name__)
flask_cors.CORS(app, supports_credentials=True)


@app.route('/<int:z>/<int:x>/<int:y>')
def pbf(z, x, y):
    with pymbtiles.MBtiles('./mbtiles/index.mbtiles') as src:
        tile_data = src.read_tile(z, x, (1 << z) - 1 - y)
        if (tile_data == None):
            return "", 204
        else:
            resp = flask.Response(bytes(tile_data))
            resp.headers['Content-type'] = 'application/x-protobuf'
            resp.headers['Content-Encoding'] = 'gzip'
            return resp


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=3000, debug=True)

