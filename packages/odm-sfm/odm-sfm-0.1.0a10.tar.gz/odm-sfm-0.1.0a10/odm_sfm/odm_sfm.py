#!/usr/bin/python3
# coding: utf-8

import numpy as np, logging
import os, sys, cv2, argparse
import gzip, pickle, json, yaml
from itertools import combinations


Auth = lambda x: os.system(f'sudo chown -R {os.environ["USER"]} {x}')
##########################################################################################
def merge_dir(src, dst, pre='', sep='%'):
    Auth(src); os.makedirs(dst, exist_ok=True)
    for i in os.scandir(src): # USE os.link
        if i.is_symlink(): # NOT os.symlink
            i = os.readlink(i.path)
            if not os.path.isfile(i): continue
            x = f'{dst}/{pre}{os.path.basename(i)}'
            if not os.path.isfile(x): os.link(i, x)
        elif i.is_file() and not i.is_symlink():
            x = f'{dst}/{pre}{i.name}'
            if not os.path.isfile(x): os.link(i.path, x)
        else: merge_dir(i.path, dst, pre+i.name+sep)


def merge_json(src, dst, js, key=None):
    with open(f'{src}/{js}') as f: A = json.load(f)
    with open(f'{dst}/{js}') as f: B = json.load(f)
    for k,v in A.items(): # merge A to B
        if k not in B: B[k] = v
        #elif type(v)==list: B[k] += v
        elif type(v)==list: # type(B[k])==list
            B[k] += [i for i in v if i not in B[k]]
    with open(f'{dst}/{js}','w') as f: json.dump(B, f, indent=4)


########################################################
def sort_row(src, a=0, b=None):
    with open(src) as f: d = f.readlines()
    if type(a) in (list,tuple): d = sorted(a)
    elif type(a)==int: d[a:b] = sorted(d[a:b])
    with open(src,'w') as f: f.writelines(d); return d


########################################################
def feat_size(src, cfg=0.5, n=5): # update cfg
    k = 'feature_process_size'; mx = 0
    if type(cfg)==dict and k not in cfg: return
    v = cfg[k] if type(cfg)==dict else cfg
    for i in list(os.scandir(src+'/images'))[:n]:
        mx = max(mx, *cv2.imread(i.path).shape)
    if v<=0 or v>=mx: v = mx # for latest SfM
    elif type(v)==float: v = round(mx*v)
    if type(cfg)==dict: cfg[k] = min(v,mx)
    return min(v,mx) # cfg=dict/int/float


########################################################
def filter_match(pt1, pt2, mod=cv2.RANSAC, thd=1, prob=0.99):
    assert pt1.shape==pt2.shape and len(pt1)>6 and mod in (1,2,4,8)
    M, idx = cv2.findFundamentalMat(pt1, pt2, mod, thd, confidence=prob)
    idx = np.where(idx>0)[0]; return M, idx # inliers


##########################################################################################
# Ref: https://github.com/OpenDroneMap/ODM/blob/master/opendm/osfm.py
# Ref: https://github.com/mapillary/OpenSfM/blob/main/opensfm/config.py
# Ref: https://github.com/mapillary/OpenSfM/blob/main/opensfm/features_processing.py
# osfm.update_config(), config.load_config(), config.default_config()
def SfM_config(src, args):
    file = f'{src}/config.yaml'
    from opensfm.config import default_config
    if os.path.isfile(file):
        with open(file) as f: cfg = yaml.safe_load(f)
    else: cfg = default_config() # cfg=dict

    if type(args)==str and os.path.isfile(args):
        with open(args) as f: args = yaml.safe_load(f)
    if type(args)==dict: cfg.update(args)
    if cfg['feature_type']=='ORB': cfg['matcher_type']='BRUTEFORCE'
    feat_size(src, cfg) # cfg['feature_process_size']
    with open(file, 'w') as f: # update config.yaml
        f.write(yaml.dump(cfg, default_flow_style=False))


