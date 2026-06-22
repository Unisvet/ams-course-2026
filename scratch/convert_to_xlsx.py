import csv
import openpyxl

def csv_to_xlsx(csv_path, xlsx_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Quiz"
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            ws.append(row)
            
    # Auto-adjust column widths for better readability in Excel
    for col in ws.columns:
        max_len = 0
        for cell in col:
            val = str(cell.value or '')
            if len(val) > max_len:
                max_len = len(val)
        col_letter = openpyxl.utils.get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 10), 50)
        
    wb.save(xlsx_path)
    print(f"Successfully converted {csv_path} to {xlsx_path}")

# Convert Week 8 Quiz
csv_to_xlsx(
    r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\docs\quiz-ams08-2026.csv",
    r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\docs\quiz-ams08-2026.xlsx"
)

# Convert Week 9 Quiz
csv_to_xlsx(
    r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\weeks\week9\quiz-ams09-2026.csv",
    r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\weeks\week9\quiz-ams09-2026.xlsx"
)
csv_to_xlsx(
    r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\weeks\week9\quiz-ams09-2026.csv",
    r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\docs\quiz-ams09-2026.xlsx"
)
