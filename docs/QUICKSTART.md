# Quick Start Guide - AI Data Extractor

Get started in 5 minutes. Extract your first document and understand the basics.

**Status**: ✅ All commands verified working (2025-10-30)

---

## 1. Install (2 minutes)

### Already have Python 3.11+?

```bash
# Install from wheel file
pip install ai_data_extractor-1.0.0-py3-none-any.whl

# Verify
data-extract --version
```

### Need Python first?

**Windows**: Download from [python.org](https://www.python.org/downloads/) and install
**Mac**: `brew install python@3.11`
**Linux**: `sudo apt install python3.11`

Then run the install command above.

---

## 2. Verify Installation Works (30 seconds)

Test that the `data-extract` command is available:

```bash
# Check version
data-extract version
# Output: Data Extraction Tool version 1.0.0

# Get help
data-extract --help
# Shows available commands: extract, batch, version, config
```

**Optional**: Run automated validation:
```bash
python scripts/validate_installation.py
# Should show: Tests passed: 8/8 - ALL TESTS PASSED ✓
```

---

## 3. Extract Your First Document (1 minute)

### Single File Extraction

```bash
# Extract a Word document
data-extract extract my-document.docx

# This creates: my-document_extracted.json
```

### View Results

```bash
# Windows
type my-document_extracted.json

# Mac/Linux
cat my-document_extracted.json
```

You'll see structured JSON with:
- Document metadata (author, dates, hash)
- Content blocks (paragraphs, headings, tables)
- Quality scores
- Statistics

---

## 4. Try Different Formats (1 minute)

### PDF Files

```bash
data-extract extract report.pdf --format markdown
# Creates: report_extracted.md (readable format)
```

### PowerPoint

```bash
data-extract extract presentation.pptx
# Extracts: slides, titles, speaker notes
```

### Excel

```bash
data-extract extract spreadsheet.xlsx
# Extracts: all sheets, cells, formulas
```

### Plain Text

```bash
data-extract extract document.txt
# Also works with: .md (Markdown), .log (log files)
```

---

## 5. Batch Processing (1 minute)

Process multiple files at once:

```bash
# Process entire folder
data-extract batch documents_folder/

# Results go to: documents_folder_output/
```

### With Options

```bash
# Markdown output, 8 parallel workers
data-extract batch documents/ --format markdown --workers 8
```

---

## 6. Common Use Cases

### Compliance Document Analysis

```bash
# Extract all compliance PDFs
data-extract batch compliance_docs/ \
  --format json \
  --output compliance_extracted/
```

### Audit Report Processing

```bash
# Process audit reports with progress tracking
data-extract batch audit_reports/ \
  --format markdown \
  --verbose
```

### Policy Document Extraction

```bash
# Extract single policy with full details
data-extract extract policy.docx \
  --format json \
  --output policy_data.json \
  --verbose
```

---

## Output Formats Explained

### JSON (Default)
- **Use for**: AI processing, data analysis, programmatic use
- **Contains**: Full metadata, structure, quality scores
- **Example**:
  ```json
  {
    "metadata": {...},
    "blocks": [{
      "type": "heading",
      "content": "Introduction",
      "level": 1
    }],
    "quality_score": 85.5
  }
  ```

### Markdown
- **Use for**: Human reading, documentation, wikis
- **Contains**: Readable text, preserved formatting
- **Example**:
  ```markdown
  # Introduction

  This is a paragraph...

  ## Section 1
  ```

### Chunked Text
- **Use for**: LLM/AI with token limits
- **Contains**: Content split into manageable chunks
- **Example**:
  ```
  === Chunk 1/5 ===
  [Content here...]

  === Chunk 2/5 ===
  [More content...]
  ```

---

## Command Cheat Sheet

### Extract Commands

```bash
# Basic extraction (creates file_extracted.json)
data-extract extract file.docx

# With custom output path
data-extract extract file.pdf --output results.json

# Different format
data-extract extract file.pptx --format markdown

# All formats at once (json, markdown, chunked)
data-extract extract file.pdf --format all

# Force overwrite without asking
data-extract extract file.docx --force

# Verbose mode (see detailed progress)
data-extract extract large-file.pdf --verbose
```

### Batch Commands

```bash
# Process folder (output directory REQUIRED)
data-extract batch folder/ --output results/

# Filter by file type with pattern
data-extract batch folder/ --pattern "*.pdf" --output results/

# Parallel processing (faster, default is 4 workers)
data-extract batch folder/ --output results/ --workers 8

# Different output format
data-extract batch folder/ --output results/ --format markdown

# Process specific files
data-extract batch file1.pdf file2.docx --output results/
```

### Configuration Commands

```bash
# Show current config
data-extract config show

# Validate config file
data-extract config validate

# Create your config file (copy the template)
cp config.yaml.example config.yaml
# Then edit config.yaml with your settings
```

### Info Commands

```bash
# Version info
data-extract --version

# Detailed version
data-extract version --verbose

# Help
data-extract --help
data-extract extract --help
```

---

## Understanding Output

### Success Indicators

```
✓ Extraction completed: file.docx
  Blocks: 156
  Quality: 87.5/100
  Time: 2.3s
```

### Quality Scores

- **90-100**: Excellent - Complete, structured content
- **70-89**: Good - Minor issues, mostly complete
- **50-69**: Fair - Some content missed or degraded
- **0-49**: Poor - Significant issues, OCR/recovery needed

### Common Block Types

- `paragraph`: Regular text paragraphs
- `heading`: Document headings (with levels)
- `table`: Structured table data
- `list_item`: Bulleted/numbered lists
- `image`: Image metadata and captions
- `code`: Code blocks or technical content

---

## Troubleshooting

### "Command not found"

```bash
# Did you activate virtual environment?
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### "Permission denied"

```bash
# Run as admin (Windows) or use sudo (Linux)
# Or install in user space:
pip install --user ai_data_extractor-1.0.0-py3-none-any.whl
```

### "Out of memory"

```bash
# Use fewer workers
data-extract batch folder/ --workers 2

# Or process files individually
```

### Poor quality scores

```bash
# For scanned PDFs, install OCR:
pip install ai-data-extractor[ocr]

# Then extract again
data-extract extract scanned.pdf --verbose
```

---

## Next Steps

### Learn More

1. **Full User Guide**: See `USER_GUIDE.md` for complete documentation
2. **Installation Options**: See `INSTALL.md` for advanced setup
3. **Configuration**: Copy `config.yaml.example` to `config.yaml` and customize

### Try Advanced Features

```bash
# Process with custom config
data-extract extract file.pdf --config my_config.yaml

# Batch with filters
data-extract batch folder/ --formats pdf --min-size 1mb --max-size 100mb

# Export in multiple formats
data-extract extract doc.docx --format json,markdown,chunked
```

### Get Help

```bash
# Built-in help for any command
data-extract extract --help

# Check system info
data-extract version --verbose

# Validate setup
data-extract config validate
```

---

## Quick Reference Card

### Most Common Commands

| Task | Command |
|------|---------|
| Extract one file | `data-extract extract file.pdf` |
| Extract to markdown | `data-extract extract file.docx --format markdown` |
| Process folder | `data-extract batch folder/` |
| Fast batch processing | `data-extract batch folder/ --workers 8` |
| Check version | `data-extract --version` |
| Get help | `data-extract --help` |

### File Support

| Format | Extensions | Features |
|--------|------------|----------|
| Word | .docx | Text, tables, images, styles |
| PDF | .pdf | Text, tables, OCR fallback |
| PowerPoint | .pptx | Slides, notes, images |
| Excel | .xlsx, .xls | Sheets, cells, formulas |
| Text | .txt, .md, .log | Plain text, markdown, logs |

### Output Options

| Format | Flag | Best For |
|--------|------|----------|
| JSON | `--format json` | AI processing, data analysis |
| Markdown | `--format markdown` | Human reading, documentation |
| Chunked | `--format chunked` | LLMs with token limits |

---

## Example Workflows

### Audit Compliance Review

```bash
# 1. Extract all audit documents
data-extract batch audit_docs/ --format json --output audit_data/

# 2. Review quality scores
cat audit_data/summary.json

# 3. Reprocess any poor quality files
data-extract extract audit_docs/poor_scan.pdf --verbose
```

### Policy Documentation

```bash
# 1. Extract policy to readable markdown
data-extract extract policy.docx --format markdown

# 2. Extract to structured JSON for analysis
data-extract extract policy.docx --format json

# 3. Create AI-ready chunks
data-extract extract policy.docx --format chunked
```

### Regulatory Framework Processing

```bash
# 1. Batch extract NIST/COBIT documents
data-extract batch frameworks/ --workers 4 --verbose

# 2. Check results
ls frameworks_output/

# 3. Review extraction log
cat frameworks_output/extraction.log
```

---

## Tips & Best Practices

### Performance

- Use `--workers` for batch processing (default: 4, try 8 for faster)
- Process similar file types together (all PDFs, then all DOCXs)
- Large files (>100MB): Process individually with `--verbose` to monitor

### Quality

- For scanned PDFs: Install OCR support (`pip install ai-data-extractor[ocr]`)
- Check quality scores in output
- Use `--verbose` to see extraction details

### Organization

- Use consistent output folders: `data-extract batch docs/ --output docs_extracted/`
- Include dates in output names: `--output results_2025-10-30/`
- Keep original files separate from extracted data

### Troubleshooting

- Start with one file before batch processing
- Use `--verbose` to see what's happening
- Check quality scores to identify problem files
- Review logs in output folders

---

## Ready to Start?

1. **Install the tool** (see section 1)
2. **Extract a test file** (see section 2)
3. **Review the output** to understand structure
4. **Process your documents** with batch command
5. **Check USER_GUIDE.md** for advanced features

Need help? Run `data-extract --help` anytime.

---

**Version**: 1.0.0 | **Updated**: 2025-10-30 | **Status**: Production Ready
