# Personal Articles Build System

## Overview

This project provides an automated build system that converts DOCX technical articles into a complete HTML website. The system features comprehensive processing control to prevent reprocessing and ensure efficient builds.

**Author:** Christian Mulato  
**Purpose:** Technical blog with articles on Java development, software architecture, and modern technology  
**Status:** Production ready with 59 processed articles

## System Architecture

### Core Components

The build system is organized in a modular structure under `scr/build_system/`:

```
build_system/
├── core/                           # Core processing modules
│   ├── docx_converter.py          # DOCX to Markdown converter
│   ├── md_to_html.py             # Markdown to HTML converter  
│   └── site_builder.py           # Complete site builder
├── utils/                          # Utility modules
│   ├── file_manager.py           # File system operations
│   ├── normalizer.py             # Name normalization
│   └── processed_articles_manager.py  # Processing control
├── config/
│   └── settings.py               # Centralized configuration
├── build.py                      # Main build script
├── processed_articles.txt        # Processing control list
└── build.log                     # Build operation logs
```

### Processing Pipeline

1. **DOCX Conversion**: Extracts content and media from DOCX files using Pandoc
2. **Markdown Processing**: Converts DOCX to clean Markdown with proper formatting
3. **HTML Generation**: Transforms Markdown to HTML with syntax highlighting
4. **Site Building**: Generates complete website with responsive CSS and navigation
5. **Asset Management**: Handles images, stylesheets, and other media files

## Article Processing Control System

### Control Mechanism

The system implements rigorous control to prevent article reprocessing:

- **processed_articles.txt**: Contains 59 processed articles in normalized format
- **Incremental Builds**: Only processes articles NOT in the control list
- **Automatic Updates**: Adds articles to list after successful processing

### Key Features

**Complete Overlap Prevention**
- Articles in the control list are never reprocessed
- 100% protection against file conflicts
- Granular control per individual article

**Maximum Efficiency**  
- Incremental builds process only new articles
- Optimized processing time
- Preserved computational resources

**Total Flexibility**
- Selective reprocessing when needed  
- Synchronization with actual file state
- Simple management commands

**Operational Robustness**
- Persistent list across executions
- Detailed operation logging
- Automatic integrity validation

### Management Commands

The `processed_articles_manager.py` utility provides complete list management:

```bash
# View detailed status
python -m utils.processed_articles_manager status

# Remove article for reprocessing
python -m utils.processed_articles_manager remove article_name

# Synchronize with existing HTML files
python -m utils.processed_articles_manager sync

# List all processed articles
python -m utils.processed_articles_manager list

# Manually add article
python -m utils.processed_articles_manager add article_name
```

## Usage

### Daily Operations

**Check System Status**
```bash
cd c:\dev\personal_articles\scr\build_system
python build.py --status
```

**Process Only New Articles (Recommended)**
```bash
python build.py --new-only
```

**Full Build (All Articles)**
```bash
python build.py
```

### Reprocessing Specific Articles

1. Remove from control list:
```bash
python -m utils.processed_articles_manager remove article_name
```

2. Run incremental build:
```bash
python build.py --new-only
```

The system automatically:
- Detects article not in list
- Processes: DOCX → MD → HTML
- Adds back to list after success

## Dependencies

### Required Software
- Python 3.x
- Pandoc (for DOCX conversion)

### Python Packages
- markdown
- pygments  
- python-docx
- beautifulsoup4

## Installation and Setup

1. Ensure Pandoc is installed on your system
2. Install Python dependencies: `pip install -r requirements.txt`
3. Navigate to build system: `cd scr/build_system`
4. Run initial build: `python build.py`

The system will automatically validate dependencies and directory structure on first run.

## Project Structure

```
personal_articles/
├── articles/                       # Generated HTML articles
├── assets/css/                     # Site stylesheets
├── docx/                          # Source DOCX files (59 files)
├── md/                            # Generated Markdown files
├── scr/build_system/              # Build system (current)
├── old_scripts/                   # Legacy scripts (backup)
└── index.html                     # Site homepage
```

## System Migration and Cleanup

### Legacy Script Management

21 previous build scripts were systematically organized:
- **Relocated**: Moved to `old_scripts/` directory as backup
- **Documented**: Each script's purpose catalogued
- **Preserved**: All functionality maintained for reference

### Modular Benefits

- **Maintainability**: Clean separation of concerns
- **Extensibility**: Easy to add new features
- **Reliability**: Centralized error handling and logging
- **Performance**: Optimized processing pipeline

## Current Status

### Processing Statistics
- Total DOCX files: 59
- Articles processed: 59
- Awaiting processing: 0

**System State**: All articles currently processed and up to date

## Content Overview

This blog contains technical articles covering:

- **Java & Spring**: Advanced development, Spring Boot, Jakarta EE
- **Software Architecture**: Microservices, Clean Architecture, Design Patterns
- **DevOps**: Docker, Kubernetes, CI/CD, Automation
- **APIs**: REST, GraphQL, OpenAPI, Documentation
- **Testing**: TDD, Unit Testing, Integration
- **AI & Technology**: Artificial Intelligence applied to development

### Content Distribution

- Java & Spring: 35 articles (58%)
- Software Architecture: 12 articles (20%)
- DevOps & Containers: 8 articles (13%)
- AI & Technology: 5 articles (9%)

## Features

### Dark/Light Theme System

The site includes a complete theme switching system:

**Main Features**
- Intuitive toggle button in upper right corner
- Automatic persistence between sessions
- Responsive design for desktop and mobile
- Smooth transitions with 0.3s animations
- System preference auto-detection

**Technical Implementation**
- CSS Variables for easy maintenance
- LocalStorage for user preference persistence
- Media Queries for system preference detection
- ARIA Labels for accessible buttons

**Color Palette**

| Element | Light Theme | Dark Theme |
|---------|-------------|------------|
| Primary Background | `#ffffff` | `#111827` |
| Secondary Background | `#f9fafb` | `#1f2937` |
| Primary Text | `#1f2937` | `#f9fafb` |
| Secondary Text | `#6b7280` | `#d1d5db` |
| Accent Color | `#2563eb` | `#3b82f6` |

## Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Build & Processing
- Python
- Markdown
- Pygments for syntax highlighting
- Python Markdown for processing

### Tools
- Mammoth: DOCX → Markdown conversion
- Highlight.js: Frontend syntax highlighting
- Inter Font: Modern typography

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## About the Author

**Christian Mulato**  
Senior Java Developer & Software Architect

**Specialties:**
- Java/Spring Boot: Enterprise application development
- Microservices: Distributed and scalable architecture
- DevOps: Docker, Kubernetes, CI/CD
- REST APIs: Design and documentation with OpenAPI
- Testing: TDD, integration and unit testing
- AI: Artificial Intelligence applied to software development

This build system provides reliable, efficient, and controlled processing of technical articles from DOCX source files into a complete responsive website.
