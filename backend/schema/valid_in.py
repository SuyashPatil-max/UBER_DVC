from pydantic import BaseModel, Field ,field_validator,computed_field,model_validator
from typing import List,Dict ,Annotated,Literal 
from enum import Enum
from datetime import date , time ,datetime
from backend.preprocessing import time_of_day ,get_season

class payment_enum(str ,Enum) : 
    UPI ='upi'
    CASH = 'cash'
    DEBIT_CARD = 'debit_card' 
    UBER_WALLET = 'uber_wallet'
    CREDIT_CARD = 'credit_card'


class Location(str, Enum):
    SHASTRI_NAGAR = "Shastri Nagar"
    KHANDSA = "Khandsa"
    CENTRAL_SECRETARIAT = "Central Secretariat"
    GHITORNI_VILLAGE = "Ghitorni Village"
    AIIMS = "AIIMS"
    VAISHALI = "Vaishali"
    MAYUR_VIHAR = "Mayur Vihar"
    ROHINI = "Rohini"
    UDYOG_BHAWAN = "Udyog Bhawan"
    MALVIYA_NAGAR = "Malviya Nagar"
    MADIPUR = "Madipur"
    JAMA_MASJID = "Jama Masjid"
    IGI_AIRPORT = "IGI Airport"
    PUNJABI_BAGH = "Punjabi Bagh"
    GREATER_NOIDA = "Greater Noida"
    TIS_HAZARI = "Tis Hazari"
    NOIDA_SECTOR_18 = "Noida Sector 18"
    KANHAIYA_NAGAR = "Kanhaiya Nagar"
    OKHLA = "Okhla"
    SHASTRI_PARK = "Shastri Park"
    FARIDABAD_SECTOR_15 = "Faridabad Sector 15"
    MUNDKA = "Mundka"
    DLF_CITY_COURT = "DLF City Court"
    NIRMAN_VIHAR = "Nirman Vihar"
    NEW_DELHI_RAILWAY_STATION = "New Delhi Railway Station"
    CIVIL_LINES_GURGAON = "Civil Lines Gurgaon"
    SEELAMPUR = "Seelampur"
    VINOBAPURI = "Vinobapuri"
    PANIPAT = "Panipat"
    SULTANPUR = "Sultanpur"
    DILSHAD_GARDEN = "Dilshad Garden"
    AYA_NAGAR = "Aya Nagar"
    RAJIV_CHOWK = "Rajiv Chowk"
    MG_ROAD = "MG Road"
    JASOLA = "Jasola"
    KASHMERE_GATE = "Kashmere Gate"
    TUGHLAKABAD = "Tughlakabad"
    CYBER_HUB = "Cyber Hub"
    VIDHAN_SABHA = "Vidhan Sabha"
    ANAND_VIHAR = "Anand Vihar"
    UTTAM_NAGAR = "Uttam Nagar"
    MODEL_TOWN = "Model Town"
    GHITORNI = "Ghitorni"
    RAJIV_NAGAR = "Rajiv Nagar"
    SOHNA_ROAD = "Sohna Road"
    LAJPAT_NAGAR = "Lajpat Nagar"
    MOOLCHAND = "Moolchand"
    INA_MARKET = "INA Market"
    IIT_DELHI = "IIT Delhi"
    SATGURU_RAM_SINGH_MARG = "Satguru Ram Singh Marg"
    MUNIRKA = "Munirka"
    NEW_COLONY = "New Colony"
    IGNOU_ROAD = "IGNOU Road"
    MEERUT = "Meerut"
    AKSHARDHAM = "Akshardham"
    IMT_MANESAR = "IMT Manesar"
    AZADPUR = "Azadpur"
    SIKANDERPUR = "Sikanderpur"
    ROHINI_WEST = "Rohini West"
    MANDI_HOUSE = "Mandi House"
    KASHMERE_GATE_ISBT = "Kashmere Gate ISBT"
    KHERKI_DAULA_TOLL = "Kherki Daula Toll"
    MAIDAN_GARHI = "Maidan Garhi"
    YAMUNA_BANK = "Yamuna Bank"
    KHAN_MARKET = "Khan Market"
    PRAGATI_MAIDAN = "Pragati Maidan"
    MANSAROVAR_PARK = "Mansarovar Park"
    RITHALA = "Rithala"
    SAIDULAJAB = "Saidulajab"
    SHAHDARA = "Shahdara"
    TILAK_NAGAR = "Tilak Nagar"
    DLF_PHASE_3 = "DLF Phase 3"
    LAXMI_NAGAR = "Laxmi Nagar"
    HUDA_CITY_CENTRE = "Huda City Centre"
    MEHRAULI = "Mehrauli"
    BOTANICAL_GARDEN = "Botanical Garden"
    KAROL_BAGH = "Karol Bagh"
    RAMESH_NAGAR = "Ramesh Nagar"
    INDIA_GATE = "India Gate"
    BARAKHAMBA_ROAD = "Barakhamba Road"
    GURGAON_SECTOR_56 = "Gurgaon Sector 56"
    ASHRAM = "Ashram"
    GURGAON_SECTOR_29 = "Gurgaon Sector 29"
    BASAI_DHANKOT = "Basai Dhankot"
    QUTUB_MINAR = "Qutub Minar"
    UDYOG_VIHAR_PHASE_4 = "Udyog Vihar Phase 4"
    RAJ_NAGAR_EXTENSION = "Raj Nagar Extension"
    NAWADA = "Nawada"
    LOK_KALYAN_MARG = "Lok Kalyan Marg"
    GREATER_KAILASH = "Greater Kailash"
    SAROJINI_NAGAR = "Sarojini Nagar"
    PALAM_VIHAR = "Palam Vihar"
    GTB_NAGAR = "GTB Nagar"
    ADARSH_NAGAR = "Adarsh Nagar"
    GOLF_COURSE_ROAD = "Golf Course Road"
    GHAZIABAD = "Ghaziabad"
    NARSINGHPUR = "Narsinghpur"
    PANCHSHEEL_PARK = "Panchsheel Park"
    BADARPUR = "Badarpur"
    DWARKA_SECTOR_21 = "Dwarka Sector 21"
    GWAL_PAHARI = "Gwal Pahari"
    TAGORE_GARDEN = "Tagore Garden"
    SAMAYPUR_BADLI = "Samaypur Badli"
    HERO_HONDA_CHOWK = "Hero Honda Chowk"
    DELHI_GATE = "Delhi Gate"
    JOR_BAGH = "Jor Bagh"
    SHIVAJI_PARK = "Shivaji Park"
    KESHAV_PURAM = "Keshav Puram"
    JHILMIL = "Jhilmil"
    ITO = "ITO"
    INDRAPRASTHA = "Indraprastha"
    JANAKPURI = "Janakpuri"
    PITAMPURA = "Pitampura"
    JAHANGIRPURI = "Jahangirpuri"
    VATIKA_CHOWK = "Vatika Chowk"
    GOVINDPURI = "Govindpuri"
    WELCOME = "Welcome"
    PREET_VIHAR = "Preet Vihar"
    NOIDA_EXTENSION = "Noida Extension"
    INDIRAPURAM = "Indirapuram"
    SAKET = "Saket"
    SADAR_BAZAR_GURGAON = "Sadar Bazar Gurgaon"
    NOIDA_SECTOR_62 = "Noida Sector 62"
    KADARPUR = "Kadarpur"
    KALKAJI = "Kalkaji"
    ANAND_VIHAR_ISBT = "Anand Vihar ISBT"
    CHHATARPUR = "Chhatarpur"
    ARJANGARH = "Arjangarh"
    CHIRAG_DELHI = "Chirag Delhi"
    SOUTH_EXTENSION = "South Extension"
    NETAJI_SUBHASH_PLACE = "Netaji Subhash Place"
    GREEN_PARK = "Green Park"
    PATAUDI_CHOWK = "Pataudi Chowk"
    BADSHAHPUR = "Badshahpur"
    MANESAR = "Manesar"
    ASHOK_VIHAR = "Ashok Vihar"
    NEHRU_PLACE = "Nehru Place"
    SAKET_A_BLOCK = "Saket A Block"
    NOIDA_FILM_CITY = "Noida Film City"
    CHANDNI_CHOWK = "Chandni Chowk"
    GURGAON_RAILWAY_STATION = "Gurgaon Railway Station"
    INDERLOK = "Inderlok"
    RAJOURI_GARDEN = "Rajouri Garden"
    BHIWADI = "Bhiwadi"
    IFFCO_CHOWK = "IFFCO Chowk"
    ASHOK_PARK_MAIN = "Ashok Park Main"
    SUBHASH_CHOWK = "Subhash Chowk"
    ROHINI_EAST = "Rohini East"
    KARKARDUMA = "Karkarduma"
    PEERAGARHI = "Peeragarhi"
    VASANT_KUNJ = "Vasant Kunj"
    PULBANGASH = "Pulbangash"
    MOTI_NAGAR = "Moti Nagar"
    CHANAKYAPURI = "Chanakyapuri"
    KAUSHAMBI = "Kaushambi"
    SONIPAT = "Sonipat"
    CONNAUGHT_PLACE = "Connaught Place"
    SUSHANT_LOK = "Sushant Lok"
    BHIKAIJI_CAMA_PLACE = "Bhikaji Cama Place"
    BAHADURGARH = "Bahadurgarh"
    KIRTI_NAGAR = "Kirti Nagar"
    RK_PURAM = "RK Puram"
    SUBHASH_NAGAR = "Subhash Nagar"
    PATEL_CHOWK = "Patel Chowk"
    DWARKA_MOR = "Dwarka Mor"
    HAUZ_RANI = "Hauz Rani"
    UDYOG_VIHAR = "Udyog Vihar"
    ARDEE_CITY = "Ardee City"
    OLD_GURGAON = "Old Gurgaon"
    HAUZ_KHAS = "Hauz Khas"
    PAHARGANJ = "Paharganj"
    PASCHIM_VIHAR = "Paschim Vihar"
    AMBIENCE_MALL = "Ambience Mall"
    VISHWAVIDYALAYA = "Vishwavidyalaya"
    LAL_QILA = "Lal Quila"
    SARAI_KALE_KHAN = "Sarai Kale Khan"


