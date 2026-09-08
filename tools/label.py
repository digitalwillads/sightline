"""Hand-read angle labels (index -> angle) for each brand's creative clusters,
plus the positioning read. This is the layer the product's model performs."""
LABELS={
'huel.com':{
 'A':'No prep, no cooking','B':'Protein load','C':'Small change that sticks','D':'Calorie control',
 'E':'Beats the 3pm crash','F':'Complete nutrition','G':'Cost per meal','H':'GLP-1 support','I':'Taste and proof',
 'map':{ 'No prep, no cooking':(40,66),'Protein load':(62,60),'Small change that sticks':(36,38),
         'Calorie control':(50,72),'Beats the 3pm crash':(30,52),'Complete nutrition':(66,74),
         'Cost per meal':(20,68),'GLP-1 support':(72,66),'Taste and proof':(45,28) },
 'gap':(79,20),
 'note':("Huel argues almost entirely in the rational half: grams, minutes, calories and euros. "
         "Only two live ads reach for taste or feeling. The premium emotional corner, the food that "
         "says something about who you are, is empty."),
 'seq':'CCACEEBBBABHIFABAGEHBAFAGDCDDCAFECABCBACCGIC',
 'winners':[0,4,6],
 'why':["It asks for one meal, not a lifestyle. The switch is small enough that the objection never forms.",
        "It names a time, 3pm, and a failure the reader already felt today.",
        "Five variants still running after eight months. Huel keeps rebuilding this one instead of replacing it."],
},
'specsavers.ie':{
 'A':'Free check offer','B':'Booking prompt','C':'Service range','D':'Style and range',
 'E':'Problem agitation','F':'Brand purpose',
 'map':{ 'Free check offer':(22,64),'Booking prompt':(38,72),'Service range':(56,68),
         'Style and range':(64,32),'Problem agitation':(34,44),'Brand purpose':(52,22) },
 'gap':(78,26),
 'note':("Nearly every live ad is the same sentence: book, and the check is free. Price and access carry "
         "the whole account. Nothing in the set argues that better sight is worth paying more for, so the "
         "premium end is unclaimed."),
 'seq':'AABCBDCDAAAAEAF',
 'winners':[0,2,13],
 'why':["Free removes the only real objection to an appointment nobody schedules on their own.",
        "Five variants of four words. The ad is the button.",
        "Seventeen variants in five weeks. They are hunting the exact wording of a free entitlement."],
},
'layahealthcare.ie':{
 'A':'Clinic network','B':'Peace of mind','C':'Speed to cover','D':'Price anchoring',
 'E':'Discount','F':'Product range','G':'Choice and control',
 'map':{ 'Clinic network':(58,60),'Peace of mind':(46,26),'Speed to cover':(40,68),
         'Price anchoring':(22,66),'Discount':(18,74),'Product range':(54,72),'Choice and control':(64,44) },
 'gap':(76,24),
 'note':("Laya splits its money between a price message and a fear message, and runs them from separate "
         "creative families. Nothing joins the two. The premium emotional corner, insurance as something "
         "you are proud to hold, is open."),
 'seq':'AAAAABBCDECDEBBFEDGF',
 'winners':[0,5,10],
 'why':["One ad per clinic location, all running since July. The network is the product.",
        "Four words that name the fear without saying the word insurance.",
        "Quote to cover in minutes. It sells the paperwork disappearing, not the cover."],
},
}


# What each angle is actually arguing. This is the read, not the data.
NOTES = {'huel.com': {'No prep, no cooking': 'Time is the product. Every ad here counts minutes back — ready in five, just add water, no pan. None of them argues the food is better, only that it costs you nothing to make.', 'Protein load': 'A number does the persuading. 40g, 25g, 26 vitamins. Aimed at people who already track intake, so the ad never explains why protein matters. It just posts the figure.', 'Small change that sticks': "The lowest-commitment ask in the set. Don't change your life, change lunch. It works by shrinking the decision until refusing it looks unreasonable.", 'Calorie control': 'Restriction without the misery. These concede that dieting is unpleasant, then position the product as the part you no longer have to think about.', 'Beats the 3pm crash': 'The only group that names a moment. Hungry again by three, the desk lunch that failed. Specific enough that the reader checks their own afternoon.', 'Complete nutrition': 'The defensive argument. Convenient food usually cuts corners; this says theirs does not. It answers an objection rather than making a promise.', 'GLP-1 support': 'The newest land grab. Appetite drops on a GLP-1 and protein goes with it. Three live ads is a test rather than a commitment, but it is the only group aimed at a condition.', 'Cost per meal': 'Price framed per meal, never per bag. €2.30 against a bought lunch, so the reader is spending money they were spending anyway.', 'Taste and proof': "Almost nothing. Two ads out of 62 mention flavour or a customer's own words. For a food brand that is a deliberate omission, and an obvious gap."}, 'specsavers.ie': {'Free check offer': 'Two thirds of the account is one sentence: the check costs nothing. Free removes the only real objection to an appointment nobody schedules on their own.', 'Booking prompt': 'No argument at all. Book an eye test. These run on recognition, and they only work because everyone already knows the name.', 'Service range': 'The quiet upsell. Wax removal, prescription safety eyewear. Aimed at people who assume the shop only does glasses.', 'Style and range': 'The only ads selling how you look rather than when you can come in. Both are eyewear ranges, not the test.', 'Problem agitation': 'One ad naming what you are missing: the punchline, the dialogue, the sound you did not catch. The only creative that makes the reader feel the problem.', 'Brand purpose': 'Glasses given to 3,000 people in Kolkata. It sells nothing, and it is the only ad in the set asking to be liked rather than booked.'}, 'layahealthcare.ie': {'Price anchoring': '€9 a month, or pay less for private hospitals. The number is always small and always monthly, which moves the decision from savings to budget.', 'Peace of mind': 'Just in case. The fear argument, and the only group with any feeling in it. It never says the word insurance.', 'Discount': '10% off, running constantly. A discount this permanent stops reading as an offer and starts reading as the price.', 'Speed to cover': 'Quote to cover in minutes. It sells the paperwork disappearing rather than the cover, aimed at people who have been putting it off.', 'Product range': 'Travel and multi-trip. Cross-sell to people who already hold a plan, not acquisition.', 'Clinic network': 'One ad per location, all launched the same day. This is a property listing more than a persuasion angle: it exists so a search for the Cork clinic finds something.', 'Choice and control': 'A single ad about picking your own GP. The only one offering control rather than protection or a price.'}}
