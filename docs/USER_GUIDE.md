# Data Extraction Tool - User Guide

**Version**: 1.0.0
**Status**: Production Ready
**For**: Non-technical users (Auditors)
**Last Updated**: 2025-10-30

---

## What is This Tool?

The Data Extraction Tool helps you extract content from documents (Word, PDF, PowerPoint, Excel) and convert them into formats that AI systems can easily process. Think of it as a translator that takes your documents and creates well-organized versions that computers can understand.

---

## Quick Start

### Installation

```bash
pip install data-extractor-tool
```

### Your First Extraction

Extract a Word document to JSON format:

```bash
data-extract extract my-document.docx
```

This will create `my-document.json` in the same folder.

---

## Commands

### Extract a Single File

**Purpose**: Process one document at a time

**Basic Usage**:
```bash
data-extract extract document.docx
```

**With Custom Output**:
```bash
data-extract extract document.docx --output results/output.json
```

**Different Formats**:
```bash
# JSON format (default)
data-extract extract document.pdf --format json

# Markdown format (readable text)
data-extract extract document.pdf --format markdown

# All formats at once
data-extract extract document.pdf --format all
```

**Replace Existing Files**:
```bash
data-extract extract document.docx --force
```

---

### Process Multiple Files (Batch)

**Purpose**: Process many documents at once

**Process Entire Folder**:
```bash
data-extract batch ./my-documents/ --output ./results/
```

**Process Only Specific File Types**:
```bash
# Only PDF files
data-extract batch ./my-documents/ --pattern "*.pdf" --output ./results/

# Only Word documents
data-extract batch ./my-documents/ --pattern "*.docx" --output ./results/
```

**Faster Processing (More Workers)**:
```bash
data-extract batch ./my-documents/ --output ./results/ --workers 8
```

**Process Specific Files**:
```bash
data-extract batch file1.docx file2.pdf file3.pptx --output ./results/
```

---

### Progress Tracking

The tool shows real-time progress as it processes files, helping you understand what's happening and how long operations will take.

**During Single File Processing** you'll see:
- Current stage (extraction → processing → formatting)
- Progress bar with percentage complete
- Estimated time remaining

**During Batch Processing** you'll see:
- Overall progress across all files
- Which file is currently being processed
- File count (e.g., "3/10 files complete")
- Estimated time remaining for entire batch

**Control Progress Display**:
```bash
# Normal mode (show progress)
data-extract extract document.pdf

# Quiet mode (no progress, minimal output)
data-extract --quiet extract document.pdf

# Verbose mode (detailed progress with stage information)
data-extract --verbose extract document.pdf
```

**Progress Output Example**:
```
Processing file: my-document.pdf
⠋ Processing my-document.pdf ████████████████████ 65% 0:00:08

Processing 5 files...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60% (3/5 files) 0:00:12
```

---

### Check Version

**See What Version You Have**:
```bash
data-extract version
```

**See Detailed Information**:
```bash
data-extract version --verbose
```

---

### Check Configuration

**Show Current Settings**:
```bash
data-extract config show
```

**Validate Configuration File**:
```bash
data-extract --config my-config.yaml config validate
```

**See Where Config File Is**:
```bash
data-extract config path
```

---

## Configuration

### Using a Configuration File

You can customize how the tool behaves by creating a configuration file. This lets you control extraction settings, output formats, logging, and more.

**Create Your Config File**:
```bash
# Copy the template
cp config.yaml.example config.yaml

# Edit it with your preferred text editor
notepad config.yaml  # Windows
nano config.yaml     # Linux/Mac
```

**Use Your Config File**:
```bash
data-extract --config config.yaml extract document.docx
```

### What You Can Configure

**Extraction Settings**: Control how each file type is processed
- **Word**: Paragraph length limits, empty paragraph handling, style extraction
- **PDF**: OCR settings, image extraction, table extraction
- **PowerPoint**: Speaker notes, image extraction, empty slide handling
- **Excel**: Row/column limits, formula inclusion, chart metadata

**Output Settings**: Control how results are formatted
- **JSON**: Hierarchical structure, pretty printing, indentation
- **Markdown**: Frontmatter, heading offsets, metadata comments
- **Chunked Text**: Token limits, context headers, chunk overlap

**Logging**: Control what information is recorded
- Log level (DEBUG, INFO, WARNING, ERROR)
- Log format (JSON or text)
- File and console output

**Performance**: Control processing behavior
- Number of parallel workers
- Maximum file size
- Progress tracking

### Configuration Examples

**Example 1: Development Settings**
```yaml
# config-dev.yaml
logging:
  level: DEBUG
  handlers:
    console:
      enabled: true

extractors:
  pdf:
    use_ocr: false  # Skip slow OCR during testing
```

