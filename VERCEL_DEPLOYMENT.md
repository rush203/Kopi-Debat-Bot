# Vercel Deployment Guide for Kopi Debate Bot

## Quick Deployment Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from project directory**:
   ```bash
   vercel
   ```

4. **Set Environment Variables**:
   - Go to your Vercel dashboard
   - Navigate to your project
   - Go to Settings → Environment Variables
   - Add: `OPENAI_API_KEY` with your OpenAI API key

## File Structure for Vercel

The following files are essential for Vercel deployment:

- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function entry point
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification
- `.vercelignore` - Files to exclude from deployment

## Testing Endpoints

After deployment, test these endpoints:

1. **Health Check**: `GET /api/v1/health`
2. **Simple Test**: `GET /api/v1/test`
3. **Debate Endpoint**: `POST /api/v1/debate`

## Example API Call

```bash
curl -X POST "https://your-app.vercel.app/api/v1/debate" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": null,
    "message": "Sun rises from west, take stance sun rise from west."
  }'
```

## Troubleshooting

1. **404 Errors**: Check that `vercel.json` routes are correct
2. **500 Errors**: Check environment variables are set
3. **Import Errors**: Ensure `PYTHONPATH` is set correctly in `vercel.json`

## Environment Variables Required

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_BASE_URL`: Default: "https://openrouter.ai/api/v1"
- `OPENAI_MODEL`: Default: "meta-llama/llama-3.1-8b-instruct"
