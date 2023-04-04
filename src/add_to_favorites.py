# -*- coding: utf-8 -*-
import os
import time

import requests

with open(r"D:\Python310\wallhaven_collection\竖屏\url.txt", "r") as f:
    lines = f.readlines()
    num = len(lines)

pic_id = []
coll = 1482969

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"

}
cookies = {"cookie":"remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Iko1RmQ5aGFJNzdrbkwyRDV5TmtxTkE9PSIsInZhbHVlIjoiVm12bFcyRDRHVHNYZkFST0hcL2ZZVlZQS0pKVzdkb0pHS1VnMVVGNUtKaGFyMXM3QnNla0xnWjBseHZFeXN4ZzdJaDBBYWZLV2l2VUs5ODlxMnRCazJtandrbHFWZTB0b1pFSHd5XC9GV21CeDF3VktIQUZEY20wR0NodHJEN2VQeEg2WlFZTDlXSEsrVTdMbDFObjhiaFRERTFEZ2pLU0JkMmcwWDh5TE1rYytHUjZKWUl0WnVmbDNDaGFSSE45eVoiLCJtYWMiOiJjOTk5ZWNlMGFkMjM0N2FlOTU3YzVkMTM4OWE2YWY1OWU3MjRmMjU0OGNjNjliMzMxYjVkNWIyMzZmZDA3MGYyIn0%3D; XSRF-TOKEN=eyJpdiI6ImZRdmVlNUNTSkczSG9xNmU0akZoZ1E9PSIsInZhbHVlIjoiVHF4UWRUUnJBNTBpV1hTRkh0MmxtXC9Bcm9lUVFYYVBuOHM0OGRXcWNOZzlwWnJ0ZjZ4UnhQNVA2RGxrTHdOTmoiLCJtYWMiOiI3NWZjODE1OGU2NTcyOWVkZmQ5MjQ0ODMxMDE3OWE3ZGQ4NTQxOTg1YmZmNTIxNmI3ZDU1MDg5MGRlMDIyMTkxIn0%3D; wallhaven_session=eyJpdiI6InlDWlgwUEhWeEhPb3NLajRZaUdpenc9PSIsInZhbHVlIjoiZ0tEd1pJdlp2XC82OEhJeFk5R2NPS3NTeW5BaWdsRUl5WUhTWDBxbjhPMDhQc1pYVThqUG82czEzQUtUYlJRdEYiLCJtYWMiOiJmOTk2MjMwZTU4NWJkOTM1YjdmN2U2ZTk2MWQwZDJhMmUwYjgwYjU5YTE3NjljODQ3MmM5NmE1ODVhMGRiNmIzIn0%3D"}
for i,line in enumerate(lines):
    url = line.strip()
    id = url.split("/")[-1].split(".")[0].replace("wallhaven-", "")
    add_url = f"https://wallhaven.cc/favorites/add?wallHashid={id}&collectionId={coll}&_token=9E81olkpj6zX5vBaRUQTPcsVIKsksCOZ82llYBF5"
    print(f"已完成{i+1}/{num}")
    print(add_url)
    res = requests.post(add_url,headers=headers,cookies=cookies,)
    pic_id.append(add_url)
    time.sleep(3)


