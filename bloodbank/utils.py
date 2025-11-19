from datetime import date, timedelta

def check_donor_eligibility(donor):
    problems = []

    # age check
    if donor.age < 18:
        problems.append("Donor is under 18")

    # medical check
    if donor.medical_issues:
        problems.append("Medical issues prevent donation")

    # last donation check
    if donor.last_donation_date:
        days = (date.today() - donor.last_donation_date).days
        if days < 90:
            problems.append(f"Last donation was {days} days ago (must be 90 days)")
    else:
        days = 999   # first-time donor always OK

    if problems:
        return False, problems

    return True, ["Eligible for donation"]
