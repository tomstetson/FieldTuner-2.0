# Test Fixtures

This directory contains test data and fixtures for FieldTuner testing.

## 📁 Files

### **`reference_values.json`**
- **Purpose**: JSON format test data for BF6 settings
- **Content**: Expected config values and testing scenarios
- **Usage**: Automated testing of config parsing and validation

### **`reference_values.txt`**
- **Purpose**: Human-readable test data for BF6 settings
- **Content**: Expected config values in text format
- **Usage**: Manual testing and validation

## 🧪 Testing Usage

### **Automated Tests**
```python
import json
from pathlib import Path

# Load test data
fixtures_dir = Path(__file__).parent
with open(fixtures_dir / "reference_values.json") as f:
    test_data = json.load(f)

# Use in tests
def test_config_parsing():
    expected_values = test_data["expected_config_keys"]
    # Test config parsing against expected values
```

### **Manual Testing**
1. **Load** `reference_values.txt` for expected values
2. **Compare** with FieldTuner's loaded values
3. **Verify** all settings match expected configuration
4. **Test** change tracking and persistence

## 📋 Test Scenarios

### **Config Loading Tests**
- Verify FieldTuner reads correct values from config files
- Test against known good configuration values
- Validate setting type conversion (int, float, bool, string)

### **Config Writing Tests**
- Test saving changes to config files
- Verify changes persist after game restart
- Test backup and restore functionality

### **UI Tests**
- Test setting controls display correct values
- Test change tracking shows old → new values
- Test preset application and customization

## 🔧 Maintenance

### **Updating Test Data**
1. **Capture** new BF6 settings from fresh profile
2. **Update** both JSON and TXT files
3. **Test** against new reference values
4. **Commit** updated fixtures

### **Adding New Fixtures**
1. **Create** new fixture file in this directory
2. **Document** purpose and usage in this README
3. **Update** tests to use new fixtures
4. **Test** new fixtures work correctly

---

**Test Fixtures** - Supporting comprehensive FieldTuner testing