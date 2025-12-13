"""
Voice Request View - Create Request with speech recognition
"""
import streamlit as st
import requests
import speech_recognition as sr
from config import API_BASE_URL


def voice_request_view():
    """Voice request view with speech-to-text functionality"""
    
    with st.container(border=True):
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="background-color: #EFF6FF; border: 2px solid #2563EB; border-radius: 50%; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 1.25rem;">🎤</span>
            </div>
            <div style="background-color: #F8FAFC; border-radius: 8px; padding: 0.75rem 1rem; flex: 1;">
                <span style="color: #64748B;">Click start and speak clearly...</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎤 Start Voice Input", key="voice_record_btn", use_container_width=True):
            r = sr.Recognizer()
            r.energy_threshold = 300
            
            try:
                with sr.Microphone() as source:
                    with st.spinner("🤫 Calibrating background noise..."):
                        r.adjust_for_ambient_noise(source, duration=1)
                    
                    with st.spinner("🎙️ Listening... Speak now!"):
                        audio = r.listen(source, timeout=5, phrase_time_limit=10)
                        
                    st.success("✅ Audio captured! Processing...")
                    
                    # Google Speech to Text
                    raw_text = r.recognize_google(audio)
                    st.info(f"You said: '{raw_text}'")
                    
                    # Send to Backend Agent for cleaning
                    with st.spinner("🤖 AI is cleaning up your text..."):
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/clean_voice_input",
                                json={"text": raw_text}
                            )
                            if response.ok:
                                cleaned = response.json().get("cleaned", raw_text)
                                st.session_state.voice_text = cleaned
                                st.rerun()
                            else:
                                st.error(f"Backend Error: {response.status_code}")
                        except Exception as e:
                            st.error(f"Could not connect to backend: {e}")

            except sr.WaitTimeoutError:
                st.warning("⚠️ No speech detected. Try speaking louder.")
            except sr.UnknownValueError:
                st.warning("🤔 Could not understand audio. Try again.")
            except Exception as e:
                st.error(f"Error: {e}")

