
from shapely.geometry import Point, LineString, LinearRing
import geopandas
import ezdxf
POINT_PRECISION = 0.05


def check_dupl_by_centroid(df):  
    _c = geopandas.GeoDataFrame(geometry = df.centroid)
    _r = geopandas.sjoin_nearest(_c, _c, max_distance= POINT_PRECISION) 
    return _r[ _r.index < _r.index_right ].index_right

def check_dupl_by_buffer(df):
    _t = geopandas.GeoDataFrame(geometry=df.centroid)
    _t2 = geopandas.GeoDataFrame(geometry=_t.buffer( POINT_PRECISION, 2) ).sjoin(_t)
    return _t2[_t2.index < _t2.index_right].index_right


def open_dxf_with_msp(dxfname):
    assert dxfname.exists(), '输入dxf文件不存在'    
    dxffile = ezdxf.readfile(dxfname)
    return dxffile, dxffile.modelspace()  

def from_dxf_text(msp, layername, textname):
    ents = msp.query(f'TEXT[layer=="{layername}"]')
    return geopandas.GeoDataFrame(
        [{'handle': e.dxf.handle,
        textname: e.dxf.text,
        # 'stub_layer': e.dxf.layer,
        f'{textname}_pos':  Point(e.dxf.insert)}
        for e in ents],
        geometry=f'{textname}_pos').set_index('handle')
  
def from_dxf_line(msp, layername, linename):
    ents = msp.query(f'LINE[layer=="{layername}"]')    
    return geopandas.GeoDataFrame(
            [{'handle': e.dxf.handle,
            linename: LineString([e.dxf.start, e.dxf.end])}
            for e in ents],
            geometry=linename
            )