# CSIR-UGC NET Response Sheet Evaluation (Python)

## 📌 Overview
This project automates the evaluation of CSIR-UGC NET (Life Sciences) examination response sheets using Python.  
It parses official response sheets (PDF) and answer keys (HTML/ASPX) released by NTA and computes exact scores by applying section-wise marking schemes.

## 🧠 Problem Addressed
Manual score calculation from CSIR NET response sheets is error-prone due to:
- Unstructured PDF formats
- Answer keys using Question IDs and Option IDs
- Multi-subject answer key ambiguity
- Negative marking and attempt limits

This project resolves all these issues programmatically.

## ⚙️ Methodology
1. Parse response sheet PDF to extract:
   - Question Number
   - Question ID
   - Chosen Option
2. Parse official NTA answer key (ASPX):
   - Filter Life Sciences questions
   - Map correct Option IDs to option numbers
3. Match responses with correct answers using Question IDs
4. Apply CSIR NET marking scheme:
   - Part A & B: +2 / −0.5
   - Part C: +4 / −1
5. Perform verification checks to ensure correctness

## 🛠️ Technologies Used
- Python
- pdfplumber
- BeautifulSoup (bs4)
- Regular Expressions (regex)
- HTML parsing

## 📊 Output
- Section-wise correct and wrong answers
- Final score out of 200
- Fully reproducible and verifiable results

## ⚠️ Disclaimer
This project is for educational and analytical purposes only.  
Personal exam documents are not included in this repository.

## 🚀 How to Run
```bash
pip install -r requirements.txt
python evaluate_csir_net.py
