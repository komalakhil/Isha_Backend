import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # CORS Configuration
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173').split(',')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Application Configuration
    APP_NAME = os.getenv('APP_NAME', 'Isha AI Assistant')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    
    # Model Configuration
    MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-1.5-flash')
    MODEL_TEMPERATURE = float(os.getenv('MODEL_TEMPERATURE', '0.7'))
    MAX_OUTPUT_TOKENS = int(os.getenv('MAX_OUTPUT_TOKENS', '1000'))
    
    # Chat Configuration
    MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', '5'))
    
    @classmethod
    def get_gemini_config(cls):
        """Get Gemini-specific configuration"""
        return {
            'api_key': cls.GEMINI_API_KEY,
            'model': cls.MODEL_NAME,
            'temperature': cls.MODEL_TEMPERATURE,
            'max_output_tokens': cls.MAX_OUTPUT_TOKENS
        }
    
    @classmethod
    def is_gemini_configured(cls):
        """Check if Gemini API is properly configured"""
        return bool(cls.GEMINI_API_KEY and cls.GEMINI_API_KEY.strip())
    
    @classmethod
    def get_flask_config(cls):
        """Get Flask-specific configuration"""
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'debug': cls.DEBUG,
            'secret_key': cls.SECRET_KEY
        }

# Development configuration
class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# Production configuration
class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    
    @classmethod
    def validate_production_config(cls):
        """Validate production configuration"""
        errors = []
        
        if not cls.SECRET_KEY:
            errors.append("SECRET_KEY must be set in production")
        
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY must be set in production")
        
        if errors:
            raise ValueError("Production configuration errors: " + ", ".join(errors))

# Configuration factory
def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig() 