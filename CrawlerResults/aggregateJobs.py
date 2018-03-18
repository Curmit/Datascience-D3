import json

site = "MonsterboardResults"
jobsite = "Monsterboard"

studies = [
    "Biomedical Technology",
    "Business and IT",
    "Chemical Engineering",
    "Communication Science",
    "Industrial Design",
    "International Business Administration",
    "Mechanical Engineering",
    "Psychology",
    "Technical Computer Science"
]

jobSearches = {
    "Biomedical Technology": ["Biomedical Engineer wo",
     "Biomedical Researcher wo",
     "Biomedical wo",
     "Klinisch Fysicus wo"],
    "Business and IT": ["Data Scientist wo",
     "IT analyst wo",
     "IT consultant wo",
     "IT projectmanager wo"],
    "Chemical Engineering": ["Chemical Engineer wo",
     "Chemical Researcher wo",
     "Process Technology wo",
     "Chemische Technology wo"],
    "Communication Science": ["Copywriter wo",
     "Content Manager wo",
     "Online Marketeer wo",
     "Brand Manager wo"],
    "Industrial Design": ["Productontwikkelaar wo",
    "Technisch Ontwerper wo",
    "Product Technoloog wo",
    "Inkoper wo"],
    "International Business Administration": ["Finance Manager wo",
     "Accountant wo",
     "Controller wo",
     "Sales Manager wo"],
    "Mechanical Engineering": ["Bedrijfskundige wo",
     "Technisch Adviseur wo",
     "Product Manager wo",
     "Product Ingenieur wo"],
    "Psychology": ["Gedragswetenschapper wo",
     "Personeelszaken wo",
     "Psycholoog wo",
     "Relatietherapeut wo"],
    "Technical Computer Science": ["Informatie Analyst wo",
     "Programmeur wo",
     "Software Engineer wo",
     "Systeem Ontwerper wo"]
}


paths = []
result = []
for study in studies:
    for i in range(0,4):
        path = "CrawlerResults/" + site + "/" +  study + "/" + jobSearches[study][i] + ".json"
        
        # print(path)
        data = json.load(open(path))
        if len(data) > 0:
            line = {"jobSite": jobsite, "Study": study ,"jobSearch": data[0]["jobSearch"], "noVacancies": len(data)}
        else:
            line = {"jobSite": jobsite, "Study": study ,"jobSearch": jobSearches[study][i], "noVacancies": 0}
        result.append(line)
        

for res in result:
    print(res)

with open('CrawlerResults/result' + site + '.json', 'w') as fp:
    json.dump(result, fp)