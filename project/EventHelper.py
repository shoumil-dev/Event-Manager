import re

from sqlalchemy import false


def format_date(date: str):
    """
    Formats the date to match that accepted by google calendar api.

    params:
        date (str): date of the event
    """
    if type(date) != str:
        raise TypeError('Date must be a string!')
    # yyyy-mm-dd
    if date[4] == '-' and date[7] == '-':
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
    # dd-mm-yyyy
    elif date[2] == '-' and date[5] == '-':
        day = date[0:2]
        month = date[3:5]
        year = date[6:10]
    else:
        raise Exception('Invalid date entered!')
    return year + '-' + month + '-' + day


def check_valid_email(email):
    valid_email = False

    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(email_regex, email):
        valid_email = True

    return valid_email


def convert_to_id(summary: str):
    """
    Converts the summary (name) of the event to an id.
        Converts the summary to lowercase and then applies ord().

    params:
        summary (str): summary (name) of the event
    """
    if type(summary) != str:
        raise TypeError('Date must be a string!')
    if len(summary) < 5:
        raise Exception('summary must be atleast 5 characters')
    summary = summary.lower()
    numstring = ''
    for letter in summary:
        numstring += str(ord(letter))
    return numstring


def location_address_checker(address):
    if type(address) != str:
        raise TypeError("Address must be of type string!")
    countries = ['afghanistan', 'aland islands', 'albania', 'algeria', 'american samoa', 'andorra',
                 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'argentina', 'armenia',
                 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas (the)', 'bahrain', 'bangladesh',
                 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan',
                 'bolivia (plurinational state of)',
                 'bonaire, sint eustatius and saba', 'bosnia and herzegovina', 'botswana', 'bouvet island', 'brazil',
                 'british indian ocean territory (the)', 'brunei darussalam', 'bulgaria', 'burkina faso', 'burundi',
                 'cabo verde', 'cambodia', 'cameroon', 'canada', 'cayman islands (the)',
                 'central african republic (the)',
                 'chad', 'chile', 'china', 'christmas island', 'cocos (keeling) islands (the)', 'colombia',
                 'comoros (the)',
                 'congo (the democratic republic of the)', 'congo (the)', 'cook islands (the)', 'costa rica',
                 "cote d'ivoire",
                 'croatia', 'cuba', 'curacao', 'cyprus', 'czechia', 'denmark', 'djibouti', 'dominica',
                 'dominican republic (the)',
                 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia',
                 'falkland islands (the) [malvinas]',
                 'faroe islands (the)', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia',
                 'french southern territories (the)',
                 'gabon', 'gambia (the)', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada',
                 'guadeloupe', 'guam',
                 'guatemala', 'guernsey', 'guinea', 'guinea-bissau', 'guyana', 'haiti',
                 'heard island and mcdonald islands', 'holy see (the)',
                 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran (islamic republic of)',
                 'iraq', 'ireland', 'isle of man',
                 'israel', 'italy', 'jamaica', 'japan', 'jersey', 'jordan', 'kazakhstan', 'kenya', 'kiribati',
                 "korea (the democratic people's republic of)",
                 'korea (the republic of)', 'kuwait', 'kyrgyzstan', "lao people's democratic republic (the)", 'latvia',
                 'lebanon', 'lesotho', 'liberia', 'libya',
                 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'macedonia (the former yugoslav republic of)',
                 'madagascar', 'malawi',
                 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands (the)', 'martinique', 'mauritania',
                 'mauritius', 'mayotte', 'mexico',
                 'micronesia (federated states of)', 'moldova (the republic of)', 'monaco', 'mongolia', 'montenegro',
                 'montserrat', 'morocco', 'mozambique',
                 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands (the)', 'new caledonia', 'new zealand',
                 'nicaragua', 'niger (the)', 'nigeria', 'niue',
                 'norfolk island', 'northern mariana islands (the)', 'norway', 'oman', 'pakistan', 'palau',
                 'palestine, state of', 'panama', 'papua new guinea',
                 'paraguay', 'peru', 'philippines (the)', 'pitcairn', 'poland', 'portugal', 'puerto rico', 'qatar',
                 'reunion', 'romania', 'russian federation (the)',
                 'rwanda', 'saint barthelemy', 'saint helena, ascension and tristan da cunha', 'saint kitts and nevis',
                 'saint lucia', 'saint martin (french part)',
                 'saint pierre and miquelon', 'saint vincent and the grenadines', 'samoa', 'san marino',
                 'sao tome and principe', 'saudi arabia', 'senegal',
                 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten (dutch part)', 'slovakia',
                 'slovenia', 'solomon islands', 'somalia',
                 'south africa', 'south georgia and the south sandwich islands', 'south sudan', 'spain', 'sri lanka',
                 'sudan (the)', 'suriname', 'svalbard and jan mayen',
                 'swaziland', 'sweden', 'switzerland', 'syrian arab republic', 'taiwan (province of china)',
                 'tajikistan', 'tanzania, united republic of', 'thailand',
                 'timor-leste', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan',
                 'turks and caicos islands (the)', 'tuvalu',
                 'uganda', 'ukraine', 'united arab emirates (the)',
                 'united kingdom of great britain and northern ireland (the)',
                 'united states minor outlying islands (the)',
                 'united states of america (the)', 'uruguay', 'uzbekistan', 'vanuatu',
                 'venezuela (bolivarian republic of)', 'viet nam', 'virgin islands (british)',
                 'virgin islands (u.s.)', 'wallis and futuna', 'western sahara*', 'yemen', 'zambia', 'zimbabwe']
    street_types = ['street', 'st.', 'avenue', 'ave.', 'road', 'rd.', 'boulevard', 'blvd.', 'jalan', 'jln.']

    lines = address.split('\n')
    line_count = len(lines)
    check_count = 0

    if line_count != 4:
        return False

    if lines[3].lower() in countries:
        check_count += 1

    if any(street in lines[1].lower() for street in street_types):
        check_count += 1

    valid_address = False
    if check_count == 2:
        valid_address = True

    return valid_address


class Meeting:
    """Acts as an enum for meeting type."""
    OFFICIAL = 'Official Meeting'
    ONLINE = 'Online Meeting'
    PHYSICAL = 'Physical Meeting'


def main():
    pass  # pragma: no cover


if __name__ == '__main__':  # Prevents the main() function from being called by the test suite runner
    main()  # pragma: no cover
