######################################################
# Project: Project 3 (Taxes and States)
# UIN: 
# repl.it URL: https://replit.com/@CS111-Fall2021/Project-3-MariaGuallpa#main.py (OG project)

######################################################
#imports
import csv
import json
import requests
import matplotlib.pyplot as plt 
import numpy as np

#File's/internet variables (Update 2024: have been commented out for new user program, except the json as it serves for only state codes)
#csv_file = "tax_return_data_2018.csv"
json_file = "states_titlecase.json"
#url = "https://raw.githubusercontent.com/heymrhayes/class_files/main/state_populations_2018.txt"

#function definitions for file data retrieval
def get_data_from_file(fn):
  '''inputs: a file (string)
    outputs: a list of lists if the file is a csv. a list if it's a json. '''
  lst = []
  if (fn[fn.index("."):len(fn)] == ".csv"):
    f = open(fn)
    reader = csv.reader(f)
    for el in reader:
      lst.append(el)
    f.close()
    return lst
  elif (fn[fn.index("."):len(fn)] == ".json"):
    f = open(fn)
    text = f.read()
    data = json.loads(text)
    return data
  else: 
    print("Error: csv file not found. Start Over!")

def get_data_from_internet(url):
  ''' inputs: a url
      output: a json list or dictionary within a list (for urls only) '''
  response = requests.get(url)
  data = response.json()
  return data

def get_index_for_column_label(header_row, column_label):
  ''' inputs: the list of headers from a csv file and the string of the specified column label
      outputs: the index of specified column label '''
  for el in header_row:
    if el == column_label:
      index = header_row.index(el)
  return index

def get_state_name(state_names, state_code):
  '''inputs: the json list of dictionaries and state abbreviation outputs: the state name '''
  state = ''
  for el in range(0, len(state_names)):
    row = state_names[el]["abbreviation"]
    if row.lower() == state_code.lower():
      state = state_names[el]["name"]
  return state

def get_state_population(state_populations, state_name):
  ''' inputs: a list of dictionaries with state populations and a string of the state name
      outputs: the population of the specified state '''
  state_name = "." + state_name
  #print(type(state_populations))
  #to get code to work with the period
  num_pop = 0
  for el in state_populations:
    for key in el.keys():
      if key.lower() == state_name.lower():
        for values in el.values():
          num_pop = values
    #if state_name in el:
      #num_pop = el[state_name]
  return num_pop

def answer_header(question_number, question_labels):
 ''' returns the header string for each answer'''
 header = "\n"*2
 header += "="*60 + "\n"
 header += "Question " + str(question_number) + "\n"
 header += question_labels[question_number] + "\n"
 header += "="*60 + "\n"
 return header
 
#the headers that go with the questions
question_labels = [
    "",
    "average taxable income per return across all groups",
    "average taxable income per return for each agi group",
    "average taxable income (per resident) per state",
    "average taxable income per return across all groups",
    "average taxable income per return for each agi group",
    "average dependents per return for each agi group",
    "percentage of returns with no taxable income per agi group",
    "average taxable income per resident",
    "percentage of returns for each agi_group",
    "percentage of taxable income for each agi_group"
 ]

#retrieving data from csv, internet, and json (Updated 2024: so now csv amd urls are user inputed. JSON stays the same as it doesn't )
#csv_file_local = get_data_from_file(csv_file)
json_file_local = get_data_from_file(json_file)
#internet_file = get_data_from_internet(url)

#question functions

#question 1
def question1(csv_file):
  ''' the function that answers the national level question of taxable income across all groups'''
  #question 1 
  ###########################################
  #the indexes of the needed tax income in the whole US and total returns in the whole US
  index_tax_income = get_index_for_column_label(csv_file[0], "A04800")
  index_total_returns = get_index_for_column_label(csv_file[0], "N1")
  #the variables that holds the values for the total $$$ tax_income returns and the num of tax returns
  adding_counter_for_tax_income_returns_quest_1 = 0
  total_returns = 0
  #for loop that loops through file
  for item in csv_file:
    #if statement that adds the values together in their respective variables through the condition that it first denies the header row
    if item[index_tax_income] != "A04800" or item[index_total_returns] != "N1":
      adding_counter_for_tax_income_returns_quest_1 += int(item[index_tax_income])
      total_returns += int(item[index_total_returns])
  #getting the total
  total = (adding_counter_for_tax_income_returns_quest_1 / total_returns) * 1000
  total = round(total)
  return total

