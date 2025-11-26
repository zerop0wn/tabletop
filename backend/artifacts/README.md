# Artifacts Directory

This directory stores artifact files (screenshots, logs, documents) that are displayed to players during games.

## File Upload

You can upload artifact files using the API endpoint:

```
POST /api/artifacts/upload
Content-Type: multipart/form-data

file: [your file]
artifact_id: [optional - ID of artifact to update]
```

Or manually place files in this directory and update the artifact's `file_url` in the database to:
`/api/artifacts/files/[filename]`

## Example Files

The seed data expects these files (you can create placeholder images/text files):
- `email1.png` - Screenshot of suspicious email
- `siem_log.txt` - SIEM log entries
- `nmap_scan.txt` - Nmap scan output
- `ransomware.png` - Ransomware screenshot
- `intel_report.pdf` - Threat intelligence report

## Supported Formats

- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Documents: `.pdf`, `.txt`, `.md`
- Logs: `.txt`, `.log`, `.csv`

Files are served at: `/api/artifacts/files/[filename]`

