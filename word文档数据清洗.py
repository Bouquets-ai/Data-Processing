import os
import json
from docx import Document


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    valid_paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text and len(text.encode('utf-8')) >= 100:
            sentences = [s.strip() + '。' for s in text.split('。') if s.strip()]
            valid_paragraphs.extend([s for s in sentences if len(s.encode('utf-8')) >= 100])
    return valid_paragraphs


def extract_text_from_doc(file_path):
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(os.path.abspath(file_path))
        text = doc.Content.Text
        doc.Close()
        word.Quit()

        valid_sentences = []
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        for para in paragraphs:
            if len(para.encode('utf-8')) >= 100:
                sentences = [s.strip() + '。' for s in para.split('。') if s.strip()]
                valid_sentences.extend([s for s in sentences if len(s.encode('utf-8')) >= 100])
        return valid_sentences
    except Exception as e:
        print(f"处理 {file_path} 时出错: {e}")
        return []


def process_files(input_dir, output_file):
    all_data = []
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if filename.endswith('.docx'):
            all_data.extend([{"text": text} for text in extract_text_from_docx(file_path)])
        elif filename.endswith('.doc'):
            all_data.extend([{"text": text} for text in extract_text_from_doc(file_path)])

    # 写入 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f_out:
        json.dump(all_data, f_out, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    input_dir = '123'
    output_file = 'output.json' 

    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"目录不存在: {input_dir}")

    process_files(input_dir, output_file)

    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f'转换完成，结果已保存到 {output_file}')
    print(f'总条目数: {len(data)}')