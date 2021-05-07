"""
Modue Doc String.

"""

# -*- coding: utf-8 -*-

import sys
import os

from PyQt5 import (QtGui)
from PyQt5.QtCore import (Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSlot)
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QMainWindow)

from costadm_ui import Ui_CostAdm
from costadm_dialog_ui import Ui_MsgDialog
from costadm_dialogsort_ui import Ui_DialogSort
from costadm_app import CostAdmApp

# pylint: disable=attribute-defined-outside-init
# pylint: disable=invalid-name

class DfModel(QAbstractTableModel):
    """Doc String."""
    def __init__(self, data, formats=None, grouper=None):
        super(DfModel, self).__init__()
        self.df = data
        self.df_base = data
        self.formats_base = formats
        self.grouper = grouper
        self.set_columns(self.df, self.formats_base)

    def set_columns(self, data, formats):
        """Doc String."""
        if data is None:
            return

        n_cols = 0 if formats is None else len(formats)  # set to len of formats
        n_cols = n_cols if (data is None or n_cols > 0) else data.shape[1]  # set to len of df if no formats
        if n_cols == 0:
            return
        self.colname_dfcol = dict()
        self.colname_dfcol = {data.columns[i]: i for i in range(0, data.shape[1])}

        if formats is not None:
            # mop col nr to name and col no to display string  # col must be in df
            self.qtcol_colname = {i: c
                                  for i, c in enumerate([col_name for col_name in formats
                                                          if col_name in self.colname_dfcol])
                                  }

            self.qtcol_coldisplay = {i: c
                                      for i, c in
                                         enumerate([display_name for col_name, (display_name, _) in formats.items()
                                                          if col_name in self.colname_dfcol])
                                     }
            self.coldisplay_qtcol = {c: i for i, c in self.qtcol_coldisplay.items()}
            self.formats = {c: f for c, (_, f) in formats.items()
                                           if c in self.colname_dfcol}
        else:
            self.qtcol_colname = {i: data.columns[i] for i in range(0, data.shape[1])}
            self.qtcol_coldisplay = {i: data.columns[i] for i in range(0, data.shape[1])}
            self.coldisplay_qtcol = {data.columns[i]: i for i in range(0, data.shape[1])}

    def get_columns(self):
        """Doc String."""
        return [d for i, d in self.qtcol_coldisplay.items()] if self.df is not None else []

    def data(self, index, role=Qt.DisplayRole):
        """Doc String."""
        row, col = index.row(), index.column()
        col_name = self.qtcol_colname[col]
        df_col = self.colname_dfcol[col_name]    # map col to name and the to the column nr of df
        if role == Qt.DisplayRole:
            return None if self.df is None else self.formats[col_name].format(self.df.iat[row, df_col])
        elif role == Qt.TextAlignmentRole:
            # Align numbers right, text left
            return Qt.AlignLeft if self.formats[col_name] == '{}' else Qt.AlignRight
        else:
            return QVariant()

    def rowCount(self, parent=QModelIndex()):
        """Doc String."""
        # pylint: disable=unused-argument
        return 0 if self.df is None else self.df.shape[0]

    def columnCount(self, parent=QModelIndex()):
        """Doc String."""
        # pylint: disable=unused-argument
        return 0 if self.df is None else len(self.formats)   # formats contains all columns to be displayed

    def headerData(self, row_col, orientation, role=Qt.DisplayRole):
        """Doc String."""
        if role == Qt.FontRole:
            font = QtGui.QFont()
            font.setBold(True)
            return font
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.qtcol_coldisplay[row_col])
        elif orientation == Qt.Vertical:
            if role == Qt.DisplayRole:
                return QVariant('{:4d}'.format(row_col))
            elif role == Qt.TextAlignmentRole:
                return Qt.AlignRight
        return QVariant()

    def change(self, how):
        """Doc String."""
        if self.df is None:
            return
        self.layoutAboutToBeChanged.emit()
        if how == 'expand':
            print(f'*** model.change: setting back to df_base, shape {self.df_base.shape}')
            self.df = self.df_base
        elif self.grouper is not None:
            self.df = self.grouper(self.df_base)
            print(f'*** model.change: setting to grouped df, shape {self.df.shape}')
        self.set_columns(self.df, self.formats_base)
        self.layoutChanged.emit()

    def do_sort(self, sort_on_ext, order):
        """Doc String."""
        print(f'*** df.do_sort: df.columns = {self.df.columns}')
        if not sort_on_ext:
            return
        # map external column name to real columns name
        sort_on = [self.qtcol_colname[self.coldisplay_qtcol[c]] for c in sort_on_ext]

        self.layoutAboutToBeChanged.emit()
        self.df = self.df.sort_values(by=sort_on, ascending=order)
        print(f'*** model.sort: sorted by={sort_on}, ascendig={order}')
        self.set_columns(self.df, self.formats_base)
        self.layoutChanged.emit()


class MsgDialog(QDialog):
    """Doc String."""
    def __init__(self, title='Exit', msg='Unsaved Changes. You want to exit?',
                button_types='yes_no'):
        super().__init__()
        self.ui = Ui_MsgDialog()
        self.ui.setupUi(self, title, msg, button_types)


