# Railway SOCKS5 Proxy (US)

Деплой: Railway → New Project → GitHub repo.

Доступ: socks5://your-app.railway.app:<tcp-port>

Логи: Railway dashboard.


## Security Note

Password для прокси задаётся через Railway Environment Variables (Settings → Variables):

```bash
PROXY_PASSWORD=your_secure_password
```

НЕ коммитьте пароли в репозиторий!
