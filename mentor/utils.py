from calendar import isleap


def gregorian_to_jalali(gyear, gmonth, gday):
    gregorian_start = (621, 3, 22)  # March 22, 621 AD
    jalali_start = (1, 1, 1)  # March 22, 622 AD
    gy, gm, gd = int(gyear), int(gmonth), int(gday)

    # Calculate the number of days since March 22, 621 AD (gregorian_start)
    days_since_gregorian_start = (
        365 * (gy - gregorian_start[0]) +
        (gy - gregorian_start[0]) // 4 -
        (gy - gregorian_start[0] - 1) // 100 +
        (gy - gregorian_start[0]) // 400 +
        sum([31, 28 + isleap(gy), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][:gm - 1]) +
        gd - 1
    )

    # Calculate the number of days since March 22, 622 AD (jalali_start)
    days_since_jalali_start = days_since_gregorian_start - (jalali_start[0] - gregorian_start[0]) * 365 - ((jalali_start[0] - gregorian_start[0]) // 4) + (
                365 * 31 + 7)

    # Calculate the jalali year, month, and day from the number of days
    jy = 33
    while days_since_jalali_start > 0:
        if jy == 33:
            days_in_year = 366 if isleap(jy) else 365
        else:
            days_in_year = 366 if isleap(jy) else 365

        if days_since_jalali_start >= days_in_year:
            days_since_jalali_start -= days_in_year
            jy += 1
        else:
            leap = isleap(jy)
            for jm, days_in_month in enumerate([31, 31 if leap else 30, 31 if leap else 30, 31, 31, 31, 30, 30, 30, 29 if leap else 28, 29 if leap else 28, 29 if leap else 28][:]):
                if days_since_jalali_start >= days_in_month:
                    days_since_jalali_start -= days_in_month
                else:
                    break
            jd = days_since_jalali_start + 1
            break

    return f"{jy}-{jm:02}-{jd:02}"