SfM_DIR = os.popen('locate bin/opensfm').readline().strip()
SfM_DIR = SfM_DIR[:SfM_DIR.find('/bin')]; sys.path.append(SfM_DIR)
SfM_CDM = ['extract_metadata', 'detect_features', 'match_features', 'create_tracks',
    'reconstruct', 'bundle', 'mesh', 'undistort', 'compute_depthmaps', 'compute_statistics',
    'export_ply', 'export_openmvs', 'export_visualsfm', 'export_pmvs', 'export_bundler',
    'export_colmap', 'export_geocoords', 'export_report', 'extend_reconstruction',
    'create_submodels', 'align_submodels']; INFO = logging.getLogger('Hua').info
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
##########################################################################################
# Ref: https://github.com/mapillary/OpenSfM/blob/main/bin/opensfm_run_all
# Ref: https://github.com/mapillary/OpenSfM/blob/main/bin/opensfm_main.py
# Ref: https://github.com/mapillary/OpenSfM/blob/main/opensfm/commands/__init__.py
def SfM_cmd(src, cmd): # cmd=int,str,range,list,tuple
    for c in [cmd] if type(cmd) in (int,str) else cmd:
        c = SfM_CDM[c] if type(c)==int else c
        assert type(c)==str and c.split()[0] in SfM_CDM
        c = f'{SfM_DIR}/bin/opensfm {c} {src}'; INFO(c)
        os.system(c) #p = os.popen(c).readline()
        #p = subprocess.Popen(c, shell=True)


##########################################################################################
# Ref: https://github.com/mapillary/OpenSfM/blob/main/opensfm/exif.py
# Ref: https://github.com/OpenDroneMap/ODM/blob/master/opendm/photo.py
# photo.get_gps_dop(), photo.parse_exif_values(), photo.get_xmp(), exif.get_xmp()
def SfM_exif_dop(src, L=0, dop=10): # add DOP to EXIF
    if not os.path.isdir(src+'/exif'):
        SfM_cmd(src, 'extract_metadata')
    for i in os.scandir(src+'/images'):
        e = f'{src}/exif/{i.name}.exif'
        with open(e,'r') as f: x = json.load(f)
        d = SfM_xmp_dop(i.path, L); gps = x['gps']
        gps['dop'] = d if d else gps.get('dop',dop)
        with open(e,'w') as f: json.dump(x, f, indent=4)


def SfM_xmp_dop(im, L=0):
    from opensfm.exif import get_xmp
    #from exifread import process_file
    with open(im, 'rb') as f:
        xmp = get_xmp(f)[0] # get xmp info
        #xmp = process_file(f, details=False)
    x = float(xmp.get('@drone-dji:RtkStdLat', -1))
    y = float(xmp.get('@drone-dji:RtkStdLon', -1))
    z = float(xmp.get('@drone-dji:RtkStdHgt', -1))
    #gps_xy_stddev = max(x,y); gps_z_stddev = z
    if max(x,y,z)<0: return None # use default
    dp = np.array([i for i in (x,y,z) if i>0])
    return np.mean(dp**L)**(1/L) if L else max(dp)


load_im = lambda dir,i: cv2.imread(f'{dir}/images/{i}')
load_ft = lambda dir,i: np.load(f'{dir}/features/{i}.features.npz')
##########################################################################################
# Ref: https://github.com/mapillary/OpenSfM/blob/main/opensfm/features.py
# features.normalize_features(), features.denormalized_image_coordinates()
# features.load_features(), features.save_features()
def SfM_feat_denorm(pt, hw): # pt=[x,y,size,angle]
    if type(hw)==str: hw = cv2.imread(hw).shape[:2]
    elif type(hw)==np.ndarray: hw = hw.shape[:2]
    assert type(hw) in (list,tuple) and len(hw)>1
    h,w = hw[:2]; p = pt.copy(); size = max(w,h)
    p[:,0] = p[:,0] * size - 0.5 + w / 2.0
    p[:,1] = p[:,1] * size - 0.5 + h / 2.0
    if p.shape[1]>2: p[:,2:3] *= size
    return np.int32(np.round(p[:,:3]))


