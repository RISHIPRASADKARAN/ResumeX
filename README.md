# ResumeX

## AI Powered Resume Analysis and Job Compatibility Platform

ResumeX is an AI powered resume analysis platform that evaluates how well a candidate's resume matches a target job description.

The application extracts resume content, analyzes job compatibility, identifies matched and missing skills, evaluates resume quality, and provides practical recommendations to improve the resume before applying.

## Project Overview

Finding the right job is only one part of the application process. Candidates also need to understand whether their resume actually matches the requirements of a specific role.

ResumeX provides a simple interface where users can upload their resume and paste a job description. The system then analyzes both documents and generates an overall compatibility score.

## Key Features

- Resume upload using PDF, DOCX, or TXT
- OCR support for scanned or image based PDF resumes
- Job description analysis
- NLP based resume and job description similarity
- Technical skill extraction
- Matched skill identification
- Missing skill identification
- Resume quality evaluation
- Overall job compatibility score
- Score breakdown
- Personalized improvement recommendations
- Netflix inspired dark user interface
- Streamlit based web application
- Public cloud deployment

## How ResumeX Works

```text
Resume Upload
      |
      v
Resume Text Extraction
      |
      +----> Normal PDF/DOCX/TXT extraction
      |
      +----> OCR for scanned PDF
      |
      v
Resume Processing
      |
      +----> Skill Extraction
      |
      +----> Resume Quality Analysis
      |
      v
Job Description Processing
      |
      +----> Required Skill Detection
      |
      +----> NLP Similarity Analysis
      |
      v
Compatibility Calculation
      |
      v
Matched Skills + Missing Skills
      |
      v
Recommendations

Scoring Method

ResumeX calculates the overall compatibility score using three major components:

| Component      | Weight |
| -------------- | -----: |
| NLP Similarity |    35% |
| Skill Match    |    50% |
| Resume Quality |    15% |

The final score is calculated from the weighted combination of these components.

Technology Stack
Programming Language
Python
Machine Learning / NLP
Scikit-learn
TF-IDF Vectorization
Cosine Similarity
Document Processing
PyPDF
Python-docx
PyMuPDF
Tesseract OCR
Pillow
Web Application
Streamlit
HTML
CSS
Deployment
Streamlit Community Cloud
Version Control
Git
GitHub
Project Structure
ResumeX/
│
├── app.py
├── requirements.txt
├── packages.txt
└── README.md
Installation

Clone the repository:

git clone https://github.com/RISHIPRASADKARAN/ResumeX.git

Move into the project directory:

cd ResumeX

Install the required Python packages:

pip install -r requirements.txt
Run Locally

Start the Streamlit application:

streamlit run app.py

The application will open in your browser.

Usage
Step 1

Upload your resume in PDF, DOCX, or TXT format.

Step 2

Paste the complete job description into the job description field.

Step 3

Click:

ANALYZE RESUME
Step 4

Review the generated analysis:

Overall compatibility score
NLP similarity
Skill match
Resume quality
Matched skills
Missing skills
Recommendations
OCR Support

ResumeX supports scanned PDF resumes using OCR.

If a PDF does not contain selectable text, the system can process the document as an image and extract the text using Tesseract OCR.

Project Outcomes

ResumeX helps candidates:

Understand their resume's compatibility with a target role
Identify important missing technical skills
Improve resume content
Prioritize skills before applying
Understand the difference between resume quality and job specific matching
Future Improvements

Potential future versions can include:

Large Language Model based resume feedback
ATS keyword optimization
Job recommendation system
Multiple job comparison
Resume section level scoring
Resume rewriting suggestions
LinkedIn profile analysis
Industry specific skill recommendations
Resume version tracking
Authentication and user profiles
Live Demo

ResumeX is deployed using Streamlit Community Cloud.

Add your live application URL here:

YOUR_STREAMLIT_APP_URL
Project Author

Rishi Prasad Karan

B.Tech Computer Science and Engineering

License

This project is created for academic, learning, and portfolio purposes.



### One important thing


At the bottom you'll see:


```text
YOUR_STREAMLIT_APP_URL


      v
Final Resume Analysis
