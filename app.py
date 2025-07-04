import os
import logging
from datetime import datetime
from typing import Dict, Any, List
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured successfully")

# Initialize LangChain Gemini model
llm = None
if GEMINI_API_KEY:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.7,
            max_output_tokens=1000,
            convert_system_message_to_human=True
        )
        logger.info("LangChain Gemini model initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini model: {e}")

# Define the conversation state
class ConversationState(TypedDict):
    messages: List[Dict[str, Any]]
    user_name: str
    context: Dict[str, Any]

# LangGraph Agent Functions
def isha_agent(state: ConversationState) -> ConversationState:
    """
    Main agent function that processes user messages and generates responses using Gemini API
    """
    try:
        messages = state.get("messages", [])
        user_name = state.get("user_name", "User")
        
        if not messages:
            logger.warning("No messages found in state")
            return state
        
        # Get the last user message
        last_message = messages[-1] if messages else None
        if not last_message or last_message.get("role") != "user":
            logger.warning("No user message found to process")
            return state
        
        user_input = last_message.get("content", "")
        
        # Create system message for Isha
        system_message = SystemMessage(content=f"""
        You are Isha, a professional AI assistant. You are responding to a voice message from {user_name}.
        
        Key guidelines:
        1. Keep responses conversational and natural for voice interaction
        2. Be concise but informative - avoid overly long responses
        3. Speak directly to the user in a warm, friendly tone
        4. Provide clear, actionable answers
        5. If the question is complex, break it down into simple points
        6. Use natural speech patterns and avoid overly formal language
        7. Keep responses under 150 words when possible for better voice experience
        8. If you need to provide lists, use "first", "second", "third" instead of bullet points
        
        Remember: Your response will be spoken aloud to the user, so make it sound natural and conversational.
        Current conversation context: You are having a voice conversation with {user_name}.
        """)
        
        # Create the conversation messages for the LLM
        conversation_messages = [system_message]
        
        # Add recent conversation history (last 5 messages)
        recent_messages = messages[-5:] if len(messages) > 5 else messages
        for msg in recent_messages:
            if msg.get("role") == "user":
                conversation_messages.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                conversation_messages.append(AIMessage(content=msg.get("content", "")))
        
        # Generate response using Gemini
        if llm:
            response = llm.invoke(conversation_messages)
            ai_response = response.content
            
            # Ensure the response acknowledges the user's message
            if not any(phrase in ai_response.lower() for phrase in ["replying to", "responding to", "you said", "your message"]):
                ai_response = f"I'm replying to your message: {ai_response}"
            
        else:
            # Fallback response when API is not available
            ai_response = f"Hi {user_name}! I heard you say '{user_input}'. I'm Isha, your AI assistant. I'm currently running in demo mode and need the Gemini API to be configured for full functionality. But I'm still here to help you with whatever you need!"
        
        # Add the AI response to the conversation
        ai_message = {
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat(),
            "message_id": f"isha_{datetime.now().timestamp()}"
        }
        
        # Update state with the new message
        updated_messages = messages + [ai_message]
        
        return {
            **state,
            "messages": updated_messages
        }
        
    except Exception as e:
        logger.error(f"Error in isha_agent: {e}")
        error_message = {
            "role": "assistant",
            "content": f"Hi {user_name}! I encountered a technical issue while processing your request, but don't worry - I'm still here to help! Please try asking your question again.",
            "timestamp": datetime.now().isoformat(),
            "message_id": f"isha_error_{datetime.now().timestamp()}",
            "error": True
        }
        
        return {
            **state,
            "messages": state.get("messages", []) + [error_message]
        }

# Create the LangGraph workflow
def create_isha_workflow():
    """
    Creates the LangGraph workflow for Isha AI assistant
    """
    workflow = StateGraph(ConversationState)
    
    # Add the main agent node
    workflow.add_node("isha_agent", isha_agent)
    
    # Set entry point
    workflow.set_entry_point("isha_agent")
    
    # Add finish edge
    workflow.add_edge("isha_agent", END)
    
    return workflow.compile()

# Initialize the workflow
isha_workflow = create_isha_workflow()

# Flask Routes
@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "message": "Isha AI Assistant Backend is running!",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "gemini_configured": GEMINI_API_KEY is not None
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint that processes user messages and returns AI responses
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user_message = data.get('message', '').strip()
        user_name = data.get('user_name', 'User')
        conversation_history = data.get('conversation_history', [])
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        logger.info(f"Processing message from {user_name}: {user_message[:100]}...")
        
        # Create user message object
        user_message_obj = {
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat(),
            "message_id": f"user_{datetime.now().timestamp()}"
        }
        
        # Prepare the conversation state
        initial_state = {
            "messages": conversation_history + [user_message_obj],
            "user_name": user_name,
            "context": {
                "session_id": data.get('session_id', 'default'),
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Process the message through the LangGraph workflow
        result = isha_workflow.invoke(initial_state)
        
        # Extract the AI response
        messages = result.get("messages", [])
        ai_response = None
        
        for msg in reversed(messages):
            if msg.get("role") == "assistant":
                ai_response = msg
                break
        
        if not ai_response:
            ai_response = {
                "role": "assistant",
                "content": f"I'm replying to your message, {user_name}. I'm having trouble processing your request right now, but I'm here to help!",
                "timestamp": datetime.now().isoformat(),
                "message_id": f"isha_fallback_{datetime.now().timestamp()}"
            }
        
        response_data = {
            "response": ai_response.get("content", ""),
            "message_id": ai_response.get("message_id", ""),
            "timestamp": ai_response.get("timestamp", ""),
            "user_name": user_name,
            "status": "success"
        }
        
        logger.info(f"Generated response for {user_name}: {response_data['response'][:100]}...")
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": f"I'm replying to your message, but I encountered an error. Please try again!",
            "status": "error",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Detailed health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "flask": "running",
            "gemini_api": "configured" if GEMINI_API_KEY else "not_configured",
            "langgraph": "initialized"
        },
        "version": "1.0.0"
    })

@app.route('/config', methods=['GET'])
def get_config():
    """Get configuration status"""
    return jsonify({
        "gemini_configured": GEMINI_API_KEY is not None,
        "model": "gemini-1.5-flash",
        "features": {
            "voice_recognition": True,
            "conversation_history": True,
            "personalized_responses": True
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist."
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred."
    }), 500

if __name__ == '__main__':
    # Check if running in development mode
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    
    logger.info("Starting Isha AI Assistant Backend...")
    logger.info(f"Debug mode: {debug_mode}")
    logger.info(f"Gemini API configured: {GEMINI_API_KEY is not None}")
    
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 4000)),
        debug=debug_mode
    ) 