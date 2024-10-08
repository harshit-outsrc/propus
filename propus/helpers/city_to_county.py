from propus.helpers.constants import ALAMEDA
from propus.helpers.constants import ALPINE
from propus.helpers.constants import AMADOR
from propus.helpers.constants import BUTTE
from propus.helpers.constants import CALAVERAS
from propus.helpers.constants import COLUSA
from propus.helpers.constants import CONTRA_COSTA
from propus.helpers.constants import DEL_NORTE
from propus.helpers.constants import EL_DORADO
from propus.helpers.constants import FRESNO
from propus.helpers.constants import GLENN
from propus.helpers.constants import HUMBOLDT
from propus.helpers.constants import IMPERIAL
from propus.helpers.constants import INYO
from propus.helpers.constants import KERN
from propus.helpers.constants import KINGS
from propus.helpers.constants import LAKE
from propus.helpers.constants import LASSEN
from propus.helpers.constants import LOS_ANGELES
from propus.helpers.constants import MADERA
from propus.helpers.constants import MARIN
from propus.helpers.constants import MARIPOSA
from propus.helpers.constants import MENDOCINO
from propus.helpers.constants import MERCED
from propus.helpers.constants import MODOC
from propus.helpers.constants import MONO
from propus.helpers.constants import MONTEREY
from propus.helpers.constants import NAPA
from propus.helpers.constants import NEVADA
from propus.helpers.constants import ORANGE
from propus.helpers.constants import PLACER
from propus.helpers.constants import PLUMAS
from propus.helpers.constants import RIVERSIDE
from propus.helpers.constants import SACRAMENTO
from propus.helpers.constants import SANTA_BARBARA
from propus.helpers.constants import SANTA_CLARA
from propus.helpers.constants import SANTA_CRUZ
from propus.helpers.constants import SAN_BENITO
from propus.helpers.constants import SAN_BERNADINO
from propus.helpers.constants import SAN_DIEGO
from propus.helpers.constants import SAN_FRANCISCO
from propus.helpers.constants import SAN_JOAQUIN
from propus.helpers.constants import SAN_LUIS_OBISPO
from propus.helpers.constants import SAN_MATEO
from propus.helpers.constants import SHASTA
from propus.helpers.constants import SIERRA
from propus.helpers.constants import SISKIYOU
from propus.helpers.constants import SOLANO
from propus.helpers.constants import SONOMA
from propus.helpers.constants import STANISLAUS
from propus.helpers.constants import SUTTER
from propus.helpers.constants import TEHAMA
from propus.helpers.constants import TRINITY
from propus.helpers.constants import TULARE
from propus.helpers.constants import TUOLUMNE
from propus.helpers.constants import VENTURA
from propus.helpers.constants import YOLO
from propus.helpers.constants import YUBA


