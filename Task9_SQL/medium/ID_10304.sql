SELECT title, budget, CEIL((end_date-start_date)*exp) FROM linkedin_projects
    JOIN (SELECT project_id, SUM(salary)/365 AS exp FROM linkedin_employees
              JOIN linkedin_emp_projects ON emp_id = id  GROUP BY 1)x
    ON id = project_id
    WHERE CEIL((end_date-start_date)*exp) > budget