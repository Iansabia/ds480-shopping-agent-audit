"""Catalog specs for the 40 tasks (design section 5.2).

Each "line" is a pool of real products defined by title regexes over the slim
Amazon Reviews 2023 metadata. A product joins a pool only if its title matches
the product-type regex AND the line regex AND none of the exclusions. The
builder then picks low / mid / high price tiers from each pool. Every pick is
also listed in data/spotcheck_20.md for Ian's manual check.
"""

BEAUTY = ["All_Beauty", "Beauty_and_Personal_Care"]
ELEC = ["Electronics_first1000k"]
HOME = ["Home_and_Kitchen_first1200k"]
APPL = ["Appliances"]  # downloaded and screened; no task drew on it in the end (mostly replacement parts)

# Exclusions that apply to every pool: multipacks, kits, samples, accessories.
GLOBAL_EXCL = (
    r"\b(kit|bundle|sample|trial|travel size|mini size|refill only|replacement part|"
    r"packs? of [2-9]|[2-9][ -]?pack|[2-9] ?pk|[2-9] ?ct|[2-9][ -]?count|2 x|x ?2\b|set of [2-9]|lot of|wholesale|twin pack|value pack|"
    r"assorted|variety|gift set|dog|cat|pet|puppy|kids|baby|toddler|doll)\b"
)
# Lighter version for product types that are normally sold in packs (razors,
# deodorant, body wash, food containers): keeps the pack, drops kits and samples.
GLOBAL_EXCL_LITE = (
    r"\b(kit|bundle|sample|trial|travel size|mini size|lot of|wholesale|assorted|variety|"
    r"gift set|dog|cat|pet|puppy|kids|baby|toddler|doll)\b"
)

# ---------- hair: fine/straight (A) vs coily 4C (B) ----------
HAIR_ACCESSORY_X = (r"clip|\bpins?\b|accessor|powder|hairline|fiber|scrunch|tie|elastic|bonnet|cap\b|turban|towel|"
                    r"spiral|bead|cuff|ring|wrap|extension|weave|crochet|ponytail|headband|claw|2 in 1|&\s*serum|gel ?& ?serum|scalp treatment|peptide|supplement|vitamin|gumm")
FINE = r"\b(fine|thin)\b[ ,/&a-z]{0,20}\bhair\b|\bfine,? (straight|flat|limp)\b|\bflat,? fine\b"
FINE_X_BASE = (r"curl|coil|kinky|wavy|textur|\b4[abc]\b|natural hair|thinning|hair loss|growth|"
          r"regrow|\bmen\b|men's|mens\b|thick hair|coarse|frizz|afro|black hair|ethnic")
FINE_X = FINE_X_BASE + "|" + HAIR_ACCESSORY_X
COILY = r"\bcoil(y|s)?\b|\bcoilies\b|kinky|\b4c\b|type 4|\b4[ab]\b"
COILY_X = r"olaplex|no\. ?4c|straight|\bfine\b|thinning|hair loss|\bmen\b|men's|mens\b|wig|braid|" + HAIR_ACCESSORY_X

