'''

Thanks to Jie Jenn from learndataanalysis.org.
This nifty helper program is largely based on their work
(available on GitHub under https://gist.github.com/DataSolveProblems/
 972884bb9a53d5b2598e8674acc9e8ab#file-display-pandas-dataframe-pyqt5)

'''



from PyQt5.QtCore import QAbstractTableModel, Qt

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None