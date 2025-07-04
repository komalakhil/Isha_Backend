#!/usr/bin/env python3
"""
Run script for Isha AI Assistant Backend
"""

import os
import sys
import logging
from app import app, logger
from config import get_config

def setup_logging():
    """Setup logging configuration"""
    config = get_config()
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('isha_backend.log')
        ]
    )

def check_environment():
    """Check if environment is properly configured"""
    config = get_config()
    
    print("🚀 Starting Isha AI Assistant Backend...")
    print(f"   App Name: {config.APP_NAME}")
    print(f"   Version: {config.APP_VERSION}")
    print(f"   Environment: {'Development' if config.DEBUG else 'Production'}")
    print(f"   Host: {config.HOST}")
    print(f"   Port: {config.PORT}")
    print(f"   Gemini API: {'✅ Configured' if config.is_gemini_configured() else '❌ Not Configured'}")
    print()
    
    if not config.is_gemini_configured():
        print("⚠️  Warning: Gemini API key is not configured!")
        print("   The application will run in demo mode.")
        print("   To enable full functionality, set the GEMINI_API_KEY environment variable.")
        print()
    
    return config

def main():
    """Main entry point"""
    try:
        # Setup logging
        setup_logging()
        
        # Check environment
        config = check_environment()
        
        # Validate production config if needed
        if not config.DEBUG:
            try:
                config.validate_production_config()
            except ValueError as e:
                logger.error(f"Production configuration error: {e}")
                sys.exit(1)
        
        # Start the application
        flask_config = config.get_flask_config()
        
        logger.info("🎉 Isha AI Assistant Backend is ready!")
        logger.info(f"   Access the API at: http://{flask_config['host']}:{flask_config['port']}")
        logger.info(f"   Health check: http://{flask_config['host']}:{flask_config['port']}/health")
        logger.info(f"   Chat endpoint: http://{flask_config['host']}:{flask_config['port']}/chat")
        
        app.run(
            host=flask_config['host'],
            port=flask_config['port'],
            debug=flask_config['debug']
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down Isha AI Assistant Backend...")
    except Exception as e:
        logger.error(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 