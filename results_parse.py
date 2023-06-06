import json as json
import re

def parse_results(file_path):
    results = {"0-shot":"","5-shot":"","10-shot":"","25-shot":""}
    with open(file_path, 'r') as file:
        content = file.read()

    if not content:
          print("File is empty.")
          return None
    

    pattern = r'\{*"results":\s*\{.*?\}\s*\}'
    match = re.search(pattern, content, re.DOTALL)
    matches = re.findall(pattern, content, re.DOTALL)
    if not match:
        print("No valid JSON content found in the file.")
        return None
    
    for c,json_content in enumerate(matches):
          
      json_content = "{\n  " +  json_content +"\n}"
      # json_content = "{\n  " +  match.group() +"\n}"
      # print(json_content)


      try:
          results_dict = json.loads(json_content)
      except json.JSONDecodeError as e:
          print(f"Error parsing JSON: {str(e)}")
          return None


      metric_values = {}
      for metric, metric_data in results_dict['results'].items():
          metric_values[metric] = round(list(metric_data.values())[0], 5)
      results[list(results.keys())[c]]= metric_values
    return results


num = 951
out = "s-p"

# Usage example:
file_path = f'/users/xbkx052/scripts/slurm-326{num}.out'
# file_path = f'/users/xbkx052/scripts/dolly-20p-res.txt'
parsed_results = parse_results(file_path)
print(type(parsed_results))
if parsed_results is not None:
    print(parsed_results)
    # with open(f'/users/xbkx052/scripts/res_dolly-e-{out}.json', "w") as f:
    #     json.dump(parsed_results, f)



# with open("/users/xbkx052/scripts/slurm-324940.out", "r") as f:
#     for l in f:
#         if "\"results\":" in l:
#             # read until "    }"



# total = 0
# for i in results.keys():
#     total += results[i]["acc"]

# total = total / len(results.keys())
    
# print(total)