**Example 2: Production Settings**
```yaml
# config-prod.yaml
logging:
  level: WARNING
  format: json
  handlers:
    file:
      enabled: true
      path: /var/log/extractor/app.log

pipeline:
  max_workers: 8
  max_file_size_mb: 500
```

**Example 3: Fast Batch Processing**
```yaml
# config-fast.yaml
logging:
  level: ERROR

pipeline:
  show_progress: false  # For automated scripts
  max_workers: 16

extractors:
  pdf:
    ocr_dpi: 150  # Faster OCR with lower quality

formatters:
  json:
    pretty_print: false  # Smaller file size
```

### Environment Variables

You can override any configuration setting using environment variables with the `DATA_EXTRACTOR_` prefix. This is useful for temporary changes or automated scripts:

**Windows**:
```cmd
set DATA_EXTRACTOR_LOGGING_LEVEL=DEBUG
data-extract extract document.docx
```

**Linux/Mac**:
```bash
export DATA_EXTRACTOR_LOGGING_LEVEL=DEBUG
data-extract extract document.docx
```

**Common Environment Variables**:
- `DATA_EXTRACTOR_LOGGING_LEVEL`: Set log level (DEBUG, INFO, WARNING, ERROR)
- `DATA_EXTRACTOR_EXTRACTORS_PDF_USE_OCR`: Enable/disable OCR (true/false)
- `DATA_EXTRACTOR_PIPELINE_MAX_WORKERS`: Set number of parallel workers (e.g., 8)
- `DATA_EXTRACTOR_EXTRACTORS_PDF_TESSERACT_CMD`: Path to tesseract executable

**Example - Fast batch processing**:
```bash
# Windows
set DATA_EXTRACTOR_PIPELINE_MAX_WORKERS=8
data-extract batch documents/

# Linux/Mac
DATA_EXTRACTOR_PIPELINE_MAX_WORKERS=8 data-extract batch documents/
```

---

## Common Workflows

### Workflow 1: Extract Single Audit Report

You have one audit report in Word format and need to extract it to JSON:

```bash
data-extract extract "Q3 Audit Report.docx" --output results/q3-audit.json
```

### Workflow 2: Process All Documents in Folder

You have a folder with 50 audit documents in various formats:

```bash
data-extract batch ./audit-docs/ --output ./extracted/ --workers 4
```

This will:
- Process all supported files in `./audit-docs/`
- Use 4 parallel workers for speed
- Save results to `./extracted/`
- Show progress bar as it works

### Workflow 3: Extract Only PDFs to Markdown

You want readable Markdown files from all PDFs:

```bash
data-extract batch ./reports/ --pattern "*.pdf" --format markdown --output ./markdown-reports/
```

### Workflow 4: Prepare Multiple Format Outputs

You need both JSON and Markdown for analysis:

```bash
data-extract extract important-doc.docx --format all --output ./outputs/
```

This creates:
- `important-doc.json`
- `important-doc.md`
- `important-doc.txt` (chunked text)

---

## Understanding the Output

### JSON Format

Structured data with all content organized:

```json
{
  "document_metadata": {
    "file_name": "report.docx",
    "author": "John Doe",
    "created_at": "2025-01-15"
  },
  "content_blocks": [
    {
      "type": "heading",
      "content": "Executive Summary",
      "level": 1
    },
    {
      "type": "paragraph",
      "content": "This report covers..."
    }
  ]
}
```

### Markdown Format

Human-readable text format:

```markdown
# Executive Summary

This report covers the Q3 audit findings...

## Key Findings

1. First finding
2. Second finding
```

### Chunked Text Format

Text split into manageable chunks for AI processing:

```
[Chunk 1 of 5]
This is the first section...

[Chunk 2 of 5]
Continuing with...
```

---

## Supported File Formats

| Format      | Extension | Description           |
|-------------|-----------|------------------------|
| Word        | .docx     | Microsoft Word        |
| PDF         | .pdf      | PDF documents         |
| PowerPoint  | .pptx     | Presentations         |
| Excel       | .xlsx     | Spreadsheets          |
| Text        | .txt, .md, .log | Plain text, Markdown, logs |

---

## Troubleshooting

### Error: "File not found"

**Problem**: The file path you specified doesn't exist

**Solution**:
1. Check the file name spelling
2. Make sure you're in the right folder
3. Use the full path: `C:\Users\YourName\Documents\file.docx`

### Error: "Format not supported"

**Problem**: The file type isn't recognized

**Solution**:
- Make sure the file has the correct extension (.docx, .pdf, etc.)
- Check that the file isn't corrupted (try opening it normally)
- Use a supported format (see table above)

### Error: "Cannot access file"

**Problem**: Permission issue or file is open in another program

