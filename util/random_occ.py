from random import random

# Returns a dictionary in the following manner: {"OCCUPATION_1":PERCENTAGE_1,"OCCUPATION_2":PERCENTAGE_2,...}
def makeOccupationDict():
	new_dict = {}

	f = open("../data/occupations.csv", "r") # Opens file for reading

	for line in f.readlines(): # f.readlines() returns a list of lines

		line = line.replace('"', "") # Removes the unnecessary extra quotes

		line = line.strip() # Removes all extra new lines
		occupation_percentage = line.rsplit(",", 2) # Splits line in the format ["OCCUPATION", "PERCENTAGE"]

		if occupation_percentage[0] in "Job Class Total": # If the 1st value of the line is "Job Class" or "Total" skip it
			continue

		new_dict[occupation_percentage[0]] = (float(occupation_percentage[1])/100,occupation_percentage[2]) # Creates a new value in the form {"OCCUPATION": (PERCENTAGE, LINK) }

		#print(new_dict.keys(), new_dict[occupation_percentage[0]], new_dict.values())

	f.close()

	return new_dict

occupation_dict = makeOccupationDict() # Gets an dictionary occupation and their respective percentages

# Selects a random occupation
def selectRandom():
	rand_decimal = random() # Random decimals from 0 to 1

	while(rand_decimal >= .998): # rand_decimal CANNOT BE .998 because occupational percentages add up to 99.8 rather than 100 (see 'occupations.csv')
		rand_decimal = random() # Keep randomizing until rand_decimal is less than .998

	for key in occupation_dict.keys():
		
		rand_decimal -= occupation_dict[key][0] # Subtract the decimal from rand_decimal

		if rand_decimal <= 0: # If rand_decimal is less than or equal to zero, then rand_decimal has been "subtracted enough"
			return key # Return the occupation


