# AI Study Assistant - Backend API

Flask API that processes study materials using Google Gemini AI.

## Quick Deploy to Railway
1. Fork this repo
2. Connect to Railway.app  
3. Set GOOGLE_API_KEY environment variable
4. Deploy!

## API Endpoints
- `GET /` - Health check
- `POST /process` - Process text and generate summary + quiz

## Environment Variables
- `GOOGLE_API_KEY` - Required
- `ENVIRONMENT` - Set to 'production' for prod
- `FRONTEND_URL` - Your frontend domain