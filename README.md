# 📸 FREE Screenshot Editor

A **100% FREE** beginner-friendly Streamlit web application that enhances your screenshots using **local AI-powered features** - no API keys, no costs, no internet required!

## ✨ Features (All FREE!)

- **📝 Smart Alt Text**: AI-style description generation using local image analysis
- **🔒 Privacy Protection**: Detect and blur sensitive information using computer vision
- **😄 Meme Generator**: Create funny captions with local humor AI
- **✨ Quality Enhance**: Improve image sharpness and colors
- **💾 Easy Downloads**: Download your processed images instantly
- **🎯 Clean UI**: Intuitive interface with sidebar controls
- **🔐 100% Private**: Everything runs on YOUR computer - no data sent anywhere!

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- **NO API KEYS NEEDED!** 🎉

### Installation

1. **Clone or download** this project to your local machine

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and go to `http://localhost:8501`

**That's it! No API keys, no sign-ups, nothing else needed!** 🎉

## 📖 How to Use

### Step 1: Setup
- **NO API KEY NEEDED!** 🔑❌
- Choose the feature you want to use from the radio buttons
- Everything runs locally on your computer!

### Step 2: Upload Image
- Click "Browse files" or drag & drop your screenshot
- Supported formats: PNG, JPG, JPEG
- The original image will appear in the left column

### Step 3: Process
- Click the "🚀 Process" button
- Wait for Claude AI to analyze your image
- View the results in the right column

### Step 4: Download (Optional)
- For blur and meme features, download the processed image
- Click "💾 Download Processed Image" button

## 🎯 Feature Details

### 📝 Alt Text Generation
- Generates concise, descriptive alt text for accessibility
- Perfect for social media, websites, and documentation
- Focuses on main content and purpose of the screenshot

### 🔒 Sensitive Information Blur
- Detects emails, phone numbers, names, addresses, and faces
- Applies intelligent blur to protect privacy
- Conservative approach - better safe than sorry
- Adjustable blur strength (1-30)

### 😄 Meme Caption Creation
- Creates humorous, internet-culture appropriate captions
- Clean and appropriate content
- Customizable position (top/bottom)
- Adds styled text overlay to your image

## 🛠️ Technical Details

### Project Structure
```
screenshot-editor/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── processed/         # Downloaded images go here (auto-created)
```

### Dependencies Explained
- **streamlit**: Web app framework
- **anthropic**: Official Claude AI API client
- **Pillow**: Image processing and manipulation
- **opencv-python**: Computer vision for advanced image processing
- **numpy**: Numerical operations for image arrays

### Key Classes & Functions
- `ClaudeScreenshotEditor`: Main class handling Claude API interactions
- `encode_image_to_base64()`: Converts images for API calls
- `generate_alt_text()`: Alt text generation using Claude Vision
- `detect_sensitive_info()`: Privacy-focused content detection
- `apply_privacy_blur()`: Smart blurring algorithm
- `generate_meme_caption()`: Humorous caption generation
- `add_text_to_image()`: Text overlay functionality

## 🔧 Customization

### Modify Blur Areas
Edit the `apply_privacy_blur()` function in `app.py` to change which areas get blurred:
```python
# Current: blurs top 15% and bottom 10%
top_area = image.crop((0, 0, width, int(height * 0.15)))
bottom_area = image.crop((0, int(height * 0.9), width, height))
```

### Adjust Text Styling
Modify the `add_text_to_image()` function to change font, colors, or positioning:
```python
font = ImageFont.truetype("arial.ttf", 24)  # Font and size
fill=(0, 0, 0, 128)  # Background color (RGBA)
fill="white"  # Text color
```

### Add New Features
1. Create new methods in the `ClaudeScreenshotEditor` class
2. Add new radio button options in the sidebar
3. Add processing logic in the main `if` statements

## ❗ Troubleshooting

### Common Issues

**"Error initializing Claude API"**
- Check your API key is correct and active
- Ensure you have credits/usage remaining
- Verify internet connection

**"Module not found" errors**
- Run `pip install -r requirements.txt` again
- Check Python version (needs 3.8+)
- Try `pip install --upgrade [module-name]`

**Images not processing**
- Ensure image file is not corrupted
- Try smaller image sizes (< 20MB)
- Check image format is PNG/JPG/JPEG

**Blur not working as expected**
- This is a simplified implementation
- For production use, consider advanced ML models
- Adjust blur strength or modify blur areas in code

### Performance Tips
- Larger images take longer to process
- Claude API has rate limits - wait between requests
- Consider resizing very large images before processing

## 🔐 Security Notes

- API keys are handled securely (password input field)
- Images are processed locally and sent to Claude API
- No images are stored permanently
- Consider data privacy when uploading sensitive screenshots

## 📚 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Claude API Documentation](https://docs.anthropic.com)
- [Pillow (PIL) Documentation](https://pillow.readthedocs.io)
- [OpenCV Python Tutorials](https://opencv-python-tutroals.readthedocs.io)

## 🤝 Contributing

This is a beginner-friendly project! Ideas for improvements:
- Better sensitive info detection algorithms
- Face detection and blurring using OpenCV
- More meme caption styles
- Batch processing multiple images
- Image format conversion tools
- Advanced text styling options

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed correctly
3. Verify your Claude API key is working
4. Try with a different image file

---

**Made with ❤️ using Python, Streamlit, and Claude AI**

*Happy screenshot editing! 📸✨*
