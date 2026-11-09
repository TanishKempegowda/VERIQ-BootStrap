from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_policy_pdf():
    c = canvas.Canvas("ABC_Tech_Policy.pdf", pagesize=letter)
    textobject = c.beginText(40, 750)
    textobject.setFont("Helvetica", 12)
    
    policy_text = [
        "ABC TECHNOLOGIES - EMPLOYEE OFFBOARDING POLICY",
        "Effective Date: January 1, 2024",
        "",
        "1. SYSTEM ACCESS REVOCATION",
        "All system access, including Active Directory, email, and internal databases, must be revoked by the IT department on the employee's official last working day. A ticket must be logged in the IT helpdesk system confirming deactivation.",
        "",
        "2. PHYSICAL BADGE RETURN",
        "The departing employee must return their physical office access badge to the HR department by 5:00 PM on their last working day.",
        "",
        "3. KNOWLEDGE TRANSFER",
        "Before the final working day, the employee's direct manager must sign off on the Knowledge Transfer (KT) Checklist, ensuring all ongoing projects are documented and handed over.",
        "",
        "4. EXIT INTERVIEW",
        "An HR representative must conduct a mandatory exit interview with the employee prior to their departure.",
        "",
        "5. CONFIDENTIAL DATA WIPING",
        "If the employee used any personal devices (BYOD) for company work, IT must verify that all company data and proprietary code have been permanently wiped before the employee leaves the premises."
    ]
    
    for line in policy_text:
        textobject.textLine(line)
        
    c.drawText(textobject)
    c.save()
    print("✅ Successfully created 'ABC_Tech_Policy.pdf'")

if __name__ == "__main__":
    create_policy_pdf()