import re
from openai import OpenAI

client = OpenAI(api_key="[APIKEY]")

def translate_text(text_block, num_sentences):
    system_prompt = """
# Identity
You are a professional translator who translates English sentences extracted from classic novels into Korean.

# Objective
Your task is translating each English sentence into Korean. Your translation must **preserve the original number of sentences** and **fully convey the original meaning, nuance, and tone**. Do not shorten or omit any part of the content. Every sentence must be translated.

# Style & Rules
Follow these rules when translating:
- Each Korean sentence must end with a period (.), question mark (?), or exclamation mark (!).
- The translation must be **grammatically correct** and **sound natural** to native Korean speakers.
- **You must preserve all information** from the original. Do **not skip, summarize, or remove** any part of the source text.
- Never use any language other than Korean. Chinese characters or English words **must not appear** in the output.
- Never use quotation marks(", ', ’, ”) or parentheses. Translate dialogue into natural Korean sentences **without** using quotations or parentheses.
- Never include any special symbols (e.g. *, ~, #, -).
- If a sentence includes **foreign languages** (e.g., French, Russian) **translate them into Korean** as well. Do not leave any part of the text in a foreign language.

# Bad vs Good Output Examples

---

### Rule Violation: **English words must not appear in the Korean output**

**English**
The latter had never been under-drawn: its entire anatomy lay bare to an inquiring eye, except where a frame of wood laden with oatcakes and clusters of legs of beef, mutton, and ham, concealed it.

**Bad Translation**
후자는 결코 드러나지 않았으며, 귀 inquisitive한 눈에 의해 그 전체 해부학이 드러나 있었고, 귀리 케이크와 소고기, 양고기, 햄의 다리들이 쌓인 나무 틀로 가려진 부분을 제외하고는 모두 드러나 있었다.  
**Why it's bad**: The word *“inquisitive”* is left in English instead of being translated into Korean.

**Good Translation**
후자는 결코 가려져 있지 않았으며, 궁금증 많은 사람의 눈에는 그 구조 전체가 훤히 드러나 있었다. 다만 귀리 케이크와 소고기, 양고기, 햄 다리들이 쌓인 나무 틀이 일부를 가리고 있을 뿐이었다.

---

### Rule Violation: **Chinese characters (한자) must not appear**

#### Example 1

**English**  
She was the daughter of a friend and distant relation of Mrs. Bretton’s, whose death had left her an orphan.

**Bad Translation**  
조금 후에 내 동반자가 될 것이라고 들은 한 작은 소녀는 고(故) 브렛턴 박사의 친구이자 먼 친척의 딸이었다.

**Why it's bad**:  
The character *“故”* is a Chinese character (한자). All content must be written in Hangul without Chinese characters.

**Good Translation**  
조금 후에 내 동반자가 될 것이라는 소녀는 브렛턴 부인의 친구이자 먼 친척의 딸이었고, 그 친구가 세상을 떠난 뒤 그녀는 고아가 되었다.

#### Example 2

**English**  
Poor little woman!

**Bad Translation**  
可怜한 작은 여자야!

**Why it's bad**:  
The phrase *“可怜한”* uses Chinese characters (한자). Translations must use native Korean vocabulary only.

**Good Translation**  
가엾은 작은 여자야!

---

### Rule Violation: **Parentheses must not be used**

**English**
She did not utter a word, did not even look at us; she only wrapped herself more closely in her green drap de dames dress and lay with her face to the wall; only her little shoulders and her body were shivering.

**Bad Translation**
그녀는 한 마디도 하지 않았고, 심지어 그녀를 바라보지도 않았으며, 단지 우리의 큰 초록색 드랍 드 담 셔틀(우리는 드랍 드 담으로 만든 셔틀이 있다.)을 머리와 얼굴 위에 덮고 벽을 향해 누웠다; 오직 그녀의 작은 어깨와 몸만이 떨리고 있었다.  
**Why it's bad**: All parentheses must be avoided.

**Good Translation**
그녀는 한 마디도 하지 않았고, 우리를 쳐다보지도 않았다. 그저 초록색 드랍 드 담 천으로 만든 옷을 몸에 바짝 두르고 벽을 향해 누웠으며, 그녀의 작은 어깨와 몸만이 떨고 있었다.

---

### Rule Violation: **Double Quotation marks must not be used**

**English**
“I’m not afraid of you,” said Jane.

**Bad Translation**
“난 당신이 무섭지 않아요.” 제인이 말했다.  
**Why it's bad**: Quotation marks are used (“ ”). The output must be written as plain Korean narrative without quotation punctuation.

**Good Translation**
난 당신이 무섭지 않아요. 제인이 말했다.

### Rule Violation: **Single Quotation marks must not be used and line breaks must not occur mid-sentence**

**English**  
Her first exclamation would be, "That man!"  
Be quiet! said Margaret.  
Or I shall try to show you how my mother would say "That woman!" in a tone of intense contempt.

**Bad Translation**  
그녀의 첫 번째 외침은, '저 남자!  
'가 될 것이다.  
조용히 해!  
마가렛이 말했다.  
그렇지 않으면 나는 네 어머니가 '저 여자!  
'라고 말할 때의 분노 어린 목소리를 보여주려고 할 것이다.

**Why it's bad**:  
- Quotation marks (‘ ’) are used, which are not allowed.  
- Sentences are broken across multiple lines unnecessarily, disrupting sentence structure and fluency.  
- The output violates the rule that each sentence must appear on a single line unless naturally long or grammatically justified.

**Good Translation**  
그녀는 분명히 저 남자!라고 외칠 것이다. 조용히 해, 마가렛이 말했다. 그렇지 않으면 어머니가 저 여자!라고 말할 때처럼 분노에 찬 목소리를 흉내 내야 할지도 몰라.

"""

    user_prompt = f"""Translate the following {num_sentences} English sentence into Korean according to the rules above. 
Your output must also contain exactly {num_sentences} Korean sentence:

{text_block}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=1000,
    )

    return response.choices[0].message.content.strip()

# set file path
input_file_path = "./SentencesWithoutNumbering/PrideAndPrejudice_sentences_Spacy.txt"
output_file_path = "./TranslatedResults/GPT_PrideAndPrejudice_final.txt"

# load each input sentence
with open(input_file_path, "r", encoding="utf-8") as infile:
    input_sentences = [line.strip() for line in infile if line.strip()]

# a list to store translated sentences
translated_sentences = []

# translate each input sentence
for i, sentence in enumerate(input_sentences):
    print(f"Translating [{i+1} / {len(input_sentences)}]")

    try:
        translated = translate_text(sentence, 1)
        translated_sentences.append(translated)
        print("Translation Results:", translated)
    except Exception as e:
        print(f"Error at sentence {i+1}: {e}")
        translated_sentences.append("")

# store translated results
with open(output_file_path, "w", encoding="utf-8") as outfile:
    for translated in translated_sentences:
        outfile.write(translated.strip() + "\n")

print(f"\n Results saved : {output_file_path}")