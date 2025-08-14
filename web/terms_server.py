"""
Simple HTTP server to serve Terms of Service files for Discord bot registration.
This server hosts the ToS files required by Discord Developer Portal.
"""

import http.server
import socketserver
import os
import webbrowser
from urllib.parse import unquote

class TermsHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle root path
        if self.path == '/':
            self.path = '/terms-of-service-en.html'
        
        # Handle Terms of Service
        elif self.path == '/terms' or self.path == '/tos':
            self.path = '/terms-of-service-en.html'
        elif self.path == '/terms/pt' or self.path == '/tos/pt':
            self.path = '/terms-of-service.html'
        elif self.path == '/terms/en' or self.path == '/tos/en':
            self.path = '/terms-of-service-en.html'
        
        # Handle Privacy Policy
        elif self.path == '/privacy' or self.path == '/privacy-policy':
            self.path = '/privacy-policy-en.html'
        elif self.path == '/privacy/pt' or self.path == '/privacy-policy/pt':
            self.path = '/privacy-policy.html'
        elif self.path == '/privacy/en' or self.path == '/privacy-policy/en':
            self.path = '/privacy-policy-en.html'
        
        # Legacy language versions
        elif self.path == '/pt' or self.path == '/pt-br':
            self.path = '/terms-of-service.html'
        elif self.path == '/en':
            self.path = '/terms-of-service-en.html'
        
        # Remove query parameters if any
        self.path = self.path.split('?')[0]
        
        return super().do_GET()

    def end_headers(self):
        # Add CORS headers for API access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server(port=5000):
    """Start the Terms of Service server"""
    
    # Change to web directory to serve files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    handler = TermsHandler
    
    try:
        with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
            print(f"🌐 Terms of Service server running on:")
            print(f"   http://0.0.0.0:{port}")
            print(f"   http://localhost:{port}")
            print()
            print("📋 Available endpoints:")
            print("📄 Terms of Service:")
            print(f"   🇺🇸 English: http://localhost:{port}/terms")
            print(f"   🇧🇷 Português: http://localhost:{port}/terms/pt")
            print()
            print("🔒 Privacy Policy:")
            print(f"   🇺🇸 English: http://localhost:{port}/privacy")
            print(f"   🇧🇷 Português: http://localhost:{port}/privacy/pt")
            print()
            print("💡 Use these URLs in Discord Developer Portal:")
            print(f"   Terms of Service URL: http://localhost:{port}/terms")
            print(f"   Privacy Policy URL: http://localhost:{port}/privacy")
            print()
            print("Press Ctrl+C to stop the server")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_server()