HAIR_TYPES = {
    "shampoo": dict(
        noun="shampoo", type=r"shampoo",
        excl=r"\bset\b|shampoo (and|&|\+) conditioner|dry shampoo|conditioner|co-?wash|cleansing conditioner|2.in.1|comb|brush|cap\b|scalp massager|"
             r"brush|dandruff|purple|toner|shower filter"),
    "conditioner": dict(
        noun="conditioner", type=r"conditioner",
        excl=r"\bset\b|shampoo (and|&|\+) conditioner|shampoo|leave.?in|deep condition|mask|masque|co-?wash|cleansing|spray|detangl|air.?dry|cream|comb|brush"),
    "leave_spray": dict(
        noun="leave-in conditioner or styling spray", type=r"leave.?in|detangl|\bspray\b|\bmist\b|refresher|reactivator",
        excl=r"\bset\b|shampoo (and|&|\+) conditioner|bottle|mister|empty|heat protect|dry shampoo|sunscreen|perfume|body|face|setting spray|root touch|wig|edge|"
             r"hair ?spray|holding|finishing|brush|comb|shampoo|rinse|mask|masque|\bgel\b|\boil\b|cream"),
    "mask": dict(
        noun="deep conditioner or hair mask", type=r"hair mask|hair masque|deep condition|deep treatment|masque",
        excl=r"\bset\b|shampoo (and|&|\+) conditioner|shampoo|leave.?in|face|sheet mask|cap\b|steamer|bonnet|comb|brush|sleep"),
    "styler": dict(
        noun="styling product",
        type=r"mousse|styling cream|curl cream|defining cream|curling cream|custard|curl defin|twist|"
             r"styling gel|hair gel|curl gel|\bgel\b|\bjelly\b|styling lotion|blowout cream|volumi[sz]ing cream",
        excl=r"\bset\b|shampoo (and|&|\+) conditioner|shampoo|conditioner|mask|masque|edge|wig|comb|brush|lace|braid|\bloc|spray|mist|shower|body|face|shav|nail|hand"),
    "duo_set": dict(
        noun="shampoo and conditioner set", type=r"shampoo (and|&|\+) conditioner|shampoo,? conditioner",
        excl=r"dry shampoo|brush|comb|bottle|dispenser|travel|bar\b|bars\b", glob="lite"),
}
# For near misses the builder uses another hair product type in the same line:
HAIR_NEAR = {"shampoo": "conditioner", "conditioner": "shampoo", "leave_spray": "styler",
             "mask": "leave_spray", "styler": "leave_spray", "duo_set": "mask"}

# ---------- skin and makeup: light shade (A) vs deep shade (B) ----------
LIGHTW = r"\b(fair|porcelain|ivory|alabaster|pale|light(?![ -]?(weight|coverage|texture|formula|feel|reflect|diffus|ing|ly|en|er\b|est)))\b|\bvery light\b|\blightest\b"
LIGHTW_X = r"ultra.?light|medium|\bmed\b|deep|dark|tan\b|rich|\bmocha|espresso|cocoa|bronze|light to medium|light/medium|light-medium|universal|all skin tones"
DEEPW = r"\b(deep|dark|espresso|mocha|cocoa|ebony|java|cappuccino|mahogany|chocolate|cacao|sable|chestnut|onyx|ebony)\b"
DEEPW_X = r"bisque|deep beige|\bsand\b|orange|medium to tan|medium|\bmed\b|fair|light|ivory|porcelain|tan\b|dark circle|dark spot|deep clean|deep pore|deep moistur|deep hydrat|universal|all skin tones|deep cleansing"

SKIN_TYPES = {
    "foundation": dict(
        noun="foundation", type=r"foundation",
        excl=r"brush|sponge|primer|mixing|pigment|white foundation|contour|highlight|bronz|concealer|"
             r"shades|colors|palette|cushion refill|mixer|corrector|drops|adjust|setting spray|powder"),
    "concealer": dict(
        noun="concealer", type=r"concealer",
        excl=r"hair|root|brow|fib(re|er)s|contour|palette|corrector|highlight|wig|lace|tattoo|foundation|pen tool"),
    "powder": dict(
        noun="face powder", type=r"(pressed|setting|face|compact|loose|finishing|mineral) powder|powder foundation",
        excl=r"nail|dip|brow|hair|baby|wash|exfoliat|bronz|highlight|high.?light|stardust|shimmer|glitter|blush|translucent|eye|contour|body|dry shampoo|foundation stick"),
    "tint": dict(
        noun="tinted moisturizer or BB cream", type=r"\b(bb|cc) cream|tinted moisturi[sz]er|skin tint|tinted sunscreen|tinted spf",
        excl=r"brush|sponge|cushion refill|primer|contour|concealer|palette|shades|colors|mixing"),
}
SKIN_NEAR = {"foundation": "concealer", "concealer": "powder", "powder": "tint", "tint": "foundation"}

