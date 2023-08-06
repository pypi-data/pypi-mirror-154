import os
import requests
import time

from minio import Minio

defind_clear_output = False
try:
    from IPython.display import clear_output
    defind_clear_output = True
except:
    pass

discovery = "https://discovery.data.storemesh.com"

base_discovery_api = "https://api.discovery.data.storemesh.com"
# base_discovery_api = "http://192.168.24.207:8000"
discovery_api = f"{base_discovery_api}/api/v2"

base_minio_url="s3.minio.data.storemesh.com"
# base_minio_url="192.168.24.207:9000"

minio_url=f"https://{base_minio_url}"
bucket_name = 'dataplatform'

class Base:
    def __init__(self, token=None):
        """Init DSM Dataset Manager

        Args:
            jwt_token (str): JWT token from IaM.
        """
        if token is None:
            print(f"Please get token from {discovery}")
            token = input("Your Token : ")
            if defind_clear_output:
                time.sleep(2)
                clear_output()
        if token in [None, '']:
            raise Exception('Please enter your key from dsmOauth')
        self._jwt_header = {
            'Authorization': f'Bearer {token}'
        }
        self.token = token
        self._tmp_path = 'dsm.tmp'
        os.makedirs(self._tmp_path, exist_ok=True)
        _res = requests.get(f"{base_discovery_api}/api/minio/minio-user/me/", headers=self._jwt_header)
        if _res.status_code != 200:
            raise Exception("Can not get minio user")
        data = _res.json()
        self._minio_access = data['access']
        self._minio_secret = data['secret']
        
        self.client = Minio(
            base_minio_url,
            access_key=self._minio_access,
            secret_key=self._minio_secret,
            secure=True
        )