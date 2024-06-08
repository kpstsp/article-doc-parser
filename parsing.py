from docx import Document
from time import sleep

document = Document("docs//test.docx")
blocks = []
current_block = None

title = None
introduction = None
subtitle = None
subtopic_text = None
empty_para_count = 0
new_block_started = False
timeout=0

def start_new_block(title):
    return {
        "Title": title,
        "Introduction": "",
        "Subtopics": []
    }

def add_subtopic(block, subtitle, text):
    print("Added as subtopic")
    block["Subtopics"].append({
        "Subtitle": subtitle,
        "Text": text
    })

for para in document.paragraphs:
    text = para.text.strip()
    print("Start analizing text")

    if text == "":
        empty_para_count += 1
        print("ENPTY string")

    else:
        empty_para_count = 0
        print(">>> {} ...".format(text[0:24]))

    # if empty_para_count > 1:
    #     continue

    if empty_para_count == 1 and not new_block_started:
        if subtitle and subtopic_text:
            add_subtopic(current_block, subtitle, subtopic_text)
        subtitle = None
        subtopic_text = None
        # empty_para_count = 0

    if text != "":
        if not current_block:
            print("New block parse")
            title = text
            print("title is found {}".format(text))
            current_block = start_new_block(title)
            introduction = None
            subtitle = None
            subtopic_text = None
            new_block_started = True
            sleep(timeout)
        elif current_block:
            if new_block_started:
                if introduction is None:
                    if empty_para_count > 0:
                        introduction = ""
                    else:
                        introduction = text
                    print("Introduction is found : \n")
                    print(text)
                    current_block["Introduction"] = introduction
                    new_block_started = False
                elif subtitle is None:
                    subtitle = text
                    print("Found subtitle: {}".format(text))
                    sleep(timeout)
                else:
                    if subtopic_text is None:
                        print("Found subtopic: {}".format(text))
                        sleep(timeout)
                        subtopic_text = text
                    else:
                        subtopic_text += " " + text
            else:
                if subtitle is None:
                    subtitle = text
                    print("Found subtitle: {}".format(text))
                    sleep(timeout)
                else:
                    if subtopic_text is None:
                        subtopic_text = text
                        print("Found subtopic: {}".format(text))
                        sleep(timeout)
                    else:
                        subtopic_text += "\n" + text

            # if empty_para_count == 1 and subtitle and subtopic_text:
            #     add_subtopic(current_block, subtitle, subtopic_text)
            #     print("Subtopic added to block")
            #     sleep(timeout)
            #     subtitle = None
            #     subtopic_text = None

# Finalize the last block if there is one
    if current_block:
        print("Empty para count {}".format(empty_para_count)+"."*empty_para_count)
        if empty_para_count>4:
            print("Current block set as None")
            blocks.append(current_block)
            current_block = None
        # if subtitle and subtopic_text:
        #     add_subtopic(current_block, subtitle, subtopic_text)
        #     sleep(timeout)
        
        

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
