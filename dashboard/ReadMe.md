
```
docker build -t news-dashboard .
[+] Building 27.5s (7/9)                                                       docker:default
 => [internal] load build definition from Dockerfile                                     0.1s
 => => transferring dockerfile: 232B                                                     0.0s
 => [internal] load metadata for docker.io/library/python:3.10-slim                      9.3s
 => [internal] load .dockerignore                                                        0.1s
 => => transferring context: 2B                                                          0.0s
 => [1/5] FROM docker.io/library/python:3.10-slim@sha256:65c843653048a3ba22c8d5083a022f  7.3s
 => => resolve docker.io/library/python:3.10-slim@sha256:65c843653048a3ba22c8d5083a022f  0.1s
 => => sha256:c96cb1c893456d3b64ac93cbebba12262429b64eca53584506f09ae22 3.51MB / 3.51MB  1.6s
 => => sha256:fcc78f5313aaeb803973d1c97a39d7ce576e349a2cc44fc655bf99c 15.65MB / 15.65MB  5.4s
 => => sha256:65c843653048a3ba22c8d5083a022f44aef774974f0f7f70cbf8cee4e 9.13kB / 9.13kB  0.0s
 ```

 接続
 http://192.168.56.129:8501/


 ## エラートレース

ブラウザ接続したところ、以下のエラーが発生。
 ```
psycopg2.errors.UndefinedTable: relation "headlines" does not exist LINE 1: SELECT title FROM headlines ORDER BY id DESC LIMIT 10; ^
Traceback:
File "/app/app.py", line 13, in <module>
    cur.execute("SELECT title FROM headlines ORDER BY id DESC LIMIT 10;")

 ```
 このエラーの原因は、PostgreSQLに headlines という名前のテーブルが存在しないことである。
 それは作成されるのかどうか疑問
 これは、scraper側で作成される

 つまり、接続確認のみの目的であれば、達成されているのでOK.