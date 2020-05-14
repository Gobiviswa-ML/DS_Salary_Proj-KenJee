"""
Created on 13-05-2020
@author: Gobalakrishnan Viswanathan
"""

import pandas as pd
import numpy as np

df = pd.read_csv("glassdoor_jobs.csv")
desired_width = 320
pd.set_option('display.width', desired_width)

# Salary Parsing
# Company Name
# State Field
# Age of Company
# Parsing of Kob description

# Removing all the rows when Salary Estimation == -1
df = df[df['Salary Estimate'] != "-1"]

# Formatting salary
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'Per Hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'Employer Provided Salary:' in x.lower() else 0)

salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0].strip())
salary_without_kd = salary.apply(lambda x: x.replace('K', '').replace('$', ''))
min_strings_df = salary_without_kd.apply(lambda x: x.replace('Per Hour', '').replace('Employer Provided Salary:', ''))
df['min_salary'] = min_strings_df.apply(lambda x: x.split("-")[0]).astype(int)
df['max_salary'] = min_strings_df.apply(lambda x: x.split("-")[1]).astype(int)
df['avg_salary'] = (df['min_salary'] + df['max_salary'])/2

# Company Name formatting
df['company_txt'] = df.apply(lambda x: x['Company Name'].strip() if x['Rating'] < 0 else x['Company Name'][:-3].strip(), axis=1)

# State Field formatting
df['job_state'] = df['Location'].apply(lambda x: x.split(",")[0].strip())
df['job_code'] = df['Location'].apply(lambda x: x.split(",")[1].strip())

df['same_state'] = df.apply(lambda x: 1 if x['Location'] == x['Headquarters'] else 0, axis=1)
# Age of Company
df['age'] = df['Founded'].apply(lambda x: x if x<1 else 2020-x)

# Parsing Description
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

df = df.drop("Unnamed: 0", axis=1)

df.to_csv("jobs_data_cleaned.csv", index=False)

data = pd.read_csv("jobs_data_cleaned.csv")
