import Schaltjahr


def days_in_year(year, month_name, day):
    month_names = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    days_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    num_days_in_year = 365
    month = month_names.index(month_name)
    if Schaltjahr.is_leap_year(year):
        days_month[1] += 1
        num_days_in_year += 1

    if days_month[month] < day:
        return None

    days = 0
    for i in range(month):
        days += days_month[i]
    return days + day


print(days_in_year(2005, "Jan", 1))
print(days_in_year(2004, "Feb", 29))
print(days_in_year(2005, "Feb", 29))
print(days_in_year(2003, "Sep", 31))
