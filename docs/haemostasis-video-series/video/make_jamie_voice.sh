#!/bin/bash
# Records the Module 1 narration with a macOS voice (default: Jamie (Premium)).
# Uses only built-in macOS tools. Run in Terminal:   bash ~/Downloads/make_jamie_voice.sh
# Result: jamie_audio.zip on your Desktop. Send it back to Claude in the chat.
set -euo pipefail
VOICE="${1:-Jamie (Premium)}"
RATE="${2:-170}"
if ! say -v '?' | grep -qF "$VOICE"; then
  echo "The voice \"$VOICE\" is not installed."
  echo "Install it: System Settings > Accessibility > Spoken Content > System voice > Manage Voices..."
  echo "  > English (United Kingdom) > Jamie (Premium). Then run this script again."
  echo "Installed English voices:"; say -v '?' | grep -E "en_GB|en-GB" || true
  exit 1
fi
WORK="$(mktemp -d)/jamie_audio"; mkdir -p "$WORK"
TOTAL=$(grep -c $'\t' <<'LINES'
0001	High on its hill, the kingdom of Vessel on the Hill wraps a great stone wall around a red river.
0002	On peaceful days the wall's lanterns glow softly, and the message to everyone is simple: keep flowing.
0003	Then, crack.
0004	A siege stone splits the wall,
0005	and the river begins to spill.
0006	What happens next always happens in the same order.
0007	The walls squeeze.
0008	The Guards rush in.
0009	A torch relay races along the castle road to wake the Mayor,
0010	who spins a net.
0011	And when the wall has healed, a demolition crew clears the net away.
0012	This is the story of the day the wall tore.
0013	Module one.
0014	The Day the Wall Tore.
0015	This is haemostasis: the body's way of stopping bleeding at a site of injury, while keeping blood fluid everywhere else.
0016	Remember both halves of that sentence.
0017	Haemostasis is not just clotting.
0018	It is clotting in the right place, for the right length of time.
0019	We describe four phases: vascular,
0020	platelet,
0021	coagulation
0022	and fibrinolytic.
0023	The vascular and platelet phases together are called primary haemostasis.
0024	Coagulation is secondary haemostasis.
0025	Stop the bleed, keep the flow.
0026	Before any tear, the wall itself is the kingdom's chief peacekeeper.
0027	Intact endothelium is actively antithrombotic.
0028	It releases prostacyclin and nitric oxide, which dilate the vessel and keep platelets quiet.
0029	Its surface carries heparan sulphate, which strongly accelerates antithrombin,
0030	and thrombomodulin, which captures thrombin and redirects it to activate protein C.
0031	It expresses tissue factor pathway inhibitor, and it breaks down the platelet agonist A D P using the surface enzyme C D thirty-nine,
0032	and it secretes tissue plasminogen activator.
0033	The molecules that start clotting, collagen and tissue factor, sit behind the endothelium, out of contact with flowing blood.
0034	A healthy wall keeps the peace.
0035	The stone strikes.
0036	The wall flinches and squeezes, narrowing the gap.
0037	The vascular phase is immediate.
0038	A local reflex causes vasoconstriction, which slows blood flow.
0039	It is reinforced by thromboxane A two and serotonin released from platelets, and by endothelin from the endothelium.
0040	Vasoconstriction matters most in small vessels.
0041	Behind the broken stones, an alarm bell is suddenly exposed to the river.
0042	Injury also exposes what was hidden: subendothelial collagen,
0043	von Willebrand factor bound to the matrix,
0044	and tissue factor on cells such as fibroblasts and smooth muscle cells.
0045	Tissue factor is the trigger for coagulation.
0046	Note that these events start at the same moment.
0047	The four phases overlap, and we separate them only to make them easier to understand.
0048	First, the walls squeeze.
0049	Tissue factor is the alarm bell behind the wall.
0050	The Platelet Guards arrive.
0051	They throw ropes to the wall and tie on.
0052	Then they raise spiked shields and link arms with one another.
0053	The gap is plugged, but a line of guards can still be pushed aside.
0054	Primary haemostasis has three steps.
0055	Adhesion.
0056	Under the high shear of arterial and small-vessel flow, platelet glycoprotein one B,
0057	part of the G P one B, nine, five complex, binds von Willebrand factor attached to exposed collagen.
0058	Platelets also bind collagen directly through G P six and integrin alpha two beta one.
0059	Activation.
0060	Platelets change shape,
0061	release granule contents such as A D P, and make thromboxane A two.
0062	These recruit more platelets.
0063	The activated platelet also flips negatively charged phosphatidylserine to its outer surface.
0064	This surface is the stage on which coagulation will be built.
0065	Aggregation.
0066	Activated glycoprotein two B three A binds fibrinogen and von Willebrand factor,
0067	which bridge one platelet to the next.
0068	The Rope has one more job: in plasma, von Willebrand factor carries factor eight and protects it from rapid clearance.
0069	The platelet plug forms within minutes, but it is fragile.
0070	It needs a fibrin net to hold it in place.
0071	Rope ties guards to the wall.
0072	G P one B grabs the rope, two B three A links guard to guard.
0073	Guards plug the gap: quick but fragile.
0074	At the alarm bell, the first messenger lights a torch.
0075	Each messenger lights the next, and the flame runs along the castle road.
0076	But a messenger can only stand on the guards' shields if it is painted with magic ink.
0077	The messengers are built in the Liver Workshop,
0078	but four of them, two, seven, nine and ten, cannot grip the ink until the Vitamin K Forge has put the final edge on them.
0079	At the end of the road waits Thrombin the Mayor.
0080	Coagulation turns the fragile platelet plug into a stable clot.
0081	Most clotting factors circulate as inactive precursors of enzymes.
0082	Each activated factor activates the next, so a small signal is amplified into a large burst.
0083	In the body, coagulation starts when tissue factor binds factor seven A.
0084	This complex activates factors ten and nine, and a small amount of thrombin forms.
0085	This is initiation.
0086	That small amount of thrombin then amplifies the process.
0087	It fully activates platelets, and it activates factors five, eight and eleven, releasing eight from its von Willebrand factor carrier.
0088	In propagation, two complexes assemble on the activated platelet surface.
0089	The tenase complex, nine A with eight A, activates factor ten.
0090	The prothrombinase complex, ten A with five A, converts prothrombin to thrombin.
0091	The result is a burst of thrombin.
0092	These complexes need calcium, which bridges the factors to the negatively charged phospholipid.
0093	That is why blood taken into a citrate tube does not clot: citrate binds calcium,
0094	and the laboratory adds calcium back to start the test.
0095	Factors two, seven, nine and ten, together with the natural anticoagulants protein C and protein S, are made in the liver,
0096	but they only become functional once vitamin K has completed them.
0097	Vitamin K is the cofactor for gamma-carboxylation, which gives them the calcium-binding glah domains.
0098	Warfarin blocks the recycling of vitamin K,
0099	so it takes days to work fully: the factors already in the circulation have to be cleared first.
0100	Finally, thrombin converts soluble fibrinogen into fibrin,
0101	and activates factor thirteen, which cross-links the fibrin into a stable mesh.
0102	Each torch lights the next, and the flame grows.
0103	No ink, no stick.
0104	Ten, nine, seven, two: finished by K.
0105	The Mayor turns thread into net.
0106	A relay that never stopped would set the whole kingdom ablaze.
0107	So at every gate stands a Gatekeeper, dressed in gold.
0108	Natural anticoagulants keep the clot local.
0109	Antithrombin inactivates thrombin and factor ten A, and to a lesser extent nine A, eleven A and twelve A.
0110	Heparin, and heparan sulphate on the vessel wall, accelerate it enormously.
0111	Protein C is activated when thrombin binds thrombomodulin on healthy endothelium.
0112	So once the Mayor steps outside the breach, he changes sides.
0113	Activated protein C, with its cofactor protein S, cleaves and inactivates factors five A and eight A.
0114	Tissue factor pathway inhibitor switches off the starting complex early on.
0115	When a Gatekeeper is missing, the result is thrombosis, not bleeding.
0116	Antithrombin locks the Mayor's door, heparin speeds the key.
0117	C cuts, S supports: Five and Eight stop.
0118	When the wall is mended, Foreman T P A blows his whistle.
0119	The Demolition Crew, who have been camped beside the net all along, take it apart
0120	and leave a little rubble behind.
0121	Fibrinolysis removes the clot as the vessel heals.
0122	Tissue plasminogen activator, released from endothelium, converts plasminogen into plasmin.
0123	It works far better when both are bound to fibrin, which keeps lysis local.
0124	Plasmin breaks fibrin into fibrin degradation products.
0125	Cross-linked fibrin, made by factor thirteen, breaks down into fragments containing two linked D domains: D dimer.
0126	A raised D dimer tells us that fibrin was formed and then broken down.
0127	The crew has brakes too.
0128	P A I one inhibits T P A,
0129	and alpha two antiplasmin inhibits plasmin.
0130	Formation and breakdown of fibrin overlap in time.
0131	The crew's tools are on site from the start.
0132	Build the net, then clear the net.
0133	D dimer is rubble from a stitched net.
0134	When something goes wrong, the kingdom sends its Inspectors, dressed in grey.
0135	In the laboratory we split coagulation into two roads that join.
0136	The prothrombin time, P T, is started with tissue factor.
0137	It tests the short, extrinsic road through factor seven, then the common road: ten, five, two and fibrinogen.
0138	The I N R is derived from the P T to standardise warfarin monitoring.
0139	The activated partial thromboplastin time, A P T T, tests the long,
0140	intrinsic road, twelve, eleven, nine and eight, and then the same common road.
0141	The thrombin time tests only the final step, from fibrinogen to fibrin.
0142	These roads are a laboratory model.
0143	In the body, factor twelve is not needed: its deficiency prolongs the A P T T but does not cause bleeding.
0144	Worked example: in haemophilia A, messenger eight is missing from the long road.
0145	The A P T T is prolonged, the P T is normal.
0146	P T: short road, Seven.
0147	A P T T: long road: Twelve, Eleven, Nine, Eight.
0148	T T watches the Mayor's last job.
0149	Eight missing on the long road: A P T T long, P T normal.
0150	Let's walk the wall one more time.
0151	Stop the bleed, keep the flow.
0152	A healthy wall keeps the peace.
0153	First, the walls squeeze, and the alarm bell rings.
0154	Rope ties guards to the wall.
0155	Guards plug the gap: quick but fragile.
0156	Each torch lights the next.
0157	No ink, no stick.
0158	Ten, nine, seven, two: finished by K.
0159	The Mayor turns thread into net.
0160	C cuts, S supports.
0161	Build the net, then clear the net.
0162	And in haemophilia A: Eight missing on the long road, A P T T long, P T normal.
0163	Next time: the Platelet Guards, up close.
LINES
)
N=0
while IFS=$'\t' read -r ID TEXT; do
  [ -z "$ID" ] && continue
  N=$((N+1)); printf '\rRecording line %d of %d...' "$N" "$TOTAL"
  say -v "$VOICE" -r "$RATE" --file-format=WAVE --data-format=LEI16@22050 -o "$WORK/$ID.wav" -- "$TEXT"
