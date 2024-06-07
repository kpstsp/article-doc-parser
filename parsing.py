from docx import Document

document = Document("docs//test.docx")
blocks = []
current_block = None

title = None
introduction = None
subtitle = None
subtopic_text = None
empty_para_count = 0
new_block_started = False

def start_new_block(title):
    return {
        "Title": title,
        "Introduction": "",
        "Subtopics": []
    }

def add_subtopic(block, subtitle, text):
    block["Subtopics"].append({
        "Subtitle": subtitle,
        "Text": text
    })

for para in document.paragraphs:
    text = para.text.strip()

    if text == "":
        empty_para_count += 1
    else:
        empty_para_count = 0

    if empty_para_count > 1:
        continue

    if empty_para_count == 1 and not new_block_started:
        if subtitle and subtopic_text:
            add_subtopic(current_block, subtitle, subtopic_text)
        subtitle = None
        subtopic_text = None
        empty_para_count = 0

    if text != "":
        if not current_block:
            title = text
            current_block = start_new_block(title)
            introduction = None
            subtitle = None
            subtopic_text = None
            new_block_started = True
        elif current_block:
            if new_block_started:
                if introduction is None:
                    if empty_para_count > 0:
                        introduction = ""
                    else:
                        introduction = text
                    current_block["Introduction"] = introduction
                    new_block_started = False
                elif subtitle is None:
                    subtitle = text
                else:
                    if subtopic_text is None:
                        subtopic_text = text
                    else:
                        subtopic_text += " " + text
            else:
                if subtitle is None:
                    subtitle = text
                else:
                    if subtopic_text is None:
                        subtopic_text = text
                    else:
                        subtopic_text += " " + text

            if empty_para_count == 1 and subtitle and subtopic_text:
                add_subtopic(current_block, subtitle, subtopic_text)
                subtitle = None
                subtopic_text = None

# Finalize the last block if there is one
if current_block:
    if subtitle and subtopic_text:
        add_subtopic(current_block, subtitle, subtopic_text)
    blocks.append(current_block)

# Print and debug the parsed data
# print("Parsed Data:")
# for block in blocks:
#     print(f"Title: {block['Title']}")
#     print(f"Introduction: {block['Introduction']}")
#     print(f"Number of Subtopics: {len(block['Subtopics'])}")
#     for subtopic in block['Subtopics']:
#         print(f"Subtitle: {subtopic['Subtitle']}")
#         print(f"Text: {subtopic['Text']}")

# # Save to JSON file
# import json
# with open('parsed_data.json', 'w', encoding='utf-8') as f:
#     json.dump(blocks, f, ensure_ascii=False, indent=4)
