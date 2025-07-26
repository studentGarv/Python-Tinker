# ✅ Release Checklist for Python Thinker

Use this checklist to ensure consistent, high-quality releases every time.

## 🔄 Pre-Release Phase

### Code Quality & Testing
- [ ] All features work correctly in CLI mode
- [ ] All features work correctly in GUI mode
- [ ] No syntax errors or runtime exceptions
- [ ] Data persistence works correctly
- [ ] Export functions (TXT/MD) work properly
- [ ] Brainstorming mode functions correctly
- [ ] Session management works as expected
- [ ] Cross-platform compatibility verified

### Version Management
- [ ] Version number decided (semantic versioning)
- [ ] Version updated in relevant files/documentation
- [ ] Git repository is clean (no uncommitted changes)
- [ ] All changes committed to main branch
- [ ] Branch is up to date with latest changes

### Documentation
- [ ] README.md updated with new features
- [ ] CHANGELOG.md updated (if exists)
- [ ] Installation instructions verified
- [ ] Usage examples tested
- [ ] Screenshots updated (if applicable)

## 🔨 Build Phase

### Environment Setup
- [ ] Development environment is clean
- [ ] Python dependencies are up to date
- [ ] PyInstaller is working correctly
- [ ] Build scripts are tested

### Executable Creation
- [ ] Run `build_standalone.bat` successfully
- [ ] Standalone executable created in `dist/`
- [ ] Portable version created in `PythonThinker_Portable/`
- [ ] Test executable on clean Windows machine
- [ ] Verify no Python installation required for executable

### Package Creation
- [ ] Run `python prepare_release.py`
- [ ] Three ZIP files created in `release/` folder:
  - [ ] `PythonThinker-Executable-v[VERSION].zip`
  - [ ] `PythonThinker-Portable-Windows-v[VERSION].zip`
  - [ ] `PythonThinker-Source-v[VERSION].zip`
- [ ] All ZIP files contain correct contents
- [ ] File sizes are reasonable

## 🧪 Testing Phase

### Executable Testing
- [ ] Download and extract executable ZIP
- [ ] Run `PythonThinker.exe` without Python installed
- [ ] Test all major features work
- [ ] Verify data saves correctly
- [ ] Test export functionality

### Portable Testing
- [ ] Download and extract portable ZIP
- [ ] Run `Start_PythonThinker.bat`
- [ ] Test on different Windows versions if possible
- [ ] Verify folder can be copied to USB drive
- [ ] Test from different folder locations

### Source Testing
- [ ] Download and extract source ZIP
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Test launcher: `python launcher.py`
- [ ] Test direct execution: `python thinker_app.py`
- [ ] Test GUI version: `python thinker_gui.py`

## 📝 Release Preparation

### GitHub Preparation
- [ ] Create release tag (e.g., `v2025.07.26`)
- [ ] Write comprehensive release notes
- [ ] Include installation instructions
- [ ] Highlight new features and fixes
- [ ] List system requirements

### Asset Upload
- [ ] Upload `PythonThinker-Executable-v[VERSION].zip`
- [ ] Upload `PythonThinker-Portable-Windows-v[VERSION].zip`
- [ ] Upload `PythonThinker-Source-v[VERSION].zip`
- [ ] Verify all download links work
- [ ] Check file integrity (file sizes, checksums)

## 🚀 Release Phase

### GitHub Release
- [ ] Create GitHub release
- [ ] Set appropriate release type (stable/pre-release)
- [ ] Publish release
- [ ] Verify release appears in releases page
- [ ] Test download links from release page

### Communication
- [ ] Update project description if needed
- [ ] Post announcement (if applicable)
- [ ] Update any external documentation
- [ ] Notify stakeholders/users

## 🔍 Post-Release Phase

### Immediate Verification
- [ ] Download and test each release asset
- [ ] Verify installation instructions work
- [ ] Check for any immediate user feedback
- [ ] Monitor for critical issues

### Monitoring
- [ ] Watch GitHub issues for release-related problems
- [ ] Monitor download statistics
- [ ] Track user feedback and questions
- [ ] Document any issues for next release

### Documentation Updates
- [ ] Update README with latest version info
- [ ] Mark old releases as outdated (if needed)
- [ ] Update any tutorials or guides
- [ ] Archive previous version notes

## 🚨 Emergency Procedures

### If Critical Bug Found After Release
- [ ] Create hotfix branch immediately
- [ ] Apply minimal fix required
- [ ] Test hotfix thoroughly
- [ ] Create patch release (e.g., v2025.07.26.1)
- [ ] Update release notes with hotfix details
- [ ] Notify users of urgent update

### If Release Needs to be Pulled
- [ ] Mark release as draft (hide from users)
- [ ] Communicate issue to any users who downloaded
- [ ] Fix underlying problem
- [ ] Create new release with incremented version
- [ ] Learn from the issue for future releases

## 📊 Release Metrics to Track

- [ ] Download counts per package type
- [ ] User feedback sentiment
- [ ] GitHub stars/forks changes
- [ ] Issue reports related to release
- [ ] Time between releases

## 🎯 Quality Gates

**Do not release if:**
- Any core functionality is broken
- Executable doesn't run on clean Windows machine
- Data loss could occur
- Security vulnerabilities exist
- Documentation is significantly outdated

**Always remember:**
- Quality over speed
- User experience is paramount
- Each release represents the project's reputation
- It's better to delay than release broken software

---

**Final Check**: Have you completed ALL items? If yes, you're ready to release! 🎉