class vehicle(str ,Enum) : 
    GO_SEDAN = "Go Sedan"
    AUTO = "Auto"
    PREMIER_SEDAN = "Premier Sedan"
    BIKE = "Bike"
    GO_MINI = "Go Mini"
    UBER_XL = "Uber XL"
    EBIKE = "eBike"


class Ride_IN(BaseModel) : 

    payment_method : Annotated[payment_enum, Field(... ,description = "Payment method", example ="upi")]
    vtat : Annotated[float , Field(... , description = "Vtat in the uber", example = 4.9 ,gt = 0)]
    ctat : Annotated[float , Field(... , description = "ctat in the uber", example = 14.0 ,gt = 0 )]
    Booking_value : Annotated[float , Field(... , description = "Booking value of the customer",example =237.0 ,gt = 0 )]
    Ride_Distance : Annotated[float , Field(... , description = "Ride distance of the ride ", example = 5.73 , gt = 0 )]

    pickup_location : Annotated[Location ,Field(... , description = "Pickup location of the user" ,example = 'Shastri Nagar')]
    drop_location : Annotated[Location ,Field(... , description = "Pickup location of the user" ,example = 'Gurgaon Sector 56')]

    date : Annotated[date , Field(... , description = "date of the ride", example = '2024-11-29')]
    time : Annotated[time , Field(... , description = "Time of the ride" ,example = "18:01:39")]

    vehicle_type : Annotated[vehicle, Field(... , description = "Vehicle type of ride" ,example = "Go Sedan")]


    @computed_field
    @property
    def Month(self) -> int:
        return self.date.month

    @computed_field
    @property
    def Day(self) -> int:
        return self.date.day

    @computed_field
    @property
    def DayOfWeek(self) -> str:
        return self.date.strftime("%A")

    @computed_field
    @property
    def Quarter(self) -> int:
        return (self.date.month - 1) // 3 + 1

    @computed_field
    @property
    def IsWeekend(self) -> int:
        return int(self.date.weekday() >= 5)

    @computed_field
    @property
    def Hour(self) -> int:
        return self.time.hour

    @computed_field
    @property
    def TimeOfDay(self) -> str:
        return time_of_day(self.time.hour)

    @computed_field
    @property
    def Season(self) -> str:
        return get_season(self.date.month)


    @model_validator(mode = "after")
    def validation_location(self) : 
        if self.pickup_location == self.drop_location : 
            raise ValueError("Pick and drop location cannot be same")

        return self 



    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value):

        try:
            return datetime.strptime(value, "%Y-%m-%d").date()

        except (ValueError, TypeError):
            raise ValueError(
                "Invalid date format. Expected format: YYYY-MM-DD "
                "(example: 2024-11-29)"
            )


    @field_validator("time", mode="before")
    @classmethod
    def validate_time(cls, value):

        try:
            return datetime.strptime(value, "%H:%M:%S").time()

        except (ValueError, TypeError):
            raise ValueError(
                "Invalid time format. Expected format: HH:MM:SS "
                "(example: 18:01:39)"
            )







