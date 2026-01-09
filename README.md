# Railway SOCKS5 Proxy

A SOCKS5 proxy implementation using Dante server deployed on Railway.app.

## Quick Start

### Deployment

1. Create a new Railway project
2. Connect your GitHub repository
3. Railway will automatically build and deploy from this repo
4. Set the `PROXY_PASSWORD` environment variable in Railway Settings

### Configuration

The proxy will automatically:
- Listen on port 1080 internally
- Be accessible via Railway's public TCP endpoint
- Use the password from `PROXY_PASSWORD` environment variable

## Usage

### Get Your Railway App URL

1. Go to your Railway project dashboard
2. Click on your service
3. Find the "Public URL" - it will be in format: `tcp://your-app.up.railway.app:PORT`
4. Note the PORT number (Railway assigns a public port)

### Testing with curl

```bash
# Test SOCKS5 connectivity
curl --socks5-hostname your-app.up.railway.app:PORT \
  -U proxyuser:YOUR_PASSWORD \
  https://checkip.amazonaws.com
```

## Security

- Change password via `PROXY_PASSWORD` environment variable
- Never commit passwords to repository
- Default username is `proxyuser`

### Environment Variables

Set in Railway Settings:
```
PROXY_PASSWORD=your_secure_password
```
