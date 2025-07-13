# Content Transformer

A content transformation system with RAG (Retrieval-Augmented Generation) capabilities that can convert content between different formats, styles, and complexity levels.

## 1. Install Requirements

```bash
pip install -r requirements.txt
```

## 2. Create Embeddings

### How to create embeddings:
Run the style examples embedding script:
```bash
python app/style_examples.py
```

This will:
- Create a ChromaDB collection with style examples
- Embed ~60 different style examples (casual, formal, academic, marketing, blog, technical)
- Store them in the vector database for RAG retrieval


## 3. Main App Usage

### How to run the main app:
```bash
python app/main.py
```

### What the app does:
The app transforms your content based on target format, tone, and complexity. It will:

1. **Analyze your input** - Detect current format and style
2. **Plan transformation** - Create a step-by-step plan
3. **Retrieve relevant examples** - Use RAG to find similar style examples
4. **Convert content** - Transform to target format
5. **Quality check** - Verify fact preservation and quality

### Example transformations:

**Input:**
```
Hi Team,
I wanted to provide a quick update on our project. We have completed about 70% of the development work, and testing is currently 40% done. Overall, we are on track and expect to reach the next milestone by the end of this week.
Please let me know if you have any questions.
Best regards,
sowjanya
```

**Command:** `Convert it into report with simple language`

**Output:**
```
PROJECT STATUS REPORT

Current Progress:
- Development: 70% complete
- Testing: 40% complete
- Overall status: On track

Timeline:
- Next milestone: End of this week

Summary:
The project is progressing well with development at 70% completion and testing at 40%. The team remains on schedule to meet the upcoming milestone deadline.
```

### Supported transformations:
- **Formats**: Email → Report, Blog → Article, Technical → Simple
- **Tones**: Casual → Formal, Academic → Marketing, Technical → Casual
- **Complexity**: Simple → Detailed, Complex → Simple, Technical → General

### What you'll get:
- **Input Analysis**: Current format and style detection
- **Style Analysis**: Detailed style breakdown
- **Transformation Plan**: Step-by-step conversion strategy
- **Converted Output**: Your content in the target format
- **Quality Assessment**: Fact preservation and quality score 