# ft.files; ft['points']=[x,y,size,angle]
def SfM_feat_uv(im, src=0, pt=0, idx=''):
    if type(src)==type(im)==str:
        if type(pt)!=np.ndarray: # first
            pt = load_ft(src,im)['points']
        im = load_im(src, im) # then
    assert type(im)==np.ndarray, type(im)
    assert type(pt)==np.ndarray, type(pt)
    if 'float' in str(pt.dtype):
        pt = SfM_feat_denorm(pt[:,:2], im)
    pt = pt[idx] if type(idx)!=str else pt
    return im, pt[:,:2] # norm->pixel


##########################################################################################
# Ref: https://github.com/mapillary/OpenSfM/blob/main/opensfm/dataset.py
# Ref: https://github.com/mapillary/OpenSfM/blob/main/opensfm/matching.py
# Ref: https://github.com/mapillary/OpenSfM/blob/main/opensfm/actions/match_features.py
# match_features.run_dataset(), matching.match_images(), matching.save_matches()
def SfM_match(src, pre, mix=0): # match_features
    from opensfm.actions.match_features import timer, matching, write_report
    from opensfm.dataset import DataSet; data = DataSet(src); t = timer()
    GPS, RTK = [],[]; INFO(f'{SfM_DIR}/bin/opensfm match_features: {src}')
    if os.path.isdir(pre):
        merge_dir(pre+'/exif', src+'/exif')
        merge_dir(pre+'/features', src+'/features')
        merge_json(pre, src, 'camera_models.json')
        #merge_json(pre, src, 'reports/features.json')
        #merge_dir(pre+'/reports/features', src+'/reports/features')
        GPS, RTK = data.images(), DataSet(pre).images()
    else: # split data->(GPS,RTK)
        for i in data.images(): (RTK if i.startswith(pre) else GPS).append(i)
    if mix in (1,3): GPS += RTK # 1: match (GPS+RTK, RTK)
    if mix in (2,3): RTK += GPS # 2: match (GPS, RTK+GPS)
    pairs, preport = matching.match_images(data, {}, GPS, RTK)
    matching.save_matches(data, GPS, pairs)
    write_report(data, preport, list(pairs.keys()), timer()-t)


##########################################################################################
# Ref: https://github.com/mapillary/OpenSfM/blob/main/opensfm/tracking.py
# tracking.create_tracks_manager(), load_features(), load_matches()
def SfM_parse_csv(src):
    with open(f'{src}/tracks.csv') as f:
        data = f.readlines(); T = {}
    for i in data[1:]: # skip 1st-row
        i = i.split() # [im,tid,fid,xy,size,rgb,..]
        im, tid, fid = i[0], int(i[1]), int(i[2])
        xys = np.float64(i[3:6]).tolist() # [x,y,size]
        rgb = np.int32(i[6:9]).tolist() # RGB
        if im in T: # {im: {tid,fid,xys,rgb}}
            T[im]['tid'].append(tid); T[im]['fid'].append(fid)
            T[im]['xys'].append(xys); T[im]['rgb'].append(rgb)
        else: T[im] = dict(tid=[tid], fid=[fid], xys=[xys], rgb=[rgb])
        #print(i, '\n', im, tid, fid, xys, rgb)
    return T # {im: {tid,fid,xys,rgb}}


