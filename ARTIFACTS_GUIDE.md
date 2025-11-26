# Artifacts Management Guide

## Overview

Artifacts are evidence items (screenshots, logs, documents) that players see during game phases. They are now stored locally instead of pointing to external URLs.

## Team Differentiation

**Red Team** and **Blue Team** now see clearly differentiated views:

1. **Team Badge**: A colored badge at the top shows which team you're on (RED/BLUE)
2. **Team-Specific Objectives**: The objective box is color-coded:
   - Red Team: Red background with red text
   - Blue Team: Blue background with blue text
3. **Team Name Display**: Your team name is shown in the objective header

## Adding Artifacts

### Method 1: Via API (Recommended)

1. Use the upload endpoint:
   ```bash
   curl -X POST http://localhost:8001/api/artifacts/upload \
     -H "Authorization: Bearer YOUR_GM_TOKEN" \
     -F "file=@path/to/your/image.png" \
     -F "artifact_id=1"
   ```

2. This will update the artifact's `file_url` automatically.

### Method 2: Manual File Placement

1. Place your artifact file in `backend/artifacts/` directory
2. Update the artifact in the database to set `file_url` to `/api/artifacts/files/[filename]`

### Method 3: Direct Database Update

```sql
UPDATE artifacts 
SET file_url = '/api/artifacts/files/my_screenshot.png' 
WHERE id = 1;
```

## Artifact Display

- **Images** (screenshots): Displayed inline in the player view
- **Text files**: Shown as downloadable links
- **PDFs**: Shown as downloadable links
- **Other files**: Shown as downloadable links

## File Naming

Use descriptive, safe filenames:
- ✅ `suspicious_email_phase1.png`
- ✅ `siem_logs_phase2.txt`
- ❌ `file with spaces.png` (use underscores)
- ❌ `../../../etc/passwd` (security: path traversal prevented)

## Example Workflow

1. Create a screenshot or document for your scenario
2. Save it with a descriptive name (e.g., `phishing_email_phase1.png`)
3. Upload via API or place in `backend/artifacts/`
4. Update the artifact record to point to `/api/artifacts/files/phishing_email_phase1.png`
5. Players will see it automatically in the next phase

## Testing

To test artifact display:
1. Place a test image in `backend/artifacts/test.png`
2. Update an artifact's `file_url` to `/api/artifacts/files/test.png`
3. View as a player - the image should display inline

