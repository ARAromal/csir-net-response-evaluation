"""
CSIR-UGC NET Response Sheet Evaluation Script

This script evaluates CSIR-UGC NET (Life Sciences) response sheets by:
1. Parsing the official response sheet PDF
2. Parsing the official NTA answer key (ASPX/HTML)
3. Matching Question IDs and Option IDs
4. Applying section-wise marking scheme
"""

import pdfplumber
import re
from bs4 import BeautifulSoup

# --------------------------------------------------
# USER INPUT FILES (change filenames if needed)
# --------------------------------------------------
RESPONSE_SHEET_PDF = "csir_net_response_sheet.pdf"
ANSWER_KEY_HTML = "examinationservices.nic.in_ExamSys2026_KeyChallange_ChallangeAnswerKey.aspx"

# --------------------------------------------------
# STEP 1: Parse response sheet PDF
# Extract: Question Number -> (Question ID, Chosen Option)
# --------------------------------------------------
def parse_response_sheet(pdf_path):
    responses = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            # Split by question number (Q.1, Q.2, ...)
            blocks = re.split(r"Q\.(\d+)", text)[1:]

            for i in range(0, len(blocks), 2):
                qno = int(blocks[i])
                block = blocks[i + 1]

                qid_match = re.search(r"Question ID\s*:\s*(\d+)", block)
                chosen_match = re.search(r"Chosen Option\s*:\s*(\d)", block)

                if qid_match:
                    qid = qid_match.group(1)
                    chosen = int(chosen_match.group(1)) if chosen_match else None
                    responses[qno] = (qid, chosen)

    return responses


# --------------------------------------------------
# STEP 2: Parse answer key HTML
# Extract: Question ID -> Correct Option Number
# --------------------------------------------------
def parse_answer_key(html_path):
    final_answer_key = {}

    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "lxml")

    for row in soup.find_all("tr"):
        cols = [c.get_text(strip=True) for c in row.find_all("td")]

        # Expected structure:
        # [Qno, Subject, QuestionID, CorrectOptionID, OptionIDs...]
        if len(cols) >= 5 and cols[1] == "LIFE SCIENCES":
            qid = cols[2]
            correct_option_id = cols[3]

            # Extract all option IDs (10-digit numbers)
            option_ids = re.findall(r"\d{10}", cols[4])

            if correct_option_id in option_ids:
                correct_option_number = option_ids.index(correct_option_id) + 1
                final_answer_key[qid] = correct_option_number

    return final_answer_key


# --------------------------------------------------
# STEP 3: Score calculation
# --------------------------------------------------
def calculate_score(responses, answer_key):
    correct_1_70 = wrong_1_70 = 0
    correct_71_145 = wrong_71_145 = 0

    for qno, (qid, chosen) in responses.items():
        if chosen is None or qid not in answer_key:
            continue

        if chosen == answer_key[qid]:
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

    return correct_1_70, wrong_1_70, correct_71_145, wrong_71_145, score


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------
if __name__ == "__main__":
    print("Parsing response sheet...")
    responses = parse_response_sheet(RESPONSE_SHEET_PDF)
    print(f"Total questions parsed: {len(responses)}")

    print("Parsing answer key...")
    answer_key = parse_answer_key(ANSWER_KEY_HTML)
    print(f"Life Sciences answers mapped: {len(answer_key)}")

    print("Calculating score...")
    c1, w1, c2, w2, total_score = calculate_score(responses, answer_key)

    print("\n===== CSIR NET SCORE =====")
    print(f"Correct (Q1–70)   : {c1}")
    print(f"Wrong   (Q1–70)   : {w1}")
    print(f"Correct (Q71–145) : {c2}")
    print(f"Wrong   (Q71–145) : {w2}")
    print("--------------------------")
    print(f"TOTAL SCORE       : {total_score:.2f} / 200")
