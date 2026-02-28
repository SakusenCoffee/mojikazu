import re, js
from pyscript import document, when
from pyodide.ffi import create_proxy

# Compile Regex
IGNORED_CHAR_RE = re.compile(r'[\u30FB]')
KANJI_RE = re.compile(r'[\u4E00-\u9FFF]')
HIRAGANA_RE = re.compile(r'[\u3040-\u309F]')
KATAKANA_RE = re.compile(r'[\u30A0-\u30FF]')
PUNCT_RE = re.compile(r'[\u3000-\u303F]')

input_area = document.querySelector("#jptext")
display_total = document.querySelector("#total span")
display_kanji = document.querySelector("#kanji span")
display_hira = document.querySelector("#hiragana span")
display_kata = document.querySelector("#katakana span")

@when("input", "#jptext")
def count_text(event):
    text = input_area.value

    ignore = len(IGNORED_CHAR_RE.findall(text))
    kanji = len(KANJI_RE.findall(text))
    hiragana = len(HIRAGANA_RE.findall(text))
    katakana = len(KATAKANA_RE.findall(text))
    punctuation = len(PUNCT_RE.findall(text))

    total = (kanji + hiragana + katakana) - ignore

   # totalWithPunct = sum([punctuation, total])

    display_total.innerText = str(total)
    display_kanji.innerText = str(kanji)
    display_hira.innerText = str(hiragana)
    display_kata.innerText = str(katakana - ignore)

# Hidden clipboard
_hidden_copy_el = js.document.createElement("textarea")
_hidden_copy_el.style.position = "fixed"
_hidden_copy_el.style.left = "-9999px"
_hidden_copy_el.style.top = "0"
js.document.body.appendChild(_hidden_copy_el)

# Copy to clipboard
@when("click", "#total, #kanji, #hiragana, #katakana")
def handle_copy(event):
    span = event.currentTarget.querySelector("span")
    if not span: return

    text_to_copy = span.innerText

    _hidden_copy_el.value = text_to_copy
    _hidden_copy_el.select()
    js.document.execCommand("copy")

    span.innerText = "Copied!"
    def reset_text():
    span.innerText = text_to_copy
    js.setTimeout(create_proxy(reset_text), 800)
