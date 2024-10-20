from flask import Flask, render_template, request
import requests
import subprocess
import os

app = Flask(__name__)

# رابط Gist الذي يحتوي على كود Selenium
gist_url = "https://gist.githubusercontent.com/samix1990/0d43cca1aba1aefa1bd7784aeaee70e5/raw/1abc9d4e71430b1f8faf3713e9a46ba654f02747/selenium_netflix.py"

# متغير لتتبع ما إذا تم تشغيل السكريبت أم لا
script_has_run = False

@app.route('/')
def index():
    global script_has_run
    return render_template('index.html', script_has_run=script_has_run)

@app.route('/run_script', methods=['POST'])
def run_script():
    global script_has_run

    # تحقق ما إذا كان السكريبت قد تم تشغيله بالفعل
    if script_has_run:
        return "تم تشغيل السكريبت بالفعل. لا يمكنك تشغيله مرة أخرى حتى تعيد تحميل الصفحة."

    # تحميل الكود من Gist
    response = requests.get(gist_url)

    if response.status_code == 200:
        script_content = response.text

        # حفظ الكود كملف مؤقت مع استخدام utf-8 لتجنب مشاكل الترميز
        with open('temp_selenium_script.py', 'w', encoding='utf-8') as script_file:
            script_file.write(script_content)

        # تشغيل الكود باستخدام subprocess فقط إذا لم يكن في وضع إعادة التحميل
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':  # يتحقق إذا كان Flask في إعادة تشغيل
            subprocess.run(['python', 'temp_selenium_script.py'], check=True)

        # تعيين حالة السكريبت كأنه تم تشغيله
        script_has_run = True

        return "تم تشغيل السكريبت بنجاح."
    else:
        return "فشل في تحميل السكريبت من Gist."

@app.route('/reset', methods=['POST'])
def reset():
    # إعادة تعيين حالة السكريبت للسماح بتشغيله مجددًا
    global script_has_run
    script_has_run = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
