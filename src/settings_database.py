"""
Comprehensive BF6 Settings Database
Maps technical setting names to user-friendly descriptions with tooltips.
Based on extensive research of settings that BF6 players commonly modify.
"""

# Comprehensive settings database with categories, descriptions, and tooltips
BF6_SETTINGS_DATABASE = {
    # ===== GRAPHICS & RENDERING SETTINGS =====
    "GstRender.Dx12Enabled": {
        "name": "DirectX 12",
        "category": "Graphics API",
        "description": "Enable DirectX 12 rendering",
        "tooltip": "DirectX 12 provides better performance and features on modern GPUs. Recommended for most systems. Disable if you experience crashes.",
        "type": "bool",
        "default": 1,
        "range": [0, 1]
    },
    "GstRender.VSyncMode": {
        "name": "V-Sync",
        "category": "Display",
        "description": "Vertical synchronization",
        "tooltip": "Synchronizes frame rate with monitor refresh rate to prevent screen tearing. Disable for lower input lag in competitive play.",
        "type": "int",
        "default": 0,
        "range": [0, 1]
    },
    "GstRender.FrameRateLimit": {
        "name": "FPS Limit",
        "category": "Performance",
        "description": "Maximum frames per second",
        "tooltip": "Limit maximum FPS to reduce GPU load and heat. Set to 0 for unlimited, or match your monitor refresh rate (60, 144, 240, etc.).",
        "type": "float",
        "default": 0,
        "range": [0, 500]
    },
    "GstRender.FullscreenRefreshRate": {
        "name": "Refresh Rate",
        "category": "Display",
        "description": "Monitor refresh rate in Hz",
        "tooltip": "Your monitor's refresh rate. Common values: 60, 144, 165, 240, 360 Hz. Match this to your monitor's capabilities.",
        "type": "float",
        "default": 60,
        "range": [60, 360]
    },
    "GstRender.ResolutionScale": {
        "name": "Resolution Scale",
        "category": "Performance",
        "description": "Render resolution multiplier",
        "tooltip": "Scale rendering resolution. 100% = native resolution. Lower for better performance, higher for better quality. 50-200% range.",
        "type": "float",
        "default": 1.0,
        "range": [0.5, 2.0]
    },
    "GstRender.FixedResolutionScale": {
        "name": "Fixed Resolution Scale",
        "category": "Performance",
        "description": "Fixed resolution scale percentage",
        "tooltip": "Alternative resolution scaling method. 100 = native, lower = better performance, higher = better quality.",
        "type": "float",
        "default": 100,
        "range": [50, 200]
    },
    
    # ===== QUALITY SETTINGS =====
    "GstRender.TextureQuality": {
        "name": "Texture Quality",
        "category": "Graphics Quality",
        "description": "Texture detail level",
        "tooltip": "Higher = sharper textures but more VRAM usage. Low=0, Medium=1, High=2, Ultra=3, Ultra+4. Impacts VRAM heavily.",
        "type": "int",
        "default": 2,
        "range": [0, 4]
    },
    "GstRender.ShadowQuality": {
        "name": "Shadow Quality",
        "category": "Graphics Quality",
        "description": "Shadow detail and resolution",
        "tooltip": "Shadow rendering quality. Higher = better shadows but lower FPS. Low=0, Medium=1, High=2, Ultra=3. Major performance impact.",
        "type": "int",
        "default": 2,
        "range": [0, 3]
    },
    "GstRender.EffectsQuality": {
        "name": "Effects Quality",
        "category": "Graphics Quality",
        "description": "Visual effects detail",
        "tooltip": "Quality of explosions, smoke, particles. Higher = better effects but lower FPS. Low=0, Medium=1, High=2, Ultra=3.",
        "type": "int",
        "default": 2,
        "range": [0, 3]
    },
    "GstRender.LightingQuality": {
        "name": "Lighting Quality",
        "category": "Graphics Quality",
        "description": "Lighting and illumination detail",
        "tooltip": "Quality of lighting effects. Higher = more realistic lighting but lower FPS. Low=0, Medium=1, High=2, Ultra=3.",
        "type": "int",
        "default": 2,
        "range": [0, 3]
    },
    "GstRender.PostProcessQuality": {
        "name": "Post-Process Quality",
        "category": "Graphics Quality",
        "description": "Post-processing effects quality",
        "tooltip": "Quality of bloom, lens flares, color grading. Higher = better visual effects. Low=0, Medium=1, High=2, Ultra=3.",
        "type": "int",
        "default": 2,
        "range": [0, 3]
    },
    "GstRender.MeshQuality": {
        "name": "Mesh Quality",
        "category": "Graphics Quality",
        "description": "3D model detail level",
        "tooltip": "Detail level of 3D models. Higher = more detailed models but lower FPS. Low=0, Medium=1, High=2, Ultra=3.",
        "type": "int",
        "default": 2,
        "range": [0, 3]
    },
    "GstRender.TerrainQuality": {
        "name": "Terrain Quality",
        "category": "Graphics Quality",
        "description": "Terrain and landscape detail",
        "tooltip": "Quality of ground, rocks, terrain. Higher = more detailed terrain. Low=0, Medium=1, High=2, Ultra=3.",
        "type": "int",
        "default": 2,
        "range": [0, 3]
    },
    "GstRender.VegetationQuality": {
        "name": "Vegetation Quality",
        "category": "Graphics Quality",
        "description": "Grass and foliage detail",
        "tooltip": "Quality and density of grass, trees, plants. Higher = more vegetation but lower FPS. Low=0, Medium=1, High=2, Ultra=3.",
        "type": "int",
        "default": 2,
        "range": [0, 3]
    },
    
    # ===== ADVANCED GRAPHICS =====
    "GstRender.AmbientOcclusion": {
        "name": "Ambient Occlusion",
        "category": "Advanced Graphics",
        "description": "Realistic shadowing in corners",
        "tooltip": "Adds realistic shadows in corners and crevices. Improves visual quality but reduces FPS. Disable for competitive play.",
        "type": "bool",
        "default": 1,
        "range": [0, 1]
    },
    "GstRender.MotionBlurWorld": {
        "name": "Motion Blur",
        "category": "Advanced Graphics",
        "description": "Camera motion blur effect",
        "tooltip": "Blurs screen during fast movement. 0=Off, 0.5=Medium, 1.0=High. Most competitive players disable this for clarity.",
        "type": "float",
        "default": 0.5,
        "range": [0, 1.0]
    },
    "GstRender.ChromaticAberration": {
        "name": "Chromatic Aberration",
        "category": "Advanced Graphics",
        "description": "Color fringing effect",
        "tooltip": "Adds color separation at screen edges for cinematic look. Disable for clearer image in competitive play.",
        "type": "bool",
        "default": 1,
        "range": [0, 1]
    },
    "GstRender.FilmGrain": {
        "name": "Film Grain",
        "category": "Advanced Graphics",
        "description": "Film-like grain effect",
        "tooltip": "Adds grainy texture for cinematic look. Disable for clearer image. No performance impact.",
        "type": "bool",
        "default": 0,
        "range": [0, 1]
    },
    "GstRender.Vignette": {
        "name": "Vignette",
        "category": "Advanced Graphics",
        "description": "Screen edge darkening",
        "tooltip": "Darkens screen edges for cinematic effect. Disable for better peripheral vision in competitive play.",
        "type": "bool",
        "default": 0,
        "range": [0, 1]
    },
    "GstRender.LensDistortion": {
        "name": "Lens Distortion",
        "category": "Advanced Graphics",
        "description": "Camera lens warping effect",
        "tooltip": "Adds fisheye lens effect. Disable for accurate aiming in competitive play.",
        "type": "bool",
        "default": 0,
        "range": [0, 1]
    },
    
    # ===== RAY TRACING & UPSCALING =====
    "GstRender.RayTracingEnabled": {
        "name": "Ray Tracing",
        "category": "Ray Tracing",
        "description": "Enable ray-traced lighting",
        "tooltip": "Realistic lighting and reflections using ray tracing. Requires RTX GPU. Major performance impact. Disable for competitive play.",
        "type": "bool",
        "default": 0,
        "range": [0, 1]
    },
    "GstRender.DLSSEnabled": {
        "name": "DLSS",
        "category": "Upscaling",
        "description": "NVIDIA DLSS AI upscaling",
        "tooltip": "AI-powered upscaling for better performance on RTX GPUs. Quality modes: Performance, Balanced, Quality. Requires RTX GPU.",
        "type": "bool",
        "default": 0,
        "range": [0, 1]
    },
    "GstRender.AMDNvidiaUpscalingQuality": {
        "name": "Upscaling Quality",
        "category": "Upscaling",
        "description": "FSR/DLSS quality mode",
        "tooltip": "Quality vs Performance balance. 0=Performance, 1=Balanced, 2=Quality, 3=Ultra Quality. Higher = better image, lower FPS.",
        "type": "int",
        "default": 1,
        "range": [0, 3]
    },
    "GstRender.FrameGeneration": {
        "name": "Frame Generation",
        "category": "Performance",
        "description": "AI-generated frames",
        "tooltip": "Generates extra frames using AI (DLSS 3). Doubles FPS but adds latency. Requires RTX 40-series GPU.",
        "type": "bool",
        "default": 0,
        "range": [0, 1]
    },
    
    # ===== COMPETITIVE SETTINGS =====
    "GstRender.UltraLowLatency": {
        "name": "Ultra Low Latency",
        "category": "Competitive",
        "description": "NVIDIA Reflex low latency",
        "tooltip": "Reduces input lag for competitive play. Enable for best responsiveness. Requires NVIDIA GPU. Essential for competitive players.",
        "type": "bool",
        "default": 0,
        "range": [0, 1]
    },
    "GstRender.AMDLowLatency": {
        "name": "AMD Anti-Lag",
        "category": "Competitive",
        "description": "AMD Anti-Lag technology",
        "tooltip": "Reduces input lag on AMD GPUs. Enable for better responsiveness in competitive play.",
        "type": "bool",
        "default": 0,
        "range": [0, 1]
    },
    "GstRender.DRSFrameRateTarget": {
        "name": "Target Frame Rate",
        "category": "Performance",
        "description": "Dynamic resolution target FPS",
        "tooltip": "Target FPS for dynamic resolution scaling. Game will adjust resolution to maintain this FPS. Set to your desired frame rate.",
        "type": "float",
        "default": 60,
        "range": [30, 360]
    },
    
    # ===== DISPLAY SETTINGS =====
    "GstRender.HDREnabled": {
        "name": "HDR",
        "category": "Display",
        "description": "High Dynamic Range",
        "tooltip": "Enhanced color range and brightness. Requires HDR-capable monitor. Improves visual quality in supported displays.",
        "type": "bool",
        "default": 0,
        "range": [0, 1]
    },
    "GstRender.Brightness": {
        "name": "Brightness",
        "category": "Display",
        "description": "Screen brightness level",
        "tooltip": "Adjust screen brightness. 0.5 = default. Lower for darker scenes, higher for better visibility in shadows.",
        "type": "float",
        "default": 0.5,
        "range": [0, 1.0]
    },
    "GstRender.Contrast": {
        "name": "Contrast",
        "category": "Display",
        "description": "Screen contrast level",
        "tooltip": "Adjust contrast between light and dark. 0.5 = default. Higher = more dramatic lighting.",
        "type": "float",
        "default": 0.5,
        "range": [0, 1.0]
    },
    "GstRender.FieldOfViewVertical": {
        "name": "Field of View",
        "category": "Display",
        "description": "Vertical FOV in degrees",
        "tooltip": "Camera field of view. Higher = see more but fish-eye effect. 60-90 typical, 90-110 for competitive. Affects aim feel.",
        "type": "float",
        "default": 70,
        "range": [60, 120]
    },
    
    # ===== AUDIO SETTINGS =====
    "GstAudio.MasterVolume": {
        "name": "Master Volume",
        "category": "Audio",
        "description": "Overall volume level",
        "tooltip": "Master audio volume. 0 = muted, 100 = maximum. Adjust to comfortable listening level.",
        "type": "float",
        "default": 100,
        "range": [0, 100]
    },
    "GstAudio.EffectsVolume": {
        "name": "Effects Volume",
        "category": "Audio",
        "description": "Sound effects volume",
        "tooltip": "Volume of gunfire, explosions, footsteps. Important for competitive play to hear enemies.",
        "type": "float",
        "default": 100,
        "range": [0, 100]
    },
    "GstAudio.MusicVolume": {
        "name": "Music Volume",
        "category": "Audio",
        "description": "Background music volume",
        "tooltip": "In-game music volume. Many competitive players set this to 0 to hear game sounds better.",
        "type": "float",
        "default": 50,
        "range": [0, 100]
    },
    "GstAudio.VoiceVolume": {
        "name": "Voice Volume",
        "category": "Audio",
        "description": "Voice chat volume",
        "tooltip": "Volume of voice communications. Adjust to hear teammates clearly without overpowering game sounds.",
        "type": "float",
        "default": 100,
        "range": [0, 100]
    },
    
    # ===== INPUT SETTINGS =====
    "GstInput.MouseSensitivity": {
        "name": "Mouse Sensitivity",
        "category": "Input",
        "description": "Mouse movement speed",
        "tooltip": "Mouse sensitivity multiplier. Lower = more precise aim, higher = faster turns. Find your sweet spot through practice.",
        "type": "float",
        "default": 1.0,
        "range": [0.1, 10.0]
    },
    "GstInput.MouseAcceleration": {
        "name": "Mouse Acceleration",
        "category": "Input",
        "description": "Variable mouse speed",
        "tooltip": "Makes mouse speed vary with movement speed. Disable (0) for consistent aim in competitive play.",
        "type": "bool",
        "default": 0,
        "range": [0, 1]
    },
    "GstInput.InvertYAxis": {
        "name": "Invert Y-Axis",
        "category": "Input",
        "description": "Invert vertical mouse movement",
        "tooltip": "Reverse vertical mouse movement (flight sim style). Personal preference.",
        "type": "bool",
        "default": 0,
        "range": [0, 1]
    },
    "GstInput.ADSMouseSensitivity": {
        "name": "ADS Sensitivity",
        "category": "Input",
        "description": "Aim-down-sights sensitivity",
        "tooltip": "Mouse sensitivity when aiming. Lower than hipfire for precise aiming. Typically 0.5-1.0x of normal sensitivity.",
        "type": "float",
        "default": 0.7,
        "range": [0.1, 2.0]
    },
}

