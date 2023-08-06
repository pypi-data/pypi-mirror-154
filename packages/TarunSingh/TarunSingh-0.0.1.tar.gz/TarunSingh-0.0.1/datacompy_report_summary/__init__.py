import pandas as pd
def comparison_report_summary(file_path):
  """   Output report summary for comparison report for two datasets will be saved in below format.
  Row Index                  Column Index
  Row 0      ****** Column Summary ******
  Row 1      Number of columns in common with matching schemas: 261
  Row 2      Number of columns in common with schema differences: 0
  Row 3      Number of columns in base but not compare: 0
  Row 4      Number of columns in compare but not base: 0

  Row 5      ****** Row Summary ******
  Row 6      Number of rows in common: 4817943
  Row 7      Number of rows in base but not compare: 0
  Row 8      Number of rows in compare but not base: 0
  Row 9      Number of duplicate rows found in base: 0
  Row 10     Number of duplicate rows found in compare: 0

  Row 11     ****** Row Comparison ******
  Row 12     Number of rows with some columns unequal: 0
  Row 13     Number of rows with all columns equal: 4817943

  Row 14     ****** Column Comparison ******
  Row 15     Number of columns compared with some values unequal: 0
  Row 16     Number of columns compared with all values equal: 260

  Row 17     ****** Columns with Equal/Unequal Values ******

  From this report we are checking for row no. 2,3,4,7,8,9,10,12,15 values to be '0' as the results generated will always be the same if two datasets matches.
  If there is any difference between the datasets from the above results it will result into datasets mismatch"""

  # Reading the generated report and only display if the datasets are exactly matching or not
  report_summary = pd.read_csv(file_path,header=None)

  # Only selecting rows relevant to find out exact comparison
  filtered_report_summary = report_summary[report_summary.index<18]

  # Split the string and only get the string after ":" from the rows
  filtered_report_summary[0] = filtered_report_summary[0].str.split(':').str.get(-1)

  # Checking for rows where value should be 0 for exact comparison
  check_list = [2,3,4,7,8,9,10,12,15]

  # Initialize counter as 0 and iterate over the table rows to check if check_list rows values matches " 0". If it matches increment counter
  count = 0
  for i in range(len(check_list)):
    if filtered_report_summary[0][check_list[i]] == ' 0':
      count = count+1 
      
  # Check if count value is equal to 9 for an exact match. If counter values is less than 9 then datasets doesn't matches and return False.
  if count == 9:
    return True
  else:
    return False