#from pyproj import Proj, transform
LLA = '+proj=lonlat +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
ECEF = '+proj=geocent +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
##########################################################################################
# Ref: https://github.com/mapillary/OpenSfM/blob/main/opensfm/geo.py
# Ref: https://github.com/mapillary/OpenSfM/blob/main/opensfm/actions/export_geocoords.py
# export_geocoords._transform_image_positions(), geo.to_topocentric(), geo.to_lla()
# transform(Proj(LLA), Proj(ECEF), *v, radians=False); Proj(LLA)(x,y,inverse=True)
def export_image_gps(src, tsv='image_geocoords.tsv'):
    from opensfm.dataset import DataSet; txt = tsv[:-3]+'txt'; rename_rec(src)
    os.system(f'{SfM_DIR}/bin/export_gps {src} --output={src}/{txt}') # lat,lon,alt,a
    SfM_cmd(src, f'export_geocoords --image-positions --proj="{LLA}" --output={tsv}')
    geo = sort_row(f'{src}/{tsv}', 1); rename_rec(src) # recover topocentric

    with open(f'{src}/{txt}') as f: gps = f.readlines()
    data = DataSet(src); ref = data.load_reference(); dif = []
    for u,v in zip(geo[1:], gps[1:]): # skip 1st-row
        u,v = u.split(), v.split(); assert u[0]==v[0]; im = u[0]
        u,v = np.float64(u[1:4])[[1,0,2]], np.float64(v[1:4])
        o = list(data.load_exif(im)['gps'].values())[:3] # lat,lon,alt
        ou = ref.to_topocentric(*u)-np.array(ref.to_topocentric(*o))
        ov = ref.to_topocentric(*v)-np.array(ref.to_topocentric(*o))
        dif += [f'{im} lla={v}\tdif={ov.tolist()}\n']
        #print(u-o, v-o, abs(u-v)); print(ou, ov)
    with open(f'{src}/{tsv[:-4]}.dif.txt','w') as f: f.writelines(dif)


# Ref: https://github.com/OpenDroneMap/ODM/blob/master/stages/run_opensfm.py
def rename_rec(src): # for odm: rename|recover topocentric.json
    Auth(src); rec = src+'/reconstruction.json'
    tpc = rec[:-4]+'topocentric.json'; tmp = rec+'='
    if os.path.isfile(tpc): os.rename(rec, tmp); os.rename(tpc, rec)
    elif os.path.isfile(tmp): os.rename(rec, tpc); os.rename(tmp, rec)


IDX = lambda x,y: np.where(x==np.asarray(y)[:,None])[-1]
##########################################################################################
# Ref: https://opensfm.org/docs/using.html#ground-control-points
# gz->fid->track2->tid2->reconstruction2->tid2->xyz2->lla2->gcp
def SfM_gcp_gz(GPS, RTK='', thd=1, dst=0):
    from opensfm.dataset import DataSet
    if not os.path.isdir(RTK): RTK = GPS
    rec = RTK+'/reconstruction.topocentric.json'
    if not os.path.isfile(rec): rec = rec[:-16]+'json'
    with open(rec) as f: R = json.load(f)[0]['points']
    R = {int(k):v['coordinates'] for k,v in R.items()}
    T = SfM_parse_csv(RTK) # {im2: {tid2,fid2,xys2,rgb2}}
    ref = DataSet(RTK).load_reference(); gcp = [LLA]

    mt_dir = GPS+'/matches'; npz = {}
    if not os.path.isdir(mt_dir): mt_dir += '_gcp'
    for gz in os.scandir(mt_dir): # parse pkl.gz
        im1 = gz.name[:-15] # *_matches.pkl.gz
        with gzip.open(gz.path, 'rb') as f: gz = pickle.load(f)
        for im2, fid in gz.items(): # (im1,im2):[fid1,fid2]
            if len(fid)<7: INFO(f'skip: {im1} {im2}'); continue # filter
            _, uv1 = SfM_feat_uv(im1, src=GPS, idx=fid[:,0]) # norm->pixel
            _, uv2 = SfM_feat_uv(im2, src=RTK, idx=fid[:,1]) # norm->pixel
            _, idx = filter_match(uv1, uv2, thd=thd/2); fid = fid[idx]

            idx = IDX(T[im2]['fid'], fid[:,1]) # filter: track+fid2->tid2
            tid2, fid2, xys2, rgb2 = [np.array(T[im2][k])[idx] for k in T[im2]]
            idx = IDX(tid2, list(R)) # filter: reconstruction+tid2->tid2
            tid2, fid2, xys2, rgb2 = tid2[idx], fid2[idx], xys2[idx], rgb2[idx]
            xyz2 = np.array([R[i] for i in tid2]) # reconstruction->xyz
            lla2 = np.array([ref.to_lla(*i) for i in xyz2]) # xyz->lla
            num = dict(org=len(uv1), ransac=len(fid), track=len(lla2))
            INFO(f'{im1} {im2} gz_gcp: {num}')

            idx = IDX(fid[:,1], fid2); fid = fid[idx]
            _, uv1 = SfM_feat_uv(im1, src=GPS, idx=fid[:,0]) # fid1
            _, uv2 = SfM_feat_uv(im2, src=RTK, pt=xys2) # norm->pixel
            for (lat,lon,alt),uv in zip(lla2,uv1):
                gcp += [(3*'%.15f '+2*'%4s '+'%s')%(lon,lat,alt,*uv,im1)]
            npz[f'{im1}-{im2}'] = np.hstack([uv1, uv2])
    if npz: np.savez(GPS+'/gcp_gz.npz', **npz)
    with open(GPS+'/gcp_list.txt','w') as f:
        gcp = dedup_gcp(gcp); f.write('\n'.join(gcp))
    gcp = filter_gcp(GPS, RTK, thd=thd) # filter_reproject
    INFO(f'Created {len(gcp)-1} GCPs: {GPS}/gcp_list.txt\n')
    cv2.destroyAllWindows(); return gcp # list