#question2
def question2(csv_file):
  ''' the function that answers the national level of taxable income per AGI group'''
  #question 2
  ##########################################
  #the summary dict - the total $$$ tax income and total num of tax returns for each group in the whole US
  add_dic = {}
  #the answers dic
  averages_per_AGI = {}
  #the indexes of the agi groups column, the needed tax income in the whole US, and total returns in each agi group in the whole US
  index_tax_income = get_index_for_column_label(csv_file[0], "A04800")
  index_total_returns = get_index_for_column_label(csv_file[0], "N1")
  index_agi_groups = get_index_for_column_label(csv_file[0], "agi_stub")
  #for loop that loops through file
  for item in csv_file:
    #if statement that adds the values together in their respective variables through the condition that it first denies the header row
    if item[index_tax_income] != "A04800" or item[index_total_returns] != "N1" or item[index_agi_groups] != "agi_stub":
      #tests to see if element is in the dict. and makes different, seperate dicts. that have keys that hold the adding of the total tax income of a group as well as total returns
      if str(item[index_agi_groups]) in add_dic:
        item[index_tax_income] = int(item[index_tax_income])
        item[index_total_returns] = int(item[index_total_returns])
        add_dic[item[index_agi_groups]]["total_tax_income_of_group"] += item[index_tax_income]
        add_dic[item[index_agi_groups]]["total_tax_returns"] += item[index_total_returns]
      else:
        item[index_tax_income] = int(item[index_tax_income])
        item[index_total_returns] = int(item[index_total_returns])
        add_dic[item[index_agi_groups]] = {"total_tax_income_of_group": item[index_tax_income] , "total_tax_returns": item[index_total_returns]}
  #the answers to 2 in a dict - rounded to the nearest number
  averages_per_AGI["Group 1"] = round(add_dic["1"]["total_tax_income_of_group"] / add_dic["1"]["total_tax_returns"] * 1000)
  averages_per_AGI["Group 2"] = round(add_dic["2"]["total_tax_income_of_group"] / add_dic["2"]["total_tax_returns"] * 1000)
  averages_per_AGI["Group 3"] = round(add_dic["3"]["total_tax_income_of_group"] / add_dic["3"]["total_tax_returns"] * 1000)
  averages_per_AGI["Group 4"] = round(add_dic["4"]["total_tax_income_of_group"] / add_dic["4"]["total_tax_returns"] * 1000)
  averages_per_AGI["Group 5"] = round(add_dic["5"]["total_tax_income_of_group"] / add_dic["5"]["total_tax_returns"] * 1000)
  averages_per_AGI["Group 6"] = round(add_dic["6"]["total_tax_income_of_group"] / add_dic["6"]["total_tax_returns"] * 1000)
  return averages_per_AGI

#question 3
def question3(csv_file, internet_file):
  ''' function that answers question 3 - the tax income averages for each state/territory in the US '''
  #question 3
  ##########################################
  #the summary dic - tax income avaerages for each state/territory
  sum_dic_state_data = {}
  #the ans dic
  averages = {}
  #the indexes of the needed tax income in the whole US and the state column in each agi group in the whole US
  index_tax_income = get_index_for_column_label(csv_file[0], "A04800")
  index_state = get_index_for_column_label(csv_file[0], "STATE")
  #for loop that loops through the length of file and through counter holds the dictionary's objects
  for item in range(1, len(csv_file)):
    row = csv_file[item]
    state_code = row[index_state]
  #if statement that puts tax income data into a specific state key if state isn't in summary dic
    if state_code not in sum_dic_state_data:
      sum_dic_state_data[state_code]= {"taxable_income": 0}
    #adds remaining tax income data if state is in dic
    sum_dic_state_data[state_code]["taxable_income"] += int(row[index_tax_income])
  #gets state name and population from state code in sum dic as well adds summary dic data into the averages dic
  for state_code in sum_dic_state_data:
    state_name = get_state_name(json_file_local, state_code)
    state_population = get_state_population(internet_file, state_name)
    #gets the state averagages for each state
    sum_dic_state_data[state_code]["avg"] = round(sum_dic_state_data[state_code]["taxable_income"] / state_population * 1000)
    if state_code not in averages:
      averages[state_code] = sum_dic_state_data[state_code]["avg"]
  return averages

