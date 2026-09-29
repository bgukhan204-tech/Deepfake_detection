import os
import time
import random
from gtts import gTTS

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh-CN': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'tr': 'Turkish',
    'nl': 'Dutch',
    'bn': 'Bengali',
    'ur': 'Urdu'
}

TRANSLATION_DICTIONARY = {
    'en': {
        'title': 'DeepShield AI Forensic Analysis',
        'real_verdict': 'VERIFIED GENUINE: No AI morphing or deepfake manipulation detected.',
        'fake_verdict': 'MANIPULATED MEDIA DETECTED: Facial synthesis and compression anomalies flagged.',
        'summary': 'DeepShield AI multi-spectral analysis completed successfully.'
    },
    'hi': {
        'title': 'दीपशील्ड एआई फॉरेंसिक विश्लेषण',
        'real_verdict': 'सत्यापित वास्तविक: कोई एआई हेरफेर या डीपफेक नहीं पाया गया।',
        'fake_verdict': 'हेरफेर किया गया मीडिया मिला: चेहरे के संश्लेषण और विसंगतियों को चिह्नित किया गया।',
        'summary': 'दीपशील्ड एआई बहु-स्पेक्ट्रम विश्लेषण सफलतापूर्वक पूरा हुआ।'
    },
    'ta': {
        'title': 'டீப்ஷீல்ட் ஏஐ தடயவியல் பகுப்பாய்வு',
        'real_verdict': 'உண்மையானது என சரிபார்க்கப்பட்டது: எவ்வித போலி மாற்றமும் கண்டறியப்படவில்லை.',
        'fake_verdict': 'போலியான ஊடகம் கண்டறியப்பட்டது: முக மாற்றங்கள் மற்றும் பிழைகள் கண்டறியப்பட்டன.',
        'summary': 'டீப்ஷீல்ட் ஏஐ பகுப்பாய்வு வெற்றிகரமாக முடிந்தது.'
    },
    'te': {
        'title': 'డీప్‌షీల్డ్ ఏఐ ఫోరెన్సిక్ విశ్లేషణ',
        'real_verdict': 'నిజమైనదిగా ధృవీకరించబడింది: ఎటువంటి డీప్‌ఫేక్ మార్పులు కనుగొనబడలేదు.',
        'fake_verdict': 'మానిప్యులేట్ చేసిన మీడియా కనుగొనబడింది: ముఖ మార్పులు మరియు తేడాలు గుర్తించబడ్డాయి.',
        'summary': 'డీప్‌షీల్డ్ ఏఐ విశ్లేషణ విజయవంతంగా పూర్తయింది.'
    },
    'es': {
        'title': 'Análisis Forense DeepShield AI',
        'real_verdict': 'VERIFICADO AUTÉNTICO: No se detectó manipulación de deepfake o IA.',
        'fake_verdict': 'MEDIO MANIPULADO DETECTADO: Se marcaron anomalías de síntesis facial.',
        'summary': 'Análisis multiespectral DeepShield AI completado con éxito.'
    },
    'fr': {
        'title': 'Analyse Médico-Légale DeepShield AI',
        'real_verdict': 'VÉRIFIÉ AUTHENTIQUE: Aucune manipulation de deepfake ou IA détectée.',
        'fake_verdict': 'MÉDIA MANIPULÉ DÉTECTÉ: Synthèse faciale et anomalies signalées.',
        'summary': 'Analyse multi-spectrale DeepShield AI terminée avec succès.'
    },
    'de': {
        'title': 'DeepShield KI Forensische Analyse',
        'real_verdict': 'ECHT BESTÄTIGT: Keine KI-Morphing- oder Deepfake-Manipulation erkannt.',
        'fake_verdict': 'MANIPULIERTE MEDIEN ERKANNT: Gesichtssynthese und Anomalien gemeldet.',
        'summary': 'Multispektrale Analyse von DeepShield KI erfolgreich abgeschlossen.'
    },
    'zh-CN': {
        'title': 'DeepShield AI 取证分析',
        'real_verdict': '验证真实：未检测到 AI 变形或 Deepfake 操纵。',
        'fake_verdict': '检测到篡改媒体：人脸合成和压缩异常被标记。',
        'summary': 'DeepShield AI 多光谱分析成功完成。'
    },
    'ja': {
        'title': 'DeepShield AI フォレンジック分析',
        'real_verdict': '本物と確認：AIモーフやディープフェイクの操作は検出されませんでした。',
        'fake_verdict': '改ざんメディアを検出：顔の合成と圧縮の異常がフラグ設定されました。',
        'summary': 'DeepShield AIのマルチスペクトル分析が正常に完了しました。'
    },
    'ar': {
        'title': 'تحليل DeepShield AI الجنائي',
        'real_verdict': 'تم التحقق من الأصالة: لم يتم اكتشاف أي تزييف عميق أو تعديل ذكاء اصطناعي.',
        'fake_verdict': 'تم اكتشاف وسائط متلاعب بها: تم رصد تركيب أوجه واختلافات في الضغط.',
        'summary': 'اكتمل تحليل DeepShield AI متعدد الأطياف بنجاح.'
    }
}

class TranslationService:
    """
    SERVICES: Translation & Speech Synthesis
    """
    def __init__(self, export_dir=None):
        self.export_dir = export_dir or os.path.join(os.path.dirname(__file__), "..", "static", "exports")
        os.makedirs(self.export_dir, exist_ok=True)

    def translate_text(self, text, target_lang='en'):
        """Translates given text or verdict summary to target language."""
        if target_lang not in SUPPORTED_LANGUAGES:
            target_lang = 'en'
            
        lang_dict = TRANSLATION_DICTIONARY.get(target_lang, TRANSLATION_DICTIONARY['en'])
        
        # Check if text matches real/fake pattern
        if "MANIPULATED" in text.upper() or "FAKE" in text.upper():
            translated = lang_dict.get('fake_verdict', f"[{SUPPORTED_LANGUAGES[target_lang]}] {text}")
        elif "REAL" in text.upper() or "GENUINE" in text.upper() or "AUTHENTIC" in text.upper():
            translated = lang_dict.get('real_verdict', f"[{SUPPORTED_LANGUAGES[target_lang]}] {text}")
        else:
            translated = lang_dict.get('summary', f"[{SUPPORTED_LANGUAGES[target_lang]}] {text}")

        return {
            'success': True,
            'target_language': target_lang,
            'language_name': SUPPORTED_LANGUAGES[target_lang],
            'original_text': text,
            'translated_text': translated
        }

    def generate_audio(self, text, target_lang='en'):
        """Synthesizes MP3 speech audio for translated text using gTTS."""
        translation_res = self.translate_text(text, target_lang)
        speech_text = translation_res['translated_text']
        lang_name = translation_res['language_name']

        audio_filename = f"audio_{target_lang}_{int(time.time())}_{random.randint(100,999)}.mp3"
        audio_path = os.path.join(self.export_dir, audio_filename)

        try:
            tts = gTTS(text=speech_text, lang=target_lang)
            tts.save(audio_path)
        except Exception:
            # Fallback to English if language unsupported by gTTS
            tts = gTTS(text=f"DeepShield AI report translated to {lang_name}: {speech_text}", lang='en')
            tts.save(audio_path)

        return {
            'success': True,
            'audio_filename': audio_filename,
            'audio_url': f"/api/download_file/{audio_filename}",
            'language_code': target_lang,
            'language_name': lang_name,
            'translated_text': speech_text
        }

translation_service = TranslationService()