def dedup_gcp(gcp, eps=0.01):
    from opensfm.geo import ecef_from_lla
    if type(gcp)==str and os.path.isdir(gcp):
        with open(gcp+'/gcp_list.txt') as f:
            gcp = f.readlines()
    elif type(gcp)==str and os.path.isfile(gcp):
        with open(gcp) as f: gcp = f.readlines()
    assert type(gcp)==list; res = {}
    for i in gcp[1:]: # skip 1st-row
        lon, lat, alt, x, y, im = i.split()
        lla = np.float64([lat,lon,alt])
        k = f'{x}:{y}:{im}'
        if k in res: res[k] += [lla]
        else: res[k] = [lla]
    gcp = [gcp[0].strip()] # clear gcp
    for k,v in res.items():
        m = np.mean(v, axis=0)
        v = [ecef_from_lla(*i) for i in v]
        v -= np.asarray(ecef_from_lla(*m))
        v = np.linalg.norm(v, axis=1); #print(v)
        if np.all(v<eps): # meters
            m = (m[1], m[0], m[2], *k.split(':'))
            gcp += [(3*'%.15f '+2*'%4s '+'%s')%m]
    return gcp # list: without '\n'


########################################################
def filter_gcp(GPS, RTK, thd=2):
    from odm_filter import Camera
    from opensfm.dataset import DataSet
    K = Camera(GPS+'/camera_models.json').K()
    ref = DataSet(RTK).load_reference(); res = {}
    with open(GPS+'/gcp_list.txt') as f: gcp = f.readlines()
    for v in gcp[1:]: # skip 1st-row
        v = v.split(); im = v[-1]
        v = np.float64(v[:5]+[np.inf]*2) # lon,lat,alt
        v[:3] = ref.to_topocentric(*v[[1,0,2]]) # lat,lon,alt
        if im not in res: res[im] = [v]
        else: res[im].append(v)

    for k,v in res.items():
        v = res[k] = np.float64(v)
        if len(v)<5: continue # skip
        pt, uv = v[:,:3].copy(), v[:,3:5] # copy()->new mem-block
        _, Rvec, Tvec, Ins  = cv2.solvePnPRansac(pt, uv, K, None)
        # cv2.projectPoints: pt must be continuous mem-block
        xy, Jacob = cv2.projectPoints(pt, Rvec, Tvec, K, None)
        #RMat = cv2.Rodrigues(Rvec) # RotVecor<->RotMatrix
        err = v[:,5] = np.linalg.norm(xy.squeeze()-uv, axis=1)

        his = np.histogram(err, bins=[*range(11),np.inf])[0]
        for c in range(len(his)-1,-1,-1): # len(v)=sum(his)
            if sum(his[c:])>=len(v)*0.2: break
        idx = np.where(err<=c)[0]
        if len(idx)<7: continue # skip
        _, Rvec, Tvec  = cv2.solvePnP(pt[idx], uv[idx], K, None)
        xy, Jacob = cv2.projectPoints(pt, Rvec, Tvec, K, None)
        v[:,6] = np.linalg.norm(xy.squeeze()-uv, axis=1) # err2

    err = np.vstack(list(res.values()))[:,5:]
    for i,v in enumerate(err):
        v = np.mean(v) if max(v)<np.inf else min(v)
        if v<thd: gcp[i+1] = '' # skip 1st-row
    with open(GPS+'/gcp_list.txt','w') as f: f.writelines(gcp)
    return [i.strip() for i in gcp if i] # list: without '\n'