#state level questions
def question4(state_input, csv_file):
  ''' function that answers question 4 - based on user input get the average tax income of state inputed'''
  #variable that holds the int average
  total = 0
  index_tax_income = get_index_for_column_label(csv_file[0], "A04800")
  index_total_returns = get_index_for_column_label(csv_file[0], "N1")
  index_state = get_index_for_column_label(csv_file[0], "STATE")
  #the variables that holds the values for the total $$$ tax_income returns, the state column, and the num of tax returns
  adding_counter_for_tax_income_returns_quest_1 = 0
  total_returns = 0
  #for loop that loops through file
  for item in csv_file:
    #if statement that adds the values together in their respective variables through the condition that it first denies the header row
    if item[index_tax_income] != "A04800" or item[index_total_returns] != "N1":
      if state_input == item[index_state]:
        adding_counter_for_tax_income_returns_quest_1 += int(item[index_tax_income])
        total_returns += int(item[index_total_returns])
  #getting the total
  total = (adding_counter_for_tax_income_returns_quest_1 / total_returns) * 1000
  total = round(total)
  return total

def question5(state_input, csv_file):
  ''' gets the answer of the question 5 - the average taxable income for each agi group for state specified in user input '''
  #the ans dic
  sum_total = {}
  #the summary dict - the total $$$ tax income and total num of tax returns for each group in state
  add_dic = {}
  #the indexes of the agi groups column, the needed tax income in the state inputed, the state column,and total returns in each agi group in the state inputed
  index_tax_income = get_index_for_column_label(csv_file[0], "A04800")
  index_total_returns = get_index_for_column_label(csv_file[0], "N1")
  index_agi_groups = get_index_for_column_label(csv_file[0], "agi_stub")
  index_state = get_index_for_column_label(csv_file[0], "STATE")
  #for loop that loops through file
  for item in csv_file:
    #if statement that adds the values together in their respective variables through the condition that it first denies the header row
    if item[index_tax_income] != "A04800" or item[index_total_returns] != "N1" or item[index_agi_groups] != "agi_stub":
      #checks for state 
      if item[index_state] == state_input:
      #tests to see if element is in the dict. and makes different, seperate dicts. that have keys that hold the adding of the total tax income of a group as well as total returns
        if str(item[index_agi_groups]) in add_dic:
          item[index_tax_income] = int(item[index_tax_income])
          item[index_total_returns] = int(item[index_total_returns])
          add_dic[item[index_agi_groups]]["total_tax_income_of_group"] += item[index_tax_income]
          add_dic[item[index_agi_groups]]["total_tax_returns"] += item[index_total_returns]
        else:
          item[index_tax_income] = int(item[index_tax_income])
          item[index_total_returns] = int(item[index_total_returns])
          add_dic[item[index_agi_groups]] = {"total_tax_income_of_group": item[index_tax_income] , "total_tax_returns": item[index_total_returns]}
  #the answers to 5 in a dict - rounded to the nearest number
  sum_total["Group 1"] = round(add_dic["1"]["total_tax_income_of_group"] / add_dic["1"]["total_tax_returns"] * 1000)
  sum_total["Group 2"] = round(add_dic["2"]["total_tax_income_of_group"] / add_dic["2"]["total_tax_returns"] * 1000)
  sum_total["Group 3"] = round(add_dic["3"]["total_tax_income_of_group"] / add_dic["3"]["total_tax_returns"] * 1000)
  sum_total["Group 4"] = round(add_dic["4"]["total_tax_income_of_group"] / add_dic["4"]["total_tax_returns"] * 1000)
  sum_total["Group 5"] = round(add_dic["5"]["total_tax_income_of_group"] / add_dic["5"]["total_tax_returns"] * 1000)
  sum_total["Group 6"] = round(add_dic["6"]["total_tax_income_of_group"] / add_dic["6"]["total_tax_returns"] * 1000)
  return sum_total

