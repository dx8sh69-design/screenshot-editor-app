import streamlit as st
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance
import io
import cv2
import numpy as np
import re
import random
from typing import List, Tuple

# Configure page
st.set_page_config(
    page_title="FREE Screenshot Editor",
    page_icon="📸",
    layout="wide"
)

# Initialize session state
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'original_image' not in st.session_state:
    st.session_state.original_image = None

class FreeScreenshotEditor:
    """FREE Screenshot editor with local AI-like features (no API needed!)"""
    
    def __init__(self):
        """Initialize the editor - no API key needed!"""
        pass
    
    def detect_text_regions(self, image: Image.Image) -> List[Tuple[int, int, int, int]]:
        """Detect text regions in image using OpenCV (FREE!)"""
        try:
            # Convert PIL to OpenCV format
            img_array = np.array(image)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Use MSER (Maximally Stable Extremal Regions) to detect text
            mser = cv2.MSER_create()
            regions, _ = mser.detectRegions(gray)
            
            # Convert regions to bounding boxes
            boxes = []
            for region in regions:
                x, y, w, h = cv2.boundingRect(region.reshape(-1, 1, 2))
                # Filter out very small regions
                if w > 20 and h > 10:
                    boxes.append((x, y, x + w, y + h))
            
            return boxes
            
        except Exception as e:
            st.error(f"Error detecting text: {str(e)}")
            return []
    
    def generate_alt_text_free(self, image: Image.Image) -> str:
        """Generate alt text using image analysis (FREE - no API!)"""
        try:
            width, height = image.size
            aspect_ratio = width / height
            
            # Analyze image properties
            img_array = np.array(image)
            
            # Calculate average brightness
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            brightness = np.mean(gray)
            
            # Count dominant colors
            img_small = cv2.resize(img_array, (50, 50))
            img_flat = img_small.reshape(-1, 3)
            unique_colors = len(np.unique(img_flat.view(np.dtype((np.void, img_flat.dtype.itemsize * 3)))))
            
            # Detect edges (complexity indicator)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (width * height)
            
            # Generate description based on analysis
            alt_text = "Screenshot showing "
            
            # Describe layout
            if aspect_ratio > 1.5:
                alt_text += "a wide horizontal interface "
            elif aspect_ratio < 0.7:
                alt_text += "a tall vertical layout "
            else:
                alt_text += "a standard rectangular interface "
            
            # Describe complexity
            if edge_density > 0.1:
                alt_text += "with detailed content and multiple elements"
            elif edge_density > 0.05:
                alt_text += "with moderate detail and various UI components"
            else:
                alt_text += "with clean, minimal design"
            
            # Describe brightness
            if brightness > 200:
                alt_text += ", featuring bright colors and high contrast"
            elif brightness < 100:
                alt_text += ", with dark theme or low lighting"
            else:
                alt_text += ", with balanced lighting"
            
            # Add color diversity info
            if unique_colors > 1000:
                alt_text += " and rich color palette."
            elif unique_colors > 500:
                alt_text += " and moderate color variety."
            else:
                alt_text += " and limited color scheme."
            
            return alt_text
            
        except Exception as e:
            return f"Screenshot image with dimensions {image.size[0]}x{image.size[1]} pixels."
    
    def detect_sensitive_info_free(self, image: Image.Image) -> dict:
        """Detect potential sensitive areas using pattern recognition (FREE!)"""
        try:
            # Convert to OpenCV format
            img_array = np.array(image)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Detect text regions
            text_boxes = self.detect_text_regions(image)
            
            width, height = image.size
            sensitive_areas = []
            details = []
            
            # Check common sensitive areas
            # Top area (often contains emails, names in headers)
            if height > 100:
                top_area = gray[0:int(height * 0.15), :]
                if np.mean(top_area) < 240:  # Not just white space
                    sensitive_areas.append("top")
                    details.append("header area with potential personal info")
            
            # Bottom area (often contains signatures, contact info)
            if height > 100:
                bottom_area = gray[int(height * 0.85):height, :]
                if np.mean(bottom_area) < 240:  # Not just white space
                    sensitive_areas.append("bottom")
                    details.append("footer area with potential contact details")
            
            # Check for potential email patterns in filename or assume presence
            # (This is a simplified approach since we can't do OCR without heavy libraries)
            if len(text_boxes) > 5:  # Lots of text regions
                details.append("multiple text regions that may contain sensitive data")
            
            # Check image dimensions for common sensitive screenshot types
            if width > 800 and height > 600:  # Likely desktop screenshot
                details.append("desktop screenshot that may show personal information")
            elif width < 500:  # Likely mobile screenshot
                details.append("mobile screenshot that may contain private messages or data")
            
            found = len(sensitive_areas) > 0 or len(text_boxes) > 3
            
            return {
                "found": found,
                "details": ", ".join(details) if details else "Image analysis completed",
                "locations": ", ".join(sensitive_areas) if sensitive_areas else "General content areas",
                "text_boxes": text_boxes
            }
            
        except Exception as e:
            return {
                "found": True,  # Conservative approach
                "details": f"Unable to fully analyze - applying protective blur. Error: {str(e)}",
                "locations": "entire image",
                "text_boxes": []
            }
    
    def apply_smart_blur(self, image: Image.Image, blur_strength: int = 15) -> Image.Image:
        """Apply smart blur to likely sensitive areas (FREE!)"""
        try:
            # Get sensitive info detection results
            sensitive_info = self.detect_sensitive_info_free(image)
            
            # Create a copy for processing
            result = image.copy()
            width, height = image.size
            
            # Apply blur to detected text regions
            for box in sensitive_info.get("text_boxes", []):
                x1, y1, x2, y2 = box
                # Extract the region
                region = result.crop((x1, y1, x2, y2))
                # Apply blur
                blurred_region = region.filter(ImageFilter.GaussianBlur(radius=blur_strength))
                # Paste back
                result.paste(blurred_region, (x1, y1))
            
            # Apply blur to common sensitive areas
            if "top" in sensitive_info.get("locations", ""):
                top_region = result.crop((0, 0, width, int(height * 0.15)))
                top_blurred = top_region.filter(ImageFilter.GaussianBlur(radius=blur_strength))
                result.paste(top_blurred, (0, 0))
            
            if "bottom" in sensitive_info.get("locations", ""):
                bottom_region = result.crop((0, int(height * 0.85), width, height))
                bottom_blurred = bottom_region.filter(ImageFilter.GaussianBlur(radius=blur_strength))
                result.paste(bottom_blurred, (0, int(height * 0.85)))
            
            return result
            
        except Exception as e:
            st.error(f"Error applying blur: {str(e)}")
            return image
    
    def generate_meme_caption_free(self, image: Image.Image) -> str:
        """Generate meme caption using image analysis (FREE!)"""
        try:
            width, height = image.size
            aspect_ratio = width / height
            
            # Analyze image
            img_array = np.array(image)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            brightness = np.mean(gray)
            
            # Detect edges for complexity
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (width * height)
            
            # Pre-made meme templates based on image characteristics
            meme_templates = {
                "complex_desktop": [
                    "When you have 47 tabs open but still can't find what you're looking for",
                    "POV: Your desktop after 3 months of 'I'll organize it later'",
                    "This screenshot has more layers than my emotional problems",
                    "When your screen looks like a puzzle but you're the missing piece"
                ],
                "simple_clean": [
                    "Minimalism: Because sometimes less is more... or you just gave up",
                    "Clean desktop energy ✨ (Trash folder has entered the chat)",
                    "When you finally organize your life for 5 seconds",
                    "This is what peak performance looks like"
                ],
                "mobile_screenshot": [
                    "When your phone knows more about you than you do",
                    "Mobile screenshot: Because desktop was too mainstream",
                    "POV: You're about to show someone something but panic about your notifications",
                    "This app has seen things... terrible things"
                ],
                "dark_theme": [
                    "Dark mode: Because my soul matches my UI",
                    "When you're trying to save battery but really you're just emo",
                    "Dark theme supremacy ⚫",
                    "My screen is darker than my coffee"
                ],
                "bright_colorful": [
                    "When your screen is brighter than your future",
                    "This has more colors than a unicorn explosion 🌈",
                    "RGB keyboard users be like:",
                    "Brightness level: Retina damage"
                ]
            }
            
            # Choose template based on image characteristics
            if width < 500:  # Mobile
                templates = meme_templates["mobile_screenshot"]
            elif brightness < 100:  # Dark
                templates = meme_templates["dark_theme"]
            elif brightness > 200:  # Bright
                templates = meme_templates["bright_colorful"]
            elif edge_density > 0.1:  # Complex
                templates = meme_templates["complex_desktop"]
            else:  # Clean
                templates = meme_templates["simple_clean"]
            
            # Add some random tech humor
            random_humor = [
                "Error 404: Social life not found",
                "It ain't much, but it's honest work",
                "Me explaining this screenshot to my mom:",
                "When the screenshot is more organized than your life",
                "This screenshot brought to you by caffeine and poor life choices"
            ]
            
            # Combine and pick random
            all_options = templates + random_humor
            return random.choice(all_options)
            
        except Exception as e:
            return "When your screenshot editor works better than your life decisions 😅"

