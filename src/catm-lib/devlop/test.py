"""!
@file test.py
@version 1
@author Fumitaka ENDO
@date 2025-07-07T13:50:18+09:00
@brief test
"""
import argparse
import pathlib
# import xml.etree.ElementTree as ET
import catmlib.util.xcfgreader as uxr
import plotly.graph_objects as go


this_file_path = pathlib.Path(__file__).parent


def get_smds(root):
    smds = []
    for smd in root.findall(".//smd"):
        smds.append(dict(smd.attrib))

    return smds


def plot_smds(smds):
    fig = go.Figure()

    for smd in smds:
        # 数値化
        x = float(smd["x"])
        y = float(smd["y"])
        dx = float(smd["dx"])
        dy = float(smd["dy"])
        name = smd["name"]
        layer = smd.get("layer", "")

        # 矩形の4隅
        x0 = x - dx/2
        x1 = x + dx/2
        y0 = y - dy/2
        y1 = y + dy/2

        # 矩形を追加
        fig.add_shape(
            type="rect",
            x0=x0, x1=x1, y0=y0, y1=y1,
            line=dict(color="red"),
            fillcolor="lightcoral",
            opacity=0.5
        )

        # テキストも追加
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            text=[f"{name}"],
            mode="text",
            showlegend=False
        ))

    fig.update_layout(
        title="SMD Pads",
        xaxis_title="X",
        yaxis_title="Y",
        yaxis=dict(scaleanchor="x", scaleratio=1),  # 等倍率
        width=600, height=600
    )
    fig.show()


def list_packages(root):

    packages = root.findall(".//packages/package")
    names = [pkg.attrib.get("name") for pkg in packages]
    return names


def get_package_by_name(root, name):

    for pkg in root.findall(".//packages/package"):
        if pkg.attrib.get("name") == name:
            return pkg
    return None

def extract_polygons(package_elem):
    """
    <package> 要素から <polygon> 情報を取得
    :param package_elem: <package> の Element
    :return: [{'width': ..., 'layer': ..., 'vertices': [(x,y),...]}, ...]
    """
    polygons = []
    for poly in package_elem.findall(".//polygon"):
        poly_info = {
            "width": float(poly.attrib.get("width", 0)),
            "layer": int(poly.attrib.get("layer", 0)),
            "vertices": []
        }
        for vtx in poly.findall(".//vertex"):
            x = float(vtx.attrib.get("x", 0))
            y = float(vtx.attrib.get("y", 0))
            poly_info["vertices"].append( (x, y) )
        polygons.append(poly_info)
    return polygons

def plot_polygons(polygons):
    fig = go.Figure()

    for idx, poly in enumerate(polygons):
        x, y = zip(*poly['vertices'])
        # 閉じるために最初の点をもう一度追加
        x = list(x) + [x[0]]
        y = list(y) + [y[0]]

        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode="lines+markers",
            name=f"Polygon #{idx+1} (layer {poly['layer']})",
            line=dict(width=poly['width']*10, color='blue'),
            fill="toself",
            opacity=0.6
        ))

    fig.update_layout(
        title="Polygons",
        xaxis_title="X",
        yaxis_title="Y",
        yaxis=dict(scaleanchor="x", scaleratio=1),
        width=600,
        height=600,
        showlegend=True
    )

    fig.show()



if __name__ == "__main__":

    #lbr_path = "/Users/fendo/Work/Data/eagle-lbr/ReadoutPad3mmEndo.lbr" 
    lbr_path = "/Users/fendo/Work/Data/eagle-lbr/5025983393.lbr" 
    

    root = uxr.get_tree(lbr_path)
    name_list = list_packages(root)
    print(name_list)
    data = get_package_by_name(root, name_list[0])
    print(data)
    smds = get_smds(data)
    plot_smds(smds)
    # poly = extract_polygons(data)
    # plot_polygons(poly)