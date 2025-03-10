import gradio as gr
import google.generativeai as genai
from duckduckgo_search import DDGS

# API AYARLARI
API_KEY = "API KEY"  # Google AI Studio'dan alınan geçerli anahtar
MODEL_NAME = "gemini-2.0-flash"     # Güncel model 


def akilli_asistan(soru):
    try:
        # 1. DuckDuckGo ile Gerçek Zamanlı Arama
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(soru, max_results=5)]
        
        # 2. Context Oluşturma
        context = "\n\n".join([f"🔗 {r['title']}\n{r['body']}" for r in results])
        
        # 3. Gemini Modelini Yapılandır
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)
        
        # 4. Yanıt Üret
        response = model.generate_content(
            f"""
            **Kullanıcı Sorusu:** {soru}
            **Web Araştırması Sonuçları:** {context}
            
            **Talimatlar:**
            - Yanıtı maddeler halinde formatla
            - Gerçek zamanlı verilere öncelik ver
            - Tarih, saat ve kaynakları belirt
            - Emoji kullanarak görselleştir
            - görsel linkleri ekleyerek destekle
            - İlgili bağlantıları ekleyerek kaynak göster
            - önemli kelimeleri kalınlaştır
            - kullanıcaya önerilerde bulun
            """
        )
        
        return response.text
    
    except Exception as e:
        return f"🚨 Hata: {str(e)}"

# Gradio Arayüzü
interface = gr.Interface(
    fn=akilli_asistan,
    inputs=gr.Textbox(label="NE ÖĞRENMEK İSTERSİNİZ?", placeholder="Örn: İstanbul hava durumu, Bitcoin fiyatı..."),
    outputs=gr.Markdown(label="CANLI YANIT"),
    title="🤖 GOOGLE GEMİNİ 2.0 ASİSTAN",
    description="Gerçek zamanlı web verileriyle çalışan yapay zeka asistanı",
    allow_flagging="never"
)

if __name__ == "__main__":
    interface.launch(share=True)  # İnternet üzerinden paylaşım için
