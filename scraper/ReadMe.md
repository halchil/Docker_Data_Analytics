② スクレイパー実行（1回試す）

```
cd ../scraper
docker build -t news-scraper .
docker run --network=db_mynet --env-file ../shared/.env news-scraper
```

※ cron で定期実行したい場合はホスト側で cron ジョブに追加するか、別途 scheduler コンテナを組むのが理想です。
③ Streamlit ダッシュボード起動
