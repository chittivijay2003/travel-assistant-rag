"""Curated travel documents dataset for knowledge base."""

from ..models.domain import TravelDocument, TravelCategory

# Comprehensive travel documents
TRAVEL_DOCUMENTS = [
    # VISA REQUIREMENTS - JAPAN
    TravelDocument(
        id="visa_india_japan_001",
        title="Japan Tourist Visa Requirements for Indian Citizens",
        content="""
Indian citizens require a tourist visa to visit Japan for tourism purposes.

Required Documents:
- Valid passport (minimum 6 months validity from date of travel)
- Completed visa application form with recent photograph
- Recent passport-size color photograph (4.5cm x 4.5cm)
- Round-trip flight itinerary/booking confirmation
- Hotel reservations or accommodation proof for entire stay
- Bank statements for last 3-6 months showing sufficient funds
- Employment letter or business registration certificate
- Income Tax Returns (ITR) for last 2-3 years
- Cover letter explaining purpose of visit

Processing Time: 5-7 business days
Visa Validity: Typically 3 months (single or multiple entry)
Stay Duration: Up to 15, 30, or 90 days depending on visa type
Application Fee: Approximately ₹500-1000 (varies)

Application Process:
1. Submit documents to VFS Global or Japanese Embassy/Consulate
2. Pay visa processing fee
3. Attend interview if required
4. Track application status online
5. Collect visa once approved

Important Notes:
- No visa-on-arrival facility for Indian passport holders
- Travel insurance is highly recommended
- Proof of sufficient funds (minimum ₹50,000-75,000 per person)
- Return flight tickets must be confirmed
- Hotel bookings should match visa validity period
        """,
        category=TravelCategory.VISA_REQUIREMENTS,
        country="Japan",
        source_country="India",
        tags=["tourist_visa", "documents", "processing_time", "requirements"],
        source="Japanese Embassy India Official Website",
        last_updated="2024-11-01",
        reliability_score=0.95,
    ),
    # VISA REQUIREMENTS - USA
    TravelDocument(
        id="visa_india_usa_001",
        title="USA Tourist Visa (B1/B2) Requirements for Indian Citizens",
        content="""
Indian citizens need a B1/B2 visa for tourism and business visits to the United States.

Required Documents:
- Valid passport (minimum 6 months validity beyond intended stay)
- DS-160 confirmation page with barcode
- Visa appointment confirmation letter
- Recent color photograph (2x2 inches, white background)
- Proof of financial ability (bank statements, property papers, ITR)
- Employment letter and salary slips (if employed)
- Business documents (if self-employed)
- Previous visa copies (if applicable)
- Travel itinerary and purpose of visit

Visa Interview: Mandatory at US Embassy/Consulate

Processing Time: 3-5 weeks on average
Visa Fee: $185 (approximately ₹15,000)
Visa Validity: Typically 10 years (multiple entry)
Maximum Stay: 180 days per visit

Application Process:
1. Complete DS-160 form online
2. Pay visa fee and schedule appointment
3. Gather supporting documents
4. Attend visa interview
5. Wait for passport with visa stamp

Important Notes:
- Visa does not guarantee entry; immigration officer has final say
- ESTA not available for Indian passport holders
- Strong ties to India (job, property, family) improve approval chances
- Sponsor documents required if sponsored by US resident
        """,
        category=TravelCategory.VISA_REQUIREMENTS,
        country="USA",
        source_country="India",
        tags=["B1_B2_visa", "interview", "documents", "fee"],
        source="US Embassy India",
        last_updated="2024-10-15",
        reliability_score=0.98,
    ),
    # VISA REQUIREMENTS - UK
    TravelDocument(
        id="visa_india_uk_001",
        title="UK Standard Visitor Visa Requirements for Indians",
        content="""
Indian nationals require a Standard Visitor visa to visit the UK for tourism, business, or visiting family/friends.

Required Documents:
- Current passport with blank page for visa
- Old passports (if any)
- Completed online application form
- Two recent color photographs
- Bank statements for last 6 months
- Salary slips (if employed) or business documents
- Income Tax Returns
- Hotel reservations and flight bookings
- Travel itinerary
- Invitation letter (if visiting someone)
- Sponsor documents (if applicable)

Processing Time: 3 weeks (standard), expedited options available
Visa Fee: £115 (approximately ₹12,000) for 6-month visa
Visa Validity Options: 6 months, 2 years, 5 years, 10 years
Maximum Stay: 180 days in any 12-month period

Application Process:
1. Complete online application on gov.uk
2. Pay visa fee online
3. Book biometric appointment at VFS Global
4. Submit documents and biometrics
5. Track application online
6. Receive decision by email

Important Notes:
- No interview typically required unless requested
- Health surcharge may apply for longer visas
- Show strong ties to India (employment, property, family)
- Maintain sufficient funds (£1,000-2,000 recommended minimum)
        """,
        category=TravelCategory.VISA_REQUIREMENTS,
        country="UK",
        source_country="India",
        tags=["standard_visitor", "biometrics", "processing", "fee"],
        source="UK Government Official Website",
        last_updated="2024-10-20",
        reliability_score=0.96,
    ),
    # VISA REQUIREMENTS - SCHENGEN
    TravelDocument(
        id="visa_india_schengen_001",
        title="Schengen Visa Requirements for Indian Citizens",
        content="""
Indian passport holders need a Schengen visa to visit 27 European countries in the Schengen Area.

Required Documents:
- Valid passport (minimum 3 months validity beyond intended stay, issued within last 10 years)
- Completed and signed visa application form
- Two recent passport-size photographs
- Travel health insurance (minimum €30,000 coverage)
- Round-trip flight reservation
- Hotel bookings or accommodation proof
- Bank statements for last 3-6 months
- Employment letter and salary slips
- ITR for last 2-3 years
- Cover letter explaining travel purpose
- Day-by-day travel itinerary

Processing Time: 15 calendar days (can extend to 30-45 days)
Visa Fee: €80 (approximately ₹7,500)
Visa Validity: Typically 90 days within 180-day period
Multiple Entry Options: Available based on travel history

Application Through: Embassy/Consulate of main destination country

Important Notes:
- Apply at least 15 days before travel (not more than 6 months in advance)
- Travel insurance mandatory - must cover all Schengen countries
- Sufficient funds: €50-60 per day recommended
- Enter through country that issued visa or main destination
- Can visit all 27 Schengen countries with single visa

Schengen Countries Include:
Austria, Belgium, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Italy, Latvia, Liechtenstein, Lithuania, Luxembourg, Malta, Netherlands, Norway, Poland, Portugal, Slovakia, Slovenia, Spain, Sweden, Switzerland, Romania, Bulgaria
        """,
        category=TravelCategory.VISA_REQUIREMENTS,
        country="Schengen Area",
        source_country="India",
        tags=["schengen", "europe", "travel_insurance", "multiple_entry"],
        source="Schengen Visa Official Information",
        last_updated="2024-11-05",
        reliability_score=0.97,
    ),
    # VISA REQUIREMENTS - DUBAI/UAE
    TravelDocument(
        id="visa_india_uae_001",
        title="UAE/Dubai Tourist Visa for Indian Citizens",
        content="""
Indian citizens can obtain a visa-on-arrival or e-visa for visiting UAE/Dubai.

Visa Options:
1. Visa on Arrival (96 hours) - Available at Dubai Airport
2. 30-day tourist visa
3. 60-day tourist visa

Required Documents:
- Valid passport (minimum 6 months validity)
- Return flight ticket
- Hotel booking confirmation
- Proof of sufficient funds
- Passport-size photograph
- Visa application form

For Visa on Arrival:
- Available for free to Indian passport holders holding US visa/Green Card or UK/EU residence
- Return ticket mandatory
- AED 100 fee for 14-day visa extension

E-Visa Application:
- Apply through official UAE government portal or airlines
- Processing: 3-5 working days
- Fee: AED 300-650 depending on duration

Important Notes:
- Visa on arrival NOT available for all Indian passport holders
- Must have valid US/UK/Schengen visa or residence permit
- Hotel booking confirmation required
- Minimum funds: $3,000-5,000 recommended
- Travel insurance recommended but not mandatory
        """,
        category=TravelCategory.VISA_REQUIREMENTS,
        country="UAE",
        source_country="India",
        tags=["visa_on_arrival", "e_visa", "dubai", "requirements"],
        source="UAE Government Portal",
        last_updated="2024-10-25",
        reliability_score=0.94,
    ),
    # LOCAL LAWS - JAPAN
    TravelDocument(
        id="laws_japan_001",
        title="Important Laws and Regulations in Japan for Tourists",
        content="""
Key Legal Points for Travelers in Japan:

Drug Laws:
- ZERO tolerance for drugs - even small amounts result in arrest and deportation
- Many over-the-counter medicines containing pseudoephedrine are illegal
- Prescription medications may need approval - carry doctor's letter
- Cannabis is strictly illegal (including CBD products)

Alcohol:
- Legal drinking age: 20 years
- Public drinking is allowed in most places
- No alcohol sales after 11 PM in some areas
- Drunk driving laws are extremely strict - zero tolerance

Public Behavior:
- Smoking only in designated areas (heavy fines for street smoking)
- Tattoos may restrict entry to hot springs, gyms, and pools
- Loud talking on trains is considered rude
- No eating while walking in some areas
- Taking photos may be restricted in certain shrines and temples

Photography Restrictions:
- Military installations - prohibited
- Some religious sites - ask permission first
- No upskirt photography (serious crime with jail time)
- Respect privacy in onsen (hot springs)

Other Important Laws:
- Always carry ID/passport or copy
- Jaywalking is illegal and enforced
- Littering carries fines
- Defacing property (including writing on walls) is serious crime
- Overstaying visa results in detention and deportation
- Using someone else's WiFi without permission is illegal

Emergency Numbers:
- Police: 110
- Ambulance/Fire: 119
- Tourist Helpline: 050-3816-2787 (English)

Penalties:
- Japanese prisons are strict with no special treatment for foreigners
- Deportation results in 5-10 year ban from re-entry
- Employers and embassy will be notified of arrests
        """,
        category=TravelCategory.LOCAL_LAWS,
        country="Japan",
        tags=["laws", "drugs", "alcohol", "public_behavior", "penalties"],
        source="Japan National Tourism Organization",
        last_updated="2024-09-15",
        reliability_score=0.96,
    ),
    # LOCAL LAWS - UAE
    TravelDocument(
        id="laws_uae_001",
        title="UAE/Dubai Laws and Regulations for Tourists",
        content="""
Critical Laws to Know in UAE/Dubai:

Dress Code:
- Modest dress required in public areas
- No revealing clothing in shopping malls, government buildings
- Swimwear only at beach/pool areas
- Cover shoulders and knees in religious sites
- Fines for indecent exposure: AED 1,000+

Alcohol Laws:
- Legal drinking age: 21 years
- Alcohol license required for residents (not tourists)
- Drinking only in licensed venues (hotels, restaurants, bars)
- Zero tolerance for drinking and driving - mandatory jail time
- Public intoxication is illegal - can result in arrest

Public Behavior:
- No public displays of affection (PDA) - holding hands OK, kissing can result in arrest
- Swearing and rude gestures are illegal
- Taking photos of people without permission is illegal
- No photos of government buildings, military installations, or palaces

Ramadan Restrictions:
- No eating, drinking, smoking in public during fasting hours
- Dress more conservatively
- Reduced business hours
- Respect prayer times

Serious Offenses:
- Drug possession: Mandatory 4-year minimum jail sentence
- Bouncing checks: Criminal offense with jail time
- Debt default: Can result in travel ban
- Adultery and extramarital sex: Illegal (jail + deportation)
- Homosexuality: Illegal
- Cohabitation without marriage: Illegal but rarely enforced for tourists

Social Media/Internet:
- VoIP calls (Skype, WhatsApp calls) may be blocked
- Posting offensive content online is punishable
- Criticism of government/royalty is serious crime
- Sharing someone's photo without consent is illegal

Other Important Points:
- Always carry ID/passport copy
- Friday is holy day - many businesses closed until afternoon
- No tolerance for disrespecting Islam or Emirati culture
- Jaywalking enforced with fines
- Littering: AED 500-1,000 fine

Emergency Numbers:
- Police: 999
- Ambulance: 998
- Tourist Police: 800-4888

Legal Help:
- Contact your embassy immediately if arrested
- Right to legal representation
- Do not sign documents you don't understand
        """,
        category=TravelCategory.LOCAL_LAWS,
        country="UAE",
        tags=["laws", "dress_code", "alcohol", "ramadan", "public_behavior"],
        source="UAE Government Legal Portal",
        last_updated="2024-10-10",
        reliability_score=0.97,
    ),
    # CULTURAL ETIQUETTE - JAPAN
    TravelDocument(
        id="culture_japan_001",
        title="Japanese Cultural Etiquette and Customs",
        content="""
Essential Japanese Cultural Practices for Visitors:

Greetings:
- Bow when greeting (deeper bow shows more respect)
- Remove shoes when entering homes, temples, some restaurants
- Exchange business cards with both hands
- Say "Itadakimasu" before meals, "Gochisousama" after

Dining Etiquette:
- Never stick chopsticks upright in rice (funeral ritual)
- Don't pass food chopstick to chopstick
- Slurping noodles is acceptable and shows appreciation
- Say itadakimasu before eating
- Don't walk while eating
- Finish everything on your plate
- Pour drinks for others, not yourself

Public Behavior:
- Keep voice down in public transportation
- No phone calls on trains
- Stand on left side of escalators (right in Osaka)
- Line up orderly and wait your turn
- Don't blow nose in public (go to restroom)
- Cover mouth when using toothpick

Tipping:
- NO TIPPING in Japan - considered rude
- Service charge included in bill
- Exceptional service is standard expectation

Gift Giving:
- Bring small gifts (omiyage) when visiting someone
- Present and receive gifts with both hands
- Don't open gifts immediately
- Wrap gifts nicely (wrapping is important)
- Avoid sets of 4 or 9 (unlucky numbers)

Onsen (Hot Springs) Etiquette:
- Wash thoroughly before entering bath
- No swimsuits - bathing naked is mandatory
- Tattoos may not be allowed (check beforehand)
- Tie up long hair
- No towel in the water
- Rinse off before returning to changing area

Temple/Shrine Etiquette:
- Bow before entering torii gate
- Wash hands at purification fountain
- Photography may be restricted - check signs
- Don't touch artifacts or statues
- Quiet and respectful behavior required
- Appropriate dress (covered shoulders/knees)

Social Interactions:
- Punctuality is extremely important
- Avoid physical contact (no hugging)
- Don't point with finger (use whole hand)
- Remove hat indoors
- Respect personal space
- Learn a few Japanese phrases (greatly appreciated)

Useful Phrases:
- Arigatou gozaimasu (Thank you)
- Sumimasen (Excuse me/Sorry)
- Konnichiwa (Hello)
- Sayonara (Goodbye)
        """,
        category=TravelCategory.CULTURAL_ETIQUETTE,
        country="Japan",
        tags=["culture", "etiquette", "manners", "customs", "onsen"],
        source="Japan National Tourism Organization",
        last_updated="2024-09-01",
        reliability_score=0.95,
    ),
    # CULTURAL ETIQUETTE - UAE
    TravelDocument(
        id="culture_uae_001",
        title="UAE Cultural Etiquette and Islamic Customs",
        content="""
Cultural Practices and Etiquette in UAE:

Greetings:
- Use right hand for handshakes
- Men should wait for women to extend hand first
- "As-salamu alaykum" (Peace be upon you) is respectful greeting
- Avoid physical contact with opposite gender

Dress Code:
- Dress modestly - cover shoulders and knees
- Women: avoid tight or see-through clothing
- Men: no shorts in formal settings
- More conservative dress in Sharjah and Ajman
- Beachwear only at beaches/pools
- Religious sites require conservative dress

Dining Etiquette:
- Use right hand for eating (left hand is unclean)
- Remove shoes if dining on floor
- Finish food on plate (wasting food is disrespectful)
- Don't eat pork or discuss it
- During Ramadan: no eating/drinking in public during fasting hours

Social Interactions:
- Don't point feet at people (sign of disrespect)
- Don't show soles of feet
- Photography: ask permission before photographing people (especially women)
- Avoid discussing politics, religion, or criticizing royal family
- Respect prayer times (5 times daily)
- Friday is holy day (like Sunday in West)

Business Etiquette:
- Punctuality expected but meetings may start late
- Business cards with Arabic translation appreciated
- Don't schedule meetings during prayer times
- Accept coffee/tea when offered (rude to refuse)
- Business relationships built on personal trust

Ramadan Considerations:
- No eating, drinking, smoking in public during daylight
- Reduced working hours
- Many restaurants closed during day
- Be extra respectful
- Check business hours (many operate night schedule)

Gender Interactions:
- Avoid being alone with opposite gender if not married
- Public display of affection is illegal
- Men should not approach or photograph Emirati women
- Segregated areas in some public places

Religious Respect:
- Don't criticize Islam or make jokes about religion
- Dress conservatively near mosques
- Non-Muslims can visit some mosques (Jumeirah Mosque in Dubai)
- Remove shoes before entering mosques
- Women may need to cover head in mosques

Alcohol:
- Only consume in licensed venues
- Never drink and drive (zero tolerance)
- Don't be drunk in public
- Cannot purchase alcohol from stores without license (residents only)

Gift Giving:
- Gifts appreciated but not expected
- Avoid alcohol, pork products, or items with dogs
- Give and receive with right hand
- High-quality chocolates, dates, or perfumes are good options

Important Don'ts:
- Don't use left hand for giving/receiving
- Don't cross legs showing sole of shoe
- Don't interrupt prayer or walk in front of someone praying
- Don't take photos of government buildings or palaces
- Don't raise voice or show anger publicly

Useful Arabic Phrases:
- Shukran (Thank you)
- Marhaba (Hello)
- Min fadlak/fadlik (Please)
- Ma'a salama (Goodbye)
        """,
        category=TravelCategory.CULTURAL_ETIQUETTE,
        country="UAE",
        tags=["culture", "islam", "etiquette", "ramadan", "customs"],
        source="UAE Tourism Authority",
        last_updated="2024-10-05",
        reliability_score=0.96,
    ),
    # SAFETY - JAPAN
    TravelDocument(
        id="safety_japan_001",
        title="Safety Guidelines and Emergency Information for Japan",
        content="""
Safety Information for Travelers in Japan:

General Safety:
- Japan is one of the safest countries in the world
- Violent crime against tourists is extremely rare
- Petty theft is uncommon but can occur
- Keep valuables secure in tourist areas
- Lost items often returned to police or lost & found

Natural Disasters:
- Earthquakes common but buildings are earthquake-proof
- Typhoon season: June to October
- Heavy snow in northern regions in winter
- Tsunami risk in coastal areas
- Download disaster apps: Safety Tips, Japan Official Travel App

Earthquake Safety:
- Drop, Cover, Hold On during shaking
- Stay away from windows and heavy furniture
- Don't rush outside during shaking
- Follow evacuation signs (green emergency exits)
- Designated evacuation areas in each district
- Keep emergency bag with water, food, flashlight

Health & Medical:
- Excellent healthcare but expensive
- Travel insurance highly recommended
- Prescription medications require permission
- English-speaking doctors in major cities
- Hospitals: Tokyo Medical & Surgical Clinic, St. Luke's International
- Ambulance: 119 (free service)

Transportation Safety:
- Trains and buses extremely safe and punctual
- Watch for pickpockets during rush hour
- Stand clear of platform edge (suicide incidents rare but occur)
- Taxis are safe but expensive
- Traffic drives on left side

Emergency Contacts:
- Police: 110
- Ambulance/Fire: 119
- Japan Helpline (24/7 English): 0570-000-911
- Tourist Information Center: +81-50-3816-2787
- Your Embassy Contact

Scams to Avoid:
- Bar/Club scams (especially Roppongi, Kabukicho)
- Massage parlor overcharging
- "Free" guide services (may lead to shops)
- Fake monks asking for donations
- Overpriced taxis at airports (use legitimate taxi stands)

Women Safety:
- Generally very safe for solo female travelers
- Women-only train cars available during rush hour (pink signs)
- Avoid walking alone late night in entertainment districts
- Groping (chikan) can occur on crowded trains - report immediately
- Stay in well-lit areas at night

Areas Requiring Caution:
- Kabukicho (Tokyo's red-light district) late at night
- Roppongi nightlife area
- Dotonbori (Osaka) late night can be rowdy
- Avoid yakuza (Japanese mafia) - identifiable by tattoos and sharp suits

Cyber Safety:
- Use secure WiFi networks
- Be careful with public WiFi
- Keep phone charged (power banks useful)
- Download offline maps

Food Safety:
- Food safety standards are excellent
- Tap water is safe to drink
- Raw fish is safe to eat
- Food poisoning is rare

Radiation Safety (Post-Fukushima):
- Tokyo and major cities are completely safe
- Avoid restricted zones around Fukushima plant
- Food products are strictly tested

Important Apps:
- Safety Tips (earthquake/tsunami alerts)
- Japan Official Travel App
- Google Translate (offline mode)
- Hyperdia (train schedules)
- Google Maps (works well in Japan)

Travel Insurance:
- Essential for medical emergencies
- Cover earthquake/natural disasters
- Evacuation coverage recommended
- Lost luggage coverage
        """,
        category=TravelCategory.SAFETY_GUIDELINES,
        country="Japan",
        tags=["safety", "emergency", "earthquake", "health", "disasters"],
        source="Japan Tourism Agency & Travel Safety",
        last_updated="2024-09-20",
        reliability_score=0.97,
    ),
    # ========== INDIA TRAVEL DOCUMENTS (FOR FOREIGNERS) ==========
    # VISA REQUIREMENTS - INDIA (for US Citizens)
    TravelDocument(
        id="visa_to_india_usa_001",
        title="India e-Visa and Tourist Visa Requirements for US Citizens",
        content="""
US citizens need a visa to visit India for tourism, business, or medical purposes.

E-Visa Options (Most Popular):
1. e-Tourist Visa (30 days, 1 year, or 5 years validity)
2. e-Business Visa (1 year validity)
3. e-Medical Visa (60 days validity)

Required Documents for e-Tourist Visa:
- Valid US passport (minimum 6 months validity from arrival date)
- Recent passport-size color photograph (white background)
- Scanned copy of passport bio page
- Confirmed return flight ticket
- Hotel bookings or address in India
- Credit/debit card for online payment
- Email address for visa communication

E-Visa Processing:
- Apply online at: https://indianvisaonline.gov.in/evisa/
- Apply at least 4 days before travel (up to 120 days in advance)
- Processing time: 3-5 business days
- Visa sent via email (print and carry)
- Entry allowed through 28 designated airports and 5 seaports

E-Tourist Visa Fees (for US Citizens):
- 30-day visa (April-June): $10
- 30-day visa (July-March): $25
- 1-year multiple entry: $40
- 5-year multiple entry: $80

Stay Duration:
- 30-day visa: Continuous stay up to 30 days
- 1-year visa: Multiple entries, max 90 days per visit
- 5-year visa: Multiple entries, max 90 days per visit

Traditional Tourist Visa (Embassy/Consulate):
Required for:
- Stays longer than 90 days
- Visiting restricted/protected areas
- Work or study purposes
- Journalism or research

Processing Time: 7-10 business days
Fees: $100-160 depending on duration
Validity: Up to 10 years (multiple entry)

Important Notes:
- No visa on arrival for US citizens
- E-visa cannot be extended (must leave and reapply)
- Registration required if staying more than 180 days
- Pakistan/Bangladesh border crossings not allowed with e-visa
- Protected areas (Sikkim, Ladakh, etc.) need special permits
- Yellow fever vaccination certificate required if coming from endemic countries

Useful Links:
- Official e-Visa portal: https://indianvisaonline.gov.in/evisa/
- Indian Embassy USA: https://www.indiainnewyork.gov.in/
        """,
        category=TravelCategory.VISA_REQUIREMENTS,
        country="India",
        source_country="USA",
        tags=["e_visa", "tourist_visa", "online_application", "requirements"],
        source="Indian Ministry of External Affairs",
        last_updated="2024-11-15",
        reliability_score=0.98,
    ),
    # VISA REQUIREMENTS - INDIA (for UK Citizens)
    TravelDocument(
        id="visa_to_india_uk_001",
        title="India e-Visa Requirements for UK Citizens",
        content="""
UK citizens require a visa to travel to India. The e-Visa is the most convenient option.

E-Visa Categories:
1. e-Tourist Visa (30 days to 5 years)
2. e-Business Visa (1 year)
3. e-Medical Visa (60 days)
4. e-Conference Visa (120 days)

Required Documents:
- Valid UK passport (6+ months validity)
- Digital passport-size photo (white background, 350x350 pixels)
- Passport bio page scan (PDF format)
- Return flight booking
- Accommodation proof (hotel or host address)
- Payment card (Visa/Mastercard)

E-Tourist Visa Fees for UK Citizens:
- 30-day single entry (April-June): £8
- 30-day single entry (July-March): £20
- 1-year multiple entry: £32
- 5-year multiple entry: £64

Application Process:
1. Apply online at https://indianvisaonline.gov.in/evisa/
2. Fill application form (15-20 minutes)
3. Upload documents (photo and passport scan)
4. Pay visa fee online
5. Receive ETA (Electronic Travel Authorization) via email
6. Print and carry ETA with you

Processing Time: 3-5 business days
Apply: Minimum 4 days before travel, maximum 120 days

Entry Points for E-Visa Holders:
- 28 designated airports including Delhi, Mumbai, Chennai, Bangalore, Kolkata
- 5 seaports including Mumbai, Cochin, Goa
- Exit allowed from any immigration checkpoint

Stay Restrictions:
- 30-day visa: Max 30 days continuous stay
- 1-year visa: Multiple entries, max 90 days per visit
- 5-year visa: Multiple entries, max 90 days per visit

Important Notes:
- E-visa cannot be extended
- Not valid for restricted/protected areas without additional permits
- Regular visa required for journalism, research, or long-term stay
- Check passport has at least 2 blank pages
- Carry printout of e-visa approval

Traditional Visa (VFS/Consulate):
- For stays over 90 days
- For work, study, or special purposes
- Processing: 7-15 working days
- Fees: £104-£150
- Validity: Up to 10 years

Protected Areas Requiring Special Permits:
- Parts of Sikkim, Ladakh, Arunachal Pradesh, Andaman Islands
- Apply through Indian mission or local authorities

Useful Information:
- Indian High Commission UK: https://www.hcilondon.gov.in/
- E-visa portal: https://indianvisaonline.gov.in/evisa/
        """,
        category=TravelCategory.VISA_REQUIREMENTS,
        country="India",
        source_country="UK",
        tags=["e_visa", "uk_citizens", "tourist_visa", "online"],
        source="Indian High Commission UK",
        last_updated="2024-11-10",
        reliability_score=0.97,
    ),
    # LOCAL LAWS - INDIA
    TravelDocument(
        id="laws_india_001",
        title="Important Laws and Regulations in India for Tourists",
        content="""
Key Legal Points for Foreign Travelers in India:

Drug Laws:
- Strict drug laws with severe penalties
- Possession of even small amounts: 6 months to 10 years imprisonment
- Cannabis illegal in most states (legal in some parts of Himachal Pradesh)
- Death penalty possible for large quantities
- Foreign nationals subject to same laws

Alcohol Laws:
- Legal drinking age: 18-25 years (varies by state)
- Alcohol banned in Gujarat, Bihar, Nagaland, and parts of other states
- Dry days on national holidays and election days
- Public drinking illegal - drink only in licensed premises
- Drunk driving: Heavy fines and possible imprisonment
- Carry alcohol across state borders may be restricted

Photography Restrictions:
- No photography of military installations, airports, bridges
- Tribal areas may restrict photography
- Ask permission before photographing people (especially women)
- Some religious sites prohibit photography
- Drones require special permission

Public Behavior:
- Public displays of affection discouraged (holding hands usually OK)
- Kissing in public can lead to arrest in some places
- Modest dress recommended, especially at religious sites
- Remove shoes before entering temples, mosques, and homes
- Respect religious sentiments - avoid beef in Hindu areas, pork near Muslim areas

Currency Laws:
- Bringing in/taking out more than $5,000 cash requires declaration
- Indian Rupees: Can bring up to ₹25,000; export up to ₹25,000
- Foreign exchange receipts should be preserved
- Currency exchange only through authorized dealers

Drone Laws:
- Drones require DGCA permission
- Heavy penalties for unauthorized drone use
- Registration mandatory for all drones
- No-fly zones around airports, military areas, government buildings

Wildlife Protection:
- Strict laws protecting endangered species
- No purchase of ivory, tiger/leopard products, shahtoosh shawls
- Heavy fines and imprisonment for wildlife trade
- No feeding or disturbing wildlife in national parks

Archaeological Sites:
- No removal of artifacts or stones from heritage sites
- Damaging monuments: Imprisonment up to 2 years + fine
- Follow Archaeological Survey of India (ASI) guidelines

Visa Overstay:
- Heavy fines for overstaying visa
- Possible deportation and re-entry ban
- Register with FRRO if staying more than 180 days
- Keep visa documents and passport safe

Women's Safety Laws:
- Eve-teasing (harassment) is illegal
- Report incidents to women's helpline: 1091
- Special women's police stations in major cities

Customs Regulations:
- Gold jewelry: Max 20g for women, 10g for men duty-free
- Liquor: 2 liters duty-free
- Cigarettes: 200 cigarettes or 50 cigars duty-free
- Declare items worth more than $1,500

Cybercrime Laws:
- Strict IT Act penalties for cyber offenses
- No posting offensive content about religion or government
- Revenge porn illegal with severe penalties

Emergency Numbers:
- Police: 100
- Ambulance: 102
- Fire: 101
- Women's Helpline: 1091
- Tourist Helpline: 1363/1800-111-363
- National Emergency: 112

Registration Requirements:
- Register with FRRO/FRO if staying more than 180 days
- Required for employment, research, study visas
- Online registration: https://indianfrro.gov.in/

Important Don'ts:
- Don't carry or consume beef in some states (illegal in several states)
- Don't disrespect national symbols (flag, anthem, currency)
- Don't purchase antiquities without proper certification
- Don't engage in missionary activities on tourist visa
- Don't overstay your visa

Legal Assistance:
- Contact your embassy/consulate if arrested
- Right to legal representation
- Police must inform embassy of arrest
- Bail may be difficult for foreign nationals
        """,
        category=TravelCategory.LOCAL_LAWS,
        country="India",
        tags=["laws", "regulations", "drugs", "alcohol", "visa", "customs"],
        source="Indian Government Legal Information",
        last_updated="2024-10-28",
        reliability_score=0.96,
    ),
    # CULTURAL ETIQUETTE - INDIA
    TravelDocument(
        id="culture_india_001",
        title="Indian Cultural Etiquette and Customs for Visitors",
        content="""
Essential Cultural Practices and Etiquette in India:

Greetings:
- Namaste (hands pressed together, slight bow) is universal greeting
- Handshakes common in business, but ask before shaking hands with women
- Address elders with "ji" suffix (e.g., "Sharma ji")
- Remove shoes before entering homes and religious places
- Touch elder's feet as sign of respect (if invited to do so)

Religious Etiquette:
- Dress modestly at religious sites (covered shoulders, knees)
- Cover head in Sikh gurudwaras (scarves provided)
- Remove shoes before entering temples, mosques, gurudwaras
- Don't touch idols or religious artifacts
- Walk clockwise around shrines
- No leather items in some temples (especially Jain temples)
- Menstruating women may be restricted from some temples
- Ask before taking photos in religious places
- Maintain silence in prayer areas

Dining Etiquette:
- Wash hands before and after meals
- Eat with right hand only (left hand considered unclean)
- Wait to be served, don't start eating before elders
- Finish all food on plate (wasting food is disrespectful)
- Don't touch communal food with used utensils
- Burping after meal may be seen as compliment
- Many Indians are vegetarian - respect dietary restrictions
- Avoid beef (sacred animal for Hindus) and pork near Muslim areas

Dress Code:
- Dress modestly, especially in rural areas and religious sites
- Women: Cover shoulders and knees; avoid tight or revealing clothes
- Men: Avoid shorts and sleeveless shirts at religious sites
- Beachwear only at beaches (not in towns)
- Remove shoes when entering homes
- Conservative dress shows respect

Social Interactions:
- Personal space is limited - crowds are common
- Avoid public displays of affection (PDA)
- Same-sex friends holding hands is normal and non-romantic
- Don't point feet at people or religious objects
- Don't touch others' heads (considered sacred)
- Use right hand for giving/receiving items
- Bargaining expected in markets (not in fixed-price stores)

Communication:
- Indians may avoid saying "no" directly (watch for indirect refusals)
- Head wobble (side-to-side) usually means "yes" or acknowledgment
- Personal questions about age, salary, marital status are normal
- Maintain respectful tone with elders
- "Yes" doesn't always mean agreement (may mean "I heard you")

Tipping:
- Restaurants: 10% if service charge not included
- Hotel porters: ₹50-100 per bag
- Taxi drivers: Round up fare
- Tour guides: ₹200-500 per day
- Not mandatory but appreciated

Gender Etiquette:
- Men should avoid touching women or excessive eye contact
- Women traveling alone should dress conservatively
- Sit in back seat of taxis/ride-shares
- Avoid empty train compartments
- Women-only metro/train cars available

Gift Giving:
- Bring small gifts if invited to someone's home (sweets, flowers, dry fruits)
- Avoid leather products for Hindus
- Avoid alcohol/beef products for religious families
- Present and receive with both hands or right hand only
- Gifts opened in private, not immediately

Festival Etiquette:
- Participate respectfully if invited
- Ask before taking photos during ceremonies
- Accept prasad (blessed food) with right hand
- Holi: Ask permission before applying colors
- Diwali: Respect noise levels and firecracker timings

Business Etiquette:
- Punctuality appreciated but flexibility expected
- Exchange business cards with both hands
- Build personal relationship before business discussion
- Hierarchy is important - address senior person first
- Tea/coffee will be offered - accept graciously
- Decisions may take time (consensus-based culture)

Bargaining:
- Expected in local markets, street vendors
- Start at 40-50% of asking price
- Be polite and friendly while negotiating
- Fixed prices in malls, branded stores, restaurants
- Don't bargain with auto-rickshaws using meters

Photography:
- Always ask permission before photographing people
- Especially important with women, children, tribal people
- Don't photograph military installations, airports
- Some areas charge camera fees at tourist sites
- Respect "No Photography" signs

Temple Offerings:
- Prasad (blessed food): Accept with right hand, eat or keep respectfully
- Can offer flowers, coconuts, money at temples
- Follow priest's instructions during ceremonies

Useful Hindi Phrases:
- Namaste - Hello/Goodbye
- Dhanyavaad - Thank you
- Kripaya - Please
- Haan - Yes
- Nahi - No
- Kitna? - How much?
- Maaf kijiye - Excuse me/Sorry

Regional Variations:
- North India: More conservative, hierarchical
- South India: Traditional, modest dress important
- Northeast: Different customs, more relaxed about alcohol
- Goa: More liberal, Western-friendly
- Tribal areas: Specific customs vary, ask local guide

Important Don'ts:
- Don't kiss or hug in public
- Don't use left hand for eating or giving
- Don't point with single finger (use full hand)
- Don't show soles of feet
- Don't touch someone's head
- Don't whistle indoors (considered rude)
- Don't step over people
- Don't waste food
- Don't criticize India or Indian customs
- Don't assume all Indians speak Hindi (many speak regional languages)

Cultural Sensitivity:
- Respect caste system (even if you disagree)
- Be patient with bureaucracy and delays
- Learn about local customs before visiting
- Show respect to all religions
- Understand "Indian Standard Time" (delays are common)
        """,
        category=TravelCategory.CULTURAL_ETIQUETTE,
        country="India",
        tags=["culture", "etiquette", "customs", "religion", "social_norms"],
        source="India Tourism & Cultural Studies",
        last_updated="2024-11-01",
        reliability_score=0.98,
    ),
    # SAFETY GUIDELINES - INDIA
    TravelDocument(
        id="safety_india_001",
        title="Safety Guidelines and Travel Tips for India",
        content="""
Comprehensive Safety Information for Travelers in India:

General Safety:
- India is generally safe but requires vigilance
- Tourist areas are well-monitored
- Violent crime against tourists is relatively low
- Petty theft, scams, and harassment can occur
- Stay alert in crowded places

Women's Safety:
- Solo female travel possible but requires extra caution
- Dress conservatively (covered shoulders, knees)
- Avoid traveling alone at night
- Use registered taxis or ride-hailing apps (Uber, Ola)
- Sit in back seat of taxis, ideally with door locked
- Avoid empty train compartments - use women's coaches
- Trust instincts - leave if situation feels uncomfortable
- Women's Helpline: 1091 (24/7)
- Save emergency contacts and embassy numbers

Transportation Safety:
- Use licensed taxis or ride-hailing apps (Uber, Ola, Rapido)
- Avoid unmarked taxis at airports/stations
- Pre-book airport transfers through hotel
- Train travel generally safe - book reserved seats
- Don't accept food/drinks from strangers on trains
- Keep valuables chained to berth in sleeper trains
- Metro systems in major cities are safe and clean
- Traffic is chaotic - be extremely careful crossing roads

Health & Hygiene:
- Only drink bottled water (check seal is intact)
- Avoid ice in drinks
- Eat at busy, clean restaurants (high turnover = fresh food)
- Wash hands frequently or use hand sanitizer
- Avoid street food initially (let stomach adjust)
- Don't eat cut fruits from street vendors
- Peel fruits yourself
- Get travel insurance with medical coverage
- Vaccinations recommended: Hepatitis A/B, Typhoid, Tetanus

Common Health Issues:
- Delhi belly (traveler's diarrhea): Carry Imodium, ORS
- Heat exhaustion: Stay hydrated, use sunscreen
- Mosquito-borne diseases: Use repellent, sleep under nets
- Air pollution in cities: Carry masks (N95)
- Altitude sickness in Himalayas: Acclimatize gradually

Medical Facilities:
- Good hospitals in major cities (Apollo, Fortis, Max)
- Rural areas have limited facilities
- Carry basic first-aid kit
- Medical tourism destination - quality care available
- Pharmacies widely available
- Emergency: 102 (ambulance)

Scams to Avoid:
- Taxi overcharging at airports (use prepaid taxi counters)
- "Free" tour guides leading to commission shops
- Gem scams (buying gems to "export")
- Fake tickets at railway stations
- Overpriced official-looking tours
- Shoe-keeper scams at temples (unofficial fee collectors)
- "Closed today" scams (touts claim attraction closed, offer alternative)
- Credit card skimming (watch card at all times)
- Drugged food/drinks (don't accept from strangers)

Money Safety:
- Use hotel safe for valuables
- Carry money in multiple places (money belt, hidden pocket)
- Avoid flashing cash or expensive jewelry
- Use ATMs inside banks during day
- Cover PIN when using ATM
- Inform bank of India travel (avoid card blocking)
- Carry emergency cash in USD (widely accepted for exchange)
- Keep photocopies of passport, visa, cards separately

Cyber Safety:
- Use VPN on public WiFi
- Don't access banking on public networks
- Be cautious of SIM card registration (requires ID)
- Hotel WiFi usually safer than public hotspots

Natural Hazards:
- Monsoon floods (June-September): Check weather, avoid flood-prone areas
- Earthquakes: Possible in Himalayas
- Cyclones: East coast during monsoon
- Extreme heat (April-June): Stay hydrated, avoid midday sun
- Landslides: Hilly areas during monsoon

Areas Requiring Caution:
- Kashmir Valley: Check travel advisories
- Northeastern states: Some require permits, check current situation
- Naxalite-affected areas in central India
- Border areas with Pakistan
- Avoid political demonstrations and large gatherings

Emergency Contacts:
- All Emergencies: 112
- Police: 100
- Ambulance: 102
- Fire: 101
- Women's Helpline: 1091
- Tourist Helpline: 1363 or 1800-111-363
- Delhi Tourism: +91-11-2336-5358

What to Carry:
- Photocopy of passport and visa (keep separate from original)
- Emergency contacts list
- Travel insurance details
- Prescription medicines in original packaging
- Doctor's prescription for medications
- Basic first-aid kit
- Hand sanitizer and wet wipes
- Sunscreen and insect repellent
- Rehydration salts (ORS)
- Water purification tablets
- Flashlight/headlamp
- Power bank for phone

Important Apps:
- Emergency SOS: Emergency contacts and location
- Google Maps: Navigation (download offline maps)
- Uber/Ola: Ride-hailing
- IRCTC: Train bookings
- MakeMyTrip/Goibibo: Travel bookings
- Google Translate: Language help
- Zomato/Swiggy: Food delivery and restaurant info
- Air Quality Index app: Check pollution levels

Food Safety:
- Stick to bottled water (brands: Bisleri, Kinley, Aquafina)
- Avoid unpasteurized dairy
- Choose busy restaurants (high turnover)
- Cooked hot food safer than cold buffets
- Be careful with meat (vegetarian food often safer)
- Wash hands before eating
- Carry hand sanitizer

Night Safety:
- Return to accommodation before late night
- Use well-lit main streets
- Pre-book taxis rather than hailing on street
- Stay in groups if possible
- Avoid deserted areas and beaches at night
- Keep hotel/hostel contact info handy

Solo Travel Tips:
- Tell someone your itinerary
- Check in regularly with family/friends
- Join group tours for certain activities
- Choose accommodation in safe neighborhoods
- Read recent reviews of hotels/hostels
- Trust instincts - change plans if uncomfortable

Police and Legal:
- Police may ask for ID - carry passport copy
- Right to contact embassy if arrested
- Corruption exists - don't offer bribes
- Get police report for insurance claims (theft, etc.)
- Some police may not speak English - be patient

Travel Insurance:
- Essential for India travel
- Cover medical emergencies and evacuation
- Include adventure activities if trekking/adventure sports
- Lost luggage coverage
- Trip cancellation coverage
- 24/7 assistance hotline

Registration:
- Register with FRRO if staying 180+ days
- Keep visa documentation safe
- Inform hotel of extended stays

Cultural Safety:
- Respect local customs to avoid confrontation
- Be sensitive about religion and politics
- Don't photograph without permission
- Avoid sensitive topics in conversation

Specific City Safety:
- Delhi: Watch for pickpockets in Old Delhi, Chandni Chowk
- Mumbai: Safe but crowded; watch belongings in trains
- Goa: Beach safety, avoid drugs, watch drinks in parties
- Varanasi: Aggressive touts, watch belongings
- Jaipur: Tourist scams, commission agents
- Agra: Aggressive touts near Taj Mahal

Wildlife Safety:
- Maintain distance from wild animals
- Follow guide instructions in national parks
- Don't feed monkeys (can be aggressive)
- Avoid disturbing dogs (rabies risk)
- Elephant/tiger areas: Stay in vehicle

Trekking Safety:
- Use registered guides for Himalayan treks
- Acclimatize properly for high altitude
- Check weather conditions
- Inform someone of trek plans
- Carry emergency supplies
- Altitude sickness can be fatal - descend if symptoms occur

Useful Contacts:
- Your Embassy/Consulate
- Hotel/Hostel 24hr reception
- Travel agent/tour company
- Credit card emergency numbers
- Travel insurance 24hr helpline

COVID-19 Considerations (if applicable):
- Check current entry requirements
- Carry masks and sanitizer
- Follow local COVID guidelines
- Have vaccination certificates ready

General Advice:
- Stay aware of surroundings
- Don't trust everyone (healthy skepticism)
- Learn few words of Hindi/local language
- Be patient - things work differently in India
- Enjoy the chaos - it's part of the experience!
- Connect with other travelers for tips
- Research before going to new areas
- Keep emergency cash hidden
- Stay hydrated in heat
- Respect local culture and you'll be respected
        """,
        category=TravelCategory.SAFETY_GUIDELINES,
        country="India",
        tags=[
            "safety",
            "health",
            "scams",
            "emergency",
            "women_safety",
            "transportation",
        ],
        source="India Tourism & Travel Safety Resources",
        last_updated="2024-11-20",
        reliability_score=0.97,
    ),
]


def get_all_documents() -> list[TravelDocument]:
    """Get all travel documents."""
    return TRAVEL_DOCUMENTS


def get_documents_by_category(category: TravelCategory) -> list[TravelDocument]:
    """Get documents filtered by category."""
    return [doc for doc in TRAVEL_DOCUMENTS if doc.category == category]


def get_documents_by_country(country: str) -> list[TravelDocument]:
    """Get documents filtered by country."""
    return [
        doc
        for doc in TRAVEL_DOCUMENTS
        if doc.country and doc.country.lower() == country.lower()
    ]


def get_document_by_id(doc_id: str) -> TravelDocument | None:
    """Get a specific document by ID."""
    for doc in TRAVEL_DOCUMENTS:
        if doc.id == doc_id:
            return doc
    return None