# Category organization for UI
SETTINGS_CATEGORIES = {
    "Graphics API": ["DirectX 12", "Vulkan"],
    "Display": ["Resolution", "Refresh Rate", "V-Sync", "HDR", "Brightness", "Contrast", "Field of View"],
    "Performance": ["FPS Limit", "Resolution Scale", "Target Frame Rate", "Frame Generation"],
    "Graphics Quality": ["Texture", "Shadow", "Effects", "Lighting", "Post-Process", "Mesh", "Terrain", "Vegetation"],
    "Advanced Graphics": ["Ambient Occlusion", "Motion Blur", "Chromatic Aberration", "Film Grain", "Vignette", "Lens Distortion"],
    "Ray Tracing": ["Ray Tracing", "Ray Traced Reflections", "Ray Traced Shadows"],
    "Upscaling": ["DLSS", "FSR", "Upscaling Quality"],
    "Competitive": ["Ultra Low Latency", "AMD Anti-Lag", "Reduce Buffering"],
    "Audio": ["Master Volume", "Effects", "Music", "Voice"],
    "Input": ["Mouse Sensitivity", "Mouse Acceleration", "ADS Sensitivity", "Invert Y-Axis"]
}

def get_setting_info(setting_key):
    """Get information about a setting."""
    return BF6_SETTINGS_DATABASE.get(setting_key, {
        "name": setting_key,
        "category": "Unknown",
        "description": "Unknown setting",
        "tooltip": "No information available",
        "type": "unknown",
        "default": 0,
        "range": [0, 1]
    })

def get_settings_by_category(category):
    """Get all settings in a specific category."""
    return {k: v for k, v in BF6_SETTINGS_DATABASE.items() if v.get("category") == category}

def get_all_categories():
    """Get list of all setting categories."""
    categories = set()
    for setting in BF6_SETTINGS_DATABASE.values():
        categories.add(setting.get("category", "Unknown"))
    return sorted(list(categories))


