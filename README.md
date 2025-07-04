# Isha AI Assistant Backend 🤖

A Flask-based backend with LangGraph integration that uses Google's Gemini API to provide intelligent responses to user messages.

## 🚀 Features

### 🧠 AI-Powered Responses
- **Gemini API Integration**: Uses Google's Gemini-1.5-flash model for intelligent responses
- **LangGraph Workflow**: Structured conversation flow with state management
- **Context-Aware**: Maintains conversation history and context
- **Personalized Responses**: Always acknowledges user messages and provides personalized replies

### 🔧 Technical Features
- **Flask REST API**: Clean RESTful endpoints for chat functionality
- **CORS Support**: Configured for frontend integration
- **Error Handling**: Comprehensive error handling with fallback responses
- **Logging**: Detailed logging for debugging and monitoring
- **Configuration Management**: Environment-based configuration

### 🛡️ Security & Privacy
- **API Key Management**: Secure handling of API keys through environment variables
- **Input Validation**: Proper validation of user inputs
- **Error Sanitization**: Safe error messages without exposing internal details

## 📋 Requirements

- Python 3.8+
- Google Gemini API Key
- Flask and dependencies (see requirements.txt)

## 🛠️ Installation

### 1. Clone and Navigate
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up Environment Variables
Create a `.env` file in the backend directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
PORT=5000
```

### 5. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and add it to your `.env` file

## 🚀 Usage

### Quick Start
```bash
# Using the run script (recommended)
python run.py

# Or directly
python app.py
```

### API Endpoints

#### 1. Health Check
```bash
GET /
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "services": {
    "flask": "running",
    "gemini_api": "configured",
    "langgraph": "initialized"
  }
}
```

#### 2. Chat Endpoint
```bash
POST /chat
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "user_name": "John",
  "conversation_history": [],
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "response": "I'm replying to your message, John. I'm doing well, thank you for asking! How can I help you today?",
  "message_id": "isha_1704067200.123",
  "timestamp": "2024-01-01T00:00:00.123Z",
  "user_name": "John",
  "status": "success"
}
```

#### 3. Configuration Check
```bash
GET /config
```

**Response:**
```json
{
  "gemini_configured": true,
  "model": "gemini-1.5-flash",
  "features": {
    "voice_recognition": true,
    "conversation_history": true,
    "personalized_responses": true
  }
}
```

## 🎯 LangGraph Workflow

The backend uses LangGraph to create a structured conversation flow:

```python
# Conversation State
{
  "messages": [
    {
      "role": "user",
      "content": "Hello!",
      "timestamp": "2024-01-01T00:00:00.000Z",
      "message_id": "user_1704067200.123"
    },
    {
      "role": "assistant", 
      "content": "I'm replying to your message...",
      "timestamp": "2024-01-01T00:00:00.456Z",
      "message_id": "isha_1704067200.456"
    }
  ],
  "user_name": "John",
  "context": {
    "session_id": "session_123",
    "timestamp": "2024-01-01T00:00:00.000Z"
  }
}
```

### Workflow Steps:
1. **Input Processing**: Validates and structures user input
2. **Context Building**: Builds conversation context with history
3. **Gemini API Call**: Sends structured prompt to Gemini
4. **Response Processing**: Ensures response acknowledges user message
5. **State Update**: Updates conversation state with new messages

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key
- `FLASK_ENV`: Environment (development/production)
- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: 0.0.0.0)
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

### Model Configuration
- `MODEL_NAME`: Gemini model name (default: gemini-1.5-flash)
- `MODEL_TEMPERATURE`: Response creativity (0.0-1.0, default: 0.7)
- `MAX_OUTPUT_TOKENS`: Maximum response length (default: 1000)
- `MAX_CONVERSATION_HISTORY`: Number of messages to keep in context (default: 5)

## 🎨 Customization

### Modifying AI Behavior
Edit the system message in `app.py`:

```python
system_message = SystemMessage(content=f"""
You are Isha, a professional AI assistant. You are responding to a message from {user_name}.

Key guidelines:
1. Always acknowledge that you are replying to their message
2. Be professional, helpful, and friendly
3. Provide clear and concise responses
4. If asked about your capabilities, mention that you can help with various tasks
5. Keep responses conversational and engaging
6. Always start your response by acknowledging their message

Current conversation context: You are chatting with {user_name} who just sent you a message.
""")
```

### Adding New Endpoints
```python
@app.route('/custom-endpoint', methods=['POST'])
def custom_endpoint():
    # Your custom logic here
    return jsonify({"message": "Custom response"})
```

## 🐛 Troubleshooting

### Common Issues

1. **Gemini API Key Issues**
   ```bash
   # Check if API key is set
   echo $GEMINI_API_KEY
   
   # Test API key
   curl -X GET "https://generativelanguage.googleapis.com/v1/models?key=$GEMINI_API_KEY"
   ```

2. **Port Already in Use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   
   # Kill process
   kill -9 <process_id>
   
   # Or use different port
   export PORT=5001
   ```

3. **CORS Issues**
   - Ensure frontend URL is in ALLOWED_ORIGINS
   - Check browser console for CORS errors
   - Verify both frontend and backend are running

4. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install --upgrade -r requirements.txt
   
   # Check Python version
   python --version  # Should be 3.8+
   ```

### Debug Mode
Set `FLASK_ENV=development` for detailed error messages and auto-reload.

### Logging
Check `isha_backend.log` for detailed logs:
```bash
tail -f isha_backend.log
```

## 📊 Monitoring

### Health Checks
```bash
# Basic health check
curl http://localhost:5000/health

# Check configuration
curl http://localhost:5000/config
```

### Performance Metrics
- Response time tracking in logs
- Error rate monitoring
- API usage tracking

## 🚀 Deployment

### Production Setup
1. Set environment variables:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   export GEMINI_API_KEY=your-api-key
   ```

2. Use production server:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "run.py"]
```

## 🔐 Security

### API Key Security
- Never commit API keys to version control
- Use environment variables or secure vaults
- Rotate keys regularly
- Monitor API usage

### Input Validation
- All user inputs are validated
- SQL injection prevention
- XSS protection through proper encoding

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `isha_backend.log`
3. Open an issue with detailed error information

---

**Made with ❤️ for intelligent conversations**

*Isha AI Assistant Backend - Powered by Gemini API & LangGraph* 