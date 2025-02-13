## Ohio Public Employee Salaries

Data are from [http://www.tos.ohio.gov/Transparency_State.aspx](http://www.tos.ohio.gov/Transparency_State.aspx) 

* State salary data from 2010--2016
  
  "All gross wage information contained in this database comes from the Ohio Department of Administrative Services including any errors, omissions, or inaccuracies. Gross wages may include, but not limited to, overtime, compensatory time, sick leave, vacation leave, personal leave, cost savings day deductions and leave payouts. Some employees may not have worked a complete year in their current position so gross wages may not be equivalent to full annual salary."

* K-12 salary data from 2006--2007 year to 2016--2017 year
  
  "All data contained in this database was provided by the Ohio Department of Education (ODE) and comes from the Education Management Information System (EMIS), which compiles information from each individual public school district in Ohio. (Click here for the EMIS Manual) Annual or hourly pay, days worked, hours per day, education level, and years teaching experience are shown as they are reported to ODE by individual school districts, in accordance with reporting standards set in the EMIS manual. These elements may not completely depict actual annual salaries, time worked, or years teaching experience. No benefits are included in the salary data. In instances where a school employee works multiple positions within a given year (for example a teacher who also coaches a sports team), these positions are listed separately."

* Local Salaries
  
  The python script [oh_local_salaries.py](oh_local_salaries.py) iterates through results from http://www.tos.ohio.gov/local_salary and creates a CSV [oh_local_salaries.csv](oh_local_salaries.csv). The CSV has the following columns: `year, name, position, gross_wage, hourly_rate, overtime, entity_type (from the dropdown), entity_name (from the dropdown)`

* Pension

  The python script [oh_pensions.py](oh_pensions.py) iterates through the dropdown results from http://www.tos.ohio.gov/Transparency_Pension.aspx and creates a CSV [oh_pensions.csv](oh_pensions.csv) that has the following columns: `year, name, job_title, recruitment_system, salary`

### Running the scripts

```
pip install -r requirements.txt
python oh_pensions.py
python oh_local_salaries.py
```

