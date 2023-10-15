# 运行方式

## 调试爬虫
``` shell
python -m crawler --debug --province xxx --city xxx
```

## 运行爬虫
``` shell
python -m crawler --all --workers ?? \
    --metadata-output OUTDIR
```

## 写入数据库
``` shell
python -m db-writer --db-host DB_ADDR \
    --db-port DB_PORT \
    --db-user DB_USER \
    --db-pswd DB_PSWD \
    --database DATABASE_NAME \
    --table TABLE_NAME \
    --metadata-path METADATA_SAVING_PATH
```

# 注意事项

1. 运行爬虫需要使用Python 3.6及以下的版本,
参考[CSDN: SSL: SSLV3_ALERT_HANDSHAKE_FAILURE](https://blog.csdn.net/qq_37435462/article/details/121564961).

2. 如果要在VS Code中使用Black Formatter, 可以临时切换到Python 3.7或以上的版本.