def question6(state_input, csv_file):
  ''' function that answers question 6 - the dependent averages for state specified'''
  #the ans dic
  dependents_total = {}
  #the summary dict - the dependents average 
  add_dic = {}
  #the indexes of the agi groups column, the needed tax income in the whole US, and total returns in each agi group in the whole US
  index_dependents = get_index_for_column_label(csv_file[0], "NUMDEP")
  index_total_returns = get_index_for_column_label(csv_file[0], "N1")
  index_agi_groups = get_index_for_column_label(csv_file[0], "agi_stub")
  index_state = get_index_for_column_label(csv_file[0], "STATE")
  #for loop that loops through file
  for item in csv_file:
    #if statement that adds the values together in their respective variables through the condition that it first denies the header row
    if item[index_dependents] != "NUMDEP" or item[index_total_returns] != "N1" or item[index_agi_groups] != "agi_stub":
      #checks state
      if item[index_state] == state_input:
      #tests to see if element is in the dict. and makes different, seperate dicts. that have keys that hold the dependents as well as the total returns
        if str(item[index_agi_groups]) in add_dic:
          item[index_dependents] = int(item[index_dependents])
          item[index_total_returns] = int(item[index_total_returns])
          add_dic[item[index_agi_groups]]["total_dependents"] += item[index_dependents]
          add_dic[item[index_agi_groups]]["total_tax_returns"] += item[index_total_returns]
        else:
          item[index_dependents] = int(item[index_dependents])
          item[index_total_returns] = int(item[index_total_returns])
          add_dic[item[index_agi_groups]] = {"total_dependents": item[index_dependents] , "total_tax_returns": item[index_total_returns]}
  #the answers to 6 in a dict - rounded to the nearest number
  dependents_total["Group 1"] = round(add_dic["1"]["total_dependents"] / add_dic["1"]["total_tax_returns"], 2)
  dependents_total["Group 2"] = round(add_dic["2"]["total_dependents"] / add_dic["2"]["total_tax_returns"], 2)
  dependents_total["Group 3"] = round(add_dic["3"]["total_dependents"] / add_dic["3"]["total_tax_returns"], 2)
  dependents_total["Group 4"] = round(add_dic["4"]["total_dependents"] / add_dic["4"]["total_tax_returns"], 2)
  dependents_total["Group 5"] = round(add_dic["5"]["total_dependents"] / add_dic["5"]["total_tax_returns"], 2)
  dependents_total["Group 6"] = round(add_dic["6"]["total_dependents"] / add_dic["6"]["total_tax_returns"], 2)
  return dependents_total

