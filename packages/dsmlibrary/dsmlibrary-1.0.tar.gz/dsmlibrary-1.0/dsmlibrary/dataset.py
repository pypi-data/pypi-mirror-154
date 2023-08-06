import os
import requests
from tqdm.auto import tqdm
from tqdm.utils import CallbackIOWrapper

from .base import discovery_api, Base
class DatasetManager(Base):

    def upload_file(self, directory=None, file_path=None, description=""):
        if type(file_path) != str :
            raise Exception(f"file_path expect `str` but got {type(file_path)}, or please input `file_path='<path>'`")
        elif not os.path.exists(file_path):
            raise Exception(f"file {os.path.abspath(file_path)} not found")
        if directory == None:
             raise Exception("please input directory, like `directory=<id>`")
        _res = requests.get(f"{discovery_api}/directory/{directory}",  headers=self._jwt_header)
        if _res.status_code == 404:
            raise Exception(f"directory {directory} not found or your dose not has permission to access directory")
        f_name = os.path.basename(file_path)
        _res = requests.post(f"{discovery_api}/file/", headers=self._jwt_header,
                             data={
                                 'name': f_name,
                                 'description': f_name,
                                 'directory': int(directory),
                                 'size': os.path.getsize(file_path),
                                 'is_use': True
                             }
                )
        if not _res.status_code in [200, 201]:
            txt = ""
            if _res.status_code < 500:
                txt = _res.json()
            raise Exception(f"{_res.status_code}, {txt}")
        data = _res.json()
        file_size = os.stat(file_path).st_size
        with open(file_path, 'rb') as f:
            with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
                wrapped_file = CallbackIOWrapper(t.update, f, "read")
                _res = requests.put(data['url'], data=wrapped_file)
        if _res.status_code == 200:
            _uploaded = True
        else:
            print(_res.content.decode())
            raise Exception("Some thing wrong with datastore")
        data.update({
            'uploaded': _uploaded 
        })
        return data
    
    def download_file(self, file_id=None):
        if file_id == None:
             raise Exception("please input file_id")
        _res = requests.get(f"{discovery_api}/file/{file_id}/",  headers=self._jwt_header)
        if _res.status_code != 200:
            raise Exception(f"File response code {_res}")
        meta = _res.json()
        _res = requests.get(f"{discovery_api}/file/{file_id}/download/",  headers=self._jwt_header)
        if _res.status_code != 200:
            raise Exception("some thing wrong in datastore")
        
        _res = requests.get(_res.json()['url'])
        f_path = os.path.join(self._tmp_path, meta['name'])
        
        total_size_in_bytes= int(_res.headers.get('content-length', 0))
        print(total_size_in_bytes)
        block_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        
        with open(f_path, 'wb') as f:
            for data in _res.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        
        meta.update({
            'download_sucess': os.path.exists(f_path),
            'f_path': f_path
        })
        return meta