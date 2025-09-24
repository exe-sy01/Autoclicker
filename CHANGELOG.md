# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- 🎯 **Smart Clicking**: Support for cursor position and fixed coordinates
- ⚡ **Customizable Intervals**: Click intervals from 1ms to 10 seconds
- 🖱️ **Multiple Mouse Buttons**: Left, right, and middle click support
- 🔢 **Multi-Click Options**: Single, double, and triple click modes
- 🔄 **Flexible Click Count**: Infinite or limited number of clicks
- ⌨️ **Global Hotkey**: F6 key for start/stop (works system-wide)
- 📍 **Position Picker**: Click-to-select target coordinates
- 💾 **Settings Persistence**: Automatic save/restore of user preferences
- 🎨 **Modern GUI**: Clean, intuitive PySide6 interface
- 🛡️ **Safety Features**: Built-in safeguards and instant stop capability

### Technical
- Built with PySide6 for modern Qt interface
- PyAutoGUI for cross-platform mouse automation
- Keyboard library for global hotkey support
- PyInstaller for standalone executable creation
- Thread-safe clicking implementation
- Settings stored using QSettings

### Distribution
- 📦 Standalone executable (no Python required)
- 🖥️ Windows 10/11 support (64-bit)
- ⚙️ Qt configuration for DPI awareness
- 📖 Comprehensive documentation and guides

## [Unreleased]

### Planned
- 🔄 Auto-update functionality
- 🎨 Theme customization options
- 📊 Click statistics and analytics
- 🔧 Advanced scripting capabilities
- 🌐 Multi-language support

---

## Release Notes

### v1.0.0 - Initial Release
This is the first stable release of AutoClicker, featuring all core functionality needed for automated mouse clicking. The application has been thoroughly tested and is ready for production use.

**Key Highlights:**
- Complete feature parity with popular auto-clicker tools
- Professional, user-friendly interface
- Standalone executable requiring no additional software
- Comprehensive safety features and global hotkey support
- Full documentation and distribution guides

**System Requirements:**
- Windows 10 or later (64-bit)
- No additional software required for executable version
- Python 3.7+ required for source code version