city_to_county_map = {
    "acampo": SAN_JOAQUIN,
    "acton": LOS_ANGELES,
    "adelanto": SAN_BERNADINO,
    "adin": MODOC,
    "agourahills": LOS_ANGELES,
    "aguanga": RIVERSIDE,
    "ahwahnee": MADERA,
    "alameda": ALAMEDA,
    "alamo": CONTRA_COSTA,
    "albany": ALAMEDA,
    "albion": MENDOCINO,
    "alderpoint": HUMBOLDT,
    "alhambra": LOS_ANGELES,
    "alisoviejo": ORANGE,
    "alleghany": SIERRA,
    "alpaugh": TULARE,
    "alpine": SAN_DIEGO,
    "alta": PLACER,
    "altadena": LOS_ANGELES,
    "alturas": MODOC,
    "alviso": SANTA_CLARA,
    "amadorcity": AMADOR,
    "amboy": SAN_BERNADINO,
    "americancanyon": NAPA,
    "anaheim": ORANGE,
    "anderson": SHASTA,
    "angelscamp": CALAVERAS,
    "angelusoaks": SAN_BERNADINO,
    "angwin": NAPA,
    "annapolis": SONOMA,
    "antelope": SACRAMENTO,
    "antioch": CONTRA_COSTA,
    "anza": RIVERSIDE,
    "applegate": PLACER,
    "applevalley": SAN_BERNADINO,
    "aptos": SANTA_CRUZ,
    "arbuckle": COLUSA,
    "arcadia": LOS_ANGELES,
    "arcata": HUMBOLDT,
    "armona": KINGS,
    "arnold": CALAVERAS,
    "aromas": MONTEREY,
    "arroyogrande": SAN_LUIS_OBISPO,
    "artesia": LOS_ANGELES,
    "arvin": KERN,
    "atascadero": SAN_LUIS_OBISPO,
    "atherton": SAN_MATEO,
    "atwater": MERCED,
    "auberry": FRESNO,
    "auburn": PLACER,
    "avalon": LOS_ANGELES,
    "avenal": KINGS,
    "avery": CALAVERAS,
    "avilabeach": SAN_LUIS_OBISPO,
    "azusa": LOS_ANGELES,
    "badger": TULARE,
    "baker": SAN_BERNADINO,
    "bakersfield": KERN,
    "baldwinpark": LOS_ANGELES,
    "ballico": MERCED,
    "bangor": BUTTE,
    "banning": RIVERSIDE,
    "bard": IMPERIAL,
    "barstow": SAN_BERNADINO,
    "basslake": MADERA,
    "bayside": HUMBOLDT,
    "bealeafb": YUBA,
    "beaumont": RIVERSIDE,
    "beckwourth": PLUMAS,
    "belden": PLUMAS,
    "bellavista": SHASTA,
    "bellflower": LOS_ANGELES,
    "bellgardens": LOS_ANGELES,
    "belmont": SAN_MATEO,
    "belvederetiburon": MARIN,
    "benicia": SOLANO,
    "benlomond": SANTA_CRUZ,
    "benton": MONO,
    "berkeley": ALAMEDA,
    "berrycreek": BUTTE,
    "bethelisland": CONTRA_COSTA,
    "beverlyhills": LOS_ANGELES,
    "bieber": LASSEN,
    "bigbar": TRINITY,
    "bigbearcity": SAN_BERNADINO,
    "bigbearlake": SAN_BERNADINO,
    "bigbend": SHASTA,
    "bigcreek": FRESNO,
    "biggs": BUTTE,
    "bigoakflat": TUOLUMNE,
    "bigpine": INYO,
    "bigsur": MONTEREY,
    "biola": FRESNO,
    "birdslanding": SOLANO,
    "bishop": INYO,
    "blairsdengraeagle": PLUMAS,
    "blocksburg": HUMBOLDT,
    "bloomington": SAN_BERNADINO,
    "bluelake": HUMBOLDT,
    "blythe": RIVERSIDE,
    "bodega": SONOMA,
    "bodegabay": SONOMA,
    "bodfish": KERN,
    "bolinas": MARIN,
    "bonita": SAN_DIEGO,
    "bonsall": SAN_DIEGO,
    "boonville": MENDOCINO,
    "boron": KERN,
    "borregosprings": SAN_DIEGO,
    "bouldercreek": SANTA_CRUZ,
    "boulevard": SAN_DIEGO,
    "bradley": MONTEREY,
    "brandeis": VENTURA,
    "branscomb": MENDOCINO,
    "brawley": IMPERIAL,
    "brea": ORANGE,
    "brentwood": CONTRA_COSTA,
    "bridgeport": MONO,
    "bridgeville": HUMBOLDT,
    "brisbane": SAN_MATEO,
    "brookdale": SANTA_CRUZ,
    "brooks": YOLO,
    "brownsvalley": YUBA,
    "brownsville": YUBA,
    "buellton": SANTA_BARBARA,
    "buenapark": ORANGE,
    "burbank": LOS_ANGELES,
    "burlingame": SAN_MATEO,
    "burney": SHASTA,
    "burntranch": TRINITY,
    "burson": CALAVERAS,
    "buttecity": GLENN,
    "buttonwillow": KERN,
    "byron": CONTRA_COSTA,
    "cabazon": RIVERSIDE,
    "calabasas": LOS_ANGELES,
    "calexico": IMPERIAL,
    "caliente": KERN,
    "californiacity": KERN,
    "californiahotsprings": TULARE,
    "calimesa": RIVERSIDE,
    "calipatria": IMPERIAL,
    "calistoga": NAPA,
    "callahan": SISKIYOU,
    "calpine": SIERRA,
    "camarillo": VENTURA,
    "cambria": SAN_LUIS_OBISPO,
    "camino": EL_DORADO,
    "campbell": SANTA_CLARA,
    "campnelson": TULARE,
    "campo": SAN_DIEGO,
    "camposeco": CALAVERAS,
    "camppendleton": SAN_DIEGO,
    "camptonville": YUBA,
    "canby": MODOC,
    "canogapark": LOS_ANGELES,
    "cantil": KERN,
    "cantuacreek": FRESNO,
    "canyon": CONTRA_COSTA,
    "canyoncountry": LOS_ANGELES,
    "canyondam": PLUMAS,
    "capay": YOLO,
    "capistranobeach": ORANGE,
    "capitola": SANTA_CRUZ,
    "cardiffbythesea": SAN_DIEGO,
    "carlotta": HUMBOLDT,
    "carlsbad": SAN_DIEGO,
    "carmel": MONTEREY,
    "carmelbythesea": MONTEREY,
    "carmelvalley": MONTEREY,
    "carmichael": SACRAMENTO,
    "carnelianbay": PLACER,
    "carpinteria": SANTA_BARBARA,
    "carson": LOS_ANGELES,
    "caruthers": FRESNO,
    "casmalia": SANTA_BARBARA,
    "caspar": MENDOCINO,
    "cassel": SHASTA,
    "castaic": LOS_ANGELES,
    "castella": SHASTA,
    "castrovalley": ALAMEDA,
    "castroville": MONTEREY,
    "cathedralcity": RIVERSIDE,
    "catheysvalley": MARIPOSA,
    "cayucos": SAN_LUIS_OBISPO,
    "cazadero": SONOMA,
    "cedarglen": SAN_BERNADINO,
    "cedarpinespark": SAN_BERNADINO,
    "cedarville": MODOC,
    "ceres": STANISLAUS,
    "cerritos": LOS_ANGELES,
    "challenge": YUBA,
    "chatsworth": LOS_ANGELES,
    "chester": PLUMAS,
    "chicagopark": NEVADA,
    "chico": BUTTE,
    "chilcoot": PLUMAS,
    "chino": SAN_BERNADINO,
    "chinohills": SAN_BERNADINO,
    "chowchilla": MADERA,
    "chualar": MONTEREY,
    "chulavista": SAN_DIEGO,
    "citrusheights": SACRAMENTO,
    "claremont": LOS_ANGELES,
    "clarksburg": YOLO,
    "clayton": CONTRA_COSTA,
    "clearlake": LAKE,
    "clearlakeoaks": LAKE,
    "clements": SAN_JOAQUIN,
    "clio": PLUMAS,
    "clippermills": BUTTE,
    "cloverdale": SONOMA,
    "clovis": FRESNO,
    "coachella": RIVERSIDE,
    "coalinga": FRESNO,
    "coarsegold": MADERA,
    "cobb": LAKE,
    "coleville": MONO,
    "colfax": PLACER,
    "colton": SAN_BERNADINO,
    "columbia": TUOLUMNE,
    "colusa": COLUSA,
    "comptche": MENDOCINO,
    "compton": LOS_ANGELES,
    "concord": CONTRA_COSTA,
    "cool": EL_DORADO,
    "copperopolis": CALAVERAS,
    "corcoran": KINGS,
    "corning": TEHAMA,
    "corona": RIVERSIDE,
    "coronadelmar": ORANGE,
    "coronado": SAN_DIEGO,
    "cortemadera": MARIN,
    "costamesa": ORANGE,
    "cotati": SONOMA,
    "cottonwood": TEHAMA,
    "coulterville": MARIPOSA,
    "courtland": SACRAMENTO,
    "covelo": MENDOCINO,
    "covina": LOS_ANGELES,
    "coyote": SANTA_CLARA,
    "crescentcity": DEL_NORTE,
    "crescentmills": PLUMAS,
    "cressey": MERCED,
    "crestline": SAN_BERNADINO,
    "creston": SAN_LUIS_OBISPO,
    "crockett": CONTRA_COSTA,
    "crowslanding": STANISLAUS,
    "culvercity": LOS_ANGELES,
    "cupertino": SANTA_CLARA,
    "cutler": TULARE,
    "cypress": ORANGE,
    "daggett": SAN_BERNADINO,
    "dalycity": SAN_MATEO,
    "danapoint": ORANGE,
    "danville": CONTRA_COSTA,
    "darwin": INYO,
    "davenport": SANTA_CRUZ,
    "davis": YOLO,
    "daviscreek": MODOC,
    "deathvalley": INYO,
    "deerpark": NAPA,
    "delano": KERN,
    "delhi": MERCED,
    "delmar": SAN_DIEGO,
    "delrey": FRESNO,
    "denair": STANISLAUS,
    "descanso": SAN_DIEGO,
    "desertcenter": RIVERSIDE,
    "deserthotsprings": RIVERSIDE,
    "diablo": CONTRA_COSTA,
    "diamondbar": LOS_ANGELES,
    "diamondsprings": EL_DORADO,
    "dillonbeach": MARIN,
    "dinuba": TULARE,
    "discoverybay": CONTRA_COSTA,
    "dixon": SOLANO,
    "dobbins": YUBA,
    "dodgertown": LOS_ANGELES,
    "dorris": SISKIYOU,
    "dospalos": MERCED,
    "dosrios": MENDOCINO,
    "douglascity": TRINITY,
    "downey": LOS_ANGELES,
    "downieville": SIERRA,
    "doyle": LASSEN,
    "drytown": AMADOR,
    "duarte": LOS_ANGELES,
    "dublin": ALAMEDA,
    "ducor": TULARE,
    "dulzura": SAN_DIEGO,
    "duncansmills": SONOMA,
    "dunlap": FRESNO,
    "dunnigan": YOLO,
    "dunsmuir": SISKIYOU,
    "durham": BUTTE,
    "dutchflat": PLACER,
    "eagleville": MODOC,
    "earlimart": TULARE,
    "earp": SAN_BERNADINO,
    "echolake": EL_DORADO,
    "edison": KERN,
    "edwards": KERN,
    "elcajon": SAN_DIEGO,
    "elcentro": IMPERIAL,
    "elcerrito": CONTRA_COSTA,
    "eldorado": EL_DORADO,
    "eldoradohills": EL_DORADO,
    "eldridge": SONOMA,
    "elk": MENDOCINO,
    "elkcreek": GLENN,
    "elkgrove": SACRAMENTO,
    "elmira": SOLANO,
    "elmonte": LOS_ANGELES,
    "elnido": MERCED,
    "elportal": MARIPOSA,
    "elsegundo": LOS_ANGELES,
    "elsobrante": CONTRA_COSTA,
    "elverta": SACRAMENTO,
    "emeryville": ALAMEDA,
    "emigrantgap": PLACER,
    "empire": STANISLAUS,
    "encinitas": SAN_DIEGO,
    "encino": LOS_ANGELES,
    "escalon": SAN_JOAQUIN,
    "escondido": SAN_DIEGO,
    "esparto": YOLO,
    "essex": SAN_BERNADINO,
    "etna": SISKIYOU,
    "eureka": HUMBOLDT,
    "exeter": TULARE,
    "fairfax": MARIN,
    "fairfield": SOLANO,
    "fairoaks": SACRAMENTO,
    "fallbrook": SAN_DIEGO,
    "fallrivermills": SHASTA,
    "farmersville": TULARE,
    "farmington": SAN_JOAQUIN,
    "fawnskin": SAN_BERNADINO,
    "fellows": KERN,
    "felton": SANTA_CRUZ,
    "ferndale": HUMBOLDT,
    "fiddletown": AMADOR,
    "fieldslanding": HUMBOLDT,
    "fillmore": VENTURA,
    "finley": LAKE,
    "firebaugh": FRESNO,
    "fishcamp": MARIPOSA,
    "fivepoints": FRESNO,
    "floriston": SIERRA,
    "flournoy": TEHAMA,
    "folsom": SACRAMENTO,
    "fontana": SAN_BERNADINO,
    "foothillranch": ORANGE,
    "forbestown": BUTTE,
    "forestfalls": SAN_BERNADINO,
    "foresthill": PLACER,
    "forestknolls": MARIN,
    "forestranch": BUTTE,
    "forestville": SONOMA,
    "forksofsalmon": SISKIYOU,
    "fortbidwell": MODOC,
    "fortbragg": MENDOCINO,
    "fortirwin": SAN_BERNADINO,
    "fortjones": SISKIYOU,
    "fortuna": HUMBOLDT,
    "fountainvalley": ORANGE,
    "fowler": FRESNO,
    "frazierpark": KERN,
    "freedom": SANTA_CRUZ,
    "fremont": ALAMEDA,
    "frenchcamp": SAN_JOAQUIN,
    "frenchgulch": SHASTA,
    "fresno": FRESNO,
    "friant": FRESNO,
    "fullerton": ORANGE,
    "fulton": SONOMA,
    "galt": SACRAMENTO,
    "garberville": HUMBOLDT,
    "gardena": LOS_ANGELES,
    "gardengrove": ORANGE,
    "gardenvalley": EL_DORADO,
    "gasquet": DEL_NORTE,
    "gazelle": SISKIYOU,
    "georgetown": EL_DORADO,
    "gerber": TEHAMA,
    "geyserville": SONOMA,
    "gilroy": SANTA_CLARA,
    "glencoe": CALAVERAS,
    "glendale": LOS_ANGELES,
    "glendora": LOS_ANGELES,
    "glenellen": SONOMA,
    "glenhaven": LAKE,
    "glenn": GLENN,
    "glennville": KERN,
    "goldrun": PLACER,
    "goleta": SANTA_BARBARA,
    "gonzales": MONTEREY,
    "goodyearsbar": SIERRA,
    "granadahills": LOS_ANGELES,
    "grandterrace": SAN_BERNADINO,
    "granitebay": PLACER,
    "grassvalley": NEVADA,
    "graton": SONOMA,
    "greenbrae": MARIN,
    "greenfield": MONTEREY,
    "greenvalleylake": SAN_BERNADINO,
    "greenview": SISKIYOU,
    "greenville": PLUMAS,
    "greenwood": EL_DORADO,
    "grenada": SISKIYOU,
    "gridley": BUTTE,
    "grimes": COLUSA,
    "grizzlyflats": EL_DORADO,
    "groveland": TUOLUMNE,
    "groverbeach": SAN_LUIS_OBISPO,
    "guadalupe": SANTA_BARBARA,
    "gualala": MENDOCINO,
    "guatay": SAN_DIEGO,
    "guerneville": SONOMA,
    "guinda": YOLO,
    "gustine": MERCED,
    "haciendaheights": LOS_ANGELES,
    "halfmoonbay": SAN_MATEO,
    "hamiltoncity": GLENN,
    "hanford": KINGS,
    "happycamp": SISKIYOU,
    "harborcity": LOS_ANGELES,
    "hatcreek": SHASTA,
    "hathawaypines": CALAVERAS,
    "hawaiiangardens": LOS_ANGELES,
    "hawthorne": LOS_ANGELES,
    "hayfork": TRINITY,
    "hayward": ALAMEDA,
    "healdsburg": SONOMA,
    "heber": IMPERIAL,
    "helendale": SAN_BERNADINO,
    "helm": FRESNO,
    "hemet": RIVERSIDE,
    "herald": SACRAMENTO,
    "hercules": CONTRA_COSTA,
    "herlong": LASSEN,
    "hermosabeach": LOS_ANGELES,
    "hesperia": SAN_BERNADINO,
    "hickman": STANISLAUS,
    "hiddenvalleylake": LAKE,
    "highland": SAN_BERNADINO,
    "hilmar": MERCED,
    "hinkley": SAN_BERNADINO,
    "hollister": SAN_BENITO,
    "holt": SAN_JOAQUIN,
    "holtville": IMPERIAL,
    "homeland": RIVERSIDE,
    "homewood": PLACER,
    "honeydew": HUMBOLDT,
    "hood": SACRAMENTO,
    "hoopa": HUMBOLDT,
    "hopland": MENDOCINO,
    "hornbrook": SISKIYOU,
    "hornitos": MARIPOSA,
    "hughson": STANISLAUS,
    "hume": FRESNO,
    "huntingtonbeach": ORANGE,
    "huntingtonpark": LOS_ANGELES,
    "huron": FRESNO,
    "hyampom": TRINITY,
    "hydesville": HUMBOLDT,
    "idyllwild": RIVERSIDE,
    "igo": SHASTA,
    "imperial": IMPERIAL,
    "imperialbeach": SAN_DIEGO,
    "independence": INYO,
    "indianwells": RIVERSIDE,
    "indio": RIVERSIDE,
    "inglewood": LOS_ANGELES,
    "inverness": MARIN,
    "inyokern": KERN,
    "ione": AMADOR,
    "irvine": ORANGE,
    "isleton": SACRAMENTO,
    "ivanhoe": TULARE,
    "jackson": AMADOR,
    "jacumba": SAN_DIEGO,
    "jamestown": TUOLUMNE,
    "jamul": SAN_DIEGO,
    "janesville": LASSEN,
    "jenner": SONOMA,
    "johannesburg": KERN,
    "jolon": MONTEREY,
    "joshuatree": SAN_BERNADINO,
    "julian": SAN_DIEGO,
    "junctioncity": TRINITY,
    "junelake": MONO,
    "jurupavalley": RIVERSIDE,
    "keeler": INYO,
    "keene": KERN,
    "kelseyville": LAKE,
    "kenwood": SONOMA,
    "kerman": FRESNO,
    "kernville": KERN,
    "kettlemancity": KINGS,
    "keyes": STANISLAUS,
    "kingcity": MONTEREY,
    "kingsbeach": PLACER,
    "kingsburg": FRESNO,
    "kingscanyonnationalpk": TULARE,
    "kirkwood": ALPINE,
    "klamath": DEL_NORTE,
    "klamathriver": SISKIYOU,
    "kneeland": HUMBOLDT,
    "knightsen": CONTRA_COSTA,
    "knightslanding": YOLO,
    "korbel": HUMBOLDT,
    "kyburz": EL_DORADO,
    "lacanada": LOS_ANGELES,
    "lacanadaflintridge": LOS_ANGELES,
    "lacrescenta": LOS_ANGELES,
    "laderaranch": ORANGE,
    "lafayette": CONTRA_COSTA,
    "lagrange": TUOLUMNE,
    "lagunabeach": ORANGE,
    "lagunahills": ORANGE,
    "lagunaniguel": ORANGE,
    "lagunawoods": ORANGE,
    "lagunitas": MARIN,
    "lahabra": ORANGE,
    "lahonda": SAN_MATEO,
    "lajolla": SAN_DIEGO,
    "lakearrowhead": SAN_BERNADINO,
    "lakecity": MODOC,
    "lakeelsinore": RIVERSIDE,
    "lakeforest": ORANGE,
    "lakehead": SHASTA,
    "lakehughes": LOS_ANGELES,
    "lakeisabella": KERN,
    "lakeport": LAKE,
    "lakeshore": FRESNO,
    "lakeside": SAN_DIEGO,
    "lakewood": LOS_ANGELES,
    "lamesa": SAN_DIEGO,
    "lamirada": LOS_ANGELES,
    "lamont": KERN,
    "lancaster": LOS_ANGELES,
    "landers": SAN_BERNADINO,
    "lapalma": ORANGE,
    "lapuente": LOS_ANGELES,
    "laquinta": RIVERSIDE,
    "larkspur": MARIN,
    "lathrop": SAN_JOAQUIN,
    "laton": FRESNO,
    "laverne": LOS_ANGELES,
    "lawndale": LOS_ANGELES,
    "laytonville": MENDOCINO,
    "lebec": KERN,
    "leevining": MONO,
    "leggett": MENDOCINO,
    "legrand": MERCED,
    "lemoncove": TULARE,
    "lemongrove": SAN_DIEGO,
    "lemoore": KINGS,
    "lewiston": TRINITY,
    "likely": MODOC,
    "lincoln": PLACER,
    "linden": SAN_JOAQUIN,
    "lindsay": TULARE,
    "litchfield": LASSEN,
    "littleriver": MENDOCINO,
    "littlerock": LOS_ANGELES,
    "liveoak": SUTTER,
    "livermore": ALAMEDA,
    "livingston": MERCED,
    "llano": LOS_ANGELES,
    "lockeford": SAN_JOAQUIN,
    "lockwood": MONTEREY,
    "lodi": SAN_JOAQUIN,
    "loleta": HUMBOLDT,
    "lomalinda": SAN_BERNADINO,
    "lomamar": SAN_MATEO,
    "lomita": LOS_ANGELES,
    "lompoc": SANTA_BARBARA,
    "lonepine": INYO,
    "longbarn": TUOLUMNE,
    "longbeach": LOS_ANGELES,
    "lookout": MODOC,
    "loomis": PLACER,
    "losalamitos": ORANGE,
    "losalamos": SANTA_BARBARA,
    "losaltos": SANTA_CLARA,
    "losangeles": LOS_ANGELES,
    "losbanos": MERCED,
    "losgatos": SANTA_CLARA,
    "losmolinos": TEHAMA,
    "losolivos": SANTA_BARBARA,
    "lososos": SAN_LUIS_OBISPO,
    "losthills": KERN,
    "lotus": EL_DORADO,
    "lowerlake": LAKE,
    "loyalton": SIERRA,
    "lucerne": LAKE,
    "lucernevalley": SAN_BERNADINO,
    "ludlow": SAN_BERNADINO,
    "lynwood": LOS_ANGELES,
    "lytlecreek": SAN_BERNADINO,
    "macdoel": SISKIYOU,
    "madeline": LASSEN,
    "madera": MADERA,
    "madison": YOLO,
    "madriver": TRINITY,
    "magalia": BUTTE,
    "malibu": LOS_ANGELES,
    "mammothlakes": MONO,
    "manchester": MENDOCINO,
    "manhattanbeach": LOS_ANGELES,
    "manteca": SAN_JOAQUIN,
    "manton": TEHAMA,
    "marchairreservebase": RIVERSIDE,
    "maricopa": KERN,
    "marina": MONTEREY,
    "marinadelrey": LOS_ANGELES,
    "mariposa": MARIPOSA,
    "markleeville": ALPINE,
    "marshall": MARIN,
    "martinez": CONTRA_COSTA,
    "marysville": YUBA,
    "mather": SACRAMENTO,
    "maxwell": COLUSA,
    "maywood": LOS_ANGELES,
    "mcarthur": SHASTA,
    "mcclellan": SACRAMENTO,
    "mccloud": SISKIYOU,
    "mcfarland": KERN,
    "mckinleyville": HUMBOLDT,
    "mckittrick": KERN,
    "meadowvalley": PLUMAS,
    "meadowvista": PLACER,
    "mecca": RIVERSIDE,
    "mendocino": MENDOCINO,
    "mendota": FRESNO,
    "menifee": RIVERSIDE,
    "menlopark": SAN_MATEO,
    "mentone": SAN_BERNADINO,
    "merced": MERCED,
    "meridian": SUTTER,
    "middletown": LAKE,
    "midpines": MARIPOSA,
    "midwaycity": ORANGE,
    "milford": LASSEN,
    "millbrae": SAN_MATEO,
    "millcreek": TEHAMA,
    "millvalley": MARIN,
    "millville": SHASTA,
    "milpitas": SANTA_CLARA,
    "mineral": TEHAMA,
    "miraloma": RIVERSIDE,
    "miramonte": FRESNO,
    "miranda": HUMBOLDT,
    "missionhills": LOS_ANGELES,
    "missionviejo": ORANGE,
    "miwukvillage": TUOLUMNE,
    "modesto": STANISLAUS,
    "mojave": KERN,
    "mokelumnehill": CALAVERAS,
    "monrovia": LOS_ANGELES,
    "montague": SISKIYOU,
    "montara": SAN_MATEO,
    "montclair": SAN_BERNADINO,
    "montebello": LOS_ANGELES,
    "monterey": MONTEREY,
    "montereypark": LOS_ANGELES,
    "monterio": SONOMA,
    "montgomerycreek": SHASTA,
    "montrose": LOS_ANGELES,
    "moorpark": VENTURA,
    "moraga": CONTRA_COSTA,
    "morenovalley": RIVERSIDE,
    "morganhill": SANTA_CLARA,
    "morongovalley": SAN_BERNADINO,
    "morrobay": SAN_LUIS_OBISPO,
    "mossbeach": SAN_MATEO,
    "mosslanding": MONTEREY,
    "mountaincenter": RIVERSIDE,
    "mountainranch": CALAVERAS,
    "mountainview": SANTA_CLARA,
    "mounthamilton": SANTA_CLARA,
    "mounthermon": SANTA_CRUZ,
    "mountlaguna": SAN_DIEGO,
    "mountshasta": SISKIYOU,
    "mtbaldy": SAN_BERNADINO,
    "murphys": CALAVERAS,
    "murrieta": RIVERSIDE,
    "myersflat": HUMBOLDT,
    "napa": NAPA,
    "nationalcity": SAN_DIEGO,
    "navarro": MENDOCINO,
    "needles": SAN_BERNADINO,
    "nevadacity": NEVADA,
    "newark": ALAMEDA,
    "newberrysprings": SAN_BERNADINO,
    "newburypark": VENTURA,
    "newcastle": PLACER,
    "newcuyama": SANTA_BARBARA,
    "newhall": LOS_ANGELES,
    "newman": STANISLAUS,
    "newportbeach": ORANGE,
    "newportcoast": ORANGE,
    "nicasio": MARIN,
    "nice": LAKE,
    "nicolaus": SUTTER,
    "niland": IMPERIAL,
    "nipomo": SAN_LUIS_OBISPO,
    "nipton": SAN_BERNADINO,
    "norco": RIVERSIDE,
    "norden": PLACER,
    "northfork": MADERA,
    "northhighlands": SACRAMENTO,
    "northhills": LOS_ANGELES,
    "northhollywood": LOS_ANGELES,
    "northpalmsprings": RIVERSIDE,
    "northridge": LOS_ANGELES,
    "northsanjuan": NEVADA,
    "norwalk": LOS_ANGELES,
    "novato": MARIN,
    "nubieber": LASSEN,
    "nuevo": RIVERSIDE,
    "o'neals": MADERA,
    "oakdale": STANISLAUS,
    "oakhurst": MADERA,
    "oakland": ALAMEDA,
    "oakley": CONTRA_COSTA,
    "oakpark": VENTURA,
    "oakrun": SHASTA,
    "oakview": VENTURA,
    "occidental": SONOMA,
    "oceano": SAN_LUIS_OBISPO,
    "oceanside": SAN_DIEGO,
    "ocotillo": IMPERIAL,
    "ojai": VENTURA,
    "olancha": INYO,
    "oldstation": SHASTA,
    "olema": MARIN,
    "olivehurst": YUBA,
    "olympicvalley": PLACER,
    "ontario": SAN_BERNADINO,
    "onyx": KERN,
    "orange": ORANGE,
    "orangecove": FRESNO,
    "orangevale": SACRAMENTO,
    "oregonhouse": YUBA,
    "orick": HUMBOLDT,
    "orinda": CONTRA_COSTA,
    "orland": GLENN,
    "orleans": HUMBOLDT,
    "orogrande": SAN_BERNADINO,
    "orosi": TULARE,
    "oroville": BUTTE,
    "oxnard": VENTURA,
    "pacifica": SAN_MATEO,
    "pacificgrove": MONTEREY,
    "pacificpalisades": LOS_ANGELES,
    "pacoima": LOS_ANGELES,
    "paicines": SAN_BENITO,
    "pala": SAN_DIEGO,
    "palermo": BUTTE,
    "palmdale": LOS_ANGELES,
    "palmdesert": RIVERSIDE,
    "palmsprings": RIVERSIDE,
    "paloalto": SANTA_CLARA,
    "palocedro": SHASTA,
    "palomarmountain": SAN_DIEGO,
    "palosverdespeninsula": LOS_ANGELES,
    "paloverde": IMPERIAL,
    "panoramacity": LOS_ANGELES,
    "paradise": BUTTE,
    "paramount": LOS_ANGELES,
    "parkerdam": SAN_BERNADINO,
    "parlier": FRESNO,
    "pasadena": LOS_ANGELES,
    "paskenta": TEHAMA,
    "pasorobles": SAN_LUIS_OBISPO,
    "patterson": STANISLAUS,
    "paumavalley": SAN_DIEGO,
    "paynescreek": TEHAMA,
    "pearblossom": LOS_ANGELES,
    "pebblebeach": MONTEREY,
    "penngrove": SONOMA,
    "pennvalley": NEVADA,
    "penryn": PLACER,
    "perris": RIVERSIDE,
    "pescadero": SAN_MATEO,
    "petaluma": SONOMA,
    "petrolia": HUMBOLDT,
    "phelan": SAN_BERNADINO,
    "phillipsville": HUMBOLDT,
    "philo": MENDOCINO,
    "picorivera": LOS_ANGELES,
    "piercy": MENDOCINO,
    "pilothill": EL_DORADO,
    "pinecrest": TUOLUMNE,
    "pinegrove": AMADOR,
    "pinemountainclub": KERN,
    "pinevalley": SAN_DIEGO,
    "pinole": CONTRA_COSTA,
    "pinonhills": SAN_BERNADINO,
    "pioneer": AMADOR,
    "pioneertown": SAN_BERNADINO,
    "piru": VENTURA,
    "pismobeach": SAN_LUIS_OBISPO,
    "pittsburg": CONTRA_COSTA,
    "pixley": TULARE,
    "placentia": ORANGE,
    "placerville": EL_DORADO,
    "planada": MERCED,
    "platina": TRINITY,
    "playadelrey": LOS_ANGELES,
    "playavista": LOS_ANGELES,
    "pleasantgrove": SUTTER,
    "pleasanthill": CONTRA_COSTA,
    "pleasanton": ALAMEDA,
    "plymouth": AMADOR,
    "pointarena": MENDOCINO,
    "pointmugunawc": VENTURA,
    "pointreyesstation": MARIN,
    "pollockpines": EL_DORADO,
    "pomona": LOS_ANGELES,
    "popevalley": NAPA,
    "portcosta": CONTRA_COSTA,
    "porterranch": LOS_ANGELES,
    "porterville": TULARE,
    "porthueneme": VENTURA,
    "porthuenemecbcbase": VENTURA,
    "portola": PLUMAS,
    "portolavalley": SAN_MATEO,
    "posey": TULARE,
    "potrero": SAN_DIEGO,
    "pottervalley": MENDOCINO,
    "poway": SAN_DIEGO,
    "prather": FRESNO,
    "princeton": COLUSA,
    "quincy": PLUMAS,
    "railroadflat": CALAVERAS,
    "raisincity": FRESNO,
    "ramona": SAN_DIEGO,
    "ranchita": SAN_DIEGO,
    "ranchocordova": SACRAMENTO,
    "ranchocucamonga": SAN_BERNADINO,
    "ranchomirage": RIVERSIDE,
    "ranchopalosverdes": LOS_ANGELES,
    "ranchosantafe": SAN_DIEGO,
    "ranchosantamargarita": ORANGE,
    "randsburg": KERN,
    "ravendale": LASSEN,
    "raymond": MADERA,
    "redbluff": TEHAMA,
    "redcrest": HUMBOLDT,
    "redding": SHASTA,
    "redlands": SAN_BERNADINO,
    "redmountain": SAN_BERNADINO,
    "redondobeach": LOS_ANGELES,
    "redway": HUMBOLDT,
    "redwoodcity": SAN_MATEO,
    "redwoodvalley": MENDOCINO,
    "reedley": FRESNO,
    "rescue": EL_DORADO,
    "reseda": LOS_ANGELES,
    "rialto": SAN_BERNADINO,
    "richgrove": TULARE,
    "richmond": CONTRA_COSTA,
    "richvale": BUTTE,
    "ridgecrest": KERN,
    "rimforest": SAN_BERNADINO,
    "riodell": HUMBOLDT,
    "riolinda": SACRAMENTO,
    "rionido": SONOMA,
    "riooso": SUTTER,
    "riovista": SOLANO,
    "ripon": SAN_JOAQUIN,
    "riverbank": STANISLAUS,
    "riverdale": FRESNO,
    "riverpines": AMADOR,
    "riverside": RIVERSIDE,
    "rocklin": PLACER,
    "rodeo": CONTRA_COSTA,
    "rohnertpark": SONOMA,
    "rosamond": KERN,
    "rosemead": LOS_ANGELES,
    "roseville": PLACER,
    "ross": MARIN,
    "roughandready": NEVADA,
    "roundmountain": SHASTA,
    "rowlandheights": LOS_ANGELES,
    "rumsey": YOLO,
    "runningsprings": SAN_BERNADINO,
    "rutherford": NAPA,
    "ryde": SACRAMENTO,
    "sacramento": SACRAMENTO,
    "sainthelena": NAPA,
    "salida": STANISLAUS,
    "salinas": MONTEREY,
    "saltoncity": IMPERIAL,
    "salyer": TRINITY,
    "samoa": HUMBOLDT,
    "sanandreas": CALAVERAS,
    "sananselmo": MARIN,
    "sanardo": MONTEREY,
    "sanbernardino": SAN_BERNADINO,
    "sanbruno": SAN_MATEO,
    "sancarlos": SAN_MATEO,
    "sanclemente": ORANGE,
    "sandiego": SAN_DIEGO,
    "sandimas": LOS_ANGELES,
    "sanfernando": LOS_ANGELES,
    "sanfrancisco": SAN_FRANCISCO,
    "sangabriel": LOS_ANGELES,
    "sanger": FRESNO,
    "sangeronimo": MARIN,
    "sangregorio": SAN_MATEO,
    "sanjacinto": RIVERSIDE,
    "sanjoaquin": FRESNO,
    "sanjose": SANTA_CLARA,
    "sanjuanbautista": SAN_BENITO,
    "sanjuancapistrano": ORANGE,
    "sanleandro": ALAMEDA,
    "sanlorenzo": ALAMEDA,
    "sanlucas": MONTEREY,
    "sanluisobispo": SAN_LUIS_OBISPO,
    "sanmarcos": SAN_DIEGO,
    "sanmarino": LOS_ANGELES,
    "sanmartin": SANTA_CLARA,
    "sanmateo": SAN_MATEO,
    "sanmiguel": SAN_LUIS_OBISPO,
    "sanpablo": CONTRA_COSTA,
    "sanpedro": LOS_ANGELES,
    "sanquentin": MARIN,
    "sanrafael": MARIN,
    "sanramon": CONTRA_COSTA,
    "sansimeon": SAN_LUIS_OBISPO,
    "santaana": ORANGE,
    "santabarbara": SANTA_BARBARA,
    "santaclara": SANTA_CLARA,
    "santaclarita": LOS_ANGELES,
    "santacruz": SANTA_CRUZ,
    "santafesprings": LOS_ANGELES,
    "santamargarita": SAN_LUIS_OBISPO,
    "santamaria": SANTA_BARBARA,
    "santamonica": LOS_ANGELES,
    "santapaula": VENTURA,
    "santarosa": SONOMA,
    "santaynez": SANTA_BARBARA,
    "santaysabel": SAN_DIEGO,
    "santee": SAN_DIEGO,
    "sanysidro": SAN_DIEGO,
    "saratoga": SANTA_CLARA,
    "sausalito": MARIN,
    "scotia": HUMBOLDT,
    "scottbar": SISKIYOU,
    "scottsvalley": SANTA_CRUZ,
    "sealbeach": ORANGE,
    "seaside": MONTEREY,
    "sebastopol": SONOMA,
    "seeley": IMPERIAL,
    "seiadvalley": SISKIYOU,
    "selma": FRESNO,
    "sequoianationalpark": TULARE,
    "shafter": KERN,
    "shandon": SAN_LUIS_OBISPO,
    "shasta": SHASTA,
    "shastalake": SHASTA,
    "shaverlake": FRESNO,
    "sheridan": PLACER,
    "shermanoaks": LOS_ANGELES,
    "shinglesprings": EL_DORADO,
    "shingletown": SHASTA,
    "shoshone": INYO,
    "sierracity": SIERRA,
    "sierramadre": LOS_ANGELES,
    "sierraville": SIERRA,
    "signalhill": LOS_ANGELES,
    "silverado": ORANGE,
    "simivalley": VENTURA,
    "skyforest": SAN_BERNADINO,
    "sloughhouse": SACRAMENTO,
    "smartsville": NEVADA,
    "smithriver": DEL_NORTE,
    "snelling": MERCED,
    "sodasprings": PLACER,
    "solanabeach": SAN_DIEGO,
    "soledad": MONTEREY,
    "solvang": SANTA_BARBARA,
    "somerset": EL_DORADO,
    "somesbar": SISKIYOU,
    "somis": VENTURA,
    "sonoma": SONOMA,
    "sonora": TUOLUMNE,
    "soquel": SANTA_CRUZ,
    "soulsbyville": TUOLUMNE,
    "southdospalos": MERCED,
    "southelmonte": LOS_ANGELES,
    "southgate": LOS_ANGELES,
    "southlaketahoe": EL_DORADO,
    "southpasadena": LOS_ANGELES,
    "southsanfrancisco": SAN_MATEO,
    "spreckels": MONTEREY,
    "springvalley": SAN_DIEGO,
    "springville": TULARE,
    "squawvalley": FRESNO,
    "standish": LASSEN,
    "stanford": SANTA_CLARA,
    "stanton": ORANGE,
    "stevensonranch": LOS_ANGELES,
    "stevinson": MERCED,
    "stinsonbeach": MARIN,
    "stirlingcity": BUTTE,
    "stockton": SAN_JOAQUIN,
    "stonyford": COLUSA,
    "stratford": KINGS,
    "strathmore": TULARE,
    "strawberry": TUOLUMNE,
    "strawberryvalley": YUBA,
    "studiocity": LOS_ANGELES,
    "sugarloaf": SAN_BERNADINO,
    "suisuncity": SOLANO,
    "sultana": TULARE,
    "summerland": SANTA_BARBARA,
    "sunland": LOS_ANGELES,
    "sunnyvale": SANTA_CLARA,
    "sunol": ALAMEDA,
    "sunsetbeach": ORANGE,
    "sunvalley": LOS_ANGELES,
    "surfside": ORANGE,
    "susanville": LASSEN,
    "sutter": SUTTER,
    "suttercreek": AMADOR,
    "sylmar": LOS_ANGELES,
    "taft": KERN,
    "tahoecity": PLACER,
    "tahoevista": PLACER,
    "tahoma": EL_DORADO,
    "tarzana": LOS_ANGELES,
    "taylorsville": PLUMAS,
    "tecate": SAN_DIEGO,
    "tecopa": INYO,
    "tehachapi": KERN,
    "tehama": TEHAMA,
    "temecula": RIVERSIDE,
    "templecity": LOS_ANGELES,
    "templeton": SAN_LUIS_OBISPO,
    "termo": LASSEN,
    "terrabella": TULARE,
    "thermal": RIVERSIDE,
    "thesearanch": SONOMA,
    "thornton": SAN_JOAQUIN,
    "thousandoaks": VENTURA,
    "thousandpalms": RIVERSIDE,
    "threerivers": TULARE,
    "tipton": TULARE,
    "tollhouse": FRESNO,
    "tomales": MARIN,
    "topanga": LOS_ANGELES,
    "topaz": MONO,
    "torrance": LOS_ANGELES,
    "trabucocanyon": ORANGE,
    "tracy": SAN_JOAQUIN,
    "tranquillity": FRESNO,
    "traver": TULARE,
    "travisafb": SOLANO,
    "trespinos": SAN_BENITO,
    "trinidad": HUMBOLDT,
    "trinitycenter": TRINITY,
    "trona": SAN_BERNADINO,
    "truckee": NEVADA,
    "tujunga": LOS_ANGELES,
    "tulare": TULARE,
    "tulelake": SISKIYOU,
    "tuolumne": TUOLUMNE,
    "tupman": KERN,
    "turlock": STANISLAUS,
    "tustin": ORANGE,
    "twain": PLUMAS,
    "twainharte": TUOLUMNE,
    "twentyninepalms": SAN_BERNADINO,
    "twinbridges": EL_DORADO,
    "twinpeaks": SAN_BERNADINO,
    "ukiah": MENDOCINO,
    "unioncity": ALAMEDA,
    "universalcity": LOS_ANGELES,
    "upland": SAN_BERNADINO,
    "upperlake": LAKE,
    "vacaville": SOLANO,
    "valencia": LOS_ANGELES,
    "vallecito": CALAVERAS,
    "vallejo": SOLANO,
    "valleycenter": SAN_DIEGO,
    "valleyford": MARIN,
    "valleysprings": CALAVERAS,
    "valleyvillage": LOS_ANGELES,
    "valyermo": LOS_ANGELES,
    "vannuys": LOS_ANGELES,
    "venice": LOS_ANGELES,
    "ventura": VENTURA,
    "verdugocity": LOS_ANGELES,
    "vernalis": STANISLAUS,
    "victorville": SAN_BERNADINO,
    "vidal": SAN_BERNADINO,
    "villagrande": SONOMA,
    "villapark": ORANGE,
    "vina": TEHAMA,
    "vinton": PLUMAS,
    "visalia": TULARE,
    "vista": SAN_DIEGO,
    "volcano": AMADOR,
    "wallace": CALAVERAS,
    "walnut": LOS_ANGELES,
    "walnutcreek": CONTRA_COSTA,
    "walnutgrove": SACRAMENTO,
    "warnersprings": SAN_DIEGO,
    "wasco": KERN,
    "washington": NEVADA,
    "waterford": STANISLAUS,
    "watsonville": SANTA_CRUZ,
    "weaverville": TRINITY,
    "weed": SISKIYOU,
    "weimar": PLACER,
    "weldon": KERN,
    "wendel": LASSEN,
    "weott": HUMBOLDT,
    "westcovina": LOS_ANGELES,
    "westhills": LOS_ANGELES,
    "westhollywood": LOS_ANGELES,
    "westlakevillage": VENTURA,
    "westley": STANISLAUS,
    "westminster": ORANGE,
    "westmorland": IMPERIAL,
    "westpoint": CALAVERAS,
    "westport": MENDOCINO,
    "westsacramento": YOLO,
    "westwood": LASSEN,
    "wheatland": YUBA,
    "whitethorn": HUMBOLDT,
    "whitewater": RIVERSIDE,
    "whitmore": SHASTA,
    "whittier": LOS_ANGELES,
    "wildomar": RIVERSIDE,
    "williams": COLUSA,
    "willits": MENDOCINO,
    "willowcreek": HUMBOLDT,
    "willows": GLENN,
    "wilmington": LOS_ANGELES,
    "wilseyville": CALAVERAS,
    "wilton": SACRAMENTO,
    "winchester": RIVERSIDE,
    "windsor": SONOMA,
    "winnetka": LOS_ANGELES,
    "winterhaven": IMPERIAL,
    "winters": YOLO,
    "winton": MERCED,
    "wishon": MADERA,
    "wittersprings": LAKE,
    "woffordheights": KERN,
    "woodacre": MARIN,
    "woodbridge": SAN_JOAQUIN,
    "woodlake": TULARE,
    "woodland": YOLO,
    "woodlandhills": LOS_ANGELES,
    "woody": KERN,
    "wrightwood": SAN_BERNADINO,
    "yermo": SAN_BERNADINO,
    "yolo": YOLO,
    "yorbalinda": ORANGE,
    "yorkville": MENDOCINO,
    "yosemitenationalpark": MARIPOSA,
    "yountville": NAPA,
    "yreka": SISKIYOU,
    "yubacity": SUTTER,
    "yucaipa": SAN_BERNADINO,
    "yuccavalley": SAN_BERNADINO,
    "zamora": YOLO,
    "zenia": TRINITY,
}