def question7(state_input, csv_file):
  #the ans dic
  no_tax_income = {}
  #the summary dict - the total $$$ tax income and total num of tax returns for each group
  add_dic = {}
  #the indexes of the agi groups column, the needed tax income in the state, and total returns in each agi group in the whole US
  index_tax_returns = get_index_for_column_label(csv_file[0], "N04800")
  index_total_returns = get_index_for_column_label(csv_file[0], "N1")
  index_agi_groups = get_index_for_column_label(csv_file[0], "agi_stub")
  index_state = get_index_for_column_label(csv_file[0], "STATE")
  #for loop that loops through file
  for item in csv_file:
    #if statement that adds the values together in their respective variables through the condition that it first denies the header row
    if item[index_tax_returns] != "N04800" or item[index_total_returns] != "N1" or item[index_agi_groups] != "agi_stub":
      if item[index_state] == state_input:
      #tests to see if element is in the dict. and makes different, seperate dicts. that have keys that hold the adding of the total tax income of a group as well as total returns
        if str(item[index_agi_groups]) in add_dic:
          item[index_tax_returns] = int(item[index_tax_returns])
          item[index_total_returns] = int(item[index_total_returns])
          add_dic[item[index_agi_groups]]["tax_returns"] += item[index_tax_returns]
          add_dic[item[index_agi_groups]]["total_tax_returns"] += item[index_total_returns]
        else:
          item[index_tax_returns] = int(item[index_tax_returns])
          item[index_total_returns] = int(item[index_total_returns])
          add_dic[item[index_agi_groups]] = {"tax_returns": item[index_tax_returns] , "total_tax_returns": item[index_total_returns]}
  #the answers to 7 in a dict - rounded to the nearest number
  no_tax_income["Group 1"] = round((add_dic["1"]["total_tax_returns"] - add_dic["1"]["tax_returns"]) / add_dic["1"]["total_tax_returns"] * 100, 2)
  no_tax_income["Group 2"] = round((add_dic["2"]["total_tax_returns"] - add_dic["2"]["tax_returns"]) / add_dic["2"]["total_tax_returns"] * 100, 2)
  no_tax_income["Group 3"] = round((add_dic["3"]["total_tax_returns"] - add_dic["3"]["tax_returns"]) / add_dic["3"]["total_tax_returns"] * 100, 2)
  no_tax_income["Group 4"] = round((add_dic["4"]["total_tax_returns"] - add_dic["4"]["tax_returns"]) / add_dic["4"]["total_tax_returns"] * 100, 2)
  no_tax_income["Group 5"] = round((add_dic["5"]["total_tax_returns"] - add_dic["5"]["tax_returns"]) / add_dic["5"]["total_tax_returns"] * 100, 2)
  no_tax_income["Group 6"] = round((add_dic["6"]["total_tax_returns"] - add_dic["6"]["tax_returns"]) / add_dic["6"]["total_tax_returns"] * 100, 2)
  return no_tax_income

def question8(state_input, csv_file, internet_file):
  #the variable - averages_for_state_per_resident that hold the state average tax income
  averages_for_state_per_resident = 0
  #the summary dic
  sum_dic_state_data = {}
  index_tax_income = get_index_for_column_label(csv_file[0], "A04800")
  index_state = get_index_for_column_label(csv_file[0], "STATE")
  for item in range(1, len(csv_file)):
    row = csv_file[item]
    state_code = row[index_state]
    if state_code == state_input:
      if state_code not in sum_dic_state_data:
        sum_dic_state_data[state_code]= {"taxable_income": 0}
      sum_dic_state_data[state_code]["taxable_income"] += int(row[index_tax_income])
  #gets state name and state pop in order for the avaerages to be averaged correctly
  for state_code in sum_dic_state_data:
    state_name = get_state_name(json_file_local, state_code)
    state_population = get_state_population(internet_file, state_name)
    sum_dic_state_data[state_code]["avg"] = round(sum_dic_state_data[state_code]["taxable_income"] / state_population * 1000)
    averages_for_state_per_resident = sum_dic_state_data[state_code]["avg"]
  
  return averages_for_state_per_resident

def question9(state_input, csv_file):
  ''' this function answers the % of returns per group in the state'''
  var_total_returns = 0
  percentage_of_return__per_group = {}
  sum_dic = {}
  index_total_returns = get_index_for_column_label(csv_file[0], "N1")
  index_agi_groups = get_index_for_column_label(csv_file[0], "agi_stub")
  index_state = get_index_for_column_label(csv_file[0], "STATE")
  for item in csv_file:
    #if statement that adds the values together in their respective variables through the condition that it first denies the header row
  
    if item[index_total_returns] != "N1" or item[index_agi_groups] != "agi_stub":
      if item[index_state] == state_input:
        var_total_returns += int(item[index_total_returns])
        sum_dic["total of total"] = var_total_returns
        if str(item[index_agi_groups]) in sum_dic:
          item[index_total_returns] = int(item[index_total_returns])
          sum_dic[item[index_agi_groups]]["total_tax_returns"] += item[index_total_returns]
        else:
          item[index_total_returns] = int(item[index_total_returns])
          sum_dic[item[index_agi_groups]] = {"total_tax_returns":item[index_total_returns]}
  #the answers to 9 in a dict - rounded to the nearest number
  percentage_of_return__per_group["Group 1"] = round(sum_dic["1"]["total_tax_returns"] / sum_dic["total of total"] * 100, 2)
  percentage_of_return__per_group["Group 2"] = round(sum_dic["2"]["total_tax_returns"] / sum_dic["total of total"] * 100, 2)
  percentage_of_return__per_group["Group 3"] = round(sum_dic["3"]["total_tax_returns"] / sum_dic["total of total"] * 100, 2)
  percentage_of_return__per_group["Group 4"] = round(sum_dic["4"]["total_tax_returns"] / sum_dic["total of total"] * 100, 2)
  percentage_of_return__per_group["Group 5"] = round(sum_dic["5"]["total_tax_returns"] / sum_dic["total of total"] * 100, 2)
  percentage_of_return__per_group["Group 6"] = round(sum_dic["6"]["total_tax_returns"] / sum_dic["total of total"] * 100, 2)
  return percentage_of_return__per_group 

