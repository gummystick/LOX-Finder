from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello_world():
    eiwit=request.args.get("Eiwit")
    jaartal=request.args.get("Jaartal")
    return render_template('./index.html')

@app.route('/test')
def test():
    return render_template('./test.html')


if __name__ == '__main__':
    app.run()
