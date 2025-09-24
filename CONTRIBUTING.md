# 🤝 Contributing to AutoClicker

Thank you for your interest in contributing to AutoClicker! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/AutoClicker.git`
3. **Create** a branch: `git checkout -b feature/your-feature-name`
4. **Make** your changes
5. **Test** thoroughly
6. **Commit** with clear messages
7. **Push** and create a **Pull Request**

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+ (recommended: 3.11)
- PyQt6
- Windows OS (for testing executable builds)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/AutoClicker.git
cd AutoClicker

# Install dependencies
pip install -r requirements.txt

# Run the application
python auto_clicker.py
```

### Building Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python -m PyInstaller --onefile --windowed --name "AutoClicker" --exclude-module PyQt5 auto_clicker.py

# Copy qt.conf to dist folder
copy qt.conf dist\
```

## 📋 Development Guidelines

### Code Style
- Follow **PEP 8** Python style guidelines
- Use **meaningful variable names**
- Add **comments** for complex logic
- Keep **functions focused** and small
- Use **type hints** where appropriate

### Commit Messages
Use clear, descriptive commit messages:
```
✨ Add new feature: custom hotkey support
🐛 Fix: clicking interval validation
📚 Update: README installation instructions
🎨 Style: improve button layout spacing
♻️ Refactor: extract click logic to separate method
```

### Testing
- **Test manually** on Windows 10/11
- **Test executable build** with PyInstaller
- **Verify hotkey functionality** (F6)
- **Test different click intervals** (1ms to 10s)
- **Test all click types** (Left/Right/Middle)
- **Test both modes** (Cursor/Fixed position)

## 🎯 Areas for Contribution

### 🐛 Bug Fixes
- Application crashes or freezes
- UI responsiveness issues
- Hotkey conflicts
- Memory leaks
- Cross-platform compatibility

### ✨ New Features
- **Custom hotkeys** (beyond F6)
- **Click patterns** (shapes, sequences)
- **Macro recording** and playback
- **Configuration profiles**
- **Statistics tracking**
- **Sound notifications**
- **Tray icon** functionality
- **Multi-monitor support**

### 📚 Documentation
- Code documentation
- User guides
- Video tutorials
- FAQ updates
- Translation support

### 🎨 UI/UX Improvements
- Modern themes
- Better accessibility
- Responsive design
- Icon improvements
- Animation effects

## 🔍 Code Review Process

1. **Automated checks** run on all PRs
2. **Manual review** by maintainers
3. **Testing** on different Windows versions
4. **Feedback** and requested changes
5. **Approval** and merge

## 📝 Issue Reporting

### Before Creating an Issue
- **Search existing issues** to avoid duplicates
- **Test with latest version**
- **Try the executable** version
- **Check antivirus** interference

### Bug Reports Should Include
- **Clear description** of the problem
- **Steps to reproduce**
- **Expected vs actual behavior**
- **System information** (OS, version)
- **Screenshots** if applicable
- **Error messages** (if any)

### Feature Requests Should Include
- **Clear use case** description
- **Proposed solution**
- **Alternative approaches** considered
- **UI mockups** (if applicable)

## 🛡️ Security Considerations

- **No hardcoded secrets** or credentials
- **Validate all user inputs**
- **Handle permissions** gracefully
- **Avoid privilege escalation**
- **Consider antivirus** false positives

## 📦 Release Process

1. **Update version** in relevant files
2. **Update CHANGELOG.md**
3. **Create release tag**: `git tag v1.x.x`
4. **Push tag**: `git push origin v1.x.x`
5. **GitHub Actions** builds and creates release
6. **Manual verification** of release assets

## 🤔 Questions?

- **Create an issue** for questions
- **Check existing issues** and discussions
- **Review documentation** first

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy coding!** 🎉 Thank you for helping make AutoClicker better for everyone!