# -*- coding: utf-8 -*-
# Description: Create materials from a xml for speedtree, select a abc node
import os, time
import xml.etree.ElementTree as et
import hou
import toolutils

def run():
    sel = hou.selectedNodes()
    if len(sel) < 1:
        print("Select nothing")
        return
    if not isinstance(sel[0], hou.SopNode):
        print("Selected is not a sopnode")
        return
    c = sel[0]
    pa = c.parent()
    abc_path = c.parm("fileName").eval()
    abc_path_folder = os.path.dirname(abc_path)
    def get_tex_path(fname):
        return os.path.join(abc_path_folder, fname).replace("\\", "/")
    xml_path = os.path.splitext(abc_path)[0] + ".stmat"
    if not os.path.exists(xml_path):
        print("Material is not exists")
        return
    mnn = pa.node("stmatnet")
    if mnn is None:
        mnn = pa.createNode("matnet", node_name="stmatnet")
    mn = c.createOutputNode("material")
    eto = et.parse(xml_path)
    etroot = eto.getroot()
    mn.parm("num_materials").set(len(etroot))
    chmap = {
            "Color":"basecolor", 
            "Opacity":"opaccolor",
            # "Gloss":"rough",
            "SubsurfaceColor":"ssscolor",
            "SubsurfaceAmount":"sss",
        }
    _c = 0
    for mbk in etroot:
        _c += 1
        matn = mnn.node(mbk.attrib["Name"])
        if matn is None:
            matn = mnn.createNode("principledshader", node_name=mbk.attrib["Name"])
            matn.parm("rough").set(0.75)
        mn.parm("group%d" % _c).set("%sSG" % mbk.attrib["Name"])
        mn.parm("shop_materialpath%d" % _c).set(mn.relativePathTo(matn))
        for mit in mbk.getchildren():
            if mit.tag == "Map" and mit.attrib.has_key("File"):
                _n = mit.attrib["Name"]
                if _n == "Normal":
                    matn.parm("baseBumpAndNormal_enable").set(True)
                    matn.parm("baseNormal_texture").set(get_tex_path(mit.attrib["File"]))
                else:
                    kname = chmap.get(_n)
                    if kname:
                        matn.parm("%s_useTexture" % kname).set(True)
                        matn.parm("%s_texture" % kname).set(get_tex_path(mit.attrib["File"]))

run()