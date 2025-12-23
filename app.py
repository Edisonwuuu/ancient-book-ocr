from flask import Flask, request, render_template, jsonify
import os
from paddleocr import PaddleOCR
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为16MB
app.config['UPLOAD_FOLDER'] = 'uploads'

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化PaddleOCR
# 使用最简配置，lang='ch' 支持简体和繁体中文
ocr = PaddleOCR(lang='ch')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file:
        # 保存上传的文件
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        try:
            # 进行OCR识别
            result = ocr.predict(filename)
            
            # 提取识别的文字
            texts = []
            if result and len(result) > 0:
                ocr_result = result[0]
                # OCRResult是字典类型，rec_texts包含识别的文字列表
                if 'rec_texts' in ocr_result:
                    texts = ocr_result['rec_texts']
            
            # 合并文字
            full_text = '\n'.join(texts) if texts else '未识别到文字'
            
            return jsonify({
                'success': True,
                'text': full_text
            })
        
        except Exception as e:
            return jsonify({'error': f'识别失败: {str(e)}'}), 500
        
        finally:
            # 删除临时文件
            if os.path.exists(filename):
                os.remove(filename)

@app.route('/upload_base64', methods=['POST'])
def upload_base64():
    """支持base64图片上传"""
    data = request.get_json()
    
    if 'image' not in data:
        return jsonify({'error': '没有图片数据'}), 400
    
    try:
        # 解码base64图片
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # 保存临时文件
        temp_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.png')
        image.save(temp_filename)
        
        # 进行OCR识别
        result = ocr.predict(temp_filename)
        
        # 提取识别的文字
        texts = []
        if result and len(result) > 0:
            ocr_result = result[0]
            # OCRResult是字典类型，rec_texts包含识别的文字列表
            if 'rec_texts' in ocr_result:
                texts = ocr_result['rec_texts']
        
        full_text = '\n'.join(texts) if texts else '未识别到文字'
        
        return jsonify({
            'success': True,
            'text': full_text
        })
    
    except Exception as e:
        return jsonify({'error': f'识别失败: {str(e)}'}), 500
    
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)