def question10(state_input, csv_file):
  ''' this function answers the % of taxable income per group in the state'''
  var_total_tax_income = 0
  percentage_of_tax_income__per_group = {}
  sum_dic = {}
  index_tax_income = get_index_for_column_label(csv_file[0], "A04800")
  index_agi_groups = get_index_for_column_label(csv_file[0], "agi_stub")
  index_state = get_index_for_column_label(csv_file[0], "STATE")
  for item in csv_file:
    #if statement that adds the values together in their respective variables through the condition that it first denies the header row
  
    if item[index_tax_income] != "A04800" or item[index_agi_groups] != "agi_stub":
      if item[index_state] == state_input:
        var_total_tax_income += int(item[index_tax_income])
        sum_dic["total of total"] = var_total_tax_income
        if str(item[index_agi_groups]) in sum_dic:
          item[index_tax_income] = int(item[index_tax_income])
          sum_dic[item[index_agi_groups]]["total_tax_income"] += item[index_tax_income]
        else:
          item[index_tax_income] = int(item[index_tax_income])
          sum_dic[item[index_agi_groups]] = {"total_tax_income":item[index_tax_income]}
  #the answers to 10
  percentage_of_tax_income__per_group["Group 1"] = round(sum_dic["1"]["total_tax_income"] / sum_dic["total of total"] * 100, 2)
  percentage_of_tax_income__per_group["Group 2"] = round(sum_dic["2"]["total_tax_income"] / sum_dic["total of total"] * 100, 2)
  percentage_of_tax_income__per_group["Group 3"] = round(sum_dic["3"]["total_tax_income"] / sum_dic["total of total"] * 100, 2)
  percentage_of_tax_income__per_group["Group 4"] = round(sum_dic["4"]["total_tax_income"] / sum_dic["total of total"] * 100, 2)
  percentage_of_tax_income__per_group["Group 5"] = round(sum_dic["5"]["total_tax_income"] / sum_dic["total of total"] * 100, 2)
  percentage_of_tax_income__per_group["Group 6"] = round(sum_dic["6"]["total_tax_income"] / sum_dic["total of total"] * 100, 2)
  return percentage_of_tax_income__per_group 

#calls AKA answers for 10 questions (updated 2024: to show as a file for user input. Also making charts into a seperate function for better readibility)
def pie_charts(user_input, questions, titles, pie_chart_num):
  x= []
  y = []
  counter = 0
  new_data = sorted(questions.items(), key =lambda kv: (kv[1]) ,reverse=True)
  new_data = dict(new_data)
  for key, value in new_data.items():
    x.append(key)
    counter += value
    y.append(value)
  y = np.array(y)
  plt.pie(y, labels = x, autopct = lambda p: '{:.2f}%'.format(round(p, 2) * counter / 100))
  plt.title(titles + user_input)
  plt.savefig("pie" + pie_chart_num + "_" + user_input)
  #plt.show()
  plt.clf()
  
