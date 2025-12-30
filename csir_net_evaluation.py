import pdfplumber
import re

responses = {}  # qno -> (qid, chosen_option_number)

with pdfplumber.open("csir_net_response_sheet.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue

        blocks = re.split(r"Q\.(\d+)", text)[1:]

        for i in range(0, len(blocks), 2):
            qno = int(blocks[i])
            block = blocks[i+1]

            qid_match = re.search(r"Question ID\s*:\s*(\d+)", block)
            chosen_match = re.search(r"Chosen Option\s*:\s*(\d)", block)

            if qid_match:
                qid = qid_match.group(1)
                chosen = int(chosen_match.group(1)) if chosen_match else None
                responses[qno] = (qid, chosen)

print("Total questions parsed:", len(responses))

from bs4 import BeautifulSoup
import re

final_answer_key = {}  # Question ID -> correct option number (1–4)

with open("examinationservices.nic.in_ExamSys2026_KeyChallange_ChallangeAnswerKey.aspx",
          "r", encoding="utf-8", errors="ignore") as f:
    soup = BeautifulSoup(f, "lxml")

for row in soup.find_all("tr"):
    cols = [c.get_text(strip=True) for c in row.find_all("td")]

    # Expected structure:
    # [Qno, Subject, QuestionID, CorrectOptionID, OptionIDs...]
    if len(cols) >= 5 and cols[1] == "LIFE SCIENCES":
        qid = cols[2]
        correct_option_id = cols[3]

        # Extract all option IDs (they are concatenated, so use regex)
        option_ids = re.findall(r"\d{10}", cols[4])

        if correct_option_id in option_ids:
            correct_option_number = option_ids.index(correct_option_id) + 1
            final_answer_key[qid] = correct_option_number

print("Life Sciences answers mapped:", len(final_answer_key))
correct_1_70 = wrong_1_70 = 0
correct_71_145 = wrong_71_145 = 0

for qno, (qid, chosen) in responses.items():
    if chosen is None or qid not in final_answer_key:
        continue

    if chosen == final_answer_key[qid]:
        if qno <= 70:
            correct_1_70 += 1
        else:
            correct_71_145 += 1
    else:
        if qno <= 70:
            wrong_1_70 += 1
        else:
            wrong_71_145 += 1

score = (2 * correct_1_70 - 0.5 * wrong_1_70) + \
        (4 * correct_71_145 - 1 * wrong_71_145)

print("===== CSIR NET SCORE =====")
print("Correct (Q1–70)   :", correct_1_70)
print("Wrong   (Q1–70)   :", wrong_1_70)
print("Correct (Q71–145) :", correct_71_145)
print("Wrong   (Q71–145) :", wrong_71_145)
print("--------------------------")
print(f"TOTAL SCORE       : {score:.2f} / 200")