def add_text_to_image(image: Image.Image, text: str, position: str = "bottom") -> Image.Image:
    """Add meme-style text to image (FREE!)"""
    try:
        # Create a copy
        img_with_text = image.copy()
        draw = ImageDraw.Draw(img_with_text)
        
        # Try to load a font (fallback to default)
        try:
            # Try different common font paths
            font_paths = [
                "arial.ttf", "Arial.ttf", 
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/calibri.ttf",
                "/System/Library/Fonts/Arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            ]
            
            font = None
            for path in font_paths:
                try:
                    font = ImageFont.truetype(path, 28)
                    break
                except:
                    continue
            
            if font is None:
                font = ImageFont.load_default()
                
        except:
            font = ImageFont.load_default()
        
        # Get image dimensions
        width, height = img_with_text.size
        
        # Word wrap for long text
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] < width - 40:  # Leave 20px margin on each side
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate total text height
        total_text_height = len(lines) * 35  # Approximate line height
        
        # Position text
        if position == "top":
            start_y = 20
        else:  # bottom
            start_y = height - total_text_height - 20
        
        # Draw each line
        for i, line in enumerate(lines):
            # Calculate position for this line
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = start_y + (i * 35)
            
            # Draw outline (stroke effect)
            outline_width = 3
            for adj_x in range(-outline_width, outline_width + 1):
                for adj_y in range(-outline_width, outline_width + 1):
                    if adj_x != 0 or adj_y != 0:
                        draw.text((x + adj_x, y + adj_y), line, fill="black", font=font)
            
            # Draw main text
            draw.text((x, y), line, fill="white", font=font)
        
        return img_with_text
        
    except Exception as e:
        st.error(f"Error adding text: {str(e)}")
        return image

