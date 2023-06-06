import json

metrics1 = ["boolq-0", "piqa-0", "hs-0", "hs-10", "arc-c-0", "arc-c-25", "arc-e-0", "arc-e-25", "obqa-0"]

metrics2 = ["Humanities","STEM","Social Science","Other","Average"]

metrics3 = ["race", "cb", "wsc", "wic","xnli"]

metrics4 = ["truthfulqa-mc", "crowspairs"]

file_base = "res_dolly"

model = "D"

suffixes = ["-e-s-p"]

# suffixes = ["-e-i",
#             "-ni-e-i",
#             "-nio-e-i",
#             "-e-io",
#             "-ni-e-io",
#             "-nio-e-io",
#             ]

# suffixes = ["-n-i-1",
#             "-n-i-2",
#             "-n-i-3",
#             "-n-io-1",
#             "-n-io-2",
#             "-n-io-3",
#             ]

# suffixes = ["",
#           "-n-i",
#           "-n-i-o"]

for s in suffixes:
    with open(f"{file_base}{s}.json", "r") as f:
        results = json.load(f)
        m1 = [ results["0-shot"]["boolq"], results["0-shot"]["piqa"], results["0-shot"]["hellaswag"], results["10-shot"]["hellaswag"], results["0-shot"]["arc_challenge"], results["25-shot"]["arc_challenge"],
                 results["0-shot"]["arc_easy"], results["25-shot"]["arc_easy"], results["0-shot"]["openbookqa"] ]
    
        # m2 = [results["5-shot"]["Humanities"], results["5-shot"]["STEM"], results["5-shot"]["Social Science"], results["5-shot"]["Other"], results["5-shot"]["mmlu"] ]

        # m3 = [results["0-shot"]["race"], results["0-shot"]["cb"], results["0-shot"]["wsc"], results["0-shot"]["wic"],results["0-shot"]["xnli_en"]]

        # m4 = [results["0-shot"]["truthfulqa_mc"], results["0-shot"]["crows_pairs_english"]]

        
        m1string = f"{model}{s}"
        for metric, result in zip(metrics1, m1):
            m1string += f" &{result}"
        m1string +=  " \\\ \hline"

        print(m1string)

        # m2string = f"{model}{s}"
        # for metric, result in zip(metrics2, m2):
        #     m2string += f" &  {result}"
        # m2string +=  " \\\ \hline"
        
        # print( m2string )

        # m3string = f"{model}{s}"
        # for metric, result in zip(metrics3, m3):
        #     m3string += f" &  {result}"
        # m3string +=  " \\\ \hline"
        # print( m3string )

        # m4string = f"{model}{s}"
        # for metric, result in zip(metrics4, m4):
        #     m4string += f" & {result}"
        # m4string +=  " \\\ \hline"
        
        # print( m4string )