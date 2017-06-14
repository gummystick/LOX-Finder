from flask import Flask, render_template, request
import Tabel

app = Flask(__name__)

@app.route('/')
    # de pagina die las eerste wordt aangeroepen wordt hier aangeroepen.
def index():
    return render_template('./index.html')

@app.route('/table', methods=["GET"])
    # Wanneer er een zoekopdracht is gegeven wordt deze pagina aangeroepen.
    # De zoekopdrachten worden in variabelen ingeladen en de template van de pagina wordt geretouneerd met parameters ingevuld.
def table():
    tabobject = Tabel
    eiwit = request.args.get("Eiwit")
    jaartal = request.args.get("Jaartal")
    tab = tabobject.Tabel(eiwit, jaartal)
    tab.getTable()
    return render_template('./table.html', eiwit=eiwit, jaartal=str(jaartal), artrows=tab.tabelArt, protein=tab.tabelProt)

if __name__ == '__main__':
    app.run()
