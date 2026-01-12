# docling backup for pdf extraction

from docling.document_converter import DocumentConverter
import pandas as pd
# Initialize converter
converter = DocumentConverter()

# Convert PDF
result = converter.convert("CircuitInformation.pdf")

# Export to markdown (human-readable)

doc_filename = result.input.file.stem

# Export tables
for table_ix, table in enumerate(result.document.tables):
    table_df: pd.DataFrame = table.export_to_dataframe(doc=result.document)
    print(f"## Table {table_ix}")
    print(table_df.to_markdown())

    # Save the table as CSV
    element_csv_filename = f"{doc_filename}-table-{table_ix + 1}.csv"
    print(f"Saving CSV table to {element_csv_filename}")
    table_df.to_csv(element_csv_filename)