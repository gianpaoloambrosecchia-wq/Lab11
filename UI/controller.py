import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []
        self._productChoice = None

    def fillDD(self):
        years = self._model.getAllYears()
        colors = self._model.getAllColors()
        for year in years:
            self._view._ddyear.options.append(
                ft.dropdown.Option(year)
            )
        for color in colors:
            self._view._ddcolor.options.append(
                ft.dropdown.Option(color)
            )
        self._view.update_page()


    def handle_graph(self, e):
        year = self._view._ddyear.value
        color = self._view._ddcolor.value
        if year is None or color is None:
            self._view.txtOut.controls.clear()
            self._view.create_alert("Seleziona un anno e un colore dagli appositi menù")
            self._view.update_page()
            return
        self._model.buildGraph(year, color)
        numNodes, numEdges = self._model.getGraphDetails()
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )
        self.fillDDProduct()
        self._view.txtOut.controls.append(
            ft.Text(f"Numero nodi: {numNodes}", color="blue")
        )
        self._view.txtOut.controls.append(
            ft.Text(f"Numero archi: {numEdges}", color="blue")
        )

        top3Archi = self._model.getTop3Archi()
        nodiRipetuti = self._model.getNodiRipetuti(top3Archi)
        self._view.txtOut.controls.append(
            ft.Text("I tre archi di peso maggiore sono:", color="blue")
        )
        for a in top3Archi:
            self._view.txtOut.controls.append(
                ft.Text(f"{a[0]} <-> {a[1]} | peso = {a[2]['weight']}")
            )
        self._view.txtOut.controls.append(
            ft.Text("I nodi ripetuti sono: ", color="blue")
        )
        for n in nodiRipetuti:
            self._view.txtOut.controls.append(
                ft.Text(n)
            )
        self._view.update_page()




    def fillDDProduct(self):
        products = self._model.getAllProducts()
        for product in products:
            self._view._ddnode.options.append(
                ft.dropdown.Option(data = product,
                                   text=product.Product_number,
                                   on_click=self._readProduct)
            )
        self._view.update_page()


    def _readProduct(self, e):
        self._productChoice = e.control.data


    def handle_search(self, e):
        if self._productChoice is None:
            self._view.txtOut2.controls.clear()
            self._view.create_alert("Seleziona un prodotto dal menù")
            self._view.update_page()
            return
        path = self._model.getPath(self._productChoice)
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(
            ft.Text("Il percorso ottimo è :", color="blue")
        )
        for p in path:
            self._view.txtOut2.controls.append(
                ft.Text(p)
            )
        self._view.update_page()
