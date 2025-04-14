

```
[実行コマンド]
docker compose -f docker-compose.yaml up -d

[結果]
WARN[0000] /home/mainte/Docker_Data_Analytics/db/docker-compose.yaml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
[+] Running 8/15
 ⠦ db [⣷⣿⣿⣿⣿⣿⣿⣿⡀⣿⠀⠀⠀⠀] Pulling                                                          25.6s 
   ⠦ 8a628cdd7ccc Downloading  26.02MB/28.23MB                                          21.7s 
   ✔ ada8823e5b6f Download complete                                                      1.0s 
   ✔ fc4323444c9b Download complete                                                      5.3s 
   ✔ 2d9287dc0c9b Download complete                     
```

ユーザ名とパスワードは、一旦user,password である。
これらで入れるか確認

コンテナに入る

docker exec -it my_postgres /bin/bash
root@3fdadd82ab60:/# 


ユーザでDBに接続
psql -U user -d mydb
psql (13.20 (Debian 13.20-1.pgdg120+1))
Type "help" for help.

mydb=# 


\l   -- データベース一覧
\dt  -- テーブル一覧（データベースに入ってから）
\q   -- psqlからの終了

任意のDBに入る方法（接続し直す）
\c データベース名

現在接続しているデータベース名を確認する方法
\conninfo

方法2（SQLっぽく確認）:

SELECT current_database();

まだテーブルがない
```
\c mydb
You are now connected to database "mydb" as user "user".
mydb=# \dt
Did not find any relations.

```

# 試しにテストデータを格納する流れ

テスト用データベース作成（例：testdb）

CREATE DATABASE testdb;

② testdb に接続

\c testdb

③ テーブル作成（例：users）

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL
);

④ データ挿入

INSERT INTO users (name, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com');

⑤ 確認

SELECT * FROM users;