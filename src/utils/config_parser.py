"""
FieldTuner V2.0 - Config Parser
Handles all config file parsing logic with multiple fallback methods.
"""

import re
import struct
from typing import Dict, Union

from debug import log_info, log_error, log_warning, log_debug


class ConfigParser:
    """BULLETPROOF config parser with multiple fallback methods."""
    
    @staticmethod
    def parse_text_config(content: Union[str, bytes]) -> Dict[str, str]:
        """Parse text-based config content with multiple format support."""
        config = {}
        
        try:
            # Handle both string and bytes input
            if isinstance(content, bytes):
                text_content = content.decode('utf-8', errors='ignore')
            else:
                text_content = content
            
            lines = text_content.split('\n')
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('//'):
                    continue
                
                # Try space-separated format first (BF6 format: "key value")
                if ' ' in line and not '=' in line:
                    try:
                        parts = line.split(' ', 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            if key and value:
                                config[key] = value
                    except:
                        continue
                # Try equals-separated format (standard format: "key=value")
                elif '=' in line:
                    try:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        if key and value:
                            config[key] = value
                    except:
                        continue
            
            log_info(f"Text parser found {len(config)} settings", "CONFIG")
            return config
        except Exception as e:
            log_debug(f"Text parsing error: {e}", "CONFIG")
            return {}
    
    @staticmethod
    def parse_binary_config(data: bytes) -> Dict[str, str]:
        """BULLETPROOF binary config parser with comprehensive error handling."""
        config = {}
        
        try:
            # Validate data length
            if len(data) < 16:
                log_warning("Config file too short to be valid", "CONFIG")
                return config
            
            # Check for PROFSAVE header
            if not data.startswith(b"PROFSAVE"):
                log_warning("Config file doesn't start with PROFSAVE header - trying text parser", "CONFIG")
                # Try to parse as text-based config
                try:
                    text_content = data.decode('utf-8', errors='ignore')
                    return ConfigParser.parse_text_config(text_content)
                except:
                    log_warning("Text parsing also failed", "CONFIG")
                    return config
            
            # Skip header
            offset = 8
            
            # Read version (4 bytes)
            if offset + 4 > len(data):
                log_error("Config file too short for version", "CONFIG")
                return config
            version = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            log_info(f"Config version: {version}", "CONFIG")
            
            # Read settings count (4 bytes)
            if offset + 4 > len(data):
                log_error("Config file too short for settings count", "CONFIG")
                return config
            settings_count = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            log_info(f"Settings count: {settings_count}", "CONFIG")
            
            # Parse each setting
            for i in range(settings_count):
                if offset >= len(data):
                    log_warning(f"Reached end of file at setting {i}", "CONFIG")
                    break
                
                # Read key length
                if offset + 4 > len(data):
                    break
                key_len = struct.unpack('<I', data[offset:offset+4])[0]
                offset += 4
                
                # Validate key length
                if key_len > 1000 or key_len <= 0:  # Reasonable bounds
                    log_warning(f"Key length {key_len} exceeds remaining data", "CONFIG")
                    break
                
                # Read key
                if offset + key_len > len(data):
                    break
                key = data[offset:offset+key_len].decode('utf-8', errors='ignore')
                offset += key_len
                
                # Read value type (1 byte)
                if offset + 1 > len(data):
                    break
                value_type = data[offset]
                offset += 1
                
                # Read value based on type
                if value_type == 0:  # Bool
                    if offset + 1 > len(data):
                        break
                    value = bool(data[offset])
                    offset += 1
                elif value_type == 1:  # Int
                    if offset + 4 > len(data):
                        break
                    value = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                elif value_type == 2:  # Float
                    if offset + 4 > len(data):
                        break
                    value = struct.unpack('<f', data[offset:offset+4])[0]
                    offset += 4
                elif value_type == 3:  # String
                    if offset + 4 > len(data):
                        break
                    value_len = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                    if offset + value_len > len(data):
                        break
                    value = data[offset:offset+value_len].decode('utf-8', errors='ignore')
                    offset += value_len
                elif value_type == 4:  # Double (8 bytes)
                    if offset + 8 > len(data):
                        break
                    value = struct.unpack('<d', data[offset:offset+8])[0]
                    offset += 8
                elif value_type == 5:  # Long (8 bytes)
                    if offset + 8 > len(data):
                        break
                    value = struct.unpack('<Q', data[offset:offset+8])[0]
                    offset += 8
                elif value_type == 6:  # Short (2 bytes)
                    if offset + 2 > len(data):
                        break
                    value = struct.unpack('<H', data[offset:offset+2])[0]
                    offset += 2
                elif value_type == 7:  # Byte
                    if offset + 1 > len(data):
                        break
                    value = data[offset]
                    offset += 1
                elif value_type == 8:  # Char
                    if offset + 1 > len(data):
                        break
                    value = chr(data[offset])
                    offset += 1
                elif value_type == 9:  # Bool array
                    if offset + 4 > len(data):
                        break
                    array_len = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                    if offset + array_len > len(data):
                        break
                    value = [bool(data[offset + j]) for j in range(array_len)]
                    offset += array_len
                elif value_type == 10:  # Int array
                    if offset + 4 > len(data):
                        break
                    array_len = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                    if offset + array_len * 4 > len(data):
                        break
                    value = [struct.unpack('<I', data[offset + j*4:offset + j*4 + 4])[0] for j in range(array_len)]
                    offset += array_len * 4
                elif value_type == 11:  # Float array
                    if offset + 4 > len(data):
                        break
                    array_len = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                    if offset + array_len * 4 > len(data):
                        break
                    value = [struct.unpack('<f', data[offset + j*4:offset + j*4 + 4])[0] for j in range(array_len)]
                    offset += array_len * 4
                elif value_type == 12:  # String array
                    if offset + 4 > len(data):
                        break
                    array_len = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                    value = []
                    for j in range(array_len):
                        if offset + 4 > len(data):
                            break
                        str_len = struct.unpack('<I', data[offset:offset+4])[0]
                        offset += 4
                        if offset + str_len > len(data):
                            break
                        str_value = data[offset:offset+str_len].decode('utf-8', errors='ignore')
                        offset += str_len
                        value.append(str_value)
                else:
                    # Handle unknown types by trying to skip them intelligently
                    log_debug(f"Unknown value type: {value_type}", "CONFIG")
                    
                    # Try to determine size based on common patterns
                    if value_type < 16:  # Likely a simple type
                        if offset + 4 > len(data):
                            break
                        # Try to read as 4-byte value and skip
                        offset += 4
                        value = f"<unknown_type_{value_type}>"
                    elif value_type < 32:  # Likely an 8-byte type
                        if offset + 8 > len(data):
                            break
                        offset += 8
                        value = f"<unknown_type_{value_type}>"
                    else:  # Likely a complex type, try to skip more intelligently
                        # Look for next key or end of data
                        remaining_data = data[offset:]
                        next_key_pos = remaining_data.find(b'\x00')
                        if next_key_pos > 0 and next_key_pos < 100:  # Reasonable skip distance
                            offset += next_key_pos + 1
                            value = f"<unknown_type_{value_type}>"
                        else:
                            # Skip a reasonable amount and hope for the best
                            offset += min(16, len(data) - offset)
                            value = f"<unknown_type_{value_type}>"
                    
                    # Don't add unknown types to config, just skip them
                    continue
                
                config[key] = str(value)
                log_debug(f"Parsed setting: {key} = {value} (type: {value_type})", "CONFIG")
            
            log_info(f"Binary parser found {len(config)} settings", "CONFIG")
            return config
            
        except Exception as e:
            log_debug(f"Binary parsing error: {e}", "CONFIG")
            return {}
    
    @staticmethod
    def parse_hybrid_config(data: bytes) -> Dict[str, str]:
        """Parse config using hybrid method (combines binary and text)."""
        try:
            # Try to decode as text first
            try:
                text_content = data.decode('utf-8', errors='ignore')
                config = ConfigParser.parse_text_config(text_content)
                if len(config) > 0:
                    return config
            except:
                pass
            
            # Fall back to binary parsing
            return ConfigParser.parse_binary_config(data)
        except Exception as e:
            log_debug(f"Hybrid parsing error: {e}", "CONFIG")
            return {}
    
    @staticmethod
    def parse_fallback_config(data: bytes) -> Dict[str, str]:
        """Parse config using fallback method (last resort)."""
        try:
            # Simple line-by-line parsing
            config = {}
            try:
                text_content = data.decode('utf-8', errors='ignore')
                lines = text_content.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Try space-separated format first (BF6 format: "key value")
                    if ' ' in line and not '=' in line:
                        try:
                            parts = line.split(' ', 1)
                            if len(parts) == 2:
                                key = parts[0].strip()
                                value = parts[1].strip()
                                if key and value:
                                    config[key] = value
                        except:
                            continue
                    # Try equals-separated format (standard format: "key=value")
                    elif '=' in line:
                        try:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            if key and value:
                                config[key] = value
                        except:
                            continue
                
                log_info(f"Fallback parser found {len(config)} settings", "CONFIG")
                return config
            except:
                return {}
        except Exception as e:
            log_debug(f"Fallback parsing error: {e}", "CONFIG")
            return {}