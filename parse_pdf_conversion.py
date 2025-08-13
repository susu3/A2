import json
import os
import sys
import re
import base64
import fitz  # PyMuPDF
import io
from mistralai import Mistral
from mistralai import DocumentURLChunk
from mistralai.models import OCRResponse
import openai
from pathlib import Path
import datetime
# OCR生成初步Markdown并保存,返回完整的markdown和单页markdown列表
def mistral_ocr(pdf_bytes, output_dir):
    client = Mistral(api_key=mistral_api_key)

    # 创建输出目录和图片目录
    os.makedirs(output_dir, exist_ok=True)
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # 上传并处理PDF
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    uploaded_file = client.files.upload(
        file={
            "file_name": f"pdf_{timestamp}.pdf",
            "content": pdf_bytes,
        },
        purpose="ocr",
    )

    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
    ocr_response = client.ocr.process(
        document=DocumentURLChunk(document_url=signed_url.url),
        model="mistral-ocr-latest",
        include_image_base64=True
    )

    # 保存图片
    initial_markdown = []
    for page in ocr_response.pages:
        page_images = {}
        for img in page.images:
            img_data = base64.b64decode(img.image_base64.split(',')[1])
            img_path = os.path.join(images_dir, f"{img.id}.png")
            with open(img_path, 'wb') as f:
                f.write(img_data)
            page_images[img.id] = f"images/{img.id}.png"

        for img_id, img_path in page_images.items():
            page.markdown = page.markdown.replace(f"![{img_id}]({img_id})", f"![{img_id}]({img_path})")
        initial_markdown.append(page.markdown)

    #合并为完整的markdown
    complete_markdown = "\n\n".join(initial_markdown)
    
    # 保存完整markdown
    with open(os.path.join(output_dir, "initial.md"), 'w', encoding='utf-8') as f:
        f.write(complete_markdown)

    return initial_markdown

# PDF页面转图片
def pdf_page_to_image(pdf_path, page_number):
    doc = fitz.open(pdf_path)
    try:
        page = doc[page_number]
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        return pix.tobytes("png")
    finally:
        doc.close()

# 使用GPT-4o生成图片描述
def get_image_description(page_image, openai_api_key):
    openai.api_key = openai_api_key
    #client = OpenAI()

    # 将图片转换为base64
    page_image_base64 = base64.b64encode(page_image).decode()
    prompt = (
        "You are an expert in industrial protocol standards and document interpretation. "
        "You are given: A screenshot from a specification document (image). It may contain Figures, Tables, or neither. "
        "Your task: 1. Examine the image to determine whether it contains one or more diagrammatic Figures, Do **not** only rely on the presence of the word “Figure” in the text. Instead, identify Figures based on their visual characteristics (e.g., labeled blocks, arrows, data flow, structured layout); 2. For each Figure: "
        "- Extract the **Figure number** (e.g., 1, 2, 3) from the screenshot. "
        "- Describe what the Figure shows using the visual content. Be technical and precise. "
        "- The description must begin with: 'Figure X shows' (where X is the correct number). "
        "- Locate the **first complete sentence immediately following the Figure in the image**, Not the caption,and return it as the Figure's `location`. "
        "3. If no Figure is present in the screenshot, return the following JSON: "
        "```json\n"
        "{\n"
        "    \"isFigure\": false,\n"
        "    \"num\": 0\n"
        "}\n"
        "```\n"
        "4. If one or more Figures are present, return a JSON object in this format:\n"
        "```json\n"
        "{\n"
        "    \"isFigure\": true,\n"
        "    \"num\": 2,\n"
        "    \"figure0\": {\n"
        "        \"description\": \"Figure 1 shows a basic network topology used in industrial communication systems. It illustrates a LAN (Local Area Network) in a bus configuration where multiple devices are connected to a common communication line. On the left, a 'Master' device is shown, which typically initiates communication and controls the network. To the right, there are several 'Slave' devices, which respond to the Master's commands. Each device is connected perpendicularly to the main horizontal LAN bus, representing a standard topology in master-slave industrial protocols such as Modbus. The perspective uses 3D-style blocks to visually distinguish individual nodes.\",\n"
        "        \"location\": \"The IEC 104 specification combines the application layer of IEC 60870-5-101 and the transport functions provided by a TCP/IP (Transmission Control Protocol/Internet Protocol).\"\n"
        "    },\n"
        "    \"figure1\": {\n"
        "        \"description\": \"Figure 2 shows the communication process between a Master and a Slave device in an industrial communication system. The Master device sends a request to the Slave device, which then responds with the requested data. This interaction demonstrates the basic communication flow in master-slave protocols.\",\n"
        "        \"location\": \"1.3 Communication\"\n"
        "    }\n"
        "}\n"
        "```"
    )

    response = openai.chat.completions.create(
        model="gpt-4o",  # Using gpt-4o which now supports vision tasks
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", 
                     "image_url": {"url": f"data:image/png;base64,{page_image_base64}"}}
                ]
            }
        ],
        temperature=0.5,
        max_tokens=1000
    )
    return response.choices[0].message.content

