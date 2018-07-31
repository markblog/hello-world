growth_of_unit_sql = "SELECT * FROM public.gpa_total_monthly where account_code in :account_codes and rates_rule = :rates_rules and effective_date >= :start and effective_date <= :end"
