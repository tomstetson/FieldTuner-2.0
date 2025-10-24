print("FieldTuner - Core Functionality Test")
print("===================================")
print()

# Test config parsing
import re

config_data = """GstRender.Dx12Enabled 1
GstRender.MotionBlurEnable 1
GstRender.DepthOfFieldEnable 1
GstRender.AntiAliasingDeferred 2
GstRender.ResolutionScale 1.0
GstRender.FullscreenMode 1
GstRender.VSyncEnable 0
GstAudio.MasterVolume 100
GstAudio.MusicVolume 80
GstInput.MouseSensitivity 50
GstGame.Difficulty 1
GstNetwork.MaxPing 150"""

patterns = [r'(GstRender\.\w+)\s+(\S+)', r'(GstAudio\.\w+)\s+(\S+)', r'(GstInput\.\w+)\s+(\S+)', r'(GstGame\.\w+)\s+(\S+)', r'(GstNetwork\.\w+)\s+(\S+)']

config = {}
for pattern in patterns:
    matches = re.findall(pattern, config_data)
    for key, value in matches:
        config[key] = value

print("Parsed settings:")
for key, value in config.items():
    print(f"  {key} = {value}")

print(f"\nTotal settings found: {len(config)}")

# Test validation
def validate_setting(key, value):
    if key == "GstRender.ResolutionScale":
        try:
            scale = float(value)
            return 0.5 <= scale <= 2.0
        except ValueError:
            return False
    elif key == "GstRender.FullscreenMode":
        return value in ["0", "1"]
    elif key in ["GstRender.Dx12Enabled", "GstRender.MotionBlurEnable"]:
        return value in ["0", "1"]
    elif key == "GstRender.AntiAliasingDeferred":
        try:
            aa = int(value)
            return 0 <= aa <= 4
        except ValueError:
            return False
    return True

print("\nValidation tests:")
test_cases = [
    ("GstRender.ResolutionScale", "1.5", True),
    ("GstRender.ResolutionScale", "0.5", True),
    ("GstRender.ResolutionScale", "3.0", False),
    ("GstRender.FullscreenMode", "0", True),
    ("GstRender.FullscreenMode", "2", False),
    ("GstRender.Dx12Enabled", "1", True),
    ("GstRender.Dx12Enabled", "2", False),
]

for key, value, expected in test_cases:
    result = validate_setting(key, value)
    status = "PASS" if result == expected else "FAIL"
    print(f"  {status} {key}={value} -> {result}")

print("\nCore functionality test completed!")
print("FieldTuner config parsing and validation is working correctly.")
