import re
import sys
from pathlib import Path

def redact_sensitive_data(text):
    """
    Scan text and replace sensitive information with placeholder tags.
    
    Handles:
    - Social Security Numbers (SSN) in formats: XXX-XX-XXXX
    - Email addresses
    
    Args:
        text (str): Input text to process
        
    Returns:
        str: Text with sensitive data redacted
    """
    
    # Pattern for SSN: XXX-XX-XXXX where X is a digit
    # Matches patterns like 274-38-0001, 351-94-0402, etc.
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    
    # Pattern for email addresses (standard email format)
    # Handles local-part@domain format
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Pattern for email addresses with "redacted.user@..." format (from the log)
    redacted_email_pattern = r'redacted\.user@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
    
    # Count how many redactions were made
    redaction_count = 0
    
    # Store the original text for counting
    original_text = text
    
    # Redact SSNs - replace with [SSN_REDACTED]
    text, ssn_count = re.subn(ssn_pattern, '[SSN_REDACTED]', text)
    redaction_count += ssn_count
    
    # Redact standard email addresses
    text, email_count = re.subn(email_pattern, '[EMAIL_REDACTED]', text)
    redaction_count += email_count
    
    # Redact specifically formatted redacted.user email addresses
    text, redacted_email_count = re.subn(redacted_email_pattern, '[EMAIL_REDACTED]', text)
    redaction_count += redacted_email_count
    
    # Print statistics if redactions were made
    if redaction_count > 0:
        print(f"[INFO] Redacted {ssn_count} SSN(s) and {email_count + redacted_email_count} email address(es)")
    
    return text

def process_file(input_file, output_file=None):
    """
    Read a file, redact sensitive data, and write to output file.
    
    Args:
        input_file (str): Path to input file
        output_file (str, optional): Path to output file. If None, prints to console.
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Redact sensitive data
        redacted_content = redact_sensitive_data(content)
        
        # Write or print the result
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(redacted_content)
            print(f"[SUCCESS] Redacted content written to: {output_file}")
        else:
            print("\n" + "="*80)
            print("REDACTED CONTENT:")
            print("="*80)
            print(redacted_content)
        
        return True
        
    except FileNotFoundError:
        print(f"[ERROR] File not found: {input_file}")
        return False
    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")
        return False

def process_text_directly(text):
    """
    Process text directly without file I/O.
    
    Args:
        text (str): Input text to process
        
    Returns:
        str: Redacted text
    """
    return redact_sensitive_data(text)

def main():
    """
    Main function to demonstrate the script usage.
    """
    # Example usage with the provided log content
    sample_log = """[2025-04-10 08:13:22] [FIREWALL] [POLICY: DLP-Data_Exfiltration] [ACTION: BLOCK] [SRC_IP: 192.168.12.45] [DST_IP: 34.120.8.92] [USER: jdavis] [DATA_PATTERN: 274-38-0001] [FILE: employee_review_q1.xlsx]  
[2025-04-10 08:17:05] [PROXY] [CATEGORY: Personal_Email] [ACTION: ALLOW] [USER: msmith] [URL: https://mail.example-test.local] [EMAIL_DETECTED: redacted.user@example-test.local] [POLICY: Acceptable Use - Limited Personal]  
[2025-04-10 08:22:47] [IDS] [RULE: CORP-1002 - Unencrypted PII Transmission] [ACTION: ALERT] [SRC_IP: 10.2.34.17] [USER: twilson] [PAYLOAD_CONTAINS: 351-94-0402] [DEST: 3.89.200.55:8080]  
[2025-04-10 08:35:10] [DLP] [CHANNEL: HTTP_Upload] [ACTION: QUARANTINE] [USER: arodriguez] [FILE: dept_salaries.csv] [PATTERNS_MATCHED: 058-16-0817, 574-62-0922] [POLICY: HR_Data_Protection]  
[2025-04-10 08:42:03] [ACTIVE DIRECTORY] [EVENT: 4624] [LOGON_TYPE: 10] [USER: nnguyen] [WORKSTATION: WS-022] [FROM_IP: 192.168.1.108] [POLICY: MFA-Required - Compliant]  
[2025-04-10 08:44:19] [EMAIL_GATEWAY] [RULE: Outbound_Encryption_Fail] [ACTION: BLOCK] [FROM: jlee@corp-test.local] [TO: external-partner@example-test.local] [SUBJECT: Client SSN List] [ATTACHMENT: 511-40-0444]  
[2025-04-10 08:59:33] [VPN] [AUTH_SUCCESS] [USER: rpatel] [AUTH_METHOD: Cert+Password] [ASSIGNED_IP: 172.16.10.52] [POLICY: Remote_Access - Approved Hours]  
[2025-04-10 09:05:57] [CASB] [APP: Box-ShadowIT] [ACTION: BLOCK] [USER: hkim] [DATA_CLASS: 543-14-0601] [JUSTIFICATION: "Unmanaged cloud storage - Policy CR-9"]  
[2025-04-10 09:12:44] [ENDPOINT_DLP] [PROCESS: winword.exe] [ACTION: ALERT] [USER: ejiang] [FILE: C:\\Users\\ejiang\\Desktop\\2019_tax_forms\\w2_fake_ssn_placeholder.pdf] [MATCH: 337-30-0303]  
[2025-04-10 09:21:08] [SIEM] [CORRELATION: Multiple DLP Blocks - Same User] [USER: jdavis] [COUNT: 3 attempts] [FIRST_SEEN: 08:13:22] [LAST_SEEN: 08:17:05] [TRIGGER: Incident Response - Auto_Ticket IR-442]"""

    # Check if a file was provided as command-line argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        process_file(input_file, output_file)
    else:
        # Demo: Process the sample log
        print("No input file provided. Running demo with sample log...")
        redacted = process_text_directly(sample_log)
        print("\n" + "="*80)
        print("ORIGINAL LOG (first 500 chars):")
        print("="*80)
        print(sample_log[:500] + "...\n")
        print("="*80)
        print("REDACTED LOG:")
        print("="*80)
        print(redacted)

if __name__ == "__main__":
    main()