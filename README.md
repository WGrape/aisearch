# aisearch
AI搜索项目

## 前端部署

```bash
cd web && npm install && npm run build

# 上述命令如果启动失败，则可以在当前窗口执行本地启动命令。
npm run dev
```

前端部署成功后，访问 http://127.0.0.1:3000/ 即可。

## 后端部署

```bash
python src/main.py --dir=~/github/aisearch --env=test
```

后端部署成功后，访问 http://127.0.0.1:8100 即可。
