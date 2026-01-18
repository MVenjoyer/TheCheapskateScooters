SELECT COUNT(*) AS n_admins FROM worker
    WHERE department = 'Admin' AND (joining_date >= '2014-04-01')