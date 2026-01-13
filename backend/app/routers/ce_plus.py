from fastapi import APIRouter
from fastapi.responses import Response
from pathlib import Path
import zipfile
import io
import gzip

router = APIRouter()

# EICAR test string - safe test file used for antivirus testing
EICAR_TEST_STRING = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

# Directory for storing test files
CE_PLUS_DIR = Path("/app/ce_plus_tests")
CE_PLUS_DIR.mkdir(exist_ok=True, parents=True)


def create_zip_with_eicar(filename_in_zip: str = "EICAR.TXT"):
    """Create a ZIP file containing EICAR test string."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(filename_in_zip, EICAR_TEST_STRING)
    return zip_buffer.getvalue()


def create_gzip_with_eicar():
    """Create a GZIP file containing EICAR test string."""
    gzip_buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=gzip_buffer, mode='wb') as gz_file:
        gz_file.write(EICAR_TEST_STRING.encode('utf-8'))
    return gzip_buffer.getvalue()


def create_batch_file():
    """Create a Windows batch file with EICAR."""
    # Batch file that contains EICAR string
    batch_content = f'@echo off\nREM {EICAR_TEST_STRING}\necho Test file for CE Plus assessment\n'
    return batch_content.encode('utf-8')


def create_powershell_file():
    """Create a PowerShell script with EICAR."""
    ps_content = f'# {EICAR_TEST_STRING}\nWrite-Host "CE Plus Test File"\n'
    return ps_content.encode('utf-8')


def create_vbs_file():
    """Create a VBScript file with EICAR."""
    vbs_content = f'REM {EICAR_TEST_STRING}\nWScript.Echo "CE Plus Test File"\n'
    return vbs_content.encode('utf-8')


def create_bash_file():
    """Create a Bash script with EICAR."""
    bash_content = f'#!/bin/bash\n# {EICAR_TEST_STRING}\necho "CE Plus Test File"\n'
    return bash_content.encode('utf-8')


def create_docx_with_eicar():
    """Create a DOCX file (ZIP-based) containing EICAR."""
    # DOCX is a ZIP file with specific structure
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Minimal DOCX structure
        zip_file.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>''')
        zip_file.writestr('_rels/.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>''')
        zip_file.writestr('word/document.xml', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
<w:p><w:r><w:t>{EICAR_TEST_STRING}</w:t></w:r></w:p>
<w:p><w:r><w:t>CE Plus Test Document</w:t></w:r></w:p>
</w:body>
</w:document>''')
    return zip_buffer.getvalue()


def create_xlsx_with_eicar():
    """Create an XLSX file (ZIP-based) containing EICAR."""
    # XLSX is a ZIP file with specific structure
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
</Types>''')
        zip_file.writestr('_rels/.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>''')
        zip_file.writestr('xl/workbook.xml', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets>
</workbook>''')
        zip_file.writestr('xl/worksheets/sheet1.xml', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData>
<row r="1"><c r="A1" t="inlineStr"><is><t>{EICAR_TEST_STRING}</t></is></c></row>
</sheetData>
</worksheet>''')
    return zip_buffer.getvalue()


def create_pdf_with_eicar():
    """Create a PDF file containing EICAR string."""
    # Simple PDF structure with EICAR text
    pdf_content = f'''%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
>>
endobj
4 0 obj
<<
/Length 100
>>
stream
BT
/F1 12 Tf
100 700 Td
({EICAR_TEST_STRING}) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000300 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
400
%%EOF'''
    return pdf_content.encode('utf-8')


def create_apk_with_eicar():
    """Create an APK file (ZIP-based) containing EICAR."""
    # APK is a ZIP file with Android-specific structure
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Minimal APK structure
        zip_file.writestr('AndroidManifest.xml', '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.ceplus.test">
    <application android:label="CE Plus Test">
    </application>
</manifest>''')
        zip_file.writestr('classes.dex', b'dex\n035\x00' + EICAR_TEST_STRING.encode('utf-8'))
        zip_file.writestr('META-INF/MANIFEST.MF', f'Manifest-Version: 1.0\n{EICAR_TEST_STRING}\n')
    return zip_buffer.getvalue()


def create_jar_with_eicar():
    """Create a JAR file (ZIP-based) containing EICAR."""
    # JAR is a ZIP file with Java-specific structure
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Minimal JAR structure with manifest
        zip_file.writestr('META-INF/MANIFEST.MF', f'''Manifest-Version: 1.0
{EICAR_TEST_STRING}
Main-Class: Test
''')
        # Create a simple Java class file placeholder
        zip_file.writestr('Test.class', b'\xca\xfe\xba\xbe' + EICAR_TEST_STRING.encode('utf-8')[:60])
        zip_file.writestr('Test.java', f'// {EICAR_TEST_STRING}\npublic class Test {{ public static void main(String[] args) {{ }} }}')
    return zip_buffer.getvalue()


def create_python_file():
    """Create a Python script with EICAR."""
    py_content = f'# {EICAR_TEST_STRING}\nprint("CE Plus Test File")\n'
    return py_content.encode('utf-8')


def create_javascript_file():
    """Create a JavaScript file with EICAR."""
    js_content = f'// {EICAR_TEST_STRING}\nconsole.log("CE Plus Test File");\n'
    return js_content.encode('utf-8')


def create_msi_zip():
    """Create a ZIP containing MSI-like structure (simplified)."""
    # MSI files are complex, so we'll create a ZIP that simulates it
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('test.msi', EICAR_TEST_STRING)
        zip_file.writestr('META-INF/manifest.xml', f'<?xml version="1.0"?><manifest>{EICAR_TEST_STRING}</manifest>')
    return zip_buffer.getvalue()


def create_scr_file():
    """Create a Windows screensaver file with EICAR."""
    # SCR files are essentially EXE files, we'll use a simple structure
    scr_content = b'MZ' + EICAR_TEST_STRING.encode('utf-8') + b'\x00' * 100
    return scr_content


@router.get("/")
async def get_ce_plus_info():
    """Get information about available CE Plus malware tests."""
    return {
        "title": "UK Cyber Essentials Plus - Malware Testing",
        "description": "Comprehensive endpoint protection testing for CE Plus assessment",
        "categories": [
            {
                "id": "eicar",
                "name": "EICAR Test Files",
                "description": "Standard EICAR test patterns recognized by all antivirus software",
                "platforms": [
                    {
                        "id": "all",
                        "name": "All Platforms",
                        "tests": [
                            {"id": "eicar_com", "name": "EICAR.COM", "description": "Standard EICAR test file (.com) - Windows executable format", "type": "executable"},
                            {"id": "eicar_txt", "name": "EICAR.TXT", "description": "EICAR test file (.txt) - Universal text format", "type": "text"},
                            {"id": "eicar_zip", "name": "EICAR.ZIP", "description": "EICAR test file in ZIP archive - Universal container format", "type": "container"},
                        ]
                    },
                ]
            },
            {
                "id": "executables",
                "name": "Executable Files",
                "description": "Native binaries and scripts executable by default on common platforms",
                "platforms": [
                    {
                        "id": "windows",
                        "name": "Windows",
                        "tests": [
                            {"id": "bat_file", "name": "test.bat", "description": "Batch script with EICAR pattern", "type": "executable"},
                            {"id": "ps1_file", "name": "test.ps1", "description": "PowerShell script with EICAR pattern", "type": "executable"},
                            {"id": "vbs_file", "name": "test.vbs", "description": "VBScript with EICAR pattern", "type": "executable"},
                            {"id": "scr_file", "name": "test.scr", "description": "Windows screensaver file with EICAR pattern", "type": "executable"},
                            {"id": "msi_zip", "name": "test.msi (in ZIP)", "description": "MSI installer in ZIP archive", "type": "container"},
                            {"id": "exe_zip", "name": "test.exe (in ZIP)", "description": "Executable file in ZIP archive", "type": "container"},
                        ]
                    },
                    {
                        "id": "mac",
                        "name": "macOS",
                        "tests": [
                            {"id": "sh_file", "name": "test.sh", "description": "Bash script with EICAR pattern", "type": "executable"},
                            {"id": "py_file", "name": "test.py", "description": "Python script with EICAR pattern", "type": "executable"},
                            {"id": "dmg_file", "name": "test.dmg", "description": "DMG disk image with EICAR", "type": "container"},
                            {"id": "pkg_zip", "name": "test.pkg (in ZIP)", "description": "Package file in ZIP archive", "type": "container"},
                        ]
                    },
                    {
                        "id": "android",
                        "name": "Android",
                        "tests": [
                            {"id": "malicious_apk", "name": "malicious.apk", "description": "Malicious APK file with EICAR pattern", "type": "executable"},
                            {"id": "apk_zip", "name": "malicious.apk (in ZIP)", "description": "Malicious APK in ZIP archive", "type": "container"},
                        ]
                    },
                    {
                        "id": "java",
                        "name": "Java (Cross-Platform)",
                        "tests": [
                            {"id": "jar_file", "name": "test.jar", "description": "Java JAR file with EICAR pattern", "type": "executable"},
                            {"id": "jar_zip", "name": "test.jar (in ZIP)", "description": "Java JAR file in ZIP archive", "type": "container"},
                        ]
                    },
                    {
                        "id": "scripts",
                        "name": "Script Files (Cross-Platform)",
                        "tests": [
                            {"id": "py_file", "name": "test.py", "description": "Python script with EICAR pattern", "type": "executable"},
                            {"id": "js_file", "name": "test.js", "description": "JavaScript file with EICAR pattern", "type": "executable"},
                        ]
                    },
                ]
            },
            {
                "id": "containers",
                "name": "Container Formats",
                "description": "Compressed files that may contain malicious content",
                "platforms": [
                    {
                        "id": "all",
                        "name": "All Platforms",
                        "tests": [
                            {"id": "zip_eicar", "name": "EICAR.ZIP", "description": "ZIP archive containing EICAR", "type": "container"},
                            {"id": "gz_eicar", "name": "EICAR.gz", "description": "GZIP archive containing EICAR", "type": "container"},
                            {"id": "zip_nested", "name": "nested.zip", "description": "Nested ZIP archives with EICAR", "type": "container"},
                        ]
                    },
                ]
            },
            {
                "id": "documents",
                "name": "Documents with Embedded Malware",
                "description": "Common document types containing inert malware samples",
                "platforms": [
                    {
                        "id": "all",
                        "name": "All Platforms",
                        "tests": [
                            {"id": "docx_eicar", "name": "test.docx", "description": "Word document with embedded EICAR", "type": "document"},
                            {"id": "xlsx_eicar", "name": "test.xlsx", "description": "Excel spreadsheet with embedded EICAR", "type": "document"},
                            {"id": "pdf_eicar", "name": "test.pdf", "description": "PDF document with embedded EICAR", "type": "document"},
                        ]
                    },
                ]
            },
        ]
    }


@router.get("/download/{category}/{platform}/{test_id}")
async def download_test_file(category: str, platform: str, test_id: str):
    """Download test file for specified category, platform and test type."""
    
    # Validate category
    valid_categories = ["eicar", "executables", "containers", "documents"]
    if category not in valid_categories:
        return Response(
            content=f"Invalid category. Must be one of: {', '.join(valid_categories)}",
            status_code=400
        )
    
    # Validate platform
    valid_platforms = ["windows", "mac", "ios", "android", "java", "scripts", "all"]
    if platform not in valid_platforms:
        return Response(
            content=f"Invalid platform. Must be one of: {', '.join(valid_platforms)}",
            status_code=400
        )
    
    # EICAR category
    if category == "eicar":
        if test_id == "eicar_com" and platform == "all":
            content = EICAR_TEST_STRING.encode('utf-8')
            filename = "EICAR.COM"
            media_type = "application/x-msdownload"
            
        elif test_id == "eicar_txt" and platform == "all":
            content = EICAR_TEST_STRING.encode('utf-8')
            filename = "EICAR.TXT"
            media_type = "text/plain"
            
        elif test_id == "eicar_zip" and platform == "all":
            content = create_zip_with_eicar()
            filename = "EICAR.ZIP"
            media_type = "application/zip"
            
        else:
            return Response(
                content=f"Invalid test_id '{test_id}' for platform '{platform}' in category '{category}'",
                status_code=400
            )
    
    # Executables category
    elif category == "executables":
        if test_id == "bat_file" and platform == "windows":
            content = create_batch_file()
            filename = "test.bat"
            media_type = "application/x-msdos-program"
            
        elif test_id == "ps1_file" and platform == "windows":
            content = create_powershell_file()
            filename = "test.ps1"
            media_type = "application/x-powershell"
            
        elif test_id == "vbs_file" and platform == "windows":
            content = create_vbs_file()
            filename = "test.vbs"
            media_type = "application/x-vbs"
            
        elif test_id == "scr_file" and platform == "windows":
            content = create_scr_file()
            filename = "test.scr"
            media_type = "application/x-msdownload"
            
        elif test_id == "msi_zip" and platform == "windows":
            content = create_msi_zip()
            filename = "test.zip"
            media_type = "application/zip"
            
        elif test_id == "exe_zip" and platform == "windows":
            # Create ZIP containing a .bat file (simulating .exe in ZIP)
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr("test.bat", create_batch_file().decode('utf-8'))
            content = zip_buffer.getvalue()
            filename = "test.zip"
            media_type = "application/zip"
            
        elif test_id == "sh_file" and platform == "mac":
            content = create_bash_file()
            filename = "test.sh"
            media_type = "application/x-sh"
            
        elif test_id == "py_file" and platform == "mac":
            content = create_python_file()
            filename = "test.py"
            media_type = "text/x-python"
            
        elif test_id == "dmg_file" and platform == "mac":
            # DMG file (simplified - ZIP format)
            content = create_zip_with_eicar("EICAR.TXT")
            filename = "test.dmg"
            media_type = "application/x-apple-diskimage"
            
        elif test_id == "pkg_zip" and platform == "mac":
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr("test.pkg", EICAR_TEST_STRING)
            content = zip_buffer.getvalue()
            filename = "test.zip"
            media_type = "application/zip"
            
        elif test_id == "malicious_apk" and platform == "android":
            content = create_apk_with_eicar()
            filename = "malicious.apk"
            media_type = "application/vnd.android.package-archive"
            
        elif test_id == "apk_zip" and platform == "android":
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr("malicious.apk", create_apk_with_eicar())
            content = zip_buffer.getvalue()
            filename = "malicious.zip"
            media_type = "application/zip"
            
        elif test_id == "jar_file" and platform == "java":
            content = create_jar_with_eicar()
            filename = "test.jar"
            media_type = "application/java-archive"
            
        elif test_id == "jar_zip" and platform == "java":
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr("test.jar", create_jar_with_eicar())
            content = zip_buffer.getvalue()
            filename = "test.zip"
            media_type = "application/zip"
            
        elif test_id == "py_file" and platform == "scripts":
            content = create_python_file()
            filename = "test.py"
            media_type = "text/x-python"
            
        elif test_id == "js_file" and platform == "scripts":
            content = create_javascript_file()
            filename = "test.js"
            media_type = "application/javascript"
            
        else:
            return Response(
                content=f"Invalid test_id '{test_id}' for platform '{platform}' in category '{category}'",
                status_code=400
            )
    
    # Containers category
    elif category == "containers":
        if test_id == "zip_eicar":
            content = create_zip_with_eicar()
            filename = "EICAR.ZIP"
            media_type = "application/zip"
            
        elif test_id == "gz_eicar":
            content = create_gzip_with_eicar()
            filename = "EICAR.gz"
            media_type = "application/gzip"
            
        elif test_id == "zip_nested":
            # Nested ZIP: ZIP containing a ZIP containing EICAR
            inner_zip = create_zip_with_eicar()
            outer_zip_buffer = io.BytesIO()
            with zipfile.ZipFile(outer_zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr("inner.zip", inner_zip)
            content = outer_zip_buffer.getvalue()
            filename = "nested.zip"
            media_type = "application/zip"
            
        else:
            return Response(
                content=f"Invalid test_id '{test_id}' for category '{category}'",
                status_code=400
            )
    
    # Documents category
    elif category == "documents":
        if test_id == "docx_eicar":
            content = create_docx_with_eicar()
            filename = "test.docx"
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            
        elif test_id == "xlsx_eicar":
            content = create_xlsx_with_eicar()
            filename = "test.xlsx"
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
        elif test_id == "pdf_eicar":
            content = create_pdf_with_eicar()
            filename = "test.pdf"
            media_type = "application/pdf"
            
        else:
            return Response(
                content=f"Invalid test_id '{test_id}' for category '{category}'",
                status_code=400
            )
    
    else:
        return Response(
            content=f"Invalid category '{category}'",
            status_code=400
        )
    
    return Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Content-Type-Options": "nosniff"
        }
    )


@router.get("/test-status")
async def get_test_status():
    """Get status information about the CE Plus testing endpoints."""
    return {
        "status": "operational",
        "message": "CE Plus malware testing endpoints are available",
        "eicar_info": "EICAR test files are safe test patterns used to verify antivirus detection",
        "warning": "These files are designed to be detected by antivirus software. This is expected behavior.",
        "compliance": "Test files align with UK Cyber Essentials Plus Test Specification v3.2 requirements"
    }