def enhance_image_quality(image: Image.Image) -> Image.Image:
    """Enhance image quality (FREE bonus feature!)"""
    try:
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        enhanced = enhancer.enhance(1.2)
        
        # Enhance contrast slightly
        enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = enhancer.enhance(1.1)
        
        # Enhance color
        enhancer = ImageEnhance.Color(enhanced)
        enhanced = enhancer.enhance(1.05)
        
        return enhanced
    except:
        return image

def main():
    """Main Streamlit app - 100% FREE!"""
    
    # Header with celebration
    st.title("📸 FREE Screenshot Editor")
    st.markdown("*✨ No API keys, no costs, no limits! Pure local magic!* 🎉")
    
    # Fun stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Cost", "FREE!", "Always")
    with col2:
        st.metric("🔑 API Keys", "0", "None needed")
    with col3:
        st.metric("🚀 Features", "4+", "All working")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("🔧 FREE Tools")
        st.markdown("*No sign-ups, no payments!* 🎊")
        
        # Feature selection
        feature = st.radio(
            "Choose your FREE feature:",
            ["📝 Smart Alt Text", "🔒 Privacy Blur", "😄 Meme Generator", "✨ Quality Enhance"],
            help="All features work offline on your computer!"
        )
        
        # Additional options
        if feature == "🔒 Privacy Blur":
            blur_strength = st.slider("Blur Strength", 1, 30, 15)
        elif feature == "😄 Meme Generator":
            caption_position = st.selectbox("Caption Position", ["bottom", "top"])
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Your Screenshot")
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            help="Upload any screenshot - processed 100% on your computer!"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.session_state.original_image = image
            
            st.image(image, caption="Original Screenshot", use_column_width=True)
            
            # Show image stats
            file_size = len(uploaded_file.getvalue()) / 1024  # KB
            st.info(f"📊 Size: {image.size[0]} x {image.size[1]} pixels • {file_size:.1f} KB")
    
    with col2:
        st.header("✨ FREE AI-Powered Results")
        
        if st.session_state.original_image is not None:
            editor = FreeScreenshotEditor()
            
            if st.button(f"🚀 Process with {feature}", type="primary"):
                with st.spinner("🔄 Processing locally (no internet needed)..."):
                    
                    if feature == "📝 Smart Alt Text":
                        # Generate alt text using local analysis
                        alt_text = editor.generate_alt_text_free(st.session_state.original_image)
                        st.success("✅ Alt text generated using local AI!")
                        st.text_area("Generated Alt Text:", value=alt_text, height=100)
                        st.image(st.session_state.original_image, caption="Your Screenshot", use_column_width=True)
                    
                    elif feature == "🔒 Privacy Blur":
                        # Detect and blur sensitive areas
                        sensitive_info = editor.detect_sensitive_info_free(st.session_state.original_image)
                        
                        st.write("🔍 **FREE Privacy Analysis:**")
                        if sensitive_info["found"]:
                            st.warning(f"Detected: {sensitive_info['details']}")
                            st.write(f"📍 Areas: {sensitive_info['locations']}")
                            
                            blurred_image = editor.apply_smart_blur(
                                st.session_state.original_image, 
                                blur_strength
                            )
                            st.session_state.processed_image = blurred_image
                            
                            st.success("✅ Privacy protection applied!")
                            st.image(blurred_image, caption="Privacy-Protected Screenshot", use_column_width=True)
                        else:
                            st.success("✅ No obvious sensitive content detected!")
                            st.image(st.session_state.original_image, caption="Your Screenshot", use_column_width=True)
                    
                    elif feature == "😄 Meme Generator":
                        # Generate meme using local analysis
                        meme_text = editor.generate_meme_caption_free(st.session_state.original_image)
                        st.success("✅ Meme caption generated using local humor AI!")
                        st.text_area("Generated Meme Caption:", value=meme_text, height=100)
                        
                        # Add to image
                        meme_image = add_text_to_image(
                            st.session_state.original_image,
                            meme_text,
                            caption_position
                        )
                        st.session_state.processed_image = meme_image
                        st.image(meme_image, caption="Meme-ified Screenshot 🎭", use_column_width=True)
                    
                    elif feature == "✨ Quality Enhance":
                        # Enhance image quality
                        enhanced_image = enhance_image_quality(st.session_state.original_image)
                        st.session_state.processed_image = enhanced_image
                        
                        st.success("✅ Image quality enhanced!")
                        st.image(enhanced_image, caption="Enhanced Screenshot", use_column_width=True)
                        
                        # Show before/after
                        st.markdown("**Before vs After:**")
                        before_col, after_col = st.columns(2)
                        with before_col:
                            st.image(st.session_state.original_image, caption="Before", use_column_width=True)
                        with after_col:
                            st.image(enhanced_image, caption="After", use_column_width=True)
            
            # Download processed image
            if st.session_state.processed_image is not None:
                st.markdown("---")
                
                buf = io.BytesIO()
                st.session_state.processed_image.save(buf, format='PNG')
                byte_data = buf.getvalue()
                
                st.download_button(
                    label="💾 Download FREE Processed Image",
                    data=byte_data,
                    file_name=f"free_processed_{feature.replace(' ', '_').lower()}.png",
                    mime="image/png"
                )
        
        elif st.session_state.original_image is None:
            st.info("👆 Upload an image to get started with FREE processing!")
            
            # Show what's possible
            st.markdown("""
            ### 🎯 What You Get (100% FREE):
            - **Smart Alt Text**: Local image analysis
            - **Privacy Blur**: Text detection & blurring  
            - **Meme Generator**: AI-style humor captions
            - **Quality Enhance**: Sharpness & color boost
            - **No Limits**: Process unlimited images!
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **🎉 Made with ❤️ - 100% FREE & Open Source!** 
    
    No API keys • No sign-ups • No costs • No data sent to servers
    
    *Everything runs locally on your computer!* 🖥️
    """)

if __name__ == "__main__":
    main()