**Solution**:
1. Close the file if it's open in Word/Excel/etc.
2. Check file permissions
3. Try copying the file to a different location

### Error: "Configuration invalid"

**Problem**: Your config file has errors

**Solution**:
```bash
# Check what's wrong
data-extract --config my-config.yaml config validate

# See current config
data-extract config show
```

### No Progress Bar Showing

**Problem**: Progress indicators not visible

**Solution**:
- This is normal in some terminals
- Use `--verbose` to see detailed progress:
  ```bash
  data-extract extract file.docx --verbose
  ```

---

## Tips for Best Results

### 1. Organize Your Files

Keep documents organized in folders:
```
audit-docs/
  ├── 2025-Q1/
  ├── 2025-Q2/
  └── 2025-Q3/
```

Then process by quarter:
```bash
data-extract batch audit-docs/2025-Q3/ --output results/2025-Q3/
```

### 2. Use Descriptive Output Names

Instead of:
```bash
data-extract extract doc.docx --output out.json
```

Use:
```bash
data-extract extract "2025-Q3-Audit.docx" --output "results/2025-Q3-Audit-Extracted.json"
```

### 3. Check One File Before Batch

Before processing 100 files, test with one:
```bash
# Test single file first
data-extract extract test-doc.docx

# If good, process all
data-extract batch ./all-docs/ --output ./results/
```

### 4. Use Worker Threads for Speed

For many files, increase workers:
```bash
# 2 workers (default, slower)
data-extract batch ./docs/ --output ./results/

# 8 workers (faster on powerful computers)
data-extract batch ./docs/ --output ./results/ --workers 8
```

**Note**: More workers = more memory used

### 5. Quiet Mode for Scripts

If running in a script or automation:
```bash
data-extract extract doc.docx --quiet
```

---

## Examples for Common Scenarios

### Scenario: Monthly Audit Report Processing

You receive 30 audit reports each month and need to extract them:

```bash
# Create monthly folder
mkdir ./extracted/2025-January/

# Process all files
data-extract batch ./incoming/2025-January/ \
  --output ./extracted/2025-January/ \
  --workers 4 \
  --format all

# Check results
ls ./extracted/2025-January/
```

### Scenario: Preparing Documents for AI Analysis

You want to send documents to an AI system:

```bash
# Extract to JSON (best for AI)
data-extract batch ./source-docs/ \
  --output ./for-ai/ \
  --format json \
  --workers 6
```

### Scenario: Creating Readable Summaries

You want human-readable versions:

```bash
# Extract to Markdown
data-extract batch ./reports/ \
  --output ./readable/ \
  --format markdown
```

### Scenario: Processing Log Files and Text Data

Extract structured data from plain text files:

```bash
# Extract single text file
data-extract extract system.log --format json

# Process multiple log/text files
data-extract batch ./logs/ --pattern "*.log" --output ./extracted-logs/

# Works with Markdown documentation too
data-extract extract README.md --format json
```

---

## Getting Help

### Command Help

For help with any command:
```bash
# General help
data-extract --help

# Extract command help
data-extract extract --help

# Batch command help
data-extract batch --help
```

### Common Options

| Option        | Short | Purpose                    |
|---------------|-------|----------------------------|
| --help        | -h    | Show help message          |
| --verbose     | -v    | Show detailed information  |
| --quiet       | -q    | Suppress progress output   |
| --output      | -o    | Specify output location    |
| --format      | -f    | Choose output format       |
| --config      | -c    | Use custom config file     |

---

## Glossary

**Extract**: Pull content out of a document

**Format**: The type of output file (JSON, Markdown, etc.)

**Batch**: Process many files at once

**Worker**: A parallel processing thread (more workers = faster)

**Pipeline**: The series of steps used to process a document

**Glob Pattern**: A way to match files (e.g., `*.pdf` means "all PDF files")

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│            QUICK REFERENCE CARD                     │
├─────────────────────────────────────────────────────┤
│ Single File:                                        │
│   data-extract extract file.docx                    │
│                                                     │
│ Batch Processing:                                   │
│   data-extract batch ./folder/ --output ./results/  │
│                                                     │
│ Only PDFs:                                          │
│   data-extract batch ./folder/ --pattern "*.pdf"    │
│                                                     │
│ Faster Processing:                                  │
│   data-extract batch ./folder/ --workers 8          │
│                                                     │
│ All Formats:                                        │
│   data-extract extract file.docx --format all       │
│                                                     │
│ Check Version:                                      │
│   data-extract version                              │
└─────────────────────────────────────────────────────┘
```

---

**Need More Help?**

- Check the documentation in `docs/` folder
- Review example files in `examples/` folder
- Contact your IT support team

**Version**: 1.0.0 | **Status**: Production Ready | **Last Updated**: 2025-10-30
