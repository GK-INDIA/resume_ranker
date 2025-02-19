
# 📁 Resume Ranker API ⚡

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/license/apache-2-0)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge)](https://opensource.org/licenses/Apache-2.0)

Automated resume ranking system with AI-powered criteria extraction and scoring capabilities.

## 🚀 Features

- 🔍 **Job Description Analysis**: Extract key ranking criteria from PDF/DOCX files
- 📊 **Resume Scoring**: Evaluate multiple resumes against custom criteria
- 💻 **REST API**: FastAPI endpoints with Swagger documentation
- 📁 **Batch Processing**: Handle multiple resumes in single request
- 📤 **Excel Output**: Generate scored results in spreadsheet format

## 📂 Repository Structure

```
resume-ranker/
├── 📄 main.py               - FastAPI application and route handlers
├── 📄 utils.py              - Helper functions for text extraction/processing
├── 📄 requirements.txt      - Python dependencies
├── 📄 .env                  - Environment variables (template)
├── 📄 README.md             - Project documentation (you are here!)
└── 📁 tests/                - Automated test cases (optional)

```

## 🔌 API Endpoints

### 1. 🧠 Extract Ranking Criteria (`POST /extract-criteria`)

**Input**:  
📤 Job description file (PDF/DOCX)

**Output**:  
```json
{
  "criteria": [
    "5+ years Python experience",
    "AWS certification required",
    "Machine Learning expertise"
  ]
}
```

### 2. 📈 Score Resumes (`POST /score-resumes`)

**Input**:  
📤 List of criteria + Multiple resume files (PDF/DOCX)

**Output**:  
📥 Excel file with scoring matrix:
```
Candidate Name | Python Experience | AWS Certification | ... | Total Score
John Doe       | 5                 | 4                 | ... | 17
```

## 🛠️ Setup Instructions

1. **Clone Repository**
   ```bash
   git clone git@github.com:GK-INDIA/resume_ranker.git
   cd resume_ranker
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   OPENAI_API_KEY = <Enter your openai API key here>
   # Add your OpenAI API key to .env
   ```

4. **Start Server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access API Documentation**  
   🌐 Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser

## 🧪 Using the API

### Via Swagger UI
1. Visit `/docs` endpoint
2. Try endpoints with sample files:
   - For `/extract-criteria`: Upload job description
   - For `/score-resumes`: Provide criteria list and upload resumes

### Via cURL
```bash
# Extract criteria
curl -X POST -F "file=@job_description.pdf" http://localhost:8000/extract-criteria

# Score resumes
curl -X POST -F "criteria='[\"Python Experience\",\"AWS Certification\"]'" \
  -F "files=@resume1.pdf" -F "files=@resume2.docx" \
  http://localhost:8000/score-resumes --output scores.xlsx
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📄 License

Apache 2.0 License - See [LICENSE](LICENSE) for details

## 📧 Contact

[![Email](https://img.shields.io/badge/Contact-Email%20Me-blue?style=for-the-badge&logo=minutemailer)](mailto:gyanprakashkonhar18@kgpian.iitkgp.ac.in)  
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/gyan-prakash-konhar-641678191/)
```