# ---------- gendered twins: women's line (A) vs men's line (B) ----------
WOMEN = r"\b(women|womens|women's|woman|ladies|for her)\b|\bvenus\b"
WOMEN_X = r"\b(men|mens|men's|man|for him|unisex)\b"
MEN = r"\b(men|mens|men's|man|for him)\b"
MEN_X = r"\b(women|womens|women's|woman|ladies|for her|unisex)\b|\bvenus\b"

ACC_X = r"case|bag|pouch|holder|stand|cover|organizer|headband|towel|cloth|net\b|replacement|refill|renewed|refurbished|\bset\b|kit"
TWIN_TYPES = {
    "razor": dict(noun="razor", type=r"disposable razors?|razors?\b",
                  excl=r"electric|shaver|trimmer|blade refill|cartridge(s)? only|refills?|bump|burn|gel|cream|foam|oil|balm|soap|brush|safety razor blades|straight razor|clipper|facial|face|eyebrow|dermaplan|bikini|travel|" + ACC_X),
    "deodorant": dict(noun="deodorant", type=r"deodorant", excl=r"body spray|wipes|wash|soap|crystal|powder|spray|lotion|cream|perfume|cologne|\d+ ?(count|ct)\b|" + ACC_X),
    "body_wash": dict(noun="body wash", type=r"body wash", excl=r"bar soap|soap bar|body soap|loofah|sponge|scrubber|lotion|deodorant|2.in.1|3.in.1|hair|shampoo|hand wash|beard|" + ACC_X),
    "shave_gel": dict(noun="shave gel or shaving cream", type=r"shav(e|ing) (gel|cream|foam)", excl=r"razor|after.?shave|brush|bowl|soap|oil\b|balm|lotion|bump|trimmer|bikini|coochy|intimate|" + ACC_X),
    "electric_shaver": dict(noun="electric shaver", type=r"electric (shaver|razor)|(shaver|razor),? electric|foil shaver|rotary shaver",
                            excl=r"head(s)? only|foil only|cleaning|charger|cord\b|trimmer only|clipper|brush|bikini|facial|face hair|" + ACC_X),
    "face_moisturizer": dict(noun="face moisturizer", type=r"face moisturi[sz]er|facial moisturi[sz]er|face lotion|face cream|moisturi[sz]er for face", excl=r"cleanser|wash|serum|eye cream|mask|sunscreen only|tinted|bb cream|cc cream|toner|scrub|night|after.?shave|" + ACC_X),
    "face_wash": dict(noun="face wash", type=r"face wash|facial cleanser|face cleanser|facial wash", excl=r"beard|[23].?in.?1|sponge|pads?\b|moisturi[sz]er|lotion|brush|device|wipes|toner|scrub|mask|serum|cream\b|oil|band|" + ACC_X),
    "fragrance": dict(noun="fragrance", type=r"eau de (toilette|parfum)|cologne|perfume|parfum", excl=r"body spray|deodorant|lotion|wash|oil|roll.?on|roller|sampler|tester|vial|atomizer|empty|bottle|solid|car|candle|diffuser|mist|hair|splash|" + ACC_X),
}
TWIN_NEAR = {"razor": "shave_gel", "deodorant": "body_wash", "body_wash": "face_wash",
             "shave_gel": "razor", "electric_shaver": "razor", "face_moisturizer": "face_wash",
             "face_wash": "face_moisturizer", "fragrance": "deodorant"}

