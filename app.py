import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure CORS
if os.environ.get('ENVIRONMENT') == 'production':
    allowed_origins = [
        os.environ.get('FRONTEND_URL', ''),
        'https://yourdomain.com',
        'https://www.yourdomain.com'
    ]
    CORS(app, origins=[origin for origin in allowed_origins if origin])
else:
    CORS(app)

# Configure Gemini AI
try:
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Warning: Could not configure Gemini AI: {e}")
    model = None

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "AI Study Assistant API is running",
        "version": "1.0.0"
    })

@app.route('/process', methods=['POST'])
def process_text():
    try:
        if model is None:
            return jsonify({
                "error": "AI service is not configured. Please check server configuration."
            }), 500
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({"error": "No text provided"}), 400
        
        if len(text) > 10000:
            text = text[:10000] + "...\n[Text truncated for processing]"
        
        prompt = f"""
Analyze the following educational text and provide a comprehensive study aid:

**INSTRUCTIONS:**
1. Create a clear, concise SUMMARY (2-3 paragraphs)
2. Generate 5 QUIZ QUESTIONS with multiple choice options (A, B, C, D)
3. Provide the CORRECT ANSWERS at the end
4. Focus on the most important concepts and key learning points

**TEXT TO ANALYZE:**
{text}

**FORMAT YOUR RESPONSE AS:**

## SUMMARY
[Your 2-3 paragraph summary here]

## QUIZ QUESTIONS

**Question 1:** [Question text]
A) [Option A]
B) [Option B] 
C) [Option C]
D) [Option D]

**Question 2:** [Question text]
A) [Option A]
B) [Option B]
C) [Option C] 
D) [Option D]

[Continue for all 5 questions...]

## ANSWER KEY
1. [Letter] - [Brief explanation]
2. [Letter] - [Brief explanation]
[Continue for all answers...]
        """
        
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return jsonify({
                "error": "AI service returned empty response. Please try again."
            }), 500
            
        result = response.text
        
        return jsonify({
            "result": result,
            "status": "success",
            "processed_length": len(text)
        })
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({
            "error": f"Processing failed: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('ENVIRONMENT') != 'production'
    
    print(f"Starting server on port {port}")
    print(f"Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