def charts_main(user_input, question3, question9, question10):
  #Bar graph
  x = []
  y = []
  
  new_data = sorted(question3.items(), key =lambda kv: (kv[1]) ,reverse=True)
  new_data = dict(new_data)
 
  for key, value in new_data.items():
    x.append(key)
    y.append(value)
  x = np.array(x)
  y = np.array(y)
  
  plt.bar(x, y)
  plt.title("The average taxable income (per resident)per state")
  plt.xlabel("States")
  plt.ylabel("The average taxable income (per resident)")
  plt.savefig("bar1.png")
  #plt.show()
  plt.clf()

 #pie charts
  pie_charts(user_input, question9, "The percentage of returns for each AGI in ", "1")
  pie_charts(user_input, question10, "The percentage of taxable income for each AGI in ", "2")

def file_main(csv_file, url):
  #from lines 407 to 454 puts the answers into a file
  #user input
  user_input = input("What state would you like tax info. on? ")
  f = open("answers" + user_input + ".txt", "w")
  #national level questions
###########################################
  f.write(answer_header(1, question_labels))
  f.write("${:8.0f}".format(question1(csv_file)))
  
  f.write(answer_header(2, question_labels))
  for key, value in question2(csv_file).items():
    f.write(key + ":" + " " + "${:8.0f}".format(value) + "\n")

  f.write(answer_header(3, question_labels))
  for key, value in question3(csv_file, url).items():
    f.write(key + ":" + " " + "${:8.0f}".format(value) + "\n")
  
  f.write("\n")
  f.write("=" * 60 + "\n")
  f.write("State level information for " + get_state_name(json_file_local, user_input) + "\n")
  f.write("=" * 60 + "\n")
  
#state level questions
###########################################
  f.write(answer_header(4, question_labels))
  f.write("${:8.0f}".format(question4(user_input, csv_file)))
  
  f.write(answer_header(5, question_labels))
  for key, value in question5(user_input, csv_file).items():
    f.write(key + ":" + " " + "${:8.0f}".format(value) + '\n')

  f.write(answer_header(6, question_labels))
  for key, value in question6(user_input, csv_file).items():
    f.write(key + ":" + " " + "{:8.2f}".format(value) + "\n")
  
  f.write(answer_header(7, question_labels))
  for key, value in question7(user_input, csv_file).items():
    f.write(key + ":" + " "+"{:8.2f}%".format(value) + "\n")
  
  f.write(answer_header(8, question_labels))
  f.write("${:8.0f}".format(question8(user_input, csv_file, url)))
  
  f.write(answer_header(9, question_labels))
  for key, value in question9(user_input, csv_file).items():
    f.write(key + ":" + " "+"{:8.2f}%".format(value) + "\n")
  
  f.write(answer_header(10, question_labels))
  for key, value in question10(user_input, csv_file).items():
    f.write(key + ":" + " " + "{:8.2f}%".format(value) + "\n")
  f.close()
  
  #showing the file in an output
  f = open("answers" + user_input + ".txt", "r")
  print(f.read())
  f.close()

  charts_main(user_input, question3(csv_file, url), question9(user_input, csv_file), question10(user_input, csv_file))

def program():
  print("Welcome to the Tax Analyzer\n")
  print("This program analyzes tax data from any csv file that is formatted like the example files provided. The state population data is also analyzed from an online source similiar to the site given.")
  csv_tax_data = input("Pls enter a csv file for tax data.\nIf you don't have a csv file in mind, then just input the example file provided: ")
  url_pop = input("Pls enter an online source for state population.\nIf you don't have an online source, then just use the online source provided: ")
  user_input = input("Would you like to see your answers all in a file answered all at once? (Y or N). Or if you would like to exit or restart the program, press X.\n")
  csv_tax_file = get_data_from_file(csv_tax_data)
  internet_file = get_data_from_internet(url_pop)
  while user_input != "Y" and user_input != "N":
    user_input = input("Please enter (Y) for yes or (N) for No. To exit the program press X: ")
  if user_input == "Y":
      file_main(csv_tax_file, internet_file)
      program()
  if user_input == "N":
    print("Let's do this ll")
  if user_input == "X":
    print("Goodbye :)")
#calls
program()
