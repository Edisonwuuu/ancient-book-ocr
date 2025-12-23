from paddleocr import PaddleOCR
import sys

# 初始化OCR
ocr = PaddleOCR(lang='ch')

# 测试文件
test_file = sys.argv[1] if len(sys.argv) > 1 else 'test.png'

print(f"正在识别文件: {test_file}")
print("="*50)

# 执行识别
result = ocr.predict(test_file)

# 打印完整结果结构
print("完整结果类型:", type(result))
print("结果长度:", len(result) if result else 0)
print()

if result and len(result) > 0:
    ocr_result = result[0]
    print("OCRResult 类型:", type(ocr_result))
    print("OCRResult 属性:", dir(ocr_result))
    print()
    
    # 检查常用属性
    if hasattr(ocr_result, 'rec_text'):
        print("rec_text 属性存在")
        print("rec_text 类型:", type(ocr_result.rec_text))
        print("rec_text 内容:", ocr_result.rec_text)
        print()
    
    if hasattr(ocr_result, 'dt_polys'):
        print("dt_polys 属性存在")
        print("dt_polys 数量:", len(ocr_result.dt_polys) if ocr_result.dt_polys else 0)
        print()
    
    if hasattr(ocr_result, 'rec_score'):
        print("rec_score 属性存在")
        print("rec_score 内容:", ocr_result.rec_score)
        print()
    
    # 尝试迭代
    print("尝试迭代 OCRResult:")
    try:
        for i, item in enumerate(ocr_result):
            print(f"  项 {i}: {item} (类型: {type(item)})")
            if i >= 2:  # 只打印前3个
                break
    except Exception as e:
        print(f"  无法迭代: {e}")

print("="*50)
print("提取的文字:")

texts = []
if result and len(result) > 0:
    ocr_result = result[0]
    if hasattr(ocr_result, 'rec_text'):
        texts = ocr_result.rec_text if isinstance(ocr_result.rec_text, list) else [ocr_result.rec_text]
    elif hasattr(ocr_result, '__iter__'):
        for item in ocr_result:
            if hasattr(item, 'rec_text'):
                texts.append(item.rec_text)
            elif isinstance(item, str):
                texts.append(item)

print('\n'.join(texts) if texts else '未识别到文字')