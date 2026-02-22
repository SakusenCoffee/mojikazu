import re, js
from pyscript import document, when
from pyodide.ffi import create_proxy

ignored_list = ['\u30FB']
ignored_char = r'[' + ''.join(ignored_list) + r']'

@when("input", "#jptext")
def count_text(event):
    text = document.querySelector("#jptext")
    text = text.value

    kanji = len(re.findall(r'[\u4E00-\u9FFF]', text))
    hiragana = len(re.findall(r'[\u3040-\u309F]', text))
    katakana = len(re.findall(r'[\u30A0-\u30FF]', text))
    punctuation = len(re.findall(r'[\u3000-\u303F]', text))
    ignore = len (re.findall(ignored_char, text))

    total = sum([kanji, hiragana, katakana])-ignore
    totalWithPunct = sum([punctuation, total])

    document.querySelector("#total span").innerText = total
    document.querySelector("#kanji span").innerText = kanji
    document.querySelector("#hiragana span").innerText = hiragana
    document.querySelector("#katakana span").innerText = katakana

counter_ids = ["#total", "#kanji", "#hiragana", "#katakana"]

@when("click", ",".join(counter_ids))
def handle_copy(event):
    element = event.currentTarget
    element_span = element.querySelector("span")
    if not element_span:
        return

    text_to_copy = element_span.innerText

    temp_input = js.document.createElement("textarea")
    temp_input.value = text_to_copy

    temp_input.style.position = "absolute"
    temp_input.style.left = "-9999px"

    js.document.body.appendChild(temp_input)
    temp_input.select()
    js.document.execCommand("copy")

    js.document.body.removeChild(temp_input)

    original_value = text_to_copy
    element_span.innerText = "Copied!"

    def reset_text():
        element_span.innerText = text_to_copy

    js.setTimeout(create_proxy(reset_text), 800)