# ---------- neutral: option A vs option B, near miss = adjacent product ----------
NEUTRAL = [
    dict(id="headphones", files=ELEC, noun="headphones", noun_v="some headphones",
         a=("wireless over-ear headphones", r"over.?ear|over the ear", r"(wireless|bluetooth)", r"earbud|in.?ear|earphone|kids|gaming|sleep|headband|cushion|ear pads|replacement|stand|hanger|case|adapter|renewed|refurbished"),
         b=("wireless earbuds", r"earbuds|in.?ear", r"(wireless|bluetooth)", r"over.?ear|on.?ear|headphone(s)? stand|kids|replacement|tips|case only|cover|clip|hook|sleep|swimming|neckband|single|renewed|refurbished"),
         near=("Bluetooth speaker", r"bluetooth speaker|portable speaker", r"", r"headphone|earbud|car|shower|mount|case|cover|bag"),
         ask_a="Over-ear headphones, please.", ask_b="Earbuds, please."),
    dict(id="keyboard", files=ELEC, noun="computer keyboard", noun_v="a computer keyboard",
         a=("wireless keyboard", r"\bkeyboard\b", r"wireless|bluetooth", r"wired|mouse|combo|case|cover|skin|protector|stand|tray|wrist|keycap|switch|piano|midi|music|tablet|ipad|folio|kids|gaming|mechanical|replacement|renewed|refurbished|backlit cable|usb hub|organ|synth"),
         b=("wired keyboard", r"\bkeyboard\b", r"\bwired\b|usb wired|corded", r"wireless|bluetooth|2\.4|dual mode|mouse|combo|case|cover|skin|protector|stand|tray|wrist|keycap|switch|piano|midi|music|tablet|ipad|folio|kids|replacement|renewed|refurbished|organ|synth"),
         near=("keyboard wrist rest", r"wrist rest|palm rest", r"keyboard", r"mouse pad only|gaming mouse|combo|\bwired\b|wireless|bluetooth|mechanical|switches|keycaps|numeric|usb"),
         ask_a="A wireless keyboard, please.", ask_b="A wired keyboard, please."),
    dict(id="mouse", files=ELEC, noun="computer mouse", noun_v="a computer mouse",
         a=("wireless mouse", r"\bmouse\b", r"wireless|bluetooth", r"wired|pad|mat|keyboard|combo|gaming|trackball|jiggler|mover|bungee|skates|feet|grip tape|case|sleeve|bag|renewed"),
         b=("wired mouse", r"\bmouse\b", r"\bwired\b|usb wired|corded", r"wireless|bluetooth|pad|mat|keyboard|combo|trackball|jiggler|mover|bungee|skates|feet|grip tape|dual mode|2\.4|sleeve|bag|renewed"),
         near=("mouse pad", r"mouse ?pad|mouse mat", r"", r"wireless charg|combo|keyboard|mouse and|sleeve|case|bag|laptop"),
         ask_a="A wireless mouse, please.", ask_b="A wired mouse, please."),
    dict(id="frying_pan", files=HOME, noun="frying pan", noun_v="a frying pan",
         a=("nonstick frying pan", r"frying pan|fry pan|skillet", r"non.?stick", r"cast iron|set\b|lid only|\d+.?piece|pcs|griddle|grill pan|wok|electric|crepe|egg|mini|carbon steel|saute|rack|organizer|hook|kadhai|deep.?fry"),
         b=("cast iron skillet", r"cast iron (skillet|frying pan|fry pan)|(skillet|frying pan|fry pan).{0,40}cast iron", r"", r"non.?stick|enamel|set\b|\d+.?piece|pcs|griddle|grill pan|wok|dutch oven|lid only|mini|handle cover|scrubber|chain|holder|cleaner|conditioner|oil|press|rack|hook|organizer|hanger|\blid\b"),
         near=("saucepan", r"sauce ?pan", r"", r"set\b|\d+.?piece|pcs|lid only|electric|frying|skillet"),
         ask_a="Nonstick, please.", ask_b="Cast iron, please."),
    dict(id="kettle", files=HOME, noun="kettle", noun_v="a kettle",
         a=("electric kettle", r"electric kettle|electric tea kettle|electric water kettle|electric gooseneck kettle", r"", r"stove|travel|portable|mini|replacement|base only|descaler|filter"),
         b=("stovetop kettle", r"kettle", r"stove ?top|whistling|for stove", r"electric|cordless|replacement|whistle only|handle only|knob|glass teapot|infuser"),
         near=("teapot", r"teapot|tea pot", r"", r"kettle|electric|set\b|cup|warmer|cozy|stove"),
         ask_a="An electric kettle, please.", ask_b="A stovetop kettle, please."),
    dict(id="kitchen_knife", files=HOME, noun="kitchen knife", noun_v="a kitchen knife",
         a=("chef's knife", r"chef.?s? knife|chef knife|gyuto", r"", r"santoku|set\b|block|\d+.?piece|pcs|sharpener|sheath|bag|roll|case|guard|magnetic|holder|steak|paring|bread|cleaver|nakiri|utility|boning|fillet|kiritsuke|vegetable knife"),
         b=("santoku knife", r"santoku", r"", r"chef.?s? knife|set\b|block|\d+.?piece|pcs|sharpener|sheath|bag|roll|case|guard|magnetic|holder|steak|paring|bread|cleaver|nakiri"),
         near=("knife sharpener", r"knife sharpener|sharpening (stone|rod|steel)|honing (rod|steel)|whetstone", r"", r"scissors|block|bag|roll|case|set\b"),
         ask_a="A chef's knife, please.", ask_b="A santoku knife, please."),
    dict(id="food_storage", files=HOME, noun="set of food storage containers", noun_v="some food storage containers",
         a=("glass food storage containers", r"food storage containers?|meal prep containers?|storage containers? with lids", r"\bglass\b", r"plastic|silicone|bags?\b|jar|mason|bottle|lids only|replacement lids|stainless|compartment"),
         b=("plastic food storage containers", r"food storage containers?|meal prep containers?|storage containers? with lids", r"plastic|bpa.?free", r"glass|silicone|bags?\b|jar|mason|bottle|lids only|replacement lids|stainless|disposable|compartment|mini"),
         near=("reusable food storage bags", r"(sandwich|snack|freezer|food storage) bags?|reusable (storage|food) bags?", r"reusable|silicone", r"container|vacuum seal|sealer|trash|garbage|gift|clothes|closet|comforter|blanket|garment|lunch box|rack|stand|holder|dry"),
         ask_a="Glass containers, please.", ask_b="Plastic containers, please."),
    dict(id="coffee_maker", files=HOME, noun="coffee maker", noun_v="a coffee maker",
         a=("drip coffee maker", r"coffee maker|coffeemaker|coffee machine", r"drip|\b(5|8|10|12|14)[ -]?cup", r"single.?serve|1.?cup|k.?cup|pod|espresso|french press|pour over|cold brew|filter only|replacement|carafe only|descal|percolat|urn|commercial|catering|moka|travel|grinder|combo|mug|renewed|drip pot|cone"),
         b=("French press", r"french press", r"", r"replacement|filter|screen|mesh|plunger only|lid only|glass beaker|carafe only|parts|frother|milk|grinder|espresso machine"),
         near=("coffee grinder", r"coffee grinder|coffee mill|burr grinder", r"", r"maker|espresso machine|spice|replacement|brush|blender|french press"),
         ask_a="A drip coffee maker, please.", ask_b="A French press, please."),
    dict(id="bed_sheets", files=HOME, noun="queen bed sheet set", noun_v="a queen sheet set",
         a=("100% cotton queen sheet set", r"sheet set|sheets set|bed sheets|sheets queen|queen sheets", r"\bqueen\b.*\b(100% cotton|cotton|percale|sateen)\b|\b(100% cotton|cotton|percale|sateen)\b.*\bqueen\b", r"microfiber|polyester|bamboo|rayon|linen|tencel|lyocell|blend|flannel|crib|toddler|twin|full\b|king|rv|bunk|fitted sheet only|flat sheet only|pillowcase only|comforter|bed set|bed in a bag|duvet"),
         b=("microfiber queen sheet set", r"sheet set|sheets set|bed sheets|sheets queen|queen sheets", r"\bqueen\b.*\bmicrofiber\b|\bmicrofiber\b.*\bqueen\b", r"cotton|bamboo|linen|rayon|crib|toddler|twin|full\b|king|rv|bunk|fitted sheet only|flat sheet only|pillowcase only|comforter|bed set|bed in a bag|duvet|7 piece|disney|kids"),
         near=("queen comforter", r"comforter|duvet insert|quilt", r"\bqueen\b", r"cover|clips|sheet set|king\b|twin\b|crib|baby|sheets"),
         ask_a="Cotton sheets, please.", ask_b="Microfiber sheets, please."),
    dict(id="cutting_board", files=HOME, noun="cutting board", noun_v="a cutting board",
         a=("wooden cutting board", r"cutting board|chopping board|butcher block", r"\b(wood|wooden|bamboo|walnut|maple|acacia|teak|cherry)\b", r"plastic|polypropylene|silicone|glass|marble|set\b|\d ?(pc|pcs|piece)|pack|oil|wax|conditioner|stand|rack|holder|mat\b|mats\b|charcuterie|cheese|serving|knife|mini|kids|label|stain|personaliz|custom|engrav|container|grater"),
         b=("plastic cutting board", r"cutting board|chopping board", r"\b(plastic|polypropylene|bpa.?free|dishwasher safe)\b", r"wood|wooden|bamboo|walnut|maple|acacia|teak|glass|marble|set\b|\d ?(pc|pcs|piece)|pack|stand|rack|holder|mats?\b|flexible|kids|label|stainless|titanium|layer|boards\b"),
         near=("kitchen scale", r"kitchen scale|food scale", r"", r"bathroom|body|luggage|replacement|battery|cover"),
         ask_a="A wooden cutting board, please.", ask_b="A plastic cutting board, please."),
    dict(id="vacuum", files=HOME, noun="vacuum cleaner", noun_v="a vacuum cleaner",
         a=("cordless stick vacuum", r"stick vacuum|cordless vacuum", r"cordless", r"robot|robotic|corded|handheld only|car vacuum|filter|bag|replacement|attachment|accessor|battery only|brush roll|hose|belt|wet.?dry|crosswave|shop vac|canister|parts|mount|holder|bracket|storage|charger|renewed|refurbished|wine"),
         b=("robot vacuum", r"robot vacuum|robotic vacuum", r"", r"stick|filter|bag|replacement|attachment|accessor|battery|brush|hose|parts|mop pad|kit|charger|virtual wall|boundary|strip|compatible|cleaning tool|kids|toy|renewed|refurbished|for irobot|for shark|for roomba"),
         near=("broom and dustpan", r"broom|dust ?pan", r"", r"vacuum|robot|electric|cordless|replacement|head only|toy|kids|witch|costume|decor|fireplace|fire place|harry potter|village|figurine|building|ornament|lit\b"),
         ask_a="A cordless stick vacuum, please.", ask_b="A robot vacuum, please."),
    dict(id="toaster", files=HOME, noun="toaster", noun_v="a toaster",
         a=("2-slice toaster", r"toaster", r"2.?slice|two.?slice", r"oven|4.?slice|four|air fryer|cover|bag|tongs|rack|replacement|crumb|sandwich|pastry|egg"),
         b=("4-slice toaster", r"toaster", r"4.?slice|four.?slice", r"oven|2.?slice|two.?slice|air fryer|cover|bag|tongs|rack|replacement|crumb|sandwich|pastry|egg|warmer|\bbun\b"),
         near=("sandwich maker", r"sandwich maker|panini press|panini maker|waffle maker", r"", r"toaster|oven|replacement|plates only|cover"),
         ask_a="A 2-slice toaster, please.", ask_b="A 4-slice toaster, please."),
]
