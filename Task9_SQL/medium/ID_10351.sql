SELECT from_user, COUNT(*) AS count, row_number() OVER (ORDER BY COUNT(*) DESC, from_user ASC)
    FROM google_gmail_emails
    GROUP BY 1