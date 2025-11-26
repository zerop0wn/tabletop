# Fixes Applied

## ✅ Issue 1: Artifacts Still Pointing to External Domains

**Fixed!** 

1. **Updated Database**: Created and ran `update_artifacts.py` to migrate all existing artifacts from external URLs to local paths:
   - `https://example.com/artifacts/email1.png` → `/api/artifacts/files/email1.png`
   - All 5 artifacts now use local paths

2. **File Serving**: Artifacts are now served from `/api/artifacts/files/{filename}` which serves files from the `backend/artifacts/` directory

3. **Next Step**: You need to add the actual artifact files to `backend/artifacts/`:
   - `email1.png` - Screenshot of suspicious email
   - `siem_log.txt` - SIEM log entries
   - `nmap_scan.txt` - Nmap scan output  
   - `ransomware.png` - Ransomware screenshot
   - `intel_report.pdf` - Threat intelligence report

   Once you add these files, they will display inline in the player view (images) or as downloadable links (text/PDFs).

## ✅ Issue 2: Red Team Actions Same as Blue Team

**Fixed!**

1. **Separate Action Lists**: 
   - **Red Team Actions** (12 offensive actions):
     - Establish persistence
     - Escalate privileges
     - Move laterally
     - Exfiltrate data
     - Deploy backdoor
     - Cover tracks
     - Compromise credentials
     - Exploit vulnerability
     - Bypass security controls
     - Maintain access
     - Reconnaissance
     - Weaponize payload

   - **Blue Team Actions** (12 defensive actions):
     - Isolate host
     - Block IP address
     - Reset password
     - Disable user account
     - Collect forensic evidence
     - Notify stakeholders
     - Deploy countermeasures
     - Monitor network traffic
     - Patch vulnerable system
     - Escalate to management
     - Initiate incident response
     - Backup critical data

2. **Dynamic Display**: The action list now changes based on the player's team role (red vs blue)

3. **Visual Indicator**: The action selection header shows "(Red Team)" or "(Blue Team)" to make it clear which actions are available

## Testing

1. **Test Artifacts**:
   - Add a test image to `backend/artifacts/test.png`
   - Update an artifact's file_url to `/api/artifacts/files/test.png`
   - View as a player - image should display inline

2. **Test Team Actions**:
   - Join as Red team → See Red Team actions (offensive)
   - Join as Blue team → See Blue Team actions (defensive)
   - Actions should be completely different between teams

## Files Changed

- `backend/update_artifacts.py` - Migration script (run once)
- `backend/seed_data.py` - Updated to use local paths (for future seeds)
- `frontend/src/pages/PlayerView.tsx` - Added team-specific action lists
- `backend/app/routers/artifacts.py` - File serving endpoint
- `backend/app/routers/players.py` - Added team_role and team_name to response

