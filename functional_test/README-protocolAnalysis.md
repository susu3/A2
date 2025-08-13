# Protocol Analysis Test Suite

## 🚀 Quick Start

### Prerequisites
1. **Set up your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Install dependencies (if not already installed):**
   ```bash
   sudo apt install build-essential libcurl4-openssl-dev libjson-c-dev libpcre2-dev
   ```

### Run the Test
```bash
cd functional_test

# Quick test (MODBUS protocol with verification & update)
make -f Makefile.analysis_update test

# Test all protocols
make -f Makefile.analysis_update test-all
```

### View Results
- **JSON files**: Use any text editor or online JSON viewer
- **TXT files**: Use any text editor  
- **MMD files**: Copy content to [Mermaid Live Editor](https://mermaid.live/)

---

## 📖 Comprehensive Documentation

This directory contains test applications for the protocol analysis functionality in AFL-ICS, including both basic analysis and advanced analysis with verification and updating capabilities.

## Test Applications

### 1. Advanced Protocol Analysis with Verification and Update (Recommended)

**What it does:**
1. **Phase 1**: Generates initial protocol files (JSON, TXT, MMD)
2. **Phase 2**: Uses LLM verification to check quality and creates improved versions if issues are found

**Building:**
```bash
make -f Makefile.analysis_update
```

**Running:**
```bash
# Single protocol tests
make -f Makefile.analysis_update test-modbus     # Test MODBUS
make -f Makefile.analysis_update test-iec104     # Test IEC104  
make -f Makefile.analysis_update test-slmp       # Test SLMP
make -f Makefile.analysis_update test-ethernetip # Test EthernetIP

# Run all protocols
make -f Makefile.analysis_update test-all

# Manual testing
./protocol-analyzer-update <protocol_name> <spec_file_path> <output_dir>
```

**Generated Files:**

*Initial generation:*
- `{PROTOCOL}_message.json`: Protocol message grammar
- `{PROTOCOL}_message.txt`: Additional protocol constraints
- `{PROTOCOL}_fsm.mmd`: Protocol state machine

*After verification (if updates needed):*
- `new_{PROTOCOL}_message.json`: Improved protocol grammar
- `new_{PROTOCOL}_message.txt`: Improved additional constraints  
- `new_{PROTOCOL}_fsm.mmd`: Improved state machine

### 2. Basic Protocol Analysis (Legacy)

**What it does:** Generates protocol analysis files without verification or updating.

**Building:**
```bash
make -f Makefile.test
```

**Running:**
```bash
make -f Makefile.test test
./protocol-analyzer <protocol_name> <spec_file_path> <output_dir>
```

## Available Protocol Specifications

- **MODBUS**: `../sample_specs/Markdown/modbus.md`
- **IEC104**: `../sample_specs/Markdown/IEC104.md`  
- **SLMP**: `../sample_specs/Markdown/slmp.md`
- **EthernetIP**: `../sample_specs/Markdown/ethernetip.md`

## Output Structure

```
functional_test/
├── modbus_output/
│   ├── MODBUS_message.json
│   ├── MODBUS_message.txt
│   ├── MODBUS_fsm.mmd
│   ├── new_MODBUS_message.json    (if updated)
│   ├── new_MODBUS_message.txt     (if updated)
│   └── new_MODBUS_fsm.mmd         (if updated)
├── iec104_output/
├── slmp_output/
├── ethernetip_output/
└── test_output/                   (basic test)
```

## Cleanup

```bash
# Clean binaries only
make -f Makefile.test clean
make -f Makefile.analysis_update clean

# Clean output directories only (advanced test)
make -f Makefile.analysis_update clean-output

# Clean everything (binaries + output)
make -f Makefile.analysis_update clean-all
```

## Technical Details

### Verification Process
1. **Grammar Verification**: Checks JSON structure completeness and TXT constraint accuracy
2. **State Machine Verification**: Validates state connectivity, transitions, and protocol compliance
3. **Automatic Update**: Generates improved versions based on LLM feedback if issues detected

### LLM Integration
- Uses OpenAI GPT-4 for analysis and verification
- Temperature settings optimized for consistency (0.2 for verification, 0.5 for generation)
- Retry logic for robust API interaction

## Troubleshooting

### Common Issues

1. **OpenAI API errors**: Ensure your API key is valid and has sufficient credits
2. **Missing dependencies**: Install all required libraries as shown in Prerequisites
3. **File permissions**: Ensure write permissions for output directories
4. **Network connectivity**: Required for OpenAI API calls

### Debug Information

Both test applications provide verbose output showing:
- API request status
- File generation progress  
- Verification results
- Update status

---

*For more details about the AFL-ICS project, see the main repository documentation.* 