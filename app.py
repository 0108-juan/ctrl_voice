import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

def on_publish(client,userdata,result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("juan")
client1.on_message = on_message

# Configuración de la página
st.set_page_config(
    page_title="Interfaces Multimodales - Control por Voz",
    layout="wide",
    page_icon="🎤",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #1f77b4, #2e86ab);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        padding: 1rem;
    }
    .section-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 0;
        margin: 2rem 0;
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
        border: 3px solid #e2e8f0;
    }
    .section-title {
        background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 20px 20px 0 0;
        margin: 0;
        font-size: 1.6rem;
        font-weight: 600;
        border-bottom: 4px solid #2c5282;
        text-align: center;
    }
    .section-content {
        background: white;
        padding: 2.5rem;
        border-radius: 0 0 20px 20px;
        min-height: 150px;
    }
    .voice-button {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin: 1rem 0 !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4) !important;
    }
    .voice-button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(255, 107, 107, 0.6) !important;
    }
    .result-frame {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 3px solid #e2e8f0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    .info-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .feature-item {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 2px solid #e2e8f0;
        transition: transform 0.3s ease;
    }
    .feature-item:hover {
        transform: translateY(-5px);
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-online {
        background-color: #10B981;
    }
    .status-offline {
        background-color: #EF4444;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<h1 class="main-header">🎤 INTERFACES MULTIMODALES</h1>', unsafe_allow_html=True)

# Layout principal
col1, col2 = st.columns([1, 1])

with col1:
    # Sección de Control por Voz
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎙️ CONTROL POR VOZ</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
    # Imagen con marco
    st.markdown('<div style="text-align: center; margin-bottom: 2rem;">', unsafe_allow_html=True)
    try:
        image = Image.open('voice_ctrl.jpg')
        st.image(image, width=250, use_column_width=False)
    except:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 3rem; border-radius: 15px; text-align: center; border: 2px dashed #dee2e6;'>
            <span style='font-size: 4rem;'>🎤</span>
            <p style='color: #6c757d; margin-top: 1rem;'>Imagen de control por voz</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Instrucciones
    st.markdown("""
    <div class="info-card">
        <h4 style='color: #2d3748; margin-bottom: 1rem;'>🗣️ ¿Cómo funciona?</h4>
        <p style='color: #4a5568; line-height: 1.6;'>
        1. <strong>Presiona el botón "Comenzar Reconocimiento"</strong><br>
        2. <strong>Habla claramente</strong> tu comando<br>
        3. <strong>Espera</strong> a que se procese tu voz<br>
        4. <strong>Observa</strong> el resultado en pantalla
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Cierre section-content
    st.markdown('</div>', unsafe_allow_html=True)  # Cierre section-container

with col2:
    # Sección de Reconocimiento de Voz
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔊 RECONOCIMIENTO DE VOZ</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)
    
    # Estado del sistema
    st.markdown("""
    <div style='background: #f0f9ff; padding: 1.5rem; border-radius: 10px; border: 2px solid #bae6fd; margin-bottom: 2rem;'>
        <h4 style='color: #0369a1; margin-bottom: 0.5rem;'>📊 Estado del Sistema</h4>
        <p style='color: #0c4a6e; margin: 0;'>
            <span class='status-indicator status-online'></span>
            Sistema de reconocimiento vocal <strong>ACTIVO</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón de reconocimiento de voz
    st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
    st.write("### Toca el Botón y habla")
    
    stt_button = Button(label="🎤 Comenzar Reconocimiento", width=300, height=60)
    stt_button.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
     
        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if ( value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.start();
        """))

    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=100,
        debounce_time=0)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Resultados
    if result:
        if "GET_TEXT" in result:
            st.markdown('<div class="result-frame">', unsafe_allow_html=True)
            st.markdown("### 🎯 Comando Reconocido:")
            st.markdown(f"**`{result.get('GET_TEXT')}`**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Publicar en MQTT
            client1.on_publish = on_publish                            
            client1.connect(broker,port)  
            message =json.dumps({"Act1":result.get("GET_TEXT").strip()})
            ret= client1.publish("voice_juan", message)
            
            # Indicador de envío
            st.success("✅ Comando enviado exitosamente al sistema MQTT")
    
    # Características del sistema
    st.markdown("### ✨ Características del Sistema")
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-item">
            <span style="font-size: 2rem;">🎙️</span>
            <h4>Reconocimiento</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Voz a texto en tiempo real</p>
        </div>
        <div class="feature-item">
            <span style="font-size: 2rem;">📡</span>
            <h4>MQTT</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Comunicación IoT</p>
        </div>
        <div class="feature-item">
            <span style="font-size: 2rem;">🌐</span>
            <h4>Web Integration</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Compatibilidad total</p>
        </div>
        <div class="feature-item">
            <span style="font-size: 2rem;">⚡</span>
            <h4>Tiempo Real</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Procesamiento inmediato</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Cierre section-content
    st.markdown('</div>', unsafe_allow_html=True)  # Cierre section-container

# Barra lateral informativa
with st.sidebar:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; color: white; text-align: center;'>
        <h2>🎤</h2>
        <h3>Control por Voz</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; 
                border: 2px solid #e2e8f0;'>
        <h4 style='color: #2d3748;'>ℹ️ Acerca de</h4>
        <p style='color: #4a5568; font-size: 0.9rem;'>
        Esta aplicación demuestra el control multimodal mediante reconocimiento de voz 
        y comunicación MQTT para sistemas IoT.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #f8fafc; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #10B981;'>
        <h4 style='color: #2d3748;'>🚀 Tecnologías</h4>
        <ul style='color: #4a5568; font-size: 0.9rem; padding-left: 1.2rem;'>
            <li>Streamlit</li>
            <li>Web Speech API</li>
            <li>MQTT Protocol</li>
            <li>Bokeh Events</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #fff7ed; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #ea580c;'>
        <h4 style='color: #2d3748;'>📝 Notas</h4>
        <p style='color: #4a5568; font-size: 0.9rem;'>
        • Asegúrate de tener micrófono activado<br>
        • Habla claro y pausado<br>
        • Funciona mejor en Chrome
        </p>
    </div>
    """, unsafe_allow_html=True)

# Crear directorio temporal si no existe
try:
    os.mkdir("temp")
except:
    pass
