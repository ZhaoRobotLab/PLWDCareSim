class Passlist:
# A class that contains the dictionary for the pass tasks

	def __init__(self):

		self.passlist = {
            
			'pass1' : [
                """Give Participant the grocery list, including 1 box Chopped Broccoli, 1 box Green Peas, 1 box Chopped Spinach, and 1 box Broccoli Spears.
                Ask them to pick up the first four items on the list from the table.
				When the Participant selects one item successfully, proceed to the next item. Each item picked up is a substep.
				To minimize patient confusion, try to not reference the previous item unless the patient mentions it first.
                If necessary, ask Participant if they would like the instructions repeated?
				This concludes Step 1 of this task.
                """,
                """
                Give Participant the receipt for the 4 items and a wallet. Instruct them to use the wallet money to pay the exact amount for the groceries. 
                Do not reference the grocery shopping task unless Participant mentions it.
                If necessary, ask Participant if they would like the instructions repeated?
                """,
                """
                Hand Participant an envelope containing several food coupons. Ask them to check if any coupons match the items they purchased. 
                If so, instruct them to use the coupons along with this money to pay for the coupon items only.  
                Avoid referencing the previous tasks unless brought up by Participant.
                If necessary, ask Participant if they would like the instructions repeated?
                """,
                """
                Present Participant with their change. 
                Ask them to verify if they received the correct amount of change and how much they should have received. 
                This task should be introduced without referring to the earlier tasks, unless Participant initiates a discussion about them.
                """
            ],

			'pass2' : [
                """Hand Participant the checks for bill payment. Instruct them to use these checks to pay the two utility bills. 
                Remind them to use today's date on the checks. Provide an extra check if needed. 
                Mention that they can use any additional items like a pen or calculator if they usually do so when paying bills. 
                If necessary, ask Participant if they would like the instructions repeated?"
                """
                """
                Once the Participant has paid the water bill, gently guide them to pay the electric bill with another check. 
                Ensure that the focus remains on the current task without referencing the previous bill payment unless Participant mentions it.
                """
			],
            
            'pass3' : [
                """Provide Participant with a paper that has the drugstore's phone number. 
                Instruct them to call the drugstore to find out its closing time for tomorrow. 
                Keep the task focused and avoid referencing any previous activities. 
                If necessary, ask Participant if they would like the instructions repeated.""",
                """After the phone call, ask Participant to relay the closing time they were told for the drugstore tomorrow. 
                Frame this request as a standalone task, without referring back to the phone call unless the Participant does so."""
            ],

			'pass4' : [
                """Provide Participant with Bottle 1. Ask them to read the prescription label on Bottle 1 and understand the instructions for taking this medication.
                Inquire if the Participant knows when they would take the next pill if they were taking this medication today.
                Avoid referencing future tasks and ask Participant if they would like the instructions repeated?"
                """
                """
                "Introduce a medication organizer to the Participant. Describe its layout, with days of the week across the top and times of the day along the side.
                Request that the Participant places the pills for the next two days in the correct boxes of the organizer.
                Keep the task focused on the current medication without referring to Bottle 2 or previous discussions.
                If necessary, ask Participant if they would like the instructions repeated?"
                """
                """Hand Participant Bottle 2. Instruct them to read the prescription label on Bottle 2 and find the instructions for taking this medication.
                Ask when they would take the next pill if they were on this medication today, focusing solely on Bottle 2.
                Avoid referring back to Bottle 1 or the medication organizer unless the Participant brings it up.
                If needed, ask Participant if they would like the instructions repeated?
                """
                """Request the Participant to place the pills for tomorrow and the day after from Bottle 2 in the correct boxes of the organizer.
                This task should be isolated from previous ones, focusing only on Bottle 2's medication.
                If needed, ask Participant if they would like the instructions repeated."""
            ],  
                
            'pass5' : [
                """
                Provide Participant with a comfortable setting to listen to a radio announcement. 
                Instruct them to focus on the content of the announcement and be prepared to summarize it afterward. 
                If needed, ask Participant if they would like the instructions repeated."""
                """Play the radio announcement: Tuna fish lovers should listen closely to this next announcement. Cans of Pacific brand chunk tuna with a Lot number of XK3 are being recalled. The recall is due to pesticide being found in two cans of the tuna. The contaminated tuna was shipped to the Pittsburgh area and consumers are advised to check their storage shelves. Again, that is Pacific brand chunk tuna, lot number XK3.
                After the announcement, ask Participant to summarize the content, treating this request as a separate task."""
                """Following their summary of the radio announcement, ask Participant to describe one action they might consider taking after hearing such an announcement. 
                Frame this as an independent question, without directly linking it to the content of the announcement unless the Participant makes the connection."
                """
            ],

			'pass6' : [
                """Provide ParticipantName with a newspaper article titled 'Alert! Power Outages and Surges.' Instruct them to read the article, which discusses upcoming power outages and surges in Western Pennsylvania due to repairs at a hydroelectric facility. The article advises on preparation and safety measures. 
                After reading, ask the Participant to summarize the main points of the article. This should be treated as a standalone task."""
                """Next, pose a hypothetical question to the Participant: 'If you were to experience these power outages and surges as described in the article, what is one action you might take to prepare?'
                Frame this as a separate, individual question, independent of the summary task."""
            ],
            
            'pass7' : [
                """"Provide Participant with a BINGO card and a marker. Inform them that the playmate also has a card. 
                Explain that the game is won by getting 5 numbers in a row - either down, across, diagonally, or the 4 corners. 
                Instruct Participant to call out 'BINGO' upon achieving a winning row. Offer to repeat instructions if necessary.""",
                """Prior to starting the game, remind everyone to mark the FREE spaces on their BINGO cards. 
                Confirm readiness to start the game with Participant.""",
                """Proceed with calling out the BINGO numbers in a clear, sequential manner, allowing time for the participant to mark their card.
                Each number should be stated distinctly:'B 3. B 3.','O 71. O 71.','N 39. N 39.','G 57. G 57.','I 26. I 26.','B 8. B 8.','O 69. O 69.','I 30. I 30.','N 34. N 34.','B 11. B 11. ','N 43. N 43.','O 64. O 64.','G 54. G 54.', 'N 42. N 42.', 'B 12. B 12.',
                Ensure each number is understood before proceeding to the next."""
            ],
			
			'pass8' : [
                """
                Provide Participant with a clear workspace and a lunch bag containing sandwich ingredients: bread, cheese, meat, vegetables, and condiments. 
                Inform them that they are to make a sandwich using at least two of these items. 
                Direct them to first take a plate from the table to begin assembling their sandwich, emphasizing the choice of at least two items from cheese, meat, vegetables, and condiments. 
                Offer to repeat these instructions if necessary.""",
                """After the sandwich is made, instruct Participant to either enjoy it immediately or store it in a Ziplock bag for later. 
                Guide them to clean up the area by putting unused ingredients back into the lunch bag and wiping down the table with the provided wipes. 
                Frame this as a sequential, standalone task."""
            ]

		}