########################################################
def SfM_GCP(GPS, RTK, thd=1, mix=0):
    out = f'{GPS}/gcp_list.txt'
    if not os.path.isdir(f'{GPS}/features'): # extract
        SfM_exif_dop(GPS); SfM_cmd(GPS, 'detect_features')
    if os.path.isdir(f'{GPS}/matches_gcp'):
        if os.path.isdir(f'{GPS}/matches'): # backup
            os.rename(f'{GPS}/matches', f'{GPS}/matches=')
        os.rename(f'{GPS}/matches_gcp', f'{GPS}/matches')
    if not os.path.isfile(out):
        if not os.path.isdir(f'{GPS}/matches'):
            SfM_match(GPS, RTK, mix) # match (GPS,RTK)
        gcp = SfM_gcp_gz(GPS, RTK, thd=thd, dst=0)
        os.rename(f'{GPS}/matches', f'{GPS}/matches_gcp')
    if os.path.isdir(f'{GPS}/matches='): # recover
        if os.path.isdir(f'{GPS}/matches'):
            os.rename(f'{GPS}/matches', f'{GPS}/matches_gcp')
        os.rename(f'{GPS}/matches=', f'{GPS}/matches')


SfM_CFG = dict(use_exif_size=True, use_altitude_tag=True, feature_type='SIFT',
    sift_peak_threshold=0.066, feature_min_frames=10000, feature_process_size=0.5,
    matcher_type='FLANN', flann_algorithm='KDTREE', triangulation_type='ROBUST',
    matching_gps_neighbors=8, matching_gps_distance=0, matching_graph_rounds=50,
    align_orientation_prior='vertical', bundle_use_gcp=False, bundle_use_gps=True,
    align_method='auto', retriangulation_ratio=2, processes=max(1,os.cpu_count()//6),
    bundle_outlier_filtering_type='AUTO', optimize_camera_parameters=True) # odm'''
SYS = f'{os.cpu_count()} *'+os.popen('lscpu|grep name|cut -f2 -d:').readline()[9:-1]
##########################################################################################
# Ref: https://github.com/OpenDroneMap/ODM/blob/master/opendm/osfm.py
# Ref: https://github.com/OpenDroneMap/ODM/blob/master/opendm/config.py
def ODM_cmd(src, cfg, sfm=SfM_CFG, gpu=''):
    proj = f'--project-path=/root {os.path.basename(src)}'
    root = f'{os.path.dirname(os.path.abspath(src))}:/root'
    for k,v in sfm.items(): # config from sfm
        if k=='processes': cfg['max-concurrency'] = v
        elif k=='matcher_type': cfg['matcher-type'] = v.lower()
        elif k=='feature_type': cfg['feature-type'] = v.lower()
        elif k=='feature_min_frames': cfg['min-num-features'] = v
        elif k=='feature_process_size': cfg['resize-to'] = feat_size(src, v)
    for k,v in cfg.items(): # config for odm
        if k=='resize-to': cfg[k] = feat_size(src, v)
        if k.split('-')[-1] in ('type','quality'): cfg[k] = v.lower()
        if cfg[k]=='orb': cfg['matcher-type']='bruteforce'
    cfg = ' '.join(['--'+(f'{k}={v}' if v!='' else k) for k,v in cfg.items()])
    gpu = f'--gpus={gpu} opendronemap/odm:gpu' if gpu!='' else 'opendronemap/odm'
    cmd = f'docker run -ti --rm -v={root} {gpu} {proj} {cfg} --time'
    INFO('\n'+cmd); os.system(cmd)


def ODM_img_lla2(GPS, RTK, dst, mesh=0, dop=1):
    from odm_filter import filter_reconstruct; INFO(SYS)
    gps, rtk = os.path.basename(GPS), os.path.basename(RTK)
    tmp = f'{dst}/odm-RTK-{rtk}'; odm_cfg = {'end-with':'opensfm'}
    merge_dir(RTK, tmp+'/images'); merge_dir(RTK, tmp+'/opensfm/images')
    RTK = tmp; ODM_cmd(RTK, odm_cfg); filter_reconstruct(RTK)

    GCP = f'{dst}/odm-GCP-{rtk}-{gps}'; merge_dir(GPS, GCP+'/images')
    tmp = f'{dst}/sfm-GPS-{rtk}-{gps}'; merge_dir(GPS, tmp+'/images')
    GPS = tmp; SfM_config(GPS, SfM_CFG); SfM_GCP(GPS, RTK+'/opensfm')

    odm_cfg['gcp'] = f'/root/{os.path.basename(GPS)}/gcp_list.txt'
    #merge_dir(GPS+'/matches', GCP+'/opensfm/matches')
    #merge_dir(GPS+'/features', GCP+'/opensfm/features')
    ODM_cmd(GCP, odm_cfg); export_image_gps(GCP+'/opensfm')
    INFO('ALL DONE!')


def ODM_img_lla3(GPS, RTK, dst, mesh=0, dop=1):
    from odm_filter import filter_reconstruct; INFO(SYS)
    gps, rtk = os.path.basename(GPS), os.path.basename(RTK)
    tmp = f'{dst}/odm-RTK-{rtk}'; odm_cfg = {'end-with':'opensfm'}
    merge_dir(RTK, tmp+'/images'); merge_dir(RTK, tmp+'/opensfm/images')
    RTK = tmp; ODM_cmd(RTK, odm_cfg); filter_reconstruct(RTK)

    GCP = f'{dst}/odm-GCP-{rtk}-{gps}'; merge_dir(GPS, GCP+'/images')
    tmp = f'{dst}/odm-GPS-{rtk}-{gps}'; merge_dir(GPS, tmp+'/images')
    merge_dir(GPS, tmp+'/opensfm/images'); GPS = tmp; ODM_cmd(GPS, odm_cfg)
    Auth(GPS); os.rename(GPS+'/opensfm/matches', GPS+'/opensfm/matches=')
    SfM_GCP(GPS+'/opensfm', RTK+'/opensfm')

    odm_cfg['gcp'] = f'/root/{os.path.basename(GPS)}/opensfm/gcp_list.txt'
    merge_dir(GPS+'/opensfm/matches', GCP+'/opensfm/matches')
    merge_dir(GPS+'/opensfm/features', GCP+'/opensfm/features')
    ODM_cmd(GCP, odm_cfg); export_image_gps(GCP+'/opensfm')
    INFO('ALL DONE!')


from datetime import datetime as TT
APD = lambda v,t,c='': v[:-1]+f'\t-> {c}{t.total_seconds()}s\n'
IT = lambda v: TT.strptime(v[:23], '%Y-%m-%d %H:%M:%S,%f') # INFO_time
AT = lambda v: TT.strptime(v[-30:-5], '%a %b %d %H:%M:%S %Y') # asctime
##########################################################################################
def parse_log(src):
    with open(src, encoding='utf-8') as f: x = f.readlines()
    idx = [i for i,v in enumerate(x) if 'app finished' in v or \
        'opensfm/bin/opensfm' in v.lower()]+[len(x)]; print(x[0])
    for i in range(len(idx)-1):
        a, b = idx[i], idx[i+1]
        if 'detect_features' in x[a]:
            s = [v.split() for v in x[a:b] if ': Found' in v]
            s = np.float64([(v[4],v[7][:-1]) for v in s]).sum(axis=0)
            print(a, x[a][:-1]+'\t-> Feature = %d\tT = %.3fs'%(*s,))
        elif 'match_features' in x[a]:
            #s = [v for v in x[a:b] for k in KEY if k in v]
            s = [v for v in x[a:b] if 'Matched' in v or 'Created' in v]
            if len(s)>1: s[1] = APD(s[1], IT(s[1])-IT(s[0]))
            print(a, x[a], *s)
        elif 'create_tracks' in x[a]:
            v = [v for v in x[a:b] if 'Good' in v][0]
            print(a, *x[a:a+2], APD(v, IT(v)-IT(x[a+1])))
        elif 'reconstruct ' in x[a]:
            v = [v for v in x[a:b] if 'Reconstruction' in v][0]
            print(a, *x[a:a+2], APD(v, IT(v)-IT(x[a+1])))
        elif 'export_geocoords --reconstruction' in x[a]:
            s = [s for s in x[a:b] if 'Undistorting' in s]
            print(a+4, APD(s[0], IT(s[-1])-IT(s[1])))
        elif 'app finished' in x[a] and 'v' in dir() and 'Reconstruction' in v:
            print(a, APD(x[a], AT(x[a])-IT(v), 'Undistort = '))
        elif 'extract_metadata' in x[a]:
            x[a-2] = APD(x[a-2], IT(x[a])-IT(x[a-3])); print(a, *x[a-3:a+1])
        elif 'export_geocoords --image-positions' in x[a]:
            t = (IT(x[a])-IT(x[0])).total_seconds()/60
            print(a, x[a][:-1]+'\t-> Export = %.1fs = %.3f min\n'%(t,t/60))
        elif 'export_openmvs' in x[a]:
            v = [v for v in x[a:b] if 'CPU:' in v][0]; print(a, x[a][:-1])
        elif 'app finished' in x[a] and 'v' in dir() and 'CPU:' in v:
            s = x[a].split(' '); s[-3] = v[:8]; s = ' '.join(s)
            print(a, APD(x[a], AT(x[a])-AT(s), '[mvs_texturing]: '))
    v = [v for v in x[a:b] if 'DONE!' in v][0]
    t = (IT(v)-IT(x[0])).total_seconds()
    print(v[:-1]+'\t-> Total = %.1fs = %.3f min\n'%(t,t/60))


##########################################################################################
def parse_args():
    parser = argparse.ArgumentParser() # RTK-ODM-GPS
    SP = lambda x: x[:-1] if x[-1] in ('/','\\') else x
    parser.add_argument('--log', default=None, type=str, help='log file name')
    parser.add_argument('--dst', default=None, type=str, help='results folder')
    parser.add_argument('--gps', default=None, type=str, help='GPS images folder')
    parser.add_argument('--rtk', default=None, type=str, help='RTK images folder')
    parser.add_argument('--min', default=4000, type=int, help='min feature number')
    parser.add_argument('--mod', default='odm', type=str, help='method of matching')
    parser.add_argument('--dop', default=0.2, type=float, help='gps-accuracy for POS')
    parser.add_argument('--cpu', default=os.cpu_count()//6, type=int, help='concurrency')
    parser.add_argument('--mesh', default=0, type=int, help='odm_texturing_25d')
    parser.add_argument('--type', default='sift', type=str, help='feature type')
    parser.add_argument('--quality', default=0.5, type=float, help='feature quality')
    args = parser.parse_args(); os.makedirs(args.dst, exist_ok=True); # print(args)
    args.gps, args.rtk, args.dst = [SP(i) for i in (args.gps, args.rtk, args.dst)]
    if args.log: # useless
        args.log = os.path.join(args.dst, args.log)
        sys.stderr = sys.stdout = open(args.log, 'a+')
    SfM_CFG['processes'] = min(os.cpu_count(), max(1, args.cpu))
    SfM_CFG['feature_process_size'] = args.quality
    SfM_CFG['feature_type'] = args.type.upper()
    SfM_CFG['feature_min_frames'] = args.min; return args


# python3 odm_sfm.py --gps=GPS --rtk=RTK --dst=xxx > xxx.log 2>&1
##########################################################################################
if __name__ == '__main__':
    x = parse_args()
    if x.mod=='odm': ODM_img_lla3(x.gps, x.rtk, x.dst, x.mesh, x.dop)
    elif x.mod=='sfm': ODM_img_lla2(x.gps, x.rtk, x.dst, x.mesh, x.dop)
    else: parse_log(x.log)

