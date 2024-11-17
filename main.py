import os
import time
import requests
import phonenumbers
from phonenumbers import geocoder, carrier

# Initialize CITY_INFO as an empty dictionary
CITY_INFO = {}

# Expanded list of UK area codes and counties
COUNTY_MAP = {
    '020': 'Greater London',
    '0121': 'Birmingham',
    '0117': 'Bristol',
    '0131': 'Edinburgh',
    '0161': 'Manchester',
    '0141': 'Glasgow',
    '01792': 'Swansea',
    '0151': 'Liverpool',
    '0191': 'Newcastle upon Tyne',
    '0113': 'Leeds',
    '0114': 'Sheffield',
    '029': 'Cardiff',
    '0115': 'Nottingham',
    '028': 'Belfast',
    '024': 'Coventry',
    '01482': 'Hull',
    '01332': 'Derby',
    '0116': 'Leicester',
    '01603': 'Norwich',
    '0118': 'Reading',
    '01782': 'Stoke-on-Trent',
    '01904': 'York',
    '01223': 'Cambridge',
    '01865': 'Oxford',
    '01908': 'Milton Keynes',
    '01752': 'Plymouth',
    '023': 'Southampton',
    '01227': 'Canterbury',
    '01793': 'Swindon',
    '01582': 'Luton',
    '01924': 'Wakefield',
    '01642': 'Middlesbrough',
    '01253': 'Blackpool',
    '01483': 'Woking',
    '01302': 'Doncaster',
    '0191': 'Sunderland',
    '01224': 'Aberdeen',
    '01202': 'Bournemouth',
    '01522': 'Lincoln',
    '01423': 'Harrogate',
    '01702': 'Southend',
    '01463': 'Inverness',
    '01382': 'Dundee',
    '01274': 'Bradford',
    '01482': 'Kingston upon Hull',
    '01733': 'Peterborough',
    '01622': 'Maidstone',
    '01206': 'Colchester',
    '01323': 'Eastbourne',
    '01242': 'Cheltenham',
    '01256': 'Basingstoke',
    '01922': 'Walsall',
    '01924': 'Wakefield'
}


