import hou
import toolutils

def run():
    sel = hou.selectedNodes()
    if len(sel) < 1:
        return
    if not isinstance(sel[0], hou.SopNode):
        return
    c = sel[0]
    p = c.parent()
    mt = p.createNode('material')
    mt.setInput(0, c)
    mt.setDisplayFlag(True)
    mt.setRenderFlag(True)
    mn = p.createNode('matnet')
    mb = mn.createNode('pxrmaterialbuilder')
    mt.parm('shop_materialpath1').set(mt.relativePathTo(mb))
    toolutils.networkEditor().setPwd(mb)
    

run()