# Helper function to extract JSON from markdown code blocks
def extract_json_from_markdown(markdown_text):
    """Extract JSON content from a markdown code block."""
    # Check if text is wrapped in markdown code block
    import re
    json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
    match = re.search(json_pattern, markdown_text)
    
    if match:
        # Return just the JSON content inside the code block
        return match.group(1).strip()
    
    # If not found in code block, return the original text
    return markdown_text

def process_pdf(pdf_path, mistral_api_key, openai_api_key):
    pdf_path = Path(pdf_path)
    output_dir = pdf_path.with_suffix('')
    
    # 使用Mistral OCR生成初始markdown和保存图片
    pdf_bytes = pdf_path.read_bytes()
    initial_markdown = mistral_ocr(pdf_bytes, output_dir)
    
    doc = fitz.open(pdf_path)
    final_markdown = initial_markdown.copy()  # Create a copy of the list
    
    try: 
        # 处理每个图片
        for page_num in range(len(doc)):
            page_image = pdf_page_to_image(pdf_path, page_num)
            response_content = get_image_description(page_image, openai_api_key)
            print(response_content)
            
            try:
                # Extract JSON from markdown code block if present
                json_content = extract_json_from_markdown(response_content)
                result = json.loads(json_content)
                
                if result["isFigure"]:
                    # Process each figure found on the page
                    for i in range(result["num"]):
                        figure_key = f"figure{i}"
                        figure_info = result[figure_key]
                            
                        # Find the location in the markdown text
                        location_text = figure_info["location"]
                        #print(location_text)
                        description = figure_info["description"]
                        #print(description)
                            
                        # Insert the description before the location text
                        location_index = final_markdown[page_num].find(location_text)
                        #print(location_index)
                        if location_index != -1:
                            final_markdown[page_num] = (
                                final_markdown[page_num][:location_index] +
                                f"\n{description}\n\n" +
                                final_markdown[page_num][location_index:]
                            )
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON response for page {page_num + 1}: {str(e)}")
                print(f"Response content: {response_content}")
                continue
    finally:
        doc.close()

    complete_markdown = "\n\n".join(final_markdown)
    
    # 保存最终markdown
    output_path = output_dir
    with open(os.path.join(output_dir, "final.md"), 'w', encoding='utf-8') as f:
        f.write(complete_markdown)
    print(f"Markdown saved to: {output_path}")
    
    return final_markdown

if __name__ == "__main__":
    mistral_api_key = "Your Mistral OCR API"
    openai_api_key = "Your OpenAI Key"
    pdf_path = "Your PDF path"
    #figure_pattern = r'Figure\s+\d+:'
    
    try:
        process_pdf(pdf_path, mistral_api_key, openai_api_key)
        print("Processing complete!")
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
