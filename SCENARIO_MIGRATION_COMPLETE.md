# Scenario Migration Complete ✅

## Enhanced Ransomware Incident Scenario

The scenario has been successfully migrated to a **5-phase realistic ransomware attack** based on real-world tactics.

### Phase Structure

1. **Phase 1: Initial Compromise** (15 minutes)
   - Phishing email → PowerShell malware execution
   - Red: Establish access, begin reconnaissance
   - Blue: Identify entry point, contain threat
   - Artifacts: Phishing email screenshot, EDR alert

2. **Phase 2: Establishing Foothold** (15 minutes)
   - Persistence mechanisms, network scanning, C2 communication
   - Red: Create backdoors, map network, identify targets
   - Blue: Detect persistence, block C2, protect assets
   - Artifacts: Network scan results, C2 traffic analysis

3. **Phase 3: Privilege Escalation & Lateral Movement** (15 minutes)
   - Domain admin access, lateral movement to critical systems
   - Red: Escalate privileges, move to DC/file servers/backups
   - Blue: Detect escalation, isolate critical systems, revoke credentials
   - Artifacts: Privilege escalation logs, lateral movement indicators

4. **Phase 4: Data Exfiltration** (15 minutes)
   - Large-scale data theft (450 GB) to cloud storage
   - Red: Complete exfiltration, prepare for encryption
   - Blue: Stop exfiltration, assess regulatory impact, notify stakeholders
   - Artifacts: Exfiltration traffic analysis, data classification report

5. **Phase 5: Ransomware Deployment & Response** (20 minutes)
   - LockBit 3.0 deployment, 200+ systems encrypted, ransom demand
   - Red: Deploy ransomware, deliver ransom note, maintain access
   - Blue: Contain encryption, assess damage, decide on ransom payment, initiate recovery
   - Artifacts: Ransomware note screenshot, impact assessment, backup status

### Key Improvements

- **Realistic Attack Timeline**: Follows actual ransomware kill chain
- **Detailed Briefings**: Includes timestamps, system names, technical details
- **11 Enhanced Artifacts**: Realistic descriptions with specific file paths
- **Team-Specific Objectives**: Clear differentiation between Red and Blue team goals
- **Business Context**: Regulatory considerations, business impact, recovery options

### Artifact Files Needed

Place these files in `backend/artifacts/`:
- `phishing_email_phase1.png` - Phishing email screenshot
- `edr_alert_phase1.txt` - EDR log output
- `nmap_scan_phase2.txt` - Network scan results
- `c2_traffic_phase2.txt` - C2 communication logs
- `privilege_escalation_phase3.txt` - Windows event logs
- `lateral_movement_phase3.txt` - SIEM correlation logs
- `exfiltration_traffic_phase4.txt` - Network flow analysis
- `data_classification_phase4.pdf` - Data classification report
- `ransomware_note_phase5.png` - Ransomware note screenshot
- `impact_assessment_phase5.pdf` - Business impact assessment
- `backup_status_phase5.txt` - Backup system status

### Next Steps

1. **Create Artifact Files**: Add the 11 artifact files listed above
2. **Test the Scenario**: Create a new game and walk through all 5 phases
3. **Customize**: Adjust phase durations, objectives, or artifacts as needed

The migration preserved existing games (cleared their current_phase_id) and updated the scenario structure. New games will use the enhanced 5-phase scenario automatically.