POSTCODE_MAP = {
    'EC1A': ('London', ['EC1B', 'EC1C', 'EC1M', 'EC1N', 'EC1R', 'EC1V', 'EC1Y']),
    'B1': ('Birmingham', ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9']),
    'M1': ('Manchester', ['M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']),
    'G1': ('Glasgow', ['G2', 'G3', 'G4', 'G5', 'G11', 'G12', 'G13', 'G14']),
    'LS1': ('Leeds', ['LS2', 'LS3', 'LS4', 'LS5', 'LS6', 'LS7', 'LS8', 'LS9']),
    'SS1': ('Southend', ['SS2', 'SS3', 'SS4', 'SS5', 'SS6', 'SS7']),
    'NG1': ('Nottingham', ['NG2', 'NG3', 'NG4', 'NG5', 'NG6', 'NG7', 'NG8', 'NG9']),
    'AB1': ('Aberdeen', ['AB2', 'AB3', 'AB4', 'AB5', 'AB10', 'AB11', 'AB12']),
    'BS1': ('Bristol', ['BS2', 'BS3', 'BS4', 'BS5', 'BS6', 'BS7', 'BS8']),
    'CV1': ('Coventry', ['CV2', 'CV3', 'CV4', 'CV5', 'CV6', 'CV7', 'CV8']),
    'DE1': ('Derby', ['DE2', 'DE3', 'DE4', 'DE5', 'DE6', 'DE7', 'DE8']),
    'EX1': ('Exeter', ['EX2', 'EX3', 'EX4', 'EX5', 'EX6']),
    'BT1': ('Belfast', ['BT2', 'BT3', 'BT4', 'BT5', 'BT6', 'BT7']),
    'L1': ('Liverpool', ['L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9']),
    'N1': ('London', ['N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9']),
    'PE1': ('Peterborough', ['PE2', 'PE3', 'PE4', 'PE5', 'PE6', 'PE7']),
    'TQ1': ('Torquay', ['TQ2', 'TQ3', 'TQ4', 'TQ5']),
    'YO1': ('York', ['YO2', 'YO3', 'YO4', 'YO5', 'YO6']),
    'OX1': ('Oxford', ['OX2', 'OX3', 'OX4', 'OX5', 'OX6']),
    'SE1': ('London', ['SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7']),
    'HA1': ('Harrow', ['HA2', 'HA3', 'HA4', 'HA5', 'HA6']),
    'RM1': ('Romford', ['RM2', 'RM3', 'RM4', 'RM5']),
    'KT1': ('Kingston upon Thames', ['KT2', 'KT3', 'KT4', 'KT5', 'KT6']),
    'SL1': ('Slough', ['SL2', 'SL3', 'SL4', 'SL5']),
    'WN1': ('Wigan', ['WN2', 'WN3', 'WN4', 'WN5']),
    'TN1': ('Tunbridge Wells', ['TN2', 'TN3', 'TN4', 'TN5']),
    'PR1': ('Preston', ['PR2', 'PR3', 'PR4']),
    'CT1': ('Canterbury', ['CT2', 'CT3', 'CT4']),
    'ME1': ('Rochester', ['ME2', 'ME3', 'ME4', 'ME5']),
    'S1': ('Sheffield', ['S2', 'S3', 'S4', 'S5', 'S6']),
    'BH1': ('Bournemouth', ['BH2', 'BH3', 'BH4', 'BH5']),
    'WS1': ('Walsall', ['WS2', 'WS3', 'WS4']),
    'LU1': ('Luton', ['LU2', 'LU3', 'LU4', 'LU5']),
    'RG1': ('Reading', ['RG2', 'RG3', 'RG4', 'RG5']),
    'LN1': ('Lincoln', ['LN2', 'LN3', 'LN4', 'LN5', 'LN6']),
    'NE1': ('Newcastle upon Tyne', ['NE2', 'NE3', 'NE4', 'NE5']),
    'IP1': ('Ipswich', ['IP2', 'IP3', 'IP4', 'IP5']),
    'DN1': ('Doncaster', ['DN2', 'DN3', 'DN4']),
    'SK1': ('Stockport', ['SK2', 'SK3', 'SK4']),
    'ST1': ('Stoke-on-Trent', ['ST2', 'ST3', 'ST4', 'ST5']),
    'TR1': ('Truro', ['TR2', 'TR3', 'TR4']),
    'CA1': ('Carlisle', ['CA2', 'CA3', 'CA4', 'CA5']),
    'DT1': ('Dorchester', ['DT2', 'DT3', 'DT4']),
    'LA1': ('Lancaster', ['LA2', 'LA3', 'LA4']),
    'NR1': ('Norwich', ['NR2', 'NR3', 'NR4', 'NR5']),
    'PL1': ('Plymouth', ['PL2', 'PL3', 'PL4', 'PL5']),
    'SR1': ('Sunderland', ['SR2', 'SR3', 'SR4', 'SR5']),
    'CV1': ('Coventry', ['CV2', 'CV3', 'CV4']),
    'EX1': ('Exeter', ['EX2', 'EX3', 'EX4']),
    'MK1': ('Milton Keynes', ['MK2', 'MK3', 'MK4', 'MK5']),
    'B19': ('Birmingham', ['B20', 'B21', 'B22', 'B23']),
    'M16': ('Manchester', ['M17', 'M18', 'M19', 'M20']),
    'G32': ('Glasgow', ['G33', 'G34', 'G35', 'G36']),
    'YO10': ('York', ['YO11', 'YO12', 'YO13', 'YO14']),
    'OX4': ('Oxford', ['OX5', 'OX6', 'OX7']),
    'NE10': ('Gateshead', ['NE11', 'NE12', 'NE13']),
    'W1': ('London', ['W2', 'W3', 'W4', 'W5', 'W6']),
    'EC2': ('London', ['EC3', 'EC4']),
    'E1': ('London', ['E2', 'E3', 'E4']),
    'SW1': ('London', ['SW2', 'SW3', 'SW4', 'SW5']),
    'SE10': ('London', ['SE11', 'SE12', 'SE13', 'SE14']),
    'NW1': ('London', ['NW2', 'NW3', 'NW4', 'NW5']),
    'N10': ('London', ['N11', 'N12', 'N13', 'N14']),
    'B43': ('Birmingham', ['B44', 'B45', 'B46', 'B47']),
    'ME1': ('Rochester', ['ME2', 'ME3']),
    'SW6': ('London', ['SW7', 'SW8']),
    'HD1': ('Huddersfield', ['HD2', 'HD3', 'HD4']),
    'DL1': ('Darlington', ['DL2', 'DL3', 'DL4']),
    'BH15': ('Poole', ['BH16', 'BH17']),
    'BD1': ('Bradford', ['BD2', 'BD3', 'BD4', 'BD5', 'BD6']),
    'TS1': ('Middlesbrough', ['TS2', 'TS3', 'TS4', 'TS5']),
    'IP1': ('Ipswich', ['IP2', 'IP3', 'IP4', 'IP5']),
    'SA1': ('Swansea', ['SA2', 'SA3', 'SA4', 'SA5']),
    'B70': ('West Bromwich', ['B71', 'B72', 'B73', 'B74']),
    'DE1': ('Derby', ['DE2', 'DE3', 'DE4', 'DE5']),
    'PO1': ('Portsmouth', ['PO2', 'PO3', 'PO4', 'PO5']),
    'LU1': ('Luton', ['LU2', 'LU3', 'LU4', 'LU5']),
    'NR1': ('Norwich', ['NR2', 'NR3', 'NR4', 'NR5']),
    'PR1': ('Preston', ['PR2', 'PR3', 'PR4']),
    'DA1': ('Dartford', ['DA2', 'DA3', 'DA4']),
    'RG1': ('Reading', ['RG2', 'RG3', 'RG4']),
    'MK1': ('Milton Keynes', ['MK2', 'MK3', 'MK4']),
    'W4': ('Chiswick', ['W5', 'W6', 'W7']),
    'L1': ('Liverpool', ['L2', 'L3', 'L4']),
    'NE1': ('Newcastle', ['NE2', 'NE3', 'NE4'])
}

# Function to print the banner and other text in red color
def print_banner():
    red = "\033[91m"
    reset = "\033[0m"  # Reset to default color
    
    banner = '''
██╗   ██╗██╗  ██╗     █████╗ ██████╗ ███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗
██║   ██║██║ ██╔╝    ██╔══██╗██╔══██╗████╗ ████║██╔═══██╗██╔══██╗╚██╗ ██╔╝
██║   ██║█████╔╝     ███████║██████╔╝██╔████╔██║██║   ██║██████╔╝ ╚████╔╝ 
██║   ██║██╔═██╗     ██╔══██║██╔══██╗██║╚██╔╝██║██║   ██║██╔══██╗  ╚██╔╝  
╚██████╔╝██║  ██╗    ██║  ██║██║  ██║██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║   
 ╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
   

- Made By Rulzarian'''
    print(f"{red}{banner}{reset}")
    print(f"{red}UK Armory Tool!{reset}")
    print(f"{red}[1] Research Any UK Phone Number (e.g. +44 PhoneNumberHere){reset}")
    print(f"{red}[2] Search Postcode Information{reset}")

# Function to search postcode and show related city & postcodes
def search_postcode():
    postcode = input("\nEnter a UK postcode (e.g. EC1A or CL2): ").upper()

    matches = [(code, info) for code, info in POSTCODE_MAP.items() if code.startswith(postcode[:2])]

    if matches:
        for match in matches:
            code, (city, related_postcodes) = match
            print(f"\nPostcode: {code}")
            print(f"City: {city}")
            print(f"Related Postcodes: {', '.join(related_postcodes)}")
    else:
        print("\nNo postcodes found matching the first two letters.")

# Function to check phone number validity and extract details
def research_phone_number():
    phone_number = input("\nEnter A UK Phone Number (e.g. +44 PhoneNumberHere): ")

    try:
        parsed_number = phonenumbers.parse(phone_number, "GB")
        if not phonenumbers.is_valid_number(parsed_number):
            print("Invalid phone number. Please try again.")
            return
        
        location = geocoder.description_for_number(parsed_number, "en")
        carrier_name = carrier.name_for_number(parsed_number, "en")

        area_code = str(parsed_number.national_number)[:4]
        county = COUNTY_MAP.get(area_code, 'Unknown County')

        print("\nResearch Results:")
        print(f"Phone Number: {phone_number}")
        print(f"Location: {location}")
        print(f"County: {county}")
        print(f"Carrier: {carrier_name}")
        
        print("\nChecking if the number is flagged as a scammer...")
        check_for_scammer(phone_number)

    except phonenumbers.phonenumberutil.NumberParseException:
        print("There was an error parsing the number. Please try again with a valid number.")

def check_for_scammer(phone_number):
    scam_numbers = ["+44 7467056154", "+44 01419971669"]
    
    if phone_number in scam_numbers:
        print(f"Warning: The number {phone_number} has been flagged as a potential scammer!")
    else:
        print(f"The number {phone_number} appears to be safe.")

# Main menu loop
def main_menu():
    while True:
        print_banner()
        choice = input("\nSelect an option: ")

        if choice == "1":
            research_phone_number()
        elif choice == "2":
            search_postcode()
        else:
            print("Invalid choice. Please select again.")
        
        cont = input("\nDo you want to search another number or postcode? (y/n): ").lower()
        if cont != 'y':
            print("Exiting the program. Goodbye!")
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')

# Run the program
if __name__ == "__main__":
    main_menu()


