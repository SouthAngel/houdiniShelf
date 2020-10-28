# -*- coding: utf-8 -*-
import hou
from hutil.Qt import QtWidgets as qw


def foo():
    dg = hou.qt.Dialog()
    dg.setWindowTitle('MultiAddAttribute')
    lt = qw.QFormLayout()
    dg.setLayout(lt)
    wg1 = qw.QPushButton('Set Attribute')    
    wg2 = qw.QTextEdit('value_name i 1')
    def _c():
        sels = hou.selectedNodes()
        if len(sels) < 1:
            print('Nothing selected')
            return
        _sps = wg2.toPlainText().split('\n')
        pg = sels[0].parmTemplateGroup()        
        for sp in iter(_sps):
            _sp = sp.split()
            if len(_sp) < 3:
                print('Text format error')
                return
            _mp = {'i': (int, hou.IntParmTemplate), 'f': (float, hou.FloatParmTemplate), 's': (str, hou.StringParmTemplate)}
            vn = _sp[0]
            ln = _sp[0].split('_')
            ln = map(lambda x: x[0].upper()+x[1:], ln)
            tfn, hfn = _mp.get(_sp[1], 's')
            pt = hfn(vn, ' '.join(ln), 1, (tfn(_sp[2]),))
            pg.addParmTemplate(pt)
        sels[0].setParmTemplateGroup(pg)
    wg1.clicked.connect(_c)
    lt.addRow(wg1, wg2)
    wg3 = qw.QPushButton('Delete Attribute')
    wg4 = qw.QLineEdit('value_name')
    def _dc():
        sels = hou.selectedNodes()
        if len(sels) < 1:
            print('Nothing selected')
            return
        _sp = wg4.text().split()
        pg = sels[0].parmTemplateGroup()
        for each in iter(_sp):
            try:
                pg.remove(each)
                sels[0].setParmTemplateGroup(pg)
            except Exception as e:
                print(str(e))

    wg3.clicked.connect(_dc)
    lt.addRow(wg3, wg4)
    dg.show()
    
foo()
