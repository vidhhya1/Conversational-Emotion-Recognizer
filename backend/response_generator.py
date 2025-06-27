import google.generativeai as genai
import os

def generate_gemini_response(user_text, general_emotion, detailed_emotion, tone_frequency):
    """
    Generates a supportive and friendly response using Google Gemini,
    tailored to the user's mood and spoken content.

    Args:
        user_text (str): The transcribed text from the user.
        general_emotion (list): List of general emotions detected (e.g., ['happy', 'sad']).
        detailed_emotion (list): List of detailed emotions detected.
        tone_frequency (float): Detected tone frequency in Hz.

    Returns:
        str: The generated text response from the Gemini model.
    """
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please set it before running the application.")
        return "I'm sorry, but I can't generate a response right now as my AI brain is not configured. Please check the API key."

    genai.configure(api_key=api_key)

    
    general_emotion_str = ', '.join(general_emotion) if general_emotion else "Neutral"
    detailed_emotion_str = ', '.join(detailed_emotion) if detailed_emotion else "None specifically detected"
    tone_info = f"Detected tone frequency: {tone_frequency:.2f} Hz." if tone_frequency is not None else "No specific tone frequency detected."


    prompt = f"""
    You are an emotionally intelligent AI companion designed to provide supportive, friendly, and empathetic responses.
    Your goal is to make the user feel heard and understood, matching their current emotional state.

    Here is what the user said: "{user_text}"

    Emotion Analysis:
    - General Emotion(s): {general_emotion_str}
    - Detailed Emotion(s): {detailed_emotion_str}
    - {tone_info}

    Based on this information, generate a natural, concise (2-3 sentences), and supportive response.
    Do not directly mention the "tone frequency" or the "detailed emotion" unless it feels extremely natural to the conversation.
    Focus on acknowledging the general emotion and responding empathetically to the user's message.
    Make sure your response encourages further conversation.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("Sending prompt to Gemini API...")
        response = model.generate_content(prompt)
        response_text = response.text
        print("\n💬 Gemini Response Generated.")
        return response_text
    except Exception as e:
        print(f"Error generating content with Gemini API: {e}")
        return "I'm having a bit of trouble understanding right now. Could you please rephrase?"

if __name__ == '__main__':
  

    sample_user_text = "I had a really tough day at work today."
    sample_general_emotion = ["sad"]
    sample_detailed_emotion = ["grief", "disappointment"]
    sample_tone_frequency = 120.5

    generated_response = generate_gemini_response(
        sample_user_text,
        sample_general_emotion,
        sample_detailed_emotion,
        sample_tone_frequency
    )
    print("\n--- Sample Test Output ---")
    print(f"User: {sample_user_text}")
    print(f"Emotion: {sample_general_emotion}")
    print(f"Response: {generated_response}")