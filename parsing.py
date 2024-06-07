from docx import Document

document = Document("docs/test.docx")
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

    # if empty_para_count > 1:
    if empty_para_count > 1:
        print(empty_para_count*"."+" "+"- {}".format(empty_para_count))
        if empty_para_count > 5:
            current_block = None

            title = None
            introduction = None
            subtitle = None
            subtopic_text = None
            empty_para_count = 0
            new_block_started = False
    if empty_para_count == 1 and not new_block_started:
        subtitle = None
        subtopic_text = None
        empty_para_count = 0




    if text != "":
        print(para.style.name)
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
                # else:
                    # subtopic_text += " " + text
            if empty_para_count == 1 and subtitle and subtopic_text:
                add_subtopic(current_block, subtitle, subtopic_text)
                subtitle = None
                subtopic_text = None


    if current_block:
        if subtitle and subtopic_text:
            add_subtopic(current_block, subtitle, subtopic_text)
        blocks.append(current_block)




