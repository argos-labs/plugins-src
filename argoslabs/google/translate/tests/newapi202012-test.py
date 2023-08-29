from google_trans_new import google_translator

translator = google_translator()
translate_text = translator.translate('สวัสดีจีน', lang_tgt='en')
print(translate_text)
translate_text = translator.translate('สวัสดีจีน',lang_tgt='zh')
print(translate_text)
detect_result = translator.detect('สวัสดีจีน')
# <Detect text=สวัสดีจีน >
print(detect_result)