done <<'LINES'
0001	High on its hill, the kingdom of Vessel on the Hill wraps a great stone wall around a red river.
0002	On peaceful days the wall's lanterns glow softly, and the message to everyone is simple: keep flowing.
0003	Then, crack.
0004	A siege stone splits the wall,
0005	and the river begins to spill.
0006	What happens next always happens in the same order.
0007	The walls squeeze.
0008	The Guards rush in.
0009	A torch relay races along the castle road to wake the Mayor,
0010	who spins a net.
0011	And when the wall has healed, a demolition crew clears the net away.
0012	This is the story of the day the wall tore.
0013	Module one.
0014	The Day the Wall Tore.
0015	This is haemostasis: the body's way of stopping bleeding at a site of injury, while keeping blood fluid everywhere else.
0016	Remember both halves of that sentence.
0017	Haemostasis is not just clotting.
0018	It is clotting in the right place, for the right length of time.
0019	We describe four phases: vascular,
0020	platelet,
0021	coagulation
0022	and fibrinolytic.
0023	The vascular and platelet phases together are called primary haemostasis.
0024	Coagulation is secondary haemostasis.
0025	Stop the bleed, keep the flow.
0026	Before any tear, the wall itself is the kingdom's chief peacekeeper.
0027	Intact endothelium is actively antithrombotic.
0028	It releases prostacyclin and nitric oxide, which dilate the vessel and keep platelets quiet.
0029	Its surface carries heparan sulphate, which strongly accelerates antithrombin,
0030	and thrombomodulin, which captures thrombin and redirects it to activate protein C.
0031	It expresses tissue factor pathway inhibitor, and it breaks down the platelet agonist A D P using the surface enzyme C D thirty-nine,
0032	and it secretes tissue plasminogen activator.
0033	The molecules that start clotting, collagen and tissue factor, sit behind the endothelium, out of contact with flowing blood.
0034	A healthy wall keeps the peace.
0035	The stone strikes.
0036	The wall flinches and squeezes, narrowing the gap.
0037	The vascular phase is immediate.
0038	A local reflex causes vasoconstriction, which slows blood flow.
0039	It is reinforced by thromboxane A two and serotonin released from platelets, and by endothelin from the endothelium.
0040	Vasoconstriction matters most in small vessels.
0041	Behind the broken stones, an alarm bell is suddenly exposed to the river.
0042	Injury also exposes what was hidden: subendothelial collagen,
0043	von Willebrand factor bound to the matrix,
0044	and tissue factor on cells such as fibroblasts and smooth muscle cells.
0045	Tissue factor is the trigger for coagulation.
0046	Note that these events start at the same moment.
0047	The four phases overlap, and we separate them only to make them easier to understand.
0048	First, the walls squeeze.
0049	Tissue factor is the alarm bell behind the wall.
0050	The Platelet Guards arrive.
0051	They throw ropes to the wall and tie on.
0052	Then they raise spiked shields and link arms with one another.
0053	The gap is plugged, but a line of guards can still be pushed aside.
0054	Primary haemostasis has three steps.
0055	Adhesion.
0056	Under the high shear of arterial and small-vessel flow, platelet glycoprotein one B,
0057	part of the G P one B, nine, five complex, binds von Willebrand factor attached to exposed collagen.
0058	Platelets also bind collagen directly through G P six and integrin alpha two beta one.
0059	Activation.
0060	Platelets change shape,
0061	release granule contents such as A D P, and make thromboxane A two.
0062	These recruit more platelets.
0063	The activated platelet also flips negatively charged phosphatidylserine to its outer surface.
0064	This surface is the stage on which coagulation will be built.
0065	Aggregation.
0066	Activated glycoprotein two B three A binds fibrinogen and von Willebrand factor,
0067	which bridge one platelet to the next.
0068	The Rope has one more job: in plasma, von Willebrand factor carries factor eight and protects it from rapid clearance.
0069	The platelet plug forms within minutes, but it is fragile.
0070	It needs a fibrin net to hold it in place.
0071	Rope ties guards to the wall.
0072	G P one B grabs the rope, two B three A links guard to guard.
0073	Guards plug the gap: quick but fragile.
0074	At the alarm bell, the first messenger lights a torch.
0075	Each messenger lights the next, and the flame runs along the castle road.
0076	But a messenger can only stand on the guards' shields if it is painted with magic ink.
0077	The messengers are built in the Liver Workshop,
0078	but four of them, two, seven, nine and ten, cannot grip the ink until the Vitamin K Forge has put the final edge on them.
0079	At the end of the road waits Thrombin the Mayor.
0080	Coagulation turns the fragile platelet plug into a stable clot.
0081	Most clotting factors circulate as inactive precursors of enzymes.
0082	Each activated factor activates the next, so a small signal is amplified into a large burst.
0083	In the body, coagulation starts when tissue factor binds factor seven A.
0084	This complex activates factors ten and nine, and a small amount of thrombin forms.
0085	This is initiation.
0086	That small amount of thrombin then amplifies the process.
0087	It fully activates platelets, and it activates factors five, eight and eleven, releasing eight from its von Willebrand factor carrier.
0088	In propagation, two complexes assemble on the activated platelet surface.
0089	The tenase complex, nine A with eight A, activates factor ten.
0090	The prothrombinase complex, ten A with five A, converts prothrombin to thrombin.
0091	The result is a burst of thrombin.
0092	These complexes need calcium, which bridges the factors to the negatively charged phospholipid.
0093	That is why blood taken into a citrate tube does not clot: citrate binds calcium,
0094	and the laboratory adds calcium back to start the test.
0095	Factors two, seven, nine and ten, together with the natural anticoagulants protein C and protein S, are made in the liver,
0096	but they only become functional once vitamin K has completed them.
0097	Vitamin K is the cofactor for gamma-carboxylation, which gives them the calcium-binding glah domains.
0098	Warfarin blocks the recycling of vitamin K,
0099	so it takes days to work fully: the factors already in the circulation have to be cleared first.
0100	Finally, thrombin converts soluble fibrinogen into fibrin,
0101	and activates factor thirteen, which cross-links the fibrin into a stable mesh.
0102	Each torch lights the next, and the flame grows.
0103	No ink, no stick.
0104	Ten, nine, seven, two: finished by K.
0105	The Mayor turns thread into net.
0106	A relay that never stopped would set the whole kingdom ablaze.
0107	So at every gate stands a Gatekeeper, dressed in gold.
0108	Natural anticoagulants keep the clot local.
0109	Antithrombin inactivates thrombin and factor ten A, and to a lesser extent nine A, eleven A and twelve A.
0110	Heparin, and heparan sulphate on the vessel wall, accelerate it enormously.
0111	Protein C is activated when thrombin binds thrombomodulin on healthy endothelium.
0112	So once the Mayor steps outside the breach, he changes sides.
0113	Activated protein C, with its cofactor protein S, cleaves and inactivates factors five A and eight A.
0114	Tissue factor pathway inhibitor switches off the starting complex early on.
0115	When a Gatekeeper is missing, the result is thrombosis, not bleeding.
0116	Antithrombin locks the Mayor's door, heparin speeds the key.
0117	C cuts, S supports: Five and Eight stop.
0118	When the wall is mended, Foreman T P A blows his whistle.
0119	The Demolition Crew, who have been camped beside the net all along, take it apart
0120	and leave a little rubble behind.
0121	Fibrinolysis removes the clot as the vessel heals.
0122	Tissue plasminogen activator, released from endothelium, converts plasminogen into plasmin.
0123	It works far better when both are bound to fibrin, which keeps lysis local.
0124	Plasmin breaks fibrin into fibrin degradation products.
0125	Cross-linked fibrin, made by factor thirteen, breaks down into fragments containing two linked D domains: D dimer.
0126	A raised D dimer tells us that fibrin was formed and then broken down.
0127	The crew has brakes too.
0128	P A I one inhibits T P A,
0129	and alpha two antiplasmin inhibits plasmin.
0130	Formation and breakdown of fibrin overlap in time.
0131	The crew's tools are on site from the start.
0132	Build the net, then clear the net.
0133	D dimer is rubble from a stitched net.
0134	When something goes wrong, the kingdom sends its Inspectors, dressed in grey.
0135	In the laboratory we split coagulation into two roads that join.
0136	The prothrombin time, P T, is started with tissue factor.
0137	It tests the short, extrinsic road through factor seven, then the common road: ten, five, two and fibrinogen.
0138	The I N R is derived from the P T to standardise warfarin monitoring.
0139	The activated partial thromboplastin time, A P T T, tests the long,
0140	intrinsic road, twelve, eleven, nine and eight, and then the same common road.
0141	The thrombin time tests only the final step, from fibrinogen to fibrin.
0142	These roads are a laboratory model.
0143	In the body, factor twelve is not needed: its deficiency prolongs the A P T T but does not cause bleeding.
0144	Worked example: in haemophilia A, messenger eight is missing from the long road.
0145	The A P T T is prolonged, the P T is normal.
0146	P T: short road, Seven.
0147	A P T T: long road: Twelve, Eleven, Nine, Eight.
0148	T T watches the Mayor's last job.
0149	Eight missing on the long road: A P T T long, P T normal.
0150	Let's walk the wall one more time.
0151	Stop the bleed, keep the flow.
0152	A healthy wall keeps the peace.
0153	First, the walls squeeze, and the alarm bell rings.
0154	Rope ties guards to the wall.
0155	Guards plug the gap: quick but fragile.
0156	Each torch lights the next.
0157	No ink, no stick.
0158	Ten, nine, seven, two: finished by K.
0159	The Mayor turns thread into net.
0160	C cuts, S supports.
0161	Build the net, then clear the net.
0162	And in haemophilia A: Eight missing on the long road, A P T T long, P T normal.
0163	Next time: the Platelet Guards, up close.
LINES
echo
( cd "$(dirname "$WORK")" && zip -qr "$HOME/Desktop/jamie_audio.zip" jamie_audio )
echo "Done: $HOME/Desktop/jamie_audio.zip ($N lines, voice: $VOICE)"
