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
