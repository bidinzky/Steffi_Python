def is_leap_year(year):
    return year % 4 == 0 and (not (year % 100 == 0) or year % 400 == 0)


leap_years = [2000, 2004, 2008, 2012, 2016, 2020, 2024, 2028, 2032, 2036, 2040, 2044]
non_leap_years = map(lambda y: y+1, leap_years)
print(list(map(lambda y: is_leap_year(y), leap_years)))
print(list(map(lambda y: is_leap_year(y), non_leap_years)))