class DialogSort(QDialog, Ui_DialogSort):
    """Doc String."""
    def __init__(self, order_names=('Ascendente', 'Descrescente'), parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.type2name = dict(ascending=order_names[0], descending=order_names[1])
        self.name2type = {order_names[0]: 'ascending', order_names[1]: 'descending'}

        self.sort_column = [self.combo_col_1, self.combo_col_2, self.combo_col_3, self.combo_col_4, self.combo_col_5]
        self.sort_order = [self.combo_ord_1, self.combo_ord_2, self.combo_ord_3, self.combo_ord_4, self.combo_ord_5]

        for i in range(len(self.sort_column)):
            self.sort_column[i].addItem("")
            self.sort_column[i].setCurrentIndex(0)
            self.sort_order[i].addItems([self.type2name['ascending'], self.type2name['descending']])
            self.sort_order[i].setCurrentIndex(0)

    def sort_columns(self, columns):
        """Doc String."""
        for i in range(5):
            self.sort_column[i].addItems(sorted(columns))
        ret = self.exec()
        sort_how = dict()
        if ret:
            sort_how = dict()
            for i in range(len(self.sort_column)):
                if self.sort_column[i].currentText() != '':
                    print(f'*** sort_columns: {self.name2type}, {self.name2type[self.sort_order[i].currentText()]}')
                    sort_how[self.sort_column[i].currentText()] = self.name2type[self.sort_order[i].currentText()]
        return sort_how


class CostAdmMain(QMainWindow):
    """Doc String."""
    def __init__(self):
        super().__init__()
        self.exit_dialog = MsgDialog('ALERTA', 'Alterações não salvas. Quer sair mesmo?','yes_no')
        self.ui = Ui_CostAdm()
        self.ui.setupUi(self)
        self.app = CostAdmApp()
        self.init_tabs()
        self.init_menus()
        self.init_buttons()
        self.cur_tab = self.ui.cost_tab.currentIndex()

    def init_menus(self):
        """Doc String."""
        self.actions = {
            'create_structure': ['load_files', lambda x: self.create_structure('structure', x)],
            'calc_costs_item': ['no_load', lambda: self.calc_costs_item_copacker(['costs_item', 'costs_copacker'])],
            'calc_costs_avg': ['no_load', lambda: self.calc_costs_avg('costs_avg')],
            'load_structure': ['load_file', lambda x: self.load_model('structure', x, self.app.load_cost_structure)],
            'load_quotes': ['load_file', lambda x: self.load_model('quotes', x, self.app.load_quotes)],
            'load_prod': ['load_file', lambda x: self.load_model('prod_volumes', x, self.app.load_prod_vols)],
            'export_costs': ['save_file_as', lambda x: self.app.save(['costs_item', 'costs_copacker', 'costs_avg'], x)],
            'export_structure': ['save_file_as', lambda x: self.app.save(['structure'], x)],
            'quit': ['no_load', self.close],
            'expand': ['no_load', self.expand_model],
            'collapse': ['no_load', self.collapse_model],
            'sort': ['no_load', self.sort_model],
        }

    def init_tabs(self):
        """Doc String."""
        self.tabno_tabname = {
            0: 'structure',
            1: 'quotes',
            2: 'prod_volumes',
            3: 'costs_item',
            4: 'costs_copacker',
            5: 'costs_avg'
        }
        self.tabname_tabno = {n: i for i, n in self.tabno_tabname.items()}

        self.views = {
            'structure': self.ui.table_cost_structure,
            'quotes': self.ui.table_quotes,
            'prod_volumes': self.ui.table_prod_volumes,
            'costs_item': self.ui.table_costs_item,
            'costs_copacker': self.ui.table_costs_copacker,
            'costs_avg': self.ui.table_costs_avg,
        }
        self.models = dict()

        for i in self.tabname_tabno:
            self.models[i] = DfModel(None)
            self.views[i].setModel(self.models[i])

        self.cur_tab = self.ui.cost_tab.currentIndex()

    def init_buttons(self):
        """Doc String."""

    def load_model(self, name, file_name, load_func):
        """Doc String."""
        err = load_func(file_name)
        if err[0] == 'ok':
            self.models[name] = DfModel(self.app.df[name], self.app.df_formats[name], self.app.grouper[name])
            self.views[name].setModel(self.models[name])
            self.ui.cost_tab.setCurrentIndex(self.tabname_tabno[name])
            self.cur_tab = self.ui.cost_tab.currentIndex()
        else:
            print(err[1])
            MsgDialog('Load Error', err[1], 'ok').exec()

    def calc_costs_item_copacker(self, names):
        """Doc String."""
        name = names[0]
        # print(f'*** Calc_costs_item({name})')
        self.app.calc_costs_item()
        self.models[name] = DfModel(self.app.df[name], self.app.df_formats[name], self.app.grouper[name])
        self.views[name].setModel(self.models[name])
        self.ui.cost_tab.setCurrentIndex(self.tabname_tabno[name])
        self.cur_tab = self.ui.cost_tab.currentIndex()

        name = names[1]
        self.app.calc_costs_copacker()
        self.models[name] = DfModel(self.app.df[name], self.app.df_formats[name], self.app.grouper[name])
        self.views[name].setModel(self.models[name])

    def calc_costs_avg(self, name):
        """Doc String."""
        # print(f'*** Calc_costs_avg({name})')
        self.app.calc_costs_avg()
        self.models[name] = DfModel(self.app.df[name], self.app.df_formats[name], self.app.grouper[name])
        self.views[name].setModel(self.models[name])
        self.ui.cost_tab.setCurrentIndex(self.tabname_tabno[name])
        self.cur_tab = self.ui.cost_tab.currentIndex()

    def create_structure(self, name, file_names):
        """Doc String."""
        # print(f'*** create_structure({name})')
        self.app.load_recipes(file_names)
        self.models[name] = DfModel(self.app.df[name], self.app.df_formats[name],  self.app.grouper[name])
        self.views[name].setModel(self.models[name])
        self.ui.cost_tab.setCurrentIndex(self.tabname_tabno[name])
        self.cur_tab = self.ui.cost_tab.currentIndex()

    def quit(self):
        """Doc String."""
        self.close()

    def closeEvent(self, event):
        """Doc String."""
        if self.app.unsaved_changes():
            if not self.exit_dialog.exec():
                event.ignore()
                return
        event.accept()

    def collapse_model(self):
        """Doc String."""
        print(f'*** collapse: {self.cur_tab}')
        self.models[self.tabno_tabname[self.cur_tab]].change('collapse')

    def expand_model(self):
        """Doc String."""
        print(f'*** expand: {self.cur_tab}')
        self.models[self.tabno_tabname[self.cur_tab]].change('expand')

    def sort_model1(self, ascending='True'):
        """Doc String."""
        sort_keys = {
                     'structure': ['cprod', 'ind', 'type'],
                     'quotes': ['citem'],
                     'prod_volumes': ['crpod', 'ind'],
                     'costs_item': ['cprod', 'ind', 'type'],
                     'costs_copacker': ['cprod', 'ind', 'type'],
                     'costs_avg': ['cprod', 'type']
                    }
        self.models[self.tabno_tabname[self.cur_tab]].do_sort(sort_keys[self.tabno_tabname[self.cur_tab]], ascending)

    def sort_model(self):
        """Doc String."""
        columns = self.models[self.tabno_tabname[self.cur_tab]].get_columns()
        if not columns:    # empty data frame
            return

        sort_how = DialogSort().sort_columns(columns)
        if sort_how:     # make sure that at least one column was selected
            columns, order = zip(*sort_how.items())
            self.models[self.tabno_tabname[self.cur_tab]].do_sort(list(columns), [x == 'ascending' for x in order])

    @pyqtSlot('int')
    def set_tab(self, tabno):
        """Doc String."""
        self.cur_tab = tabno

    @pyqtSlot()
    def save_table(self):
        """Doc String."""

    @pyqtSlot()
    def del_table(self):
        """Doc String."""

    @pyqtSlot('QAction*')
    def do_action(self, qt_act):
        """Doc String."""
        action = self.actions[qt_act.objectName()]
        file_action = action[0]
        if file_action == 'no_load':
            return action[1]()
        file_name, is_valid = get_filename(file_action)
        if is_valid:
            return action[1](file_name)


# Helper functions
def get_filename_gen(last_dir='/Users/maxi/Documents/WOW/CUSTOS/ABR'):
    """Doc String."""
    # pylint: disable=unused-argument
    # pylint: disable=redefined-outer-name
    def get_filename(action):
        """Doc String."""
        nonlocal last_dir
        file_name = ''
        is_valid = False

        if action == 'load_file':
            file_name, _ = QFileDialog.getOpenFileName(None, 'Load File', last_dir, 'Excel Files (*.xlsx *.xls)')
            is_valid = file_name != ''

        elif action == 'load_files':
            file_name, _ = QFileDialog.getOpenFileNames(None, 'Load File', last_dir, 'Excel Files (*.xlsx *.xls)')
            is_valid = file_name != []

        elif action == 'save_file':    # We do not return a file name, application needs to know the file name
            is_valid = True

        elif action == 'save_file_as':
            file_name, _ = QFileDialog.getSaveFileName(None, 'Save File', last_dir, 'Excel Files (*.xlsx)')
            is_valid = file_name != ''

        if file_name != '' and file_name != []:
            if isinstance(file_name, list):
                last_dir = os.path.realpath(os.path.dirname(file_name[0]))
            else:
                last_dir = os.path.realpath(os.path.dirname(file_name))

        return file_name, is_valid

    return get_filename


get_filename = get_filename_gen()
# MAIN Program


if __name__ == '__main__':
    # Some code to obtain the form file name, ui_file_name
    app = QApplication(sys.argv)

    costadm = CostAdmMain()

    costadm.show()
    sys.exit(app.exec_())
