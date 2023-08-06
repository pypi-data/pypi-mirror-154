import requests
import dask.dataframe as dd
from .base import discovery_api, bucket_name, minio_url, Base

def append_slash(txt):
    if txt[-1] != '/':
        txt += '/'
    return txt

class DataNode(Base):
    def write(self, ddf=None, directory=None, name=None, description="", profiling=False):
        
        if type(ddf) != dd.DataFrame:
            raise Exception(f"Expect {dd.DataFrame} but got {type(ddf)}")
        if name == None:
            raise Exception("Please input data name")
        if description=="":
            description = f"data {name}"
        
        _res = requests.post(f'{discovery_api}/file/', headers=self._jwt_header,
                                json={
                                    "name": f'{name}.parquet',
                                    "description": description,
                                    "directory": directory,
                                    "size": 0
                                }
                            )
        if _res.status_code != 201:
            raise Exception(f"can not create directory in discovery {_res.json()}")
        meta = _res.json()
        _res = requests.patch(f"{discovery_api}/file/{meta['id']}/", headers=self._jwt_header,
                                json={
                                    "name": f"{meta['id']}-{name}.parquet",
                                }
                             )
        meta = _res.json()
        ddf.to_parquet(f"s3://{bucket_name}/{meta['key']}",
               storage_options={
                   'key': self._minio_access,
                   'secret': self._minio_secret,
                   'client_kwargs':{
                       'endpoint_url': minio_url
                   }
               }
        )
        # create profiling & data dict
        if profiling:
            requests.get(f"{discovery_api}/file/{meta['id']}/createDatadict/")
            requests.get(f"{discovery_api}/file/{meta['id']}/createProfileling/")
        
        size = sum([elm.size for elm in self.client.list_objects(bucket_name, prefix=append_slash(meta['key'])) if not elm.is_dir])
        _res = requests.patch(f"{discovery_api}/file/{meta['id']}/", headers=self._jwt_header,
                        json={
                            "size": size,
                        }
                     )
        return {
            'sucess': True,
            'file_id': meta['id'],
            'path': meta['key']
        }
    
    def read(self, file_id=None):
        _res = requests.get(f"{discovery_api}/file/{file_id}/")
        meta = _res.json()
        return dd.read_parquet(f"s3://{bucket_name}/{meta['key']}", 
               storage_options={
                   'key': self._minio_access,
                   'secret': self._minio_secret,
                   'client_kwargs':{
                       'endpoint_url': minio_url
                   }
       })