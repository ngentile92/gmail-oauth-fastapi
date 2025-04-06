# Gmail OAuth Integration with FastAPI

A FastAPI application that demonstrates Gmail API integration using OAuth 2.0 authentication. This application allows users to:
- Authenticate with their Gmail account
- View unread emails from their inbox
- Access full email content and thread history

## Features

- OAuth 2.0 authentication with Gmail
- Retrieval of unread emails with full content
- Thread context for email conversations
- HTML content parsing and formatting
- Secure credential management
- Public access support through ngrok

## Prerequisites

- Python 3.8+
- Google Cloud Console project with Gmail API enabled
- OAuth 2.0 credentials configured
- ngrok account (for public access)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd gmail-oauth-fastapi
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with the following variables:
```
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
REDIRECT_URI=your_redirect_uri
```

## Configuration

1. Set up Google Cloud Console:
   - Create a new project
   - Enable Gmail API
   - Configure OAuth consent screen
   - Create OAuth 2.0 credentials
   - Add authorized redirect URIs

2. Configure ngrok (for public access):
   - Install ngrok
   - Set up authentication token
   - Start tunnel: `ngrok http 8000`
   - Update redirect URIs in Google Console with ngrok URL

## Usage

1. Start the server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. Access the application:
   - Local: `http://localhost:8000`
   - Public: `https://your-ngrok-url.ngrok-free.app`

3. Endpoints:
   - `/login/{user_id}`: Initiate OAuth flow
   - `/oauth/callback`: Handle OAuth callback
   - `/unread_emails/{user_id}`: Get unread emails

## Security Considerations

- Keep `.env` file secure and never commit it
- Store OAuth credentials securely
- Use environment variables for sensitive data
- Implement proper error handling
- Follow OAuth 2.